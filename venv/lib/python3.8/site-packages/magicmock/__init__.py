'''
Created on Jun 23, 2013

@author: mxu
'''

import sys, os, logging
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.getcwd())
from magicmock.Http import web
from magicmock.Http.MockController import ParseConfig, InitURLMapping, InitMode
from magicmock import Utils, Log
from magicmock.Log import Output, Formatter, Logger, Name
from optparse import OptionParser
from magicmock.Http.web.wsgiserver import CherryPyWSGIServer
from magicmock.Http.HttpHandler import *
from ClientAPI import server, Mode
urls = (
        '/set/response', "SetResponse",
        '/set/response_common',"SetResponseCommon",
        '/set/mode', "SetMode",
        '/set/delay', "SetDelay",
        '/set/meta', "Meta",
        '^.*', 'RequestHandler'
        )    
application = web.application(urls, globals())


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = OptionParser()
    parser.add_option("-d", "--daemon", dest="daemon", action="store_true", help="run as daemon")
    parser.add_option("-c", "--config", dest="config", 
                      help="specify config file")
    parser.add_option("-p", "--config-path",dest="configpath",
                      help="specify the relative path of config file")
    parser.add_option("-o", "--output", dest="output",
                      help="specify output absolute path")
    
    (options, args) = parser.parse_args()
    ip, port, api_path = ParseConfig(options.config, options.configpath)
    Utils.SetOutputDir(os.path.join(options.output,"Logs"))    
    section = "MOCK_SERVER"
    loglevel = Utils.GetLogLevel(section)
    Log.Mockserver = Logger(name = Name.MockServer, path = Utils.outputdir, filename = "mockserver.log", loglevel = loglevel, output = Output.File, formatter = Formatter.MockServer).get_logger()
    Log.Request = Logger(name = Name.Request, path = Utils.outputdir, filename = 'request.log', loglevel = logging.INFO, output = Output.File, formatter = Formatter.Request).get_logger()
    Log.Response = Logger(name = Name.Response, path = Utils.outputdir, filename = 'response.log', loglevel = logging.INFO, output = Output.File, formatter = Formatter.Response).get_logger()    
    if Utils.config[section].has_key("ssl"):
        if Utils.config[section]['ssl'].lower() == 'true':
            Utils.AssertConfig(section, "sslkeypath")
            Utils.AssertConfig(section, "sslcerpath")
            CherryPyWSGIServer.ssl_certificate = Utils.config[section]['sslkeypath']
            CherryPyWSGIServer.ssl_private_key = Utils.config[section]['sslcerpath']
    if Utils.config[section]["mode"] == "Mock":
        InitURLMapping(api_path)
    InitMode()
    web.config.debug = True

#     import daemon
#     with daemon.DaemonContext():
#         s = LdapServer()
#         s.start()
    if options.daemon:
        import daemon
        with daemon.DaemonContext():
            application.run(ip = ip, port = port)
    else:
        application.run(ip = ip, port = port)

#    web.httpserver.runsimple(application, ("127.0.0.1",8081))

def setup(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 2 or argv[1] == "--help":
        print "Usage: magicmocksetup <dest dir>"
        return
    current_dir_abs = os.path.abspath(os.path.dirname(__file__))
    sampler_folder = os.path.join(current_dir_abs, "Sample")
    output_dir_abs = os.getcwd()
    output_folder = os.path.join(output_dir_abs, argv[1])
    Utils.copy_folder(sampler_folder, output_folder)
    print "Sample project created."

