
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QObject, SIGNAL
from Ui_TaskSearchDialog import Ui_taskSearchDialog

class TaskSearchDialog(QDialog, Ui_taskSearchDialog):
    """A dialog box for running queries on Hydra_rendertask."""

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.searchBtnClicked = False
        
        QObject.connect(self.cancelBtn, SIGNAL("clicked()"), 
                        self.onCancelBtnClicked)
        QObject.connect(self.searchBtn, SIGNAL("clicked()"),
                        self.onSearchBtnClicked)
        
    def getValues(self):
        taskStr = str(self.idBox.text())
        hostStr = str(self.hostnameBox.text())
        statusStr = str(self.statusBox.text())
        cmdStr = str(self.cmdBox.text())
        return dict(task_id=taskStr, host=hostStr, status=statusStr, cmd=cmdStr)
    
    def onCancelBtnClicked(self):
        self.close()
        return None
    
    def onSearchBtnClicked(self):
        self.searchBtnClicked = True
        self.close()
    
    @classmethod
    def create(cls):
        dialog = TaskSearchDialog()
        dialog.exec_()
        if dialog.searchBtnClicked:
            return dialog.getValues()
