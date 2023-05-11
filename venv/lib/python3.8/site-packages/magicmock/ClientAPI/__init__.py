'''
Created on Jun 22, 2013

@author: mxu
'''
from magicmock import Utils, Exceptions
from magicmock.Utils import Request
from magicmock.Log import Output, Formatter, Logger, Name
from magicmock import Log
import json, logging, os

class Mode:
    '''
    There are two mode of mock server which has totally different behavior:
    1. Mock: mock server will return static response predefined
    2. Proxy: mock server will forward request to real server, which serves as a proxy
    '''
    Mock = "Mock"
    Proxy = "Proxy"
    
def LoadJson(json_file, json_path = None):
    assertResult = Utils.AssertConfig("MOCK_SERVER", "JsonTemplatePath")
    paths = os.getcwd()
    if assertResult:
        for path in Utils.GetConfig("MOCK_SERVER","jsontemplatepath").split("."):
            paths = os.path.join(paths, path)
        if json_path:
            if isinstance(json_path, str):
                paths = os.path.join(paths, json_path)
            elif isinstance(json_path, list) or isinstance(json_path, tuple):
                for jpath in json_path:
                    paths = os.path.join(paths, jpath)
            else:
                print "unrecognized path list!"
        
    try:
        result = Utils.GetJsonFromFile(os.path.join(paths, json_file))
    except Exception, e:
        
        result = {"mock_server_error":"invalid json file","exception": str(e)}

    return result
def LoadImage(image_file):
    config = Utils.config
    Utils.AssertConfig("MOCK_SERVER", "JsonTemplatePath")
    paths=os.getcwd()
    for path in config["MOCK_SERVER"]["jsontemplatepath"].split("."):
        paths = os.path.join(paths, path)
    try:
        f = open(os.path.join(paths,image_file), 'rb')
        data = f.read()
    except Exception, e:
        data = {"mock_server_error":"invalid image file"}
    return data

class server:
    def __init__(self, serverAddr, port, ssl = False):
        if ssl:
            prefix = "https://"
        else:
            prefix = "http://"
        self.baseurl = "%s%s:%s" % (prefix, serverAddr, port)

    def SetResponse(self, module, response):
        '''
        set data returned by mock server
        Two args: 
            The first arg is the module instance of the api template
            The second arg is response we'd like to set
        if success, return true. else, return false
        '''
        
        uri = "/set/response"    
        #assamble body
        body = {
                "url": module.url,
                "method": module.method,
                "response": response
                }
        print body
        try:
            request = Request(url = uri, body = body, method = "post", base_url = self.baseurl)
            print request
            result = request.send().result
            print 'this is result'
            print result
            if result['status'] == '200':
                print("Set response success!")
                return True                
            else:
                raise Exception("Set response failed!")

        except:
            print("Error response returned!")
            return False      

    def SetDelay(self, delay = 0, is_global = False):
        '''
        by default the delay is 0. set value to get a delayed response. The value must be int type.
        '''
        if not isinstance(delay, int):
            raise Exception("delay must be integer!")
                    
        uri = "/set/delay"     
        body = { 'delay': delay , 'is_global': is_global}
        try:
            request = Request(url = uri, body = body, method = "post", base_url = self.baseurl)
            result = request.send().result
            if result['status'] == '200':
                print("Set delay success!")
                return True                
            else:
                raise Exception("Set delay failed!")
        except:
            print("Error response returned!")
            return False    
        


    def SetMode(self, mode = Mode.Mock, is_global = True):
        '''
        by default set mode will change mode permenently. If you don't want this, set global to false
        '''
        uri = "/set/mode"     
        body = { 'mode': mode, 'is_global': is_global}
        try:
            request = Request(url = uri, body = body, method = "post", base_url = self.baseurl)
            result = request.send().result
            if result['status'] == '200':
                print("Set mode success!")
                return True                
            else:
                raise Exception("Set mode failed!")
        except:
            print("Error response returned!")
            return False  

if __name__ == "__main__":
    Utils.configfile = "mockserver_Demo.cfg"
    Utils.configfilePath = "Trela3_6"
    Utils.InitConfig()
    from Projects.Alert.Resource.APITemplates import giftcards_detail_error

    Log.Chorus = Logger(name = Name.ChorusCore, loglevel = logging.DEBUG, output = Output.Console, formatter = Formatter.ChorusCore).get_logger()
    print SetResponse("giftcards_detail_error", giftcards_detail_error.response_821)
#    from Projects.Usher.UVS.APITemplates import user_retrieve__events_get
#    print SetResponse("user_retrieve__events_get", user_retrieve__events_get.response_device_activation)
    #SetMode(mode = Mode.Mock, is_global = False)
    #SetDelay()