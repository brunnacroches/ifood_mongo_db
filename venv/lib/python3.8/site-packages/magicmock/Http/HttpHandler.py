'''
Created on May 28, 2013

@author: mxu
'''
import json, time, os
import web, magicmock.Utils as MockUtils
from web import Mode
from magicmock.Utils import Request, Response
from magicmock import Log, Utils
from magicmock.Http import MockController

class RequestHandler(object):
    '''
    Generic class handling all http request
    '''

    def GET(self):
        '''
        Handle request with get method
        '''
        return self._process_request()
        
    def POST(self):
        '''
        Handle request with post method
        '''
        return self._process_request()
    
    def PUT(self):
        '''
        Handle request with post method
        '''
        return self._process_request()
    
    def DELETE(self):
        '''
        Handle request with post method
        '''
        return self._process_request()
            
    def _process_request(self):
        try:
            if web.mockserver.global_delay == 0:
                Log.Mockserver.debug("time delay is set to %s sec" % web.mockserver.delay)
                time.sleep(web.mockserver.delay)
            else:
                Log.Mockserver.debug("global time delay is set to %s sec" % web.mockserver.global_delay)
                time.sleep(web.mockserver.global_delay)          
                      
            MockController.RecordRequest()
            if not MockController.PerformMock():
                resp = MockController.ForwardRequest()
                MockController.RecordResponse(resp)
                web.ctx.headers = MockUtils.ConvertHeader(resp.headers)
                web.ctx.status = resp.status
                data = resp.data
            else:
                data = MockController.GetResponse()
                resp = Response()
                resp.data = data
                resp.headers = web.ctx.headers
                resp.status = web.ctx.status
                resp.url = web.ctx.fullpath

                MockController.RecordResponse(resp)
                MockController.RestoreResponse()
                if data is None:
                    data =  "API hasn't been implemented!"
            MockController.RestoreModeAndDelay()
            return data
        except Exception, e:
            Log.Mockserver.exception("general server error")
            return "general server error"
                
class SetResponse(object):
    def POST(self):
        '''
        set response for certain api
        '''
        try: 
            data = web.data()
            dct = json.loads(data)
            MockController.SetResponse(dct)
            return {"status":"ok"}
        except:
            Log.Mockserver.exception("general server error")
            return {"status":"failure"}
            
class SetResponseCommon(object):
    def POST(self):
        '''
        set response for certain api
        post body should be: {"template":"badges_get",
                              "response":"response"}
        @param template: template file name
        @param response: response to be set, should be a variable name in template file 
        '''
        try:
            data = web.data()
            dct = json.loads(data)
            MockController.SetResponseCommon(dct)
            return {"status":"ok"}
        except:
            Log.Mockserver.exception("general server error")
            return {"status":"failure"}
    
class SetMode(object):
    def POST(self):
        '''
        set mode or global mode 
        '''
        try:
            data = web.data()       
            dct = json.loads(data)
            MockController.SetMode(dct)
            return {"status":"ok"}
        except:
            Log.Mockserver.exception("general server error")
            return {"status":"failure"}
                
class SetDelay():
    def POST(self):
        '''
        set delay. Seems not necessary to set global delay
        '''
        try:
            data = web.data()
            dct = json.loads(data)
            MockController.SetDelay(dct)
            return {"status":"ok"}
        except:
            Log.Mockserver.exception("general server error")
            return {"status":"failure"}

class Meta():
    def GET(self):
        '''
        get config Meta
        '''
        try:
            meta = {"config": Utils.config["MOCK_SERVER"],
                    "configfile": Utils.configfile,
                    "configfilePath": Utils.configfilePath,
                    "configfileFullPath":os.getcwd()}
            return json.dumps(meta)
        except:
            Log.Mockserver.exception("general server error")
            return {"status":"failure"}


        
class SetLdap():
    def POST(self):
        '''
        set ldap config.
        '''
        try:
            from MockServer.Ldap import LdapController
            data = web.data()
            dct = json.loads(data)
            LdapController.SetLdapConfig(dct)
            return {"status":"ok"}
        except:
            Log.Mockserver.exception("general server error")
            return {"status":"failure"}