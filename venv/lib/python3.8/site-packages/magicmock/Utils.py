'''
Created on Mar 15, 2012

@author: mxu
'''
import os, sys, socket, stat, types, copy, signal,httplib2
import json, logging
from datetime import datetime
import pyclbr
import random
import hashlib
import shutil, errno
import ConfigParser
from subprocess import Popen, PIPE
from magicmock.Http import web
import Exceptions



    

configfile = "seletest.cfg"
configfilePath = ""
config = None


mockserver_pid = -1 # -1: disable mockserver; 0: not luanched; n: pid of mockserver
    

def ConvertHeader(headers):
    '''
    headers are defined as a dict in api templates, however, web.ctx.headers requires a list with 2-tuple.
    {'header':'content'} -> [('header','content')]
    '''
    result = []
    for k, v in headers.iteritems():
        header = (str(k).encode('utf-8'), str(v))
        result.append(header)
    return result

def ConvertHeaderToDict(headers):
    '''
    headers are defined as a list with 2-tuple, convert to dict format.
     [('header','content')] -> {'header':'content'}
    '''    
    if not isinstance(headers, list):
        raise Exceptions.IncorrectFormatError("Not a dict format!")
        
        
    result = {}
    for item in headers:
        result[item[0]] = item[1]
    return result

class Request:

    def __init__(self,
                 url = None, 
                 method = None, 
                 url_parameters = None, 
                 parameters = None, 
                 headers = None, 
                 body = None,
                 ignored_keys = None,
                 header_keys = None,
                 base_url = None,
                 follow_redirects = True):
        if base_url:
            base_url = base_url
        else:
            base_url = Utils.GetBaseUrl()
             
        if not url:
            self.url = base_url
        else:
            if base_url.endswith("/") and url.startswith("/"):
                self.url = base_url[0:-1] + url
            elif (not base_url.endswith("/")) and (not url.startswith("/")):
                self.url = base_url + "/" + url
            else:
                self.url = base_url + url
            
            

        if not method:
            self.method = None
            raise Exceptions.IncompleteInfoError("method is not defined")
        else:
            self.method = method
            
        self.url_parameters = url_parameters
        self.parameters = parameters
        self.headers = headers
        self.body = body
        self.ignored_keys = ignored_keys
        self.header_keys = header_keys
        self.cert = None
        self.key = None
        self.cert_domain = ''
        self.follow_redirects=follow_redirects
        self.proxy_host=None
        self.proxy_port=None
        self.proxy_type=None
        
    def enable_proxy(self,proxy_host,proxy_port,proxy_type,proxy_rdns=None,proxy_user=None,proxy_pass=None):
        '''HTTP=3,SOCKS4=1,SOCKS5=2'''
        self.proxy_type=int(proxy_type)
        self.proxy_host=proxy_host
        self.proxy_port=int(proxy_port)
        self.proxy_rdns=proxy_rdns
        self.proxy_user=proxy_user
        self.proxy_pass=proxy_pass
                
        
    def add_certificate(self, key_file, cert_file, domain = None):
        self.key = key_file
        self.cert = cert_file  
        if domain:
            self.cert_domain = domain
        
          
    def ShowURL(self,status):
        if self.parameters:
            params = urllib.urlencode(self.parameters)
            url = "?".join([self.url,params])
        else:
            url = self.url
        message={'status':status,
                'method':self.method,
                'URL':url,
                'body':self.body,
                'headers':self.headers,
                'ignored_keys':self.ignored_keys,
                "redirects":self.follow_redirects}
        del_para={}
        for m in message:
            if not message[m]:
                del_para[m]=True
        for n in del_para:
            del(message[n])
        return message
    def send(self):
        '''
        self.result is used for api comparison
        self.response is the responsed data returned
        Make sure use the output correctly
        '''
        if '%s' in self.url:
            if self.url_parameters==None:
                raise Exceptions.IncompleteInfoError("url and it's parameters don't match")

            self.url = self.url % self.url_parameters
        
        
        if self.parameters:
            params = urllib.urlencode(self.parameters)
            url = "?".join([self.url,params])
            params_for_read = []
            for key,value in self.parameters.items():
                params_for_read.append(str(key)+"="+str(value))
            url_for_read = self.url+"?"+"&".join(params_for_read)
        else:
            url_for_read = self.url
            url = self.url
        if isinstance(self.body, dict):
            body = json.dumps(self.body)
        else:                
            body = self.body

        print self.method.upper() + ' ' + url
        
        try:
            if self.proxy_host and self.proxy_port and self.proxy_type:
                proxy=httplib2.ProxyInfo(self.proxy_type,self.proxy_host,self.proxy_port,self.proxy_rdns,self.proxy_user,self.proxy_pass)
                http = httplib2.Http(proxy_info=proxy,disable_ssl_certificate_validation=True)
            else:
                http = httplib2.Http(disable_ssl_certificate_validation=True)
            if self.cert and self.key:
                http.add_certificate(self.key, self.cert, self.cert_domain)
            
                
            http.follow_redirects=self.follow_redirects
            resp, content = http.request(url,
                                     self.method.upper(),
                                     headers = self.headers,
                                     body = body                                 
                                     )
        except Exception, e:
            print e
            raise
            
        try:
            content_dict = Utils.GetDictFromJsonStr(content)
        except:
            content_dict = content
        
        result = {}
        
        if self.ignored_keys:
            Utils.DelInDict(content_dict, self.ignored_keys)
            
        headers = {}
        if self.header_keys:
            for item in self.header_keys:
                if resp.has_key(item):
                    headers[item] = resp[item]
                else:
                    raise Exceptions.IncompleteInfoError('No such headers!')
            if headers:
                result['headers'] = headers
        result['status'] = resp['status']
        result['data'] = content_dict
        self.result = result
        self.response = Response(response_data = content_dict, response_header = resp, status = ' '.join([str(resp.status), resp.reason]),url = url_for_read)
        
        
        return self

 
class Response:
    def __init__(self, response_data = None, response_header = None, status = None, header_keys = None, ignored_keys = None, url = None):

        self.data = response_data
        self.headers = response_header
        self.status = status    
        self.url = url

def SetConfigFile(name):
    """
    set global variable configfile
    """
    global configfile
    configfile = name
    
def SetConfigFilePath(path):
    """
    set config file path, this is used to specify a subfolder in 'conf' path
    """
    global configfilePath
    configfilePath = path
    
def GetConfig(*args):
    """
    Get value from config
    Input:
        @param paths: values indicating searching path in the config, e.g. GetConfig("USHER_VARS", "mstr_username") 
    Output:
        @param value: value got from config with paths specified. If the value is failed to retrieve, return None
    """
    global config
    result = None
    if config and isinstance(config, dict):
        if config.has_key(args[0]):
            result = config[args[0]]
        if len(args)==1:
            return result    
        for path in args[1:]:
            if result:
                if result.has_key(path):
                    result = result[path]
                else:
                    result = None
    if not result:
        print "No value retrieved for path %s" % str(args)
    return result
         
    

def SetOutputDir(dst):
    """
    set global variable outputdir
    outputdir is the path where summary.html suite.html and crashlog (if app's crash happens) is kept
    """
    global outputdir
    if os.path.isdir(dst):        
        rm_r(dst)
        print "Remove depracated output directory"
    os.makedirs(dst)
    print "Create new output directory"
    outputdir = dst
    
def SetBaseUrl(url):
    """
    set global variable baseurl
    """
    global baseurl
    baseurl = url

def GetBaseUrl():
    return baseurl

def GetJsonFromFile(filename):
    """
    get json from file
    
    @param paths: paths where file is kept
    @type paths: str
    @param filename: name of the file from which you want to read
    @type filename: str
    
    @return: jsonobj  
    """
    try:
        filestream = open(filename, 'rb')
        jsonobj = json.load(filestream,object_hook=_decode_dict)
        return jsonobj
    except Exception,e:
        print e
        raise Exception("Open file %s error or Json type not correct %s" % (filename,str(e)))
        

def GetLogLevel(section):
    '''
    by default it's info level
    '''
    global config
    log_level = {
                 'debug': logging.DEBUG,
                 'info': logging.INFO,
                 'warning': logging.WARNING,
                 'error': logging.ERROR,
                 'critical': logging.CRITICAL    
                 }
    
    if config[section].has_key('loglevel'):
        level= config[section]['loglevel'].lower()
        if log_level.has_key(level):
            return log_level[level]
    return logging.INFO

def InitConfig():
    """
    read setting from configfile 
    
    @return: config object which contains test suite info
    """
    global config
    global configfile
    global configfilePath
    config = {}
    cfg = ConfigParser.RawConfigParser()

    base_path = os.getcwd()

    if configfilePath:
        path_str = "/".join([configfilePath,configfile])
        paths = path_str.split("/")       
        full_path = base_path
        for path in paths:
            full_path = os.path.join(full_path, path)
        cfg.read(full_path)
    else:
        full_path = os.path.join(base_path, configfile)
        cfg.read(full_path)

    if not cfg.sections():
        raise Exceptions.IncorrectConfigError("Cannot read config info from %s, please check your config filename and path!" % (full_path))
    
    config["SuitesInfo"] = {}
    for section in cfg.sections():                        
        if cfg.has_option(section, 'ModulePath'):                   
            tmpdict = {}
            for option in cfg.options(section):
                tmpdict[option] = cfg.get(section, option)
            config["SuitesInfo"][section] = tmpdict
        else:
            tmpdict = {}
            for option in cfg.options(section):
                tmpdict[option] = cfg.get(section, option)
            config[section] = tmpdict
            
#    try:    
#        localip = socket.gethostbyname(socket.gethostname())
#    except:
#        print "Cannot resolve local ip... Testing aborted."
#        sys.exit(2)
        
#    cfg = ConfigParser.RawConfigParser()
#    cfg.read(GetFileStr(ConvertToList('conf'), "fbapps.cfg"))
#
#    for section in cfg.sections():
#        if localip in section:                
#            config["FBAppInfo"] = {}
#            for option in cfg.options(section):
#                config["FBAppInfo"][option] = cfg.get(section, option)            
#    if not config.has_key("FBAppInfo"):
#        print "Current ip and fbapp doesn't match... Testing aborted."
#        sys.exit(2)
    return config  

def AssertConfig(section, key):
    '''
    Check whether a required key is in config file, if not, raise an exception
    '''
    if config:
#    Log.Chorus.debug("Verifying key '%s' in section '%s..." % (section, key))
        if not config.has_key(section):
            Log.Chorus.error("%s section is missing!")
            raise Exceptions.IncorrectConfigError("%s section is missing! Please check your config file!" % section)
        if not config[section].has_key(key.lower()):
            Log.Chorus.error("%s key is missing!")        
            raise Exceptions.IncorrectConfigError("Key '%s' is missing! Please check your config file!" % key)
        return True
    else:
        return False

def DumpDictToFile(dictobj,paths,filename):
    
    filename = GetFileStr(paths,filename)
    if os.path.exists(filename):
        os.remove(filename)
    jsonobj = json.dumps(dictobj,indent=2,sort_keys=True)
    WriteToFile(filename,jsonobj)


def WriteToFile(filename,content):

    f = file(filename,"wb")
    f.write(content)
    f.close()
    
def GetFileStr(paths = None,filename = ''):
    rootpath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    fullpath = rootpath
    for path in paths:
        fullpath = os.path.join(fullpath, path)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    return os.path.join(fullpath,filename)

def GetFileStr_NoPathCreation(paths = None,filename = None):
    rootpath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    fullpath = rootpath
    for path in paths:
        fullpath = os.path.join(fullpath, path)
    return os.path.join(fullpath,filename)

def GetModuleFromPackage(pkgname, version):
    path = ['Projects']
    for item in pkgname.split('.'):
        path.append(item)
    #path.append(pkgname)
    path.append(version)
    path.append('TestSuite')
    absmodulepath = GetFileStr(path,'') 
    testsuite = {}
    for suitefile in os.listdir(absmodulepath):
        if suitefile[suitefile.rfind('.')+1::] == 'py' :
            suitename = suitefile[0:suitefile.rfind('.')]
            __import__('Projects.%s.%s.TestSuite.%s' % (pkgname, version, suitename),globals(),locals(),[suitename,''],-1)            
            objects = pyclbr.readmodule_ex('Projects.%s.%s.TestSuite.%s' % (pkgname, version, suitename))
            if objects :
                casename = []
                for case in objects[suitename].methods:
                    if case[0:4] == 'test':
                        casename.append(case)
                testsuite[suitename]=casename
    return testsuite                   

def GetTimestamp():
    now = datetime.utcnow()
    timestamp = '%s%s%s%s%s%s%s' % (now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond)
    return timestamp
            
def GetSuiteInfo(obj):
#    curmodule = obj.__class__.__dict__['__module__']
#    casename = []
#    for classkey in obj.__class__.__dict__.keys():
#        
    casename = []
    curcls=obj.__module__
    for item in dir(obj):
        if item[0:4] == 'test':
            casename.append(item)
    #casename=
    info={}
    infolist = curcls.split('.')
    info['project'] = infolist[0]
    if len(infolist) == 6:
        info['pkgname'] = infolist[1]+'.'+infolist[2]
        info['version'] = infolist[3]
    else:
        info['pkgname'] = infolist[1]
        info['version'] = infolist[2]
    info['suitename'] = infolist[-1]
    info['casename'] = casename
    return info
'''
def DumpDictToFile(filename,jsonobj):
    filestream = open(filename, 'rb')    
    jsonobj = json.load(filestream,object_hook=_decode_dict)
    return jsonobj
'''

def GetDictFromJsonStr(json_str):
    return json.loads(json_str, object_hook = _decode_dict)


def ConvertToList(*args):
    result=[]
    for stri in args:
        result.append(stri)
    return result

def Md5Encryption(*args):
    try:
        inputs = ''.join([str(i) if i is not None else '' for i in args])
        md5 = hashlib.md5()
        md5.update(inputs)
        return md5.hexdigest()
    except Exception:        
        return None
    
def StartMockServer():

    global configfile
    global configfilePath
    global outputdir
    global mockserver_pid
    if configfilePath:
        path = "-p %s" % configfilePath
    else:
        path = ""
    
    mockserverpath = os.path.join("MockServer", "HttpServer.py")
    cmd = "python %s -c %s %s -o %s" % (mockserverpath,
                                                              configfile,
                                                              path,
                                                              outputdir)
    cmd_list = cmd.split(' ')
    process = exec_cmd(cmd_list, wait = False)
    Log.Chorus.info("Mock server started...")
    mockserver_pid = process.pid
def StopMockServer():
    Log.Chorus.info("Mock server stopped...")
    global mockserver_pid
    os.kill(mockserver_pid, signal.SIGKILL)



def cmp_list(lst1,lst2):
    if len(lst1) <> len(lst2):
        return cmp(len(lst1),len(lst2))
    else:
        return cmp(sorted(lst1),sorted(lst2))



def _decode_list(lst):
    '''Written by Huangfu'''
    newlist = []
    for i in lst:
        if isinstance(i, unicode):
            i = i.encode('utf-8')
        elif isinstance(i, list):
            i = _decode_list(i)
        newlist.append(i)
    return newlist

def _decode_dict(dct):
    '''Written by Huangfu'''
    newdict = {}
    for k, v in dct.iteritems():
        if isinstance(k, unicode):
            k = k.encode('utf-8')
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        elif isinstance(v, list):
            v = _decode_list(v)
        newdict[k] = v
    return newdict

def exec_cmd(arg_list, communication = None, wait = True, return_process = True):
    '''Written by Huangfu, enhanced by Mingze'''
    process = Popen(arg_list, stdin = PIPE, stdout = PIPE, stderr = PIPE)
    if communication != None:
        process.communicate(communication)
    elif wait:
        output = process.communicate()    
    if return_process:
        return process
    else: 
        return output
def whereis(*args):
    suffixs=(".exe", ".bat", ".sh", ".pl")
    paths = os.environ['PATH'].split(os.pathsep)
    #print "System paths: %s" % os.environ['PATH']
    for path in paths:
            for arg in args:
                    path_exec = path + os.sep + arg
#                    print "Executable: %s" % path_exec
                    isexist = False
                    file_exec = ""
                    if os.path.exists(path_exec):
                        isexist = True
                        file_exec = path_exec
                    else:
                        for suffix in suffixs:
                            if os.path.exists(path_exec + suffix):
                                isexist = True
                                file_exec = path_exec + suffix
                    if isexist:
                        #print "Executable file is found:%s" % file_exec
                        return file_exec
    print "No executable files found! Please add it into environment path"
    return ""

def copy_folder(src, dst):
    """
    copy file from src to dst 
    also support recursively copy an entire directory tree rooted at src
    """
    shutil.rmtree(dst,ignore_errors=True)
    if not os.path.isdir(dst):   
        try:
            shutil.copytree(src, dst)
        except OSError as exc: 
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else: raise
            
def DelInDict(obj, keys):
    if isinstance(obj, dict) and isinstance(obj, dict):
        for key in copy.deepcopy(obj).keys():
            if key in keys:
                print key
                del(obj[key])
            else:
                DelInDict(obj[key], keys)               

    elif isinstance(obj, list) or isinstance(obj, tuple):

        length = len(obj)
            
        for index in range(0, length):
            DelInDict(obj[index],keys)

    return obj

#the obj comparison is originally written by huangfu, slightly enhaced by mingze
no_value = "Missing"
is_equal = True
def to_json(python_object):
    if isinstance(python_object, types.InstanceType):        
        return python_object.__dict__
    raise TypeError(repr(python_object) + 'is not JSON serializable')

def json_dump(obj, indenting = 0):
    if obj is None:
        return "None"
    else:
        return json.dumps(obj, indent = indenting, default = to_json, sort_keys=True)

def _compare(obj1, obj2):
    global is_equal
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        result = {}
        for key in obj1:
            if key in obj2:
                result[key], is_equal = compare(obj1[key], obj2.pop(key))
            else:
                result[key] = json_dump(obj1[key]), no_value
                is_equal = False
                
        for key in obj2:
            is_equal = False
            result[key] = no_value, json_dump(obj2[key])
    elif (isinstance(obj1, list) and isinstance(obj2, list)) or (isinstance(obj1, tuple) and isinstance(obj2, tuple)):
        result = {}
        length1 = len(obj1)
        length2 = len(obj2)
        if length1 < length2:
            large = length2
        else:
            large = length1
            
        for index in range(0, large):
            if index >= length1:
                is_equal = False
                result[str(index)] = no_value, json_dump(obj2[index])
            elif index >= length2:
                is_equal = False
                result[str(index)] = json_dump(obj1[index]), no_value
            else:
                result[str(index)], is_equal = compare(obj1[index], obj2[index])
        
    else:
        result = json_dump(obj1), json_dump(obj2)
        if not json_dump(obj1) == json_dump(obj2):
            is_equal = False

        
    return result, is_equal

def compare(obj1, obj2):
    result, flag = _compare(obj1, obj2)
    global is_equal
    is_equal = True
    return result, flag

def rm_r(path):
    try:
        
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False, onerror=handleRemoveReadonly)
        elif os.path.exists(path):
            os.remove(path)
    except Exception,e:
        print e
        print "Cannot remove the directory"
        
def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise
if __name__ == '__main__':
    config = {"k1":
                {"k2":
                    {"k3": "v"}
                }
             }
    print GetConfig("k1")
    print GetConfig("k1","k2")
    print GetConfig("k1","k2","k3")
    print GetConfig("k2")
