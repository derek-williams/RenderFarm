class Answer: 
    """Interface for Answer objects"""
    pass


class TimeAnswer( Answer ):
    """An Answer which stores the time."""
    def __init__( self, time ):
        self.time = time




class EchoAnswer( Answer ):
    """An Answer which stores the object specified by a Question."""
    def __init__( self, object ): # @ReservedAssignment
        self.object = object

class CMDAnswer( Answer ):
    
    def __init__( self, output ):
        self.output = output
        
        
class RenderAnswer( Answer ):
    
    def __init__( self ):
        pass

class KillCurrentJobAnswer(Answer):
    """An answer which tells whether or not child process was killed."""
    def __init__(self, childKilled):
        self.childKilled = childKilled
