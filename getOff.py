import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Ui_getOff import Ui_MainWindow

#import Servers
from Clients import Client
from Connections import TCPConnection
from Questions import KillCurrentJobQuestion
from MySQLSetup import transaction, Hydra_rendernode, IDLE, OFFLINE, READY
import Utils
from LoggingSetup import logger
from socket import error as socketerror

codes = {'I': 'idle',
         'R': 'ready',
         'O': 'offline',
         'F': 'finished',
         'S': 'started'}

class getOffWindow(QMainWindow, Ui_MainWindow, Client):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        QObject.connect(self.onlineButton, SIGNAL("clicked()"), self.online)
        QObject.connect(self.offlineButton, SIGNAL("clicked()"), self.offline)
        QObject.connect(self.getoffButton, SIGNAL("clicked()"), self.getOff)
        QObject.connect(self.refreshButton, SIGNAL("clicked()"), self.updateRenderNodeInfo)
    
    def updateRenderNodeInfo(self):
        with transaction():
            [thisNode] = Hydra_rendernode.fetch ("where host = '%s'" % Utils.myHostName( ))
        
        if thisNode.host:
            self.nameLabel.setText("Node name: " + thisNode.host)
            self.statusLabel.setText("Status: " + codes[thisNode.status])
            if thisNode.task_id:
                self.jobLabel.setText("Job id: {0:d}".format(thisNode.task_id))
            else:
                self.jobLabel.setText("Job id: None")
        else:
            QMessageBox.about(self, "Error", "This computer is not registered as a render node.")

    def getOff(self):
        """
        Offlines the node and sends a message to the render node server running on localhost to
        kill its current task
        """
        self.offline()
        try:
            self.connection = TCPConnection()
            killed = self.getAnswer(KillCurrentJobQuestion(statusAfterDeath=READY))
            if not killed:
                logger.debug("There was a problem killing the task.")
                QMessageBox.about(self, "Error", "There was a problem killing the task.")
        except socketerror:
            QMessageBox.about(self, "Error", "The render node software is not running or has become unresponsive.")
            
        self.updateRenderNodeInfo()
        
    def online(self):
        """Changes the local render node's status to online if it wasn't on-line already"""
        with transaction():
            [thisNode] = Hydra_rendernode.fetch ("where host = '%s'" % Utils.myHostName( ))
            if thisNode.status == OFFLINE:
                thisNode.status = IDLE
                thisNode.update()
            else:
                logger.debug("Node is already online.")
            self.updateRenderNodeInfo()
            
    def offline(self):
        """Changes the local render node's status to offline"""
        with transaction():
            [thisNode] = Hydra_rendernode.fetch ("where host = '%s'" % Utils.myHostName( ))
            thisNode.status = OFFLINE
            thisNode.update()
        self.updateRenderNodeInfo()
        
if __name__ == '__main__':
    
    app = QApplication( sys.argv )
    
    window = getOffWindow( )
    
    window.show( )
    # window.server.createIdleLoop(5, window.updateRenderNodeInfo) -- can't make it stop?
    window.updateRenderNodeInfo()
    retcode = app.exec_( )
    sys.exit( retcode )
