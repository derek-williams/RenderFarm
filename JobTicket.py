"""Classes representing submitted jobs. These contain extra information that's
not strictly necessary to getting the jobs executed."""

import pickle
from LoggingSetup import logger
from datetime import datetime

from MySQLSetup import Hydra_job, Hydra_rendertask, READY, transaction

class JobTicket:
    """A generic job ticket"""

    def __init__(self, project, priority):
        self.project = project
        self.priority = priority
    
    def submit( self ):
        job = self.createJob()
        self.createTasks( job )

    def createJob( self ):
        job = Hydra_job( pickledTicket = pickle.dumps( self ), 
                         priority = self.priority, 
                         project = self.project,
                         createTime = datetime.now())
        with transaction() as t:
            job.insert(transaction=t)
            
        return job

    def createTasks( self, job ):
        raise NotImplemented

    def name (self):
        return 'unnamed generic'

class MayaTicket( JobTicket ):

    def __init__( self, sceneFile, mayaProjectPath, startFrame, endFrame, 
                  batchSize, priority, project ):
        print ('initializing', self)
        JobTicket.__init__(self, project, priority)
        self.sceneFile = sceneFile
        self.mayaProjectPath = mayaProjectPath
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.batchSize = batchSize

    def name (self):
        return self.sceneFile

    def renderCommand(self, start, end):
        return [self.executable,
                '-mr:v', '5',
                '-s', str( start ),
                '-e', str( end ),
                '-proj', self.mayaProjectPath,
                self.sceneFile
                ]

    def createTasks( self, job ):
        starts = range( self.startFrame, self.endFrame + 1, self.batchSize )
        ends = [min( start + self.batchSize - 1,
                     self.endFrame )
                for start in starts
                ]
        for start, end in zip( starts, ends ):
            command = self.renderCommand(start, end)
            logger.debug( command )
            task = Hydra_rendertask( status = READY, 
                                     command = repr( command ),
                                     job_id = job.id, 
                                     priority = self.priority, 
                                     project = self.project,
                                     createTime = job.createTime)
            with transaction() as t:
                task.insert(transaction=t)

# these classes are selected by the submitter GUI
class Maya2011 (MayaTicket):

    executable = r'c:\program files\autodesk\maya2011\bin\render.exe'

class Maya2013 (MayaTicket):

    executable = r'c:\program files\autodesk\maya2013\bin\render.exe'

class Maya2014 (MayaTicket):

    executable = r'c:\program files\autodesk\maya2014\bin\render.exe'

class CMDTicket(JobTicket):
    """A job ticket for shoehorning arbitrary commands into the task list. You 
    know, just in case you wanted to do something like that."""
    
    def __init__(self, cmd):
        self.command = cmd
        self.priority = 50
        self.project = "Test Project"

    def name (self):
        return str (self.command)
        
    def createTasks(self, job):
        task = Hydra_rendertask( status = READY,
                                 command = repr( self.command ),
                                 job_id = job.id, 
                                 priority = self.priority,
                                 project = self.project,
                                 createTime = job.createTime)
        with transaction() as t:
            task.insert(transaction=t)
