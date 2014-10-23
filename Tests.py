import unittest
import time
import random
import exceptions
import traceback
import os

from MySQLSetup import Hydra_rendertask

import Questions
import Answers
import Connections
import Clients
import Servers
from LoggingSetup import logger

__doc__="""Multiple tests are performed to check the performance of our modules."""""

class TestQuestionsLocal( unittest.TestCase, Clients.Client ):
    """This calls on the unit test and the client class and the client module."""

    connection = Connections.LocalConnection( )
    """This defines the variable connection"""

    def testQA( self ):
        
        question = Questions.Question( )
        answer = self.getAnswer( question )
        self.assert_( isinstance( answer, Answers.Answer ) )

        """This class defines a test, within the class the variable question is defined as the module and subclass.
        Answer is defined as well, the self.assert calls on the isinstance which only returns true if the object
        argument is an instance of the classinfo argument or of a subclass."""       

    def testTime( self ):
        
        time1 = time.localtime( )
        
        question = Questions.TimeQuestion( )
        answer = self.getAnswer( question )
        time2 = answer.time

        self.assertEqual( time1, time2 )

        """This class defines a test, that checks the time. The variables time1 and time 2 are defined
        and for this test to be true time1 and time2 need to be equal"""

    def testEchoSuccess( self ):

        object = random.random( )
        question = Questions.EchoQuestion( object )
        answer = self.getAnswer( question )
        self.assertEqual( question.object, answer.object )

        """In this class echo is defined as a command with multiple parameters. It checks to makes sure
        the object in answer recieved is the same as the object in question."""

    def testEchoFail( self ):

        object = time
        question = Questions.EchoQuestion( object )
        if isinstance( self.connection, Connections.LocalConnection ):
            self.assertEqual( object, self.getAnswer( question ).object )
        else:
            self.assertRaises( exceptions.TypeError, self.getAnswer, question )

            """This class defines what happens if the test fails. The object defined as time is then set into
            put into an isinstance and set equal to the answer."""

    def testCommand( self ):
        """Tests a CMDQuestion, a command issued to this or another host."""
        question = Questions.CMDQuestion( 'cmd /c echo %computername%' )
        answer = self.getAnswer( question )
        thisComputerName = os.getenv( 'COMPUTERNAME' )
        self.assertEqual( answer.output.strip( ), thisComputerName )

    def testRenderCommand( self ):
        """Tests a Render Command, a command that invokes the Maya renderer."""
        command = [
                r'c:\program files\autodesk\maya2011\bin\render.exe',
                '-mr:v', '5',
                r'\\flex2\ProjectHydra\TestMayaFiles\Chair2.ma'
                  ]
        render_task = Hydra_rendertask()
        render_task.status = 'R'
        render_task.command = repr( command )
        render_task.insert()

        logger.debug(render_task)

        render_question = Questions.RenderQuestion( render_task.id )
        render_answer = self.getAnswer( render_question )
        logger.debug( render_answer )        
      
class TestQuestionsSocket( TestQuestionsLocal ):
    """Class to represent a test socket connection to send Questions to."""

    connection = Connections.TCPConnection ()
    
if __name__ == '__main__':

    socketServer = Servers.TCPServer( )
    unittest.main( exit=False )
    socketServer.shutdown( )
    
