import time
import subprocess
import traceback
import exceptions
import os
import datetime

#import DjangoSetup
#from Hydra.models import RenderTask

from Answers import TimeAnswer, EchoAnswer, CMDAnswer, RenderAnswer, KillCurrentJobAnswer
from MySQLSetup import Hydra_rendertask
from RenderNodeMain import RenderTCPServer

from Constants import RENDERLOGDIR

class Question:
    """Interface for Question objects."""
    
    def computeAnswer( self, server ):
        """
        Override this method when creating a Question subclass 
        code in this method will be run by the server
        """
        raise exceptions.NotImplementedError

class TimeQuestion( Question ):
    """A Question for getting the current time on the server."""
     
    def computeAnswer( self, server ):
        return TimeAnswer( time.localtime( ) )


class EchoQuestion( Question ):
    """A Question in which the specified object is to be returned as an Answer."""

    def __init__( self, object ):
        self.object = object

    def computeAnswer( self, server ):
        return EchoAnswer( self.object )

class CMDQuestion( Question ):
    """A Question for running arbitrary commands on a server."""
    def __init__( self, args ):
        self.args = args

    def computeAnswer( self, server ):
        output = subprocess.check_output( self.args,
                                          stderr=subprocess.STDOUT )
        return CMDAnswer( output )

class RenderQuestion( Question ):

    def __init__(self, render_task_id ):

        self.render_task_id = render_task_id

    def computeAnswer( self, server ):
        [render_tasks] = Hydra_rendertask.fetch("where ")
        render_task = Hydra_rendertask.fetch()
        render_task.host = os.getenv( 'COMPUTERNAME' )
        if not os.path.isdir( RENDERLOGDIR ):
            os.makedirs( RENDERLOGDIR )
        render_task.logFile = os.path.join( RENDERLOGDIR, '%010d.log.txt' % render_task.id )
        render_task.status = 'S'
        render_task.startTime = datetime.datetime.now( )
        render_task.save( )
        log = file( render_task.logFile, 'w' )
        
        try:
            log.write( 'Hydra log file %s on %s\n' % ( render_task.logFile, render_task.host ) )
            log.write( 'Command: %s\n\n' % ( render_task.command ) )
            log.flush( )
            
            render_task.exitCode = subprocess.call( eval( render_task.command ),
                                                    stdout = log,
                                                    stderr = subprocess.STDOUT )
            log.write( '\nProcess exited with code %d\n' % render_task.exitCode )
            return RenderAnswer( )
        except Exception, e:
            traceback.print_exc( e, log )
            raise
        finally:
            render_task.status = 'D'
            render_task.endTime = datetime.datetime.now( )
            render_task.save( )

            log.close( )

class KillCurrentJobQuestion (Question):
    """A Question for killing a job on a RenderTCPServer"""
    def __init__(self, statusAfterDeath):
        self.statusAfterDeath = statusAfterDeath
        
    def computeAnswer(self, server):
            server.killCurrentJob(self.statusAfterDeath)
            return KillCurrentJobAnswer(server.childKilled)
