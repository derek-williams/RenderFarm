# standard
import sys
from exceptions import NotImplementedError
from datetime import datetime as dt
import functools
import re
from socket import error as socketerror

# 3rd party
from MySQLdb import Error as sqlerror

# Qt
from PyQt4.QtGui import *                       #@UnusedWildImport
from PyQt4.QtCore import *                      #@UnusedWildImport
from Ui_FarmView import Ui_FarmView
from TaskSearchDialog import TaskSearchDialog

# Project Hydra
from tableHelpers import *                      #@UnusedWildImport
from MySQLSetup import *                        #@UnusedWildImport
from LoggingSetup import logger                 #@Reimport
import Utils                                    #@Reimport
from MessageBoxes import aboutBox, yesNoBox
from JobKill import sendKillQuestion, killJob, killTask, resurrectTask
from JobPriority import prioritizeJob
import pickle
import JobTicket                                # @UnusedImport

class FarmView( QMainWindow, Ui_FarmView ):

    def __init__( self ):
        
        QMainWindow.__init__( self )
        self.setupUi( self )
        
        # Column widths on the render node table
        self.renderNodeTable.setColumnWidth(0, 30)  # check boxes
        self.renderNodeTable.setColumnWidth(1, 200) # host
        self.renderNodeTable.setColumnWidth(2, 70)  # status
        self.renderNodeTable.setColumnWidth(3, 70)  # task id
        self.renderNodeTable.setColumnWidth(5, 100) # project
        self.renderNodeTable.setColumnWidth(6, 150) # heartbeat

        # State variables for the This Node tab
        self.lastProjectIndex = -1
        self.thisNodeButtonsEnabled = True
        
        # Connect buttons on the This Node tab with their actions
        QObject.connect(self.fetchButton, SIGNAL("clicked()"), self.doFetch)
        QObject.connect(self.onlineThisNodeButton, SIGNAL("clicked()"), 
                        self.onlineThisNodeButtonClicked)
        QObject.connect(self.offlineThisNodeButton, SIGNAL("clicked()"), 
                        self.offlineThisNodeButtonClicked)
        QObject.connect(self.getOffThisNodeButton, SIGNAL("clicked()"), 
                        self.getOffThisNodeButtonClicked)
        QObject.connect(self.projectComboBox, SIGNAL("activated(int)"), 
                        self.projectSelectionHandler)
        
        # Connect buttons on the Render Nodes tab with their actions
        QObject.connect(self.onlineRenderNodesButton, SIGNAL("clicked()"), 
                        self.onlineRenderNodesButtonClicked)
        QObject.connect(self.offlineRenderNodesButton, SIGNAL("clicked()"),
                        self.offlineRenderNodesButtonClicked)
        QObject.connect(self.getOffRenderNodesButton, SIGNAL("clicked()"),
                        self.getOffRenderNodesButtonClicked)
        
        # Connect buttons on the Job List tab with their actions
        QObject.connect(self.refreshButton, SIGNAL("clicked()"), 
                        self.updateJobTable)
        QObject.connect(self.jobTable, SIGNAL ("cellClicked(int,int)"), 
                        self.jobCellClickedHandler)
        QObject.connect (self.killJobButton, SIGNAL ("clicked()"), 
                        self.killJobButtonHandler)
        QObject.connect(self.killTaskButton, SIGNAL ("clicked()"), 
                        self.killTaskButtonHandler)
        QObject.connect(self.advancedSearchButton, SIGNAL ("clicked()"),
                        self.advancedSearchButtonClicked)
        QObject.connect(self.resurrectTaskButton, SIGNAL("clicked()"),
                        self.resurrectTaskButtonHandler)
        QObject.connect(self.prioritySetButton, SIGNAL("clicked()"),
                        self.setPriorityButtonHandler)
        QObject.connect(self.taskIDLineEdit, SIGNAL("returnPressed()"), 
                        self.searchByTaskID)
        
        self.jobTable.setColumnWidth(0, 60)     # job id
        self.jobTable.setColumnWidth(1, 60)     # priority
        self.jobTable.sortItems(0, order = Qt.DescendingOrder)
        
        # partial applications for convenience
        self.sqlErrorBox = (
            functools.partial(aboutBox, 
                        parent=self, 
                        title="Error", 
                        msg="There was a problem while trying to fetch info"
                        " from the database. Check the FarmView log file for"
                        " more details about the error.")
        )
        self.noneCheckedBox = (
            functools.partial(aboutBox,
                        parent=self,
                        title="None checked",
                        msg= "No nodes have been selected. Use the check boxes" 
                        " to make a selection from the table.")
        )
        
        # let there be data
        self.doFetch()
        
    def onlineThisNodeButtonClicked(self):
        """Changes the local render node's status to online if it was offline,
        goes back to started if it was pending offline."""
        
        # get most current info from the database
        thisNode = None
        try:
            thisNode = getThisNodeData()
        except sqlerror as err:
            logger.debug(str(err))
            self.sqlErrorBox()
            return
        
        if thisNode:
            onlineNode(thisNode)
        
        self.doFetch()
            
    def offlineThisNodeButtonClicked(self):
        """Changes the local render node's status to offline if it was idle,
        pending if it was working on something."""
        
        # get the most current info from the database
        thisNode = None
        try:
            thisNode = getThisNodeData()
        except sqlerror as err:
            logger.debug(str(err))
            self.sqlErrorBox()
            return
        
        if thisNode:
            offlineNode(thisNode)
            
        self.doFetch()
    
    def getOffThisNodeButtonClicked(self):
        """Offlines the node and sends a message to the render node server 
        running on localhost to kill its current task (task will be 
        resubmitted)"""
        
        thisNode = None
        try:
            thisNode = getThisNodeData()
        except sqlerror as err:
            logger.debug(str(err))
            self.sqlErrorBox()
            return
        
        choice = yesNoBox(self, "Confirm", "All progress on the current job"
                          " will be lost. Are you sure you want to stop it?")
        if choice != QMessageBox.Yes:
            aboutBox(self, "Abort", "No action taken.")
            return
        
        if thisNode:
            offlineNode(thisNode)
                
            if thisNode.task_id:
                try:
                    # TODO: use JobKill for getOff instead of doing it manually
                    killed = sendKillQuestion(renderhost = "localhost", 
                                              newStatus = READY)
                    if not killed:
                        logger.debug("There was a problem killing the task.")
                        aboutBox(self, "Error", "There was a problem killing"
                                 " the task.")
                    else:
                        aboutBox(self, "Success", "Job was successfully"
                                 " stopped. Node offlined.")
                except socketerror:
                    logger.debug(socketerror.message)
                    aboutBox(self, "Error", "There was a problem communicating"
                             " with the render node software. Either it's not"
                             " running, or it has become unresponsive.")
            else:
                aboutBox(self, "Offline", "No job was running. Node offlined.")
                
        self.doFetch()
    
    def onlineRenderNodesButtonClicked(self):
        
        hosts = getCheckedItems(table=self.renderNodeTable, itemColumn=1, 
                                checkBoxColumn=0)
        if len(hosts) == 0:
            self.noneCheckedBox()
            return
        
        choice = yesNoBox(self, "Confirm", "Are you sure you want to online"
                          " these nodes? <br>" + str(hosts))
        
        if choice != QMessageBox.Yes:
            aboutBox(self, "Aborted", "No action taken.")
            return
        
        with transaction() as t:
            rendernode_rows = Hydra_rendernode.fetch(explicitTransaction=t)
            for node_row in rendernode_rows:
                if node_row.host in hosts:
                    onlineNode(node_row)
        self.doFetch()
                    
    def offlineRenderNodesButtonClicked(self):
        """For all nodes with boxes checked in the render nodes table, changes
        status to offline if idle, or pending if started."""
        
        hosts = getCheckedItems(table=self.renderNodeTable, itemColumn=1,
                                checkBoxColumn=0)
        if len(hosts) == 0:
            self.noneCheckedBox()
            return
        
        choice = yesNoBox(self, "Confirm", "Are you sure you want to offline"
                          " these nodes? <br>" + str(hosts))
        
        if choice != QMessageBox.Yes:
            aboutBox(self, "Aborted", "No action taken.")
            return
        
        with transaction() as t:
            rendernode_rows = Hydra_rendernode.fetch(explicitTransaction=t)
            for node_row in rendernode_rows:
                if node_row.host in hosts:
                    offlineNode(node_row)
        self.doFetch()
    
    def getOffRenderNodesButtonClicked(self):
        """For all nodes with boxes checked in the render nodes table, changes
        status to offline if idle, or pending if started, and attempts to kill
        any task that is running on each node."""
        
        hosts = getCheckedItems(table=self.renderNodeTable, itemColumn=1,
                                checkBoxColumn=0)
        if len(hosts) == 0:
            self.noneCheckedBox()
            return
        
        choice = yesNoBox(self, "Confirm", "<B>WARNING</B>: All progress on"
                          " current tasks will be lost for the selected"
                          " render nodes. Are you sure you want to stop these"
                          " nodes? <br>" + str(hosts))
        
        if choice != QMessageBox.Yes:
            aboutBox(self, "Aborted", "No action taken.")
            return
        
        error = False
        notKilledList = list()
        with transaction() as t:
            rendernode_rows = Hydra_rendernode.fetch(explicitTransaction=t)
            for node_row in rendernode_rows:
                if node_row.host in hosts:
                    offlineNode(node_row)
                    try:
                        killed = sendKillQuestion(node_row.host, READY)
                        error = error or not killed
                    except socketerror as err:
                        logger.debug(str(err) + '\n' 
                                     + "Error while trying to contact " 
                                     + node_row.host)
                        notKilledList.append(node_row.host)
                        error = True
        if error:
            aboutBox(self, "Error", "The following nodes could not be stopped"
                     " for some reason. Look in FarmView.log for more details."
                     "<br>" + str(notKilledList))
        self.doFetch()
    
    def projectSelectionHandler(self, currentProjectIndex):
        """Checks to see if project selection has changed. If so, handles the 
        change. Else, does nothing."""
        
        if currentProjectIndex != self.lastProjectIndex:
            self.projectChangeHandler(currentProjectIndex)
        
    def projectChangeHandler(self, index):
        """Handler for the event where the project selection changed."""
        
        selectedProject = self.projectComboBox.itemText(index)
        choice = yesNoBox(self, "Change project", "Reassign this node to " + 
                          selectedProject + "? (will avoid jobs from other"
                          " projects)")
        
        if choice != QMessageBox.Yes:
            aboutBox(self, "No changes", "This node will remain assigned to " + 
                     self.thisNode.project + ".")
            self.projectComboBox.setCurrentIndex(self.lastProjectIndex)
            return
        
        # get the most up to date info from the database
        thisNode = None
        try:
            thisNode = getThisNodeData()
        except sqlerror as err:
            logger.debug(str(err))
            self.sqlErrorBox()
            return
        
        thisNode.project = self.projectComboBox.currentText()
        with transaction() as t:
            thisNode.update(t)
        self.lastProjectIndex = self.projectComboBox.currentIndex()
        aboutBox(self, "Success", "Node reassigned to " + selectedProject)

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
                                       TableWidgetItem_int(str(task.id)))
                self.taskTable.setItem(pos, 1, 
                                       TableWidgetItem_int(str(task.priority)))
                self.taskTable.setItem(pos, 2, 
                                       TableWidgetItem(str(task.host)))
                self.taskTable.setItem(pos, 3, 
                                       TableWidgetItem(str(task.status)))
                self.taskTable.setItem(pos, 4, 
                                       TableWidgetItem_dt(task.startTime))
                self.taskTable.setItem(pos, 5, 
                                       TableWidgetItem_dt(task.endTime))
                self.taskTable.setItem(pos, 6, TableWidgetItem_dt(str(tdiff)))
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
            self.updateJobTable ([])
            
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
            task_id = int(self.taskTable.item(row, 0).text())
            choice = yesNoBox(self, "Confirm", "Really kill task {:d}?"
                              .format(task_id))
            if choice == QMessageBox.Yes:
                killed = None
                try:
                    killed = killTask(task_id)
                    if not killed:
                        # TODO: make a better error message
                        aboutBox(self, "Error", "Task couldn't be killed for "
                                 "some reason.")
                except socketerror as err:
                    logger.debug(str(err))
                    aboutBox(self, "Error", "Task couldn't be killed because "
                    "there was a problem communicating with the host running "
                    "it.")
                except sqlerror as err:
                    logger.debug(str(err))
                    aboutBox(self, "SQL Error", str(err))
                
    def searchByTaskID(self):
        """Given a task id, finds the job, selects it in the job table, and
        displays the tasks for that job, including the one searched for. Does
        nothing if task id doesn't exist."""
        
        # retrieve job id by task id in the database
        task_id = str(self.taskIDLineEdit.text())
        if task_id:
            with transaction() as t:
                query = "select job_id from Hydra_rendertask where id = %s"
                t.cur.execute(query % task_id)
                job_id = t.cur.fetchall()
                
                if not job_id:
                    aboutBox(self, "Error", "The given task ID does not "
                             "correspond to an existing job.")
                    return
                
                # find item with matching job id in the table
                ((job_id,),) = job_id # unpack -- TODO: fix this hack?
                [item] = self.jobTable.findItems(str(job_id), Qt.MatchExactly)
                
                # select the row and trigger the update for the task list
                self.jobTable.setCurrentItem(item)
                self.jobCellClickedHandler(item.row(), item.column())
                [item] = self.taskTable.findItems(str(task_id), Qt.MatchExactly)
                self.taskTable.setCurrentItem(item)
        else:
            aboutBox(self, "Error", "No task ID was entered.")
            return
        
    def doFetch( self ):
        """Aggregate method for updating all of the widgets."""
        
        try:
            self.updateThisNodeInfo()
            self.updateRenderNodeTable()
            self.updateRenderTaskGrid()
            self.updateJobTable()
            self.updateStatusBar()
        except sqlerror as err:
            logger.debug(str(err))
            self.sqlErrorBox()
        
    def updateThisNodeInfo(self):
        """Updates widgets on the "This Node" tab with the most recent 
        information available."""
        
        # if the buttons are disabled, don't bother
        if not self.thisNodeButtonsEnabled:
            return
        
        # get the most current info from the database
        thisNode = None
        try:
            thisNode = getThisNodeData()
            self.updateProjectComboBox()
        except sqlerror as err:
            logger.debug(str(err))
            self.sqlErrorBox()
        
        if thisNode:
            # update the labels
            self.nodeNameLabel.setText(thisNode.host)
            self.nodeStatusLabel.setText(niceNames[thisNode.status])
            self.updateTaskIDLabel(thisNode.task_id)
            self.nodeVersionLabel.setText(
                        getSoftwareVersionText(thisNode.software_version))
            
            self.setCurrentProjectSelection(thisNode.project)
            
        else:
            QMessageBox.about(self, "Notice", 
                "Information about this node cannot be displayed because it is"
                "not registered on the render farm. You may continue to use"
                " Farm View, but it must be restarted after this node is "
                "registered if you wish to see this node's information.")
            self.setThisNodeButtonsEnabled(False)
    
    def setThisNodeButtonsEnabled(self, choice):
        """Enables or disables buttons on This Node tab"""
        
        self.onlineThisNodeButton.setEnabled(choice)
        self.offlineThisNodeButton.setEnabled(choice)
        self.getOffThisNodeButton.setEnabled(choice)
        self.projectComboBox.setEnabled(choice)
        self.thisNodeButtonsEnabled = choice
        
    def updateProjectComboBox(self):
        """Clears and refreshes the contents of the projects dropdown box."""
        
        # remove all items from the dropdown
        count = self.projectComboBox.count()
        while count:
            self.projectComboBox.removeItem(0)
            count = self.projectComboBox.count()
        
        # get current list of projects from the database
        tuples = None #@UnusedVariable
        with transaction() as t:
            t.cur.execute("select * from Hydra_projects")
            tuples = t.cur.fetchall()
        
        # make flat list out of single-element tuples fetched from db
        projectsList = [t for (t,) in tuples]
        
        # refresh the dropdown
        for project in projectsList:
            self.projectComboBox.addItem(project)
    
    def updateTaskIDLabel(self, task_id):
        
        if task_id:
            self.taskIDLabel.setText(str(task_id))
        else:
            self.taskIDLabel.setText("None")
    
    def setCurrentProjectSelection(self, project):
        """Set project selection based on node's current project setting."""
        
        
        idx = self.projectComboBox.findText(project, 
                       flags=Qt.MatchExactly|Qt.MatchCaseSensitive)
        self.projectComboBox.setCurrentIndex(idx)
        self.lastProjectIndex = idx
        
    def updateRenderNodeTable(self):
        
        # clear the table (note: this is done to avoid duplication of items)
        self.renderNodeTable.clearContents()
        self.renderNodeTable.setRowCount(0)
        
        # prevent rows from being sorted while table is populating
        self.renderNodeTable.setSortingEnabled(False)
        
        rows = Hydra_rendernode.fetch(order="order by host")
        self.renderNodeTable.setRowCount (len (rows))
        columns = [
            lambda o: TableWidgetItem_check(),
            lambda o: TableWidgetItem(str(o.host)),
            lambda o: TableWidgetItem(str(niceNames[o.status])),
            lambda o: TableWidgetItem(str(o.task_id)),
            lambda o: TableWidgetItem(str(o.project)),
            lambda o: TableWidgetItem(
                                getSoftwareVersionText(o.software_version)),
            lambda o: TableWidgetItem_dt(o.pulse),
            ]
        for (rowIndex, row) in enumerate (rows):
            for (columnIndex, columnFun) in enumerate (columns):
                columnFun (row).setIntoTable (self.renderNodeTable,
                                              rowIndex, columnIndex)
        
        self.renderNodeTable.setSortingEnabled(True)
                
    def updateJobTable (self, *args):
        self.jobTable.setSortingEnabled(False)
        try:
            jobs = Hydra_job.fetch ()
            self.jobTable.setRowCount (len (jobs))
            for pos, job in enumerate (jobs):
                ticket = pickle.loads(job.pickledTicket)
                self.jobTable.setItem (pos, 0, 
                                       TableWidgetItem_int(str(job.id)))
                self.jobTable.setItem (pos, 1, 
                                       TableWidgetItem_int(str(job.priority)))
                self.jobTable.setItem (pos, 2, 
                                       QTableWidgetItem(ticket.name()))
        except sqlerror as err:
            logger.debug(str(err))
            aboutBox(self, "SQL error", str(err))
        self.jobTable.setSortingEnabled(True)
    
    def updateRenderTaskGrid(self):
        
        columns = [
            labelFactory( 'id' ),
            labelFactory( 'status' ),
            lineEditFactory( 'logFile' ),
            labelFactory( 'host' ),
            labelFactory( 'project' ),
            labelFactory( 'command' ),
            labelFactory( 'startTime' ),
            labelFactory( 'endTime' ),
            labelFactory( 'exitCode' )]
        setup( Hydra_rendertask.fetch (order = "order by id desc", 
                                       limit = self.limitSpinBox.value ()), 
                                       columns, self.taskGrid)

    def updateStatusBar(self):
        
        with transaction() as t:
            t.cur.execute ("""select count(status), status 
                                from Hydra_rendernode
                                group by status""")
            counts = t.cur.fetchall ()
        logger.debug (counts)
        countString = ", ".join (["%d %s" % (count, niceNames[status])
                                  for (count, status) in counts])
        time = dt.now().strftime ("%H:%M")
        msg = "%s as of %s" % (countString, time)
        self.statusLabel.setText (msg)

def getSoftwareVersionText(sw_ver):
    """Given the software_version attribute of a Hydra_rendernode row, returns
    a string suitable for display purposes."""
    
    # get RenderNodeMain version number if exists
    if sw_ver:
        
        # case 1: executable in a versioned directory
        v = re.search("rendernodemain-dist-([0-9]+)", sw_ver, 
                        re.IGNORECASE)
        if v:
            return v.group(1)
        
        # case 2: source code file
        elif re.search("rendernodemain.py$", sw_ver, re.IGNORECASE):
            return "Development source"
        
        # case 3: no freakin' clue
        return sw_ver
    
    else: 
        return "None"

def getThisNodeData():
    """Gets the row corresponding to localhost in the Hydra_rendernode table.
    Raises MySQLdb.Error"""
    
    [thisNode] = Hydra_rendernode.fetch("where host = '%s'" 
                                        % Utils.myHostName())
    return thisNode

def onlineNode(node):
    """Onlines the node. 
    Precondition: node refers to a row from the Hydra_rendernode table.
    Raises MySQLdb.Error"""
    
    if node.status == IDLE:
        return
    elif node.status == OFFLINE:
        node.status = IDLE
    elif node.status == PENDING and node.task_id:
        node.status = STARTED
    with transaction() as t:
        node.update(t)

def offlineNode(node):
    """Onlines the node. 
    Precondition: node refers to a row from the Hydra_rendernode table.
    Raises MySQLdb.Error"""
    
    if node.status == OFFLINE:
            return
    elif node.task_id:
        node.status = PENDING
    else:
        node.status = OFFLINE
    with transaction() as t:
            node.update(t)

def getCheckedItems(table, itemColumn, checkBoxColumn):
    """Given a table with a column of check boxes in it, returns a list of
    the items in itemColumn which have a checked box in the same row."""
    
    nRows = table.rowCount()
    checks = list()
    for rowIndex in range(0, nRows):
        item = str(table.item(rowIndex, itemColumn).text())
        checkState = table.item(rowIndex, checkBoxColumn).checkState()
        if checkState:
            checks.append(item)
    return checks

def setup(records, columns, grid):
    """Populate a data grid. "colums" is a list of widget factory objects."""
    
    # build the header row
    for (column, attr) in enumerate( columns ):
        item = grid.itemAtPosition( 0, column )
        if item:
            grid.removeItem( item )
            item.widget().hide()
        grid.addWidget( attr.headerWidget(), 0, column )
    
    # build the data rows
    for (row, record) in enumerate( records ):
        for (column, attr) in enumerate( columns ):
            item = grid.itemAtPosition( row + 1, column )
            if item:
                grid.removeItem( item )
                item.widget().hide()
            grid.addWidget(attr.dataWidget( record ),
                           row + 1,
                           column,
                           )

class widgetFactory():
    """A widget building class intended to be subclassed for building particular 
    types of widgets. 'name' must be the name of a database column."""
    
    def __init__(self, name):
        self.name = name
    
    def headerWidget(self):
        """Makes a label for the header row of the display."""
        
        return QLabel('<b>' + self.name + '</b>')
    
    def data(self, record):
        
        return str(getattr(record, self.name))
    
    def dataWidget(self, record):
        """Create a QWidget instance and return a reference to it. To make a 
        widget, given a record, extract the named attribute from the record
        with the data method, and use that as the widget's text/data."""
        
        raise NotImplementedError

class labelFactory(widgetFactory):
    """A label widget factory. The object's name is the name of a database 
    column."""
    
    def dataWidget( self, record ):
        
        return QLabel( self.data( record ) )

class lineEditFactory(widgetFactory):
    """like labelFactory, but makes a read-only text field instead of a 
    label."""
    
    def dataWidget( self, record ):
        
        w = QLineEdit( )
        w.setText( self.data( record ) )
        w.setReadOnly( True )
        return w

class versionLabelFactory(widgetFactory):
    """Builds a label specially for the software_version column in the render
    node table, trimming out non-essential information in the process."""
    
    def dataWidget (self, record ):
        
        sw_version_text = getSoftwareVersionText(self.data(record))
        return QLabel(sw_version_text)

class getOffButton(widgetFactory):
    """As above, but makes a specialized button to implement the GetOff 
    function."""
    
    def dataWidget ( self, record ):
        
        w = QPushButton( self.name )

        # the click handler is the doGetOff method, but with the record 
        # argument already supplied. it's called a "partial application".
        handler = functools.partial (self.doGetOff, record=record)

        QObject.connect (w, SIGNAL("clicked()"), handler)
        return w

    def doGetOff (self, record):
        
        logger.debug('clobber %s', record.host)

class TableWidgetItem_int(QTableWidgetItem):
    """A QTableWidgetItem which holds integer data and sorts it properly."""
    
    def __init__(self, stringValue):
        QTableWidgetItem.__init__(self, stringValue)
    
    def __lt__(self, other):
        return int(self.text()) < int(other.text())
    
class TableWidgetItem_dt(TableWidgetItem):
    """A QTableWidgetItem which holds datetime data and sorts it properly."""

    def __init__(self, dtValue):
        QTableWidgetItem.__init__(self, str(dtValue))
        self.dtValue = dtValue
    
    def __lt__(self, other):
        if self.dtValue and other.dtValue:
            return self.dtValue < other.dtValue
        elif self.dtValue and not other.dtValue:
            return True
        else:
            return False

if __name__ == '__main__':
    app = QApplication( sys.argv )
    window = FarmView( )

    window.show( )
    retcode = app.exec_( )
    sys.exit( retcode )
