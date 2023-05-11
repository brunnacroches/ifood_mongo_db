'''
Created on Jun 22, 2013

@author: mxu
'''
from magicmock import Utils, web
import json
def GetResponse(method = None):
    if method:
        method = method.lower()
    else:
        method = 'get'
    for uri in web.url_mapping.keys():
        if uri in web.ctx.fullpath: 
            response = web.url_mapping[uri][method]
            web.ctx.headers = Utils.ConvertHeader(response["headers"])
            web.ctx.status = str(response["status"])
            return json.dumps(response["body"])
def SetDelay():
    pass
    