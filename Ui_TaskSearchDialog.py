# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_TaskSearchDialog.ui'
#
# Created: Sat Mar 09 00:57:34 2013
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

class Ui_taskSearchDialog(object):
    def setupUi(self, taskSearchDialog):
        taskSearchDialog.setObjectName(_fromUtf8("taskSearchDialog"))
        taskSearchDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        taskSearchDialog.resize(375, 216)
        taskSearchDialog.setMinimumSize(QtCore.QSize(0, 216))
        taskSearchDialog.setMaximumSize(QtCore.QSize(16777215, 216))
        self.gridLayout = QtGui.QGridLayout(taskSearchDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(taskSearchDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.idBox = QtGui.QLineEdit(self.groupBox)
        self.idBox.setObjectName(_fromUtf8("idBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.idBox)
        self.hostEqualsLabel = QtGui.QLabel(self.groupBox)
        self.hostEqualsLabel.setObjectName(_fromUtf8("hostEqualsLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.hostEqualsLabel)
        self.hostnameBox = QtGui.QLineEdit(self.groupBox)
        self.hostnameBox.setObjectName(_fromUtf8("hostnameBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.hostnameBox)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.statusBox = QtGui.QLineEdit(self.groupBox)
        self.statusBox.setObjectName(_fromUtf8("statusBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.statusBox)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cmdBox = QtGui.QLineEdit(self.groupBox)
        self.cmdBox.setObjectName(_fromUtf8("cmdBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cmdBox)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.searchBtn = QtGui.QPushButton(taskSearchDialog)
        self.searchBtn.setObjectName(_fromUtf8("searchBtn"))
        self.horizontalLayout.addWidget(self.searchBtn)
        self.cancelBtn = QtGui.QPushButton(taskSearchDialog)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(taskSearchDialog)
        QtCore.QMetaObject.connectSlotsByName(taskSearchDialog)

    def retranslateUi(self, taskSearchDialog):
        taskSearchDialog.setWindowTitle(_translate("taskSearchDialog", "Task Search", None))
        self.groupBox.setTitle(_translate("taskSearchDialog", "Select from Hydra tasks where...", None))
        self.label_2.setText(_translate("taskSearchDialog", "Task ID equals:", None))
        self.hostEqualsLabel.setText(_translate("taskSearchDialog", "Hostname equals:", None))
        self.label.setText(_translate("taskSearchDialog", "Status equals:", None))
        self.label_3.setText(_translate("taskSearchDialog", "CMD is like: ", None))
        self.searchBtn.setText(_translate("taskSearchDialog", "Search", None))
        self.cancelBtn.setText(_translate("taskSearchDialog", "Cancel", None))

