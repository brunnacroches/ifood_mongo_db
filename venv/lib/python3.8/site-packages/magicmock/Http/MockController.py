'''
Created on Jun 22, 2013

@author: mxu
'''
import web
from web import Mode
from magicmock import Exceptions, Utils
from magicmock import Log
from magicmock.Utils import  Request
import json, os, copy

ignore_headers = ['content-length', 'content-location', 'status']

def GetResponse():

    method = web.ctx.method.lower()

    for uri in web.mockserver.url_mapping.keys():
        if uri in web.ctx.fullpath: 
            response = web.mockserver.url_mapping[uri][method]
            web.ctx.headers = Utils.ConvertHeader(response["headers"])
            web.ctx.status = str(response["status"])
            if isinstance(response["body"], dict) or isinstance(response["body"], list) or isinstance(response["body"], tuple):
                return json.dumps(response["body"])
            else:
                return response["body"]
        
def ForwardRequest():
    Utils.AssertConfig('MOCK_SERVER', 'serveraddress')
    base_url = web.mockserver.config['MOCK_SERVER']['serveraddress']
    url = web.ctx.fullpath
    headers = web.ctx.env['REQUEST_HEADERS']
#    headers = Utils.ConvertHeaderToDict(web.ctx.headers)
    body = web.data()
    method = web.ctx.method
    Log.Mockserver.debug("remote server url is %s, headers are %s" % (base_url, str(headers)))
    request = Request(url = url, headers = None, method = method, body = body, base_url =  base_url)
    req = request.send()
    if isinstance(req.response.data, dict) or isinstance(req.response.data, list) or isinstance(req.response.data, tuple):
        req.response.data = json.dumps(req.response.data)
    for k in req.response.headers.keys():
        if k in ignore_headers:
            del(req.response.headers[k]) 
    return req.response

def RecordRequest():
    url = web.ctx.homedomain+web.ctx.fullpath
    headers = web.ctx.env['REQUEST_HEADERS']
    body = web.data()   
    method = web.ctx.method
    request = {
               'url': url,
               'method':method,
               'headers':headers,
               'body':body
               }
    try:
        Log.Mockserver.info("print request")
        Log.Request.info("", extra = request)
    except:
        Log.Mockserver.error("Fail to log request: %s" % request['url'])
    
def RecordResponse(resp):
    response = {
               'url': web.ctx.fullpath,
               'status': resp.status,
               'headers':resp.headers,
               'body':resp.data
               }   
    print response
    try:
        Log.Mockserver.info("print response")
        Log.Response.info("",extra = response)
    except:
        Log.Mockserver.error("Failed to log response: %s" % response['url'])
def PerformMock():
    is_mock = False
    if web.mockserver.mode:
        if web.mockserver.mode == Mode.mock:
            is_mock = True
    else:
        if web.mockserver.global_mode == Mode.mock:
            is_mock = True
    return is_mock
            


def ParseConfig(config_file, config_path):
    Utils.SetConfigFilePath(config_path)
    Utils.SetConfigFile(config_file)
    Utils.InitConfig()
    config = Utils.config
    section = "MOCK_SERVER"
    Utils.AssertConfig(section, "BASEURL")
    Utils.AssertConfig(section, "Port")
    Utils.AssertConfig(section, "Mode")
    if config[section]["mode"] == "Mock":
        Utils.AssertConfig(section, "APITemplatePath")
        apiTemplatePath = config[section]["apitemplatepath"]
    else:
        apiTemplatePath = None  
    try:
        port = int(config["MOCK_SERVER"]["port"])
    except:
        raise Exceptions.IncorrectConfigError("Port should be an integer")
    web.mockserver.config = config
    return config["MOCK_SERVER"]["baseurl"], port, apiTemplatePath

def InitURLMapping(api_path):
    Log.Mockserver.info("Generate url mapping")
    paths = os.getcwd()
    Log.Mockserver.info(paths)
    for path in api_path.split("."):
        paths = os.path.join(paths, path)

    abs_path = paths
    Log.Mockserver.info(paths)
    for filename in os.listdir(abs_path):
        if filename != "__init__.py":
            if filename[filename.rfind('.')+1::] == 'py' :
                filename_no_ext = filename[0:filename.rfind('.')]
                module = __import__('%s' % api_path,globals(),locals(),[filename_no_ext],-1)     
                template = getattr(module, filename_no_ext)
                
                if not hasattr(template, 'url'):
                    raise Exceptions.IncompleteInfoError("No url info is found in template %s" % template.__name__)
                if not hasattr(template, 'method'):
                    raise Exceptions.IncompleteInfoError("No method info is found in template %s" % template.__name__)
                if not hasattr(template, 'response'):
                    raise Exceptions.IncompleteInfoError("No default response is found in template %s" % template.__name__)
               
                if web.mockserver.url_mapping.has_key(template.url):
                    web.mockserver.url_mapping[template.url][template.method] = template.response
                else:
                    web.mockserver.url_mapping[template.url]={template.method:template.response}
    Log.Mockserver.debug("URL Mapping: %s" % web.mockserver.url_mapping)

def InitMode():
    Utils.AssertConfig("MOCK_SERVER", "Mode") 
    web.mockserver.global_mode = Utils.config['MOCK_SERVER']["mode"]
    web.mockserver.mode = web.mockserver.global_mode
    
                         
def SetResponse(dct):

    response = dct['response']
    url = dct['url']
    method = dct['method']
    
    if web.mockserver.url_mapping.has_key(url):
        web.mockserver.mapping_changes[url] = {method.lower(): copy.deepcopy(web.mockserver.url_mapping[url][method])}
        web.mockserver.url_mapping[url][method] = response

def SetResponseCommon(dct):
    template_name = str(dct['template'])
    response = str(dct['response'])
    api_path = Utils.config["MOCK_SERVER"]['apitemplatepath']
    module = __import__('Projects.%s' % api_path,globals(),locals(),[template_name],-1)     
    template = getattr(module, template_name)
    response_info = getattr(template, response)
    url = template.url
    method = template.method
    
    if web.mockserver.url_mapping.has_key(url):
        web.mockserver.mapping_changes[url] = {method.lower(): copy.deepcopy(web.mockserver.url_mapping[url][method])}
        web.mockserver.url_mapping[url][method] = response_info     


def SetMode(dct):
    if dct['is_global']:
        web.mockserver.global_mode = dct['mode']
    else:
        web.mockserver.mode = dct['mode']
    Log.Mockserver.debug("Set Mode to: %s" %dct['mode'])
    if dct['mode'] == "Mock" and len(web.mockserver.url_mapping) == 0:
        section = "MOCK_SERVER"
        apiTemplatePath = Utils.config[section]["apitemplatepath"]
        InitURLMapping(apiTemplatePath)
        
def RestoreResponse():
    for uri in web.mockserver.mapping_changes.keys():
        if uri in web.ctx.fullpath: 
            for k in web.mockserver.mapping_changes[uri].keys():
                if k.lower() == web.ctx.method.lower():
                    Log.Mockserver.info("Restoring response...")
                    _restore_resp(uri, web.ctx.method.lower())
def RestoreModeAndDelay():
    web.mockserver.mode = web.mockserver.global_mode
    web.mockserver.delay = 0
    
def _restore_resp(uri, method):
    if web.mockserver.url_mapping.has_key(uri):
        if web.mockserver.url_mapping[uri].has_key(method):
            Log.Mockserver.debug("Restore original response")
            web.mockserver.url_mapping[uri][method] = copy.deepcopy(web.mockserver.mapping_changes[uri][method])
            Log.Mockserver.debug("Clean up response")
            del(web.mockserver.mapping_changes[uri][method])
            if not web.mockserver.mapping_changes[uri].keys():
                del(web.mockserver.mapping_changes[uri])
def SetDelay(dct):
    if dct.has_key("is_global"):
        if dct['is_global']:
            Log.Mockserver.info("Set global delay to %ss" % str(dct['delay']))
            web.mockserver.global_delay = dct['delay']
            return
    Log.Mockserver.info("Set delay to %ss" % str(dct['delay']))
    web.mockserver.delay = dct['delay']


def CheckLdap():
    config = web.mockserver.config["MOCK_SERVER"]
    if config.has_key("ldap"):
        if config['ldap']:
            return True
    else:
        return False
    
def LoadLdapConfig():
    Log.Mockserver.info("Load ldap config")
    template_path = web.mockserver.config["MOCK_SERVER"]['ldaptemplatepath']
    
    paths = ['Projects']
    for path in template_path.split("."):
        paths.append(path)
    try:
        config = Utils.GetJsonFromFile(paths, "default.json")
        return config
    except:
        raise Exceptions.UnableToRetrieveDataError("Error to load ldap config data. Please check file existence or format.")
    


    
    
