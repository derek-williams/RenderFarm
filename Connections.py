import exceptions
import socket
import pickle

import Servers
import Constants
#import Answers
from LoggingSetup import logger

"""A Connection allows a Client to ask a Server for
an Answer to a Question."""

class Connection:
    "A connection to a Hydra server. Base class, must be subclassed."

    def getAnswer( self, question ):
        """Protocol for getting the server to answer a question.
        Must be implemented in subclasses."""

        raise exceptions.NotImplementedError

class LocalConnection( Connection ):
    "A connection to a local Hydra server"
    def __init__( self,
                  localServer = Servers.Server( )
                  ):
        """Constructor. By default it creates a new local server
            if you don't supply one."""
        self.localServer = localServer

    def getAnswer( self, question ):
        # call computeAnswer directly, since we have the server right here
        return question.computeAnswer( self.localServer )

class TCPConnection( Connection ):
    "A connection to a remote Hydra server, using TCP"
    def __init__( self,
                  hostname = Constants.HOSTNAME,
                  port = Constants.PORT
                  ):
        """Constructor. Supply a hostname to connect to another computer."""
        self.hostname = hostname
        self.port = port
    
    def getAnswer( self, question ):
        # send the question to a remote server and get an answer back

        # create a TCP socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

        try:
            # connect to the server
            logger.info( 'connect to %s %s', self.hostname, self.port )
            sock.connect( ( self.hostname, self.port ) )
            # convert the question to ASCII
            questionBytes = pickle.dumps( question )
            # send the question
            sock.sendall( questionBytes )
            # close the sending half of the connection so the other side
            # knows we're done sending
            sock.shutdown( socket.SHUT_WR )

            # read the response, an ASCII encoded object
            answerBytes = sock.recv( Constants.MANYBYTES )
            # convert the response to an object
            answer = pickle.loads( answerBytes )
 
        finally:
            sock.close( )
        
        return answer


