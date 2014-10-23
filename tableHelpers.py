from PyQt4.QtGui import *       # @UnusedWildImport
from PyQt4.QtCore import *      # @UnusedWildImport

class TableWidgetItem (QTableWidgetItem):

    def setIntoTable (self, table, row, column):
        table.setItem (row, column, self)

class WidgetForTable:

    def setIntoTable (self, table, row, column):
        table.setCellWidget (row, column, self)

class LabelForTable (QLabel, WidgetForTable): pass

class TableWidgetItem_check(TableWidgetItem):
    def __init__(self):
        TableWidgetItem.__init__(self)
        self.setCheckState(Qt.Unchecked)