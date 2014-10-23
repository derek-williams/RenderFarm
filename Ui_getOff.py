# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_getOff.ui'
#
# Created: Tue Feb 19 23:44:49 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(433, 165)
        MainWindow.setMinimumSize(QtCore.QSize(433, 165))
        MainWindow.setMaximumSize(QtCore.QSize(433, 165))
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 95, 100))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.onlineButton = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.onlineButton.sizePolicy().hasHeightForWidth())
        self.onlineButton.setSizePolicy(sizePolicy)
        self.onlineButton.setObjectName(_fromUtf8("onlineButton"))
        self.gridLayout.addWidget(self.onlineButton, 0, 0, 1, 1)
        self.getoffButton = QtGui.QPushButton(self.layoutWidget)
        self.getoffButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.getoffButton.setObjectName(_fromUtf8("getoffButton"))
        self.gridLayout.addWidget(self.getoffButton, 2, 0, 1, 1)
        self.offlineButton = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.offlineButton.sizePolicy().hasHeightForWidth())
        self.offlineButton.setSizePolicy(sizePolicy)
        self.offlineButton.setObjectName(_fromUtf8("offlineButton"))
        self.gridLayout.addWidget(self.offlineButton, 1, 0, 1, 1)
        self.statusLabel = QtGui.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(140, 40, 281, 16))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.jobLabel = QtGui.QLabel(self.centralwidget)
        self.jobLabel.setGeometry(QtCore.QRect(140, 60, 281, 16))
        self.jobLabel.setObjectName(_fromUtf8("jobLabel"))
        self.nameLabel = QtGui.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(140, 20, 281, 16))
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.refreshButton = QtGui.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(140, 90, 93, 28))
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Render Node Control", None))
        self.onlineButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Set render node status to ONLINE. The node will begin looking for new render jobs to do.</p></body></html>", None))
        self.onlineButton.setText(_translate("MainWindow", "Online", None))
        self.getoffButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Kill the current job and set render node status to OFFLINE. The render node will not look for new jobs until its put back on-line.</p></body></html>", None))
        self.getoffButton.setText(_translate("MainWindow", "Get Off!", None))
        self.offlineButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Set render node status to OFFLINE. The render node will complete its current job, if any, and stop looking for new jobs.</p></body></html>", None))
        self.offlineButton.setText(_translate("MainWindow", "Offline", None))
        self.statusLabel.setText(_translate("MainWindow", "Status:", None))
        self.jobLabel.setText(_translate("MainWindow", "Job id:", None))
        self.nameLabel.setText(_translate("MainWindow", "Node name:", None))
        self.refreshButton.setText(_translate("MainWindow", "Refresh Info", None))

