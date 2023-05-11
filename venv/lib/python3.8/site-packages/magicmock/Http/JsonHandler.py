'''
Created on Jun 21, 2013

@author: mxu
'''
from magicmock import Utils, Exceptions
import json
def LoadJson(json_file):
    config = Utils.config
    if not config["MOCK_SERVER"].has_key("jsontemplatepath"):
        raise Exceptions.IncorrectConfigError("Key '%S' is missing!" % config["MOCK_SERVER"]['JsonTemplatePath'])
    paths = ['Projects']
    for path in config["MOCK_SERVER"]["jsontemplatepath"].split("."):
        paths.append(path)
    result = Utils.GetJsonFromFile(paths, json_file)
    return result