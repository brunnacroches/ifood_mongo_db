'''
Created on Jun 21, 2013

@author: mxu
'''
from magicmock import ClientAPI
from __init__ import StatusCode, Header

url = "/key/value"
method = "get"
url_parameters = ()
parameters = {}
headers = {}
body = {}
ignored_keys = []
response = {
            "headers": Header.get(),
            "body":ClientAPI.LoadJson("key_value_one_two.json"),
            "status": StatusCode.code_200
            }
response_no_org = {
            "headers": Header.get(),
            "body":ClientAPI.LoadJson("key_value_one_two.json"),
            "status": StatusCode.code_200
            }
            


