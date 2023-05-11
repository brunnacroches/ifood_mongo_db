'''
Created on Jan 16, 2012

@author: Mingze

Logger user guide:
1. predefined loggers:
    MockServer:
        Formatter: MockServer
        Output: File
        default level: Info
        sample usage
            from ChorusCore import Log
            Log.MockServer.info("starting server...")
    Request:
        Formatter: Request
        Output: File
        default level: Info
        sample usage
            from ChoursCore import Log
            request = {"url":"/badges",
                       "method":"get"
                       "headers":"headers",
                       "body":""}
            Log.Request.info(extra=request)
    Response:
        Formatter: Response
        Output: File
        default level: Info
        sample usage
            from ChoursCore import Log
            request = {"url":"/badges",
                       "method":"get"
                       "headers":"headers",
                       "body":""}
            Log.Response.info("",extra=response)            
            
    You must init logger before starting to use.
        sample usage:        
            from ChorusCore import Log
            Log.Mockserver = Logger(name = Name.MockServer, path = Utils.outputdir, filename = "mockserver.log", formatter = Formatter.MockServer, loglevel = logging.DEBUG, output = Output.File).get_logger()
            Log.Request = Logger(name = Name.Request, path = Utils.outputdir, filename = 'request.log', loglevel = logging.DEBUG, output = Output.Console, formatter = Formatter.Request).get_logger()
            Log.Response = Logger(name = Name.Response, path = Utils.outputdir, filename = 'response.log', loglevel = logging.DEBUG, output = Output.Console, formatter = Formatter.Request).get_logger()
2. Customize logger
    step1: Inherit Formatter from ChorusCore.log
    step2: init looger with your formatter as the input of "init_logging" function
'''
import logging, os
from magicmock import Exceptions

class Formatter:
    MockServer = "%(asctime)s - %(name)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s"
    Request = "%(url)s \n\t%(method)s \n\t%(headers)s \n\t%(body)s"
    Response = "%(url)s \n\t%(status)s \n\t%(headers)s \n\t%(body)s"
    
class Output:
    Console = "Console"
    File = "File"
    
class Name:
    ChorusCore = "ChorusCore"
    Script = "Script"
    MockServer = "MockServer"
    Request = "Request"
    Response = "Response"

class Logger:
    def __init__(self, name = 'default', loglevel = logging.INFO, output = Output.Console, formatter = Formatter.MockServer, path = None,filename =None):
    
        self.logger = logging.getLogger(name)
        self.logger.setLevel( loglevel )
        # create console handler and set level to debug
        if output == Output.File:
            if filename is None or path is None:
                Exceptions.IncompleteInfoError("filename or path is missing!")
            logfile = os.path.join( path, filename )
            ch = logging.FileHandler(logfile)
        else:
            ch = logging.StreamHandler()
    
        # create formatter
        f = logging.Formatter(formatter)
        # add formatter to ch
        ch.setFormatter( f )
        # add ch to logger
        self.logger.addHandler( ch )
        self.logger.setLevel(loglevel)
    def get_logger(self):
        return self.logger
    
Mockserver = logging.getLogger()
Request = logging.getLogger()
Response = logging.getLogger()





