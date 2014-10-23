import sys

from PyQt4.QtGui import *                       # @UnusedWildImport
from PyQt4.QtCore import *                      # @UnusedWildImport
from Ui_JobListTest import Ui_MainWindow
from TaskSearchDialog import TaskSearchDialog

from MySQLSetup import Hydra_job, Hydra_rendertask
from MySQLdb import Error as sqlerror
from LoggingSetup import logger
import pickle
from JobKill import killJob, killTask, resurrectTask, socketerror
from MessageBoxes import aboutBox, yesNoBox
from datetime import datetime as dt
from JobPriority import prioritizeJob
import JobTicket                                # @UnusedImport


codes = {'I': 'idle',
         'R': 'ready',
         'O': 'offline',
         'F': 'finished',
         'S': 'started'}

class JobListWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.refreshHandler()

        QObject.connect (self.refreshButton, SIGNAL("clicked()"), 
                         self.refreshHandler)
        QObject.connect (self.jobTable, SIGNAL ("cellClicked(int,int)"), 
                         self.jobCellClickedHandler)
        QObject.connect (self.killJobButton, SIGNAL ("clicked()"), 
                         self.killJobButtonHandler)
        QObject.connect (self.killTaskButton, SIGNAL ("clicked()"), 
                         self.killTaskButtonHandler)
        QObject.connect (self.advancedSearchButton, SIGNAL ("clicked()"),
                         self.advancedSearchButtonClicked)
        QObject.connect (self.resurrectTaskButton, SIGNAL("clicked()"),
                         self.resurrectTaskButtonHandler)
        QObject.connect (self.prioritySetButton, SIGNAL("clicked()"),
                         self.setPriorityButtonHandler)
        
    def refreshHandler (self, *args):
        try:
            jobs = Hydra_job.fetch ()
            self.jobTable.setRowCount (len (jobs))
            for pos, job in enumerate (jobs):
                ticket = pickle.loads(job.pickledTicket)
                self.jobTable.setItem (pos, 0, 
                                       QTableWidgetItem_int(str(job.id)))
                self.jobTable.setItem (pos, 1, 
                                       QTableWidgetItem_int(str(job.priority)))
                self.jobTable.setItem (pos, 2, 
                                       QTableWidgetItem(ticket.name()))
        except sqlerror as err:
            logger.debug(str(err))
            aboutBox(self, "SQL error", str(err))

    def jobCellClickedHandler (self, row, column):
        # populate the task table widget
        item = self.jobTable.item (row, 0)
        job_id = int (item.text ())
        self.taskTableLabel.setText("Task List (job: " + item.text() + ")")
        try:
            tasks = Hydra_rendertask.fetch ("where job_id = %d" % job_id)
            self.taskTable.setRowCount (len (tasks))
            for pos, task in enumerate (tasks):
                # calcuate time difference
                tdiff = None
                if task.endTime:
                    tdiff = task.endTime - task.startTime
                elif task.startTime:
                    tdiff = dt.now().replace(microsecond=0) - task.startTime
                
                # populate table
                self.taskTable.setItem(pos, 0, 
                                       QTableWidgetItem_int(str(task.id)))
                self.taskTable.setItem(pos, 1, 
                                       QTableWidgetItem_int(str(task.priority)))
                self.taskTable.setItem(pos, 2, 
                                       QTableWidgetItem(str(task.host)))
                self.taskTable.setItem(pos, 3, 
                                       QTableWidgetItem(str(task.status)))
                self.taskTable.setItem(pos, 4, 
                                       QTableWidgetItem_dt(task.startTime))
                self.taskTable.setItem(pos, 5, 
                                       QTableWidgetItem_dt(task.endTime))
                self.taskTable.setItem(pos, 6, QTableWidgetItem_dt(str(tdiff)))
        except sqlerror as err:
            aboutBox(self, "SQL Error", str(err))
            
    def advancedSearchButtonClicked(self):
        results = TaskSearchDialog.create()
        print results

    def killJobButtonHandler (self):
        item = self.jobTable.currentItem()
        if item and item.isSelected ():
            row = self.jobTable.currentRow()
            id = int(self.jobTable.item(row, 0).text()) # @ReservedAssignment
            choice = yesNoBox(self, "Confirm", "Really kill job {:d}?"
                              .format(id))
            if choice == QMessageBox.Yes:
                try:
                    if killJob(id):
                        aboutBox(self, "Error", "Some nodes couldn't kill "
                                 + "their tasks.")
                except sqlerror as err:
                    logger.debug(str(err))
                    aboutBox(self, "SQL Error", str(err))
                finally:
                    self.jobCellClickedHandler(item.row(), 0)

    def setPriorityButtonHandler (self):
        item = self.jobTable.currentItem()
        if item and item.isSelected ():
            row = self.jobTable.currentRow()
            id = int(self.jobTable.item(row, 0).text()) # @ReservedAssignment
            prioritizeJob (id, self.prioritySpinBox.value ())
            self.jobCellClickedHandler(item.row(), 0)
            self.refreshHandler ([])
            
    def resurrectTaskButtonHandler(self):
        taskItem = self.taskTable.currentItem()
        if taskItem and taskItem.isSelected():
            row = self.taskTable.currentRow()
            id = int (self.taskTable.item(row, 0).text()) # @ReservedAssignment
            choice = yesNoBox(self, "Confirm", "Resurrect task {:d}?"
                              .format(id))
            if choice == QMessageBox.Yes:
                error = None
                try:
                    error = resurrectTask(id)
                except sqlerror as err:
                    logger.debug(str(err))
                    aboutBox(self, "SQL Error", str(err))
                finally:
                    if error:
                        msg = ("Task couldn't be resurrected because it's "
                         "either not dead or is currently running.")
                        logger.debug(msg)
                        aboutBox(self, "Error", msg)
                    else:
                        jobItem = self.jobTable.currentItem()
                        self.jobCellClickedHandler(jobItem.row(), 0)

    def killTaskButtonHandler (self):
        item = self.taskTable.currentItem ()
        if item and item.isSelected ():
            row = self.taskTable.currentRow ()
            id = int (self.taskTable.item (row, 0).text ()) #@ReservedAssignment
            choice = yesNoBox(self, "Confirm", "Really kill task {:d}?"
                              .format(id))
            if choice == QMessageBox.Yes:
                try:
                    killTask(id)
                except socketerror as err:
                    logger.debug(str(err))
                    aboutBox(self, "Error", "Task couldn't be killed because "
                    "there was a problem communicating with the host running "
                    "it.")
                except sqlerror as err:
                    logger.debug(str(err))
                    aboutBox(self, "SQL Error", str(err))

class QTableWidgetItem_int(QTableWidgetItem):
    """A QTableWidgetItem which holds integer data and sorts it properly."""
    
    def __init__(self, stringValue):
        QTableWidgetItem.__init__(self, stringValue)
    
    def __lt__(self, other):
        return int(self.text()) < int(other.text())

class QTableWidgetItem_dt(QTableWidgetItem):
    """A QTableWidgetItem which holds datetime data and sorts it properly."""

    def __init__(self, dtValue):
        QTableWidgetItem.__init__(self, str(dtValue))
        self.dtValue = dtValue
    
    def __lt__(self, other):
        return self.dtValue < other.dtValue
                       
if __name__ == '__main__':
    app = QApplication( sys.argv )
    
    window = JobListWindow( )
    
    window.show( )
    retcode = app.exec_( )
    sys.exit( retcode )
