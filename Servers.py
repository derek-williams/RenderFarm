import SocketServer
import threading
import pickle
import traceback
import time

import Constants
from LoggingSetup import logger

class Server:

    def createIdleLoop( self, interval, function ):

        self.idleThread = threading.Thread( target = self.idleLoop,
                                            name = "idle thread",
                                            args = ( interval, function )
                                            )
        self.idleThread.start( )

    def idleLoop( self, interval, function ):
        while True:
            try:
                function( )
            except Exception, e:
                logger.error( """Idle loop exception:
%s""", traceback.format_exc( e ) )
            time.sleep( interval )

class LocalServer( Server ): pass

class MySocketServer(  SocketServer.TCPServer ):

    allow_reuse_address = True

class TCPServer( Server ):


    def __init__( self,
                  port = Constants.PORT,
                  ):

        MyTCPHandler.TCPserver = self
        logger.info( 'open socket %r %s', "", port )
        self.serverObject = MySocketServer( ( "", port),
                                            MyTCPHandler)
        self.serverThread = threading.Thread( target = runTheServer,
                                              name = "server thread",
                                              args = ( self.serverObject, )
                                              )
        self.serverThread.start( )

    def shutdown( self ):
        self.serverObject.shutdown( )

def runTheServer( serverObject ):
    logger.info ("off to the races")
    serverObject.serve_forever( )
        
class MyTCPHandler( SocketServer.StreamRequestHandler ):

    TCPserver = None # the Hydra server object, NOT the SocketServer.

    def handle( self ):

        logger.info ("request")

        try:        
            questionBytes = self.rfile.read( )
            question = pickle.loads( questionBytes )
            logger.debug(question)
            
            answer = question.computeAnswer( self.TCPserver )

            answerBytes = pickle.dumps( answer )
            self.wfile.write( answerBytes )
        except:
            logger.error( """Exception caught:
%s""", traceback.format_exc( ) )

import Questions # this import is necessary for unpickling questions and was moved to the bottom negate a circular import problem
Questions