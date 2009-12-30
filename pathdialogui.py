# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pathdialog.ui'
#
# Created: Tue Dec 29 01:31:08 2009
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PathDialog(object):
    def setupUi(self, PathDialog):
        PathDialog.setObjectName("PathDialog")
        PathDialog.resize(453, 297)
        self.gridLayout = QtGui.QGridLayout(PathDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonDelete = QtGui.QPushButton(PathDialog)
        self.buttonDelete.setAutoDefault(False)
        self.buttonDelete.setObjectName("buttonDelete")
        self.gridLayout.addWidget(self.buttonDelete, 1, 2, 1, 1)
        self.buttonAdd = QtGui.QPushButton(PathDialog)
        self.buttonAdd.setAutoDefault(False)
        self.buttonAdd.setDefault(True)
        self.buttonAdd.setObjectName("buttonAdd")
        self.gridLayout.addWidget(self.buttonAdd, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.treeView = QtGui.QTreeView(PathDialog)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 3)

        self.retranslateUi(PathDialog)
        QtCore.QMetaObject.connectSlotsByName(PathDialog)

    def retranslateUi(self, PathDialog):
        PathDialog.setWindowTitle(QtGui.QApplication.translate("PathDialog", "Repositories", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDelete.setText(QtGui.QApplication.translate("PathDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("PathDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

