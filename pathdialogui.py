# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pathdialog.ui'
#
# Created: Wed Dec 30 22:53:43 2009
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
        self.treeView = QtGui.QTreeView(PathDialog)
        self.treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.treeView.setIndentation(0)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.buttonAdd = QtGui.QPushButton(PathDialog)
        self.buttonAdd.setAutoDefault(False)
        self.buttonAdd.setDefault(True)
        self.buttonAdd.setObjectName("buttonAdd")
        self.gridLayout.addWidget(self.buttonAdd, 2, 0, 1, 1)
        self.buttonRescan = QtGui.QPushButton(PathDialog)
        self.buttonRescan.setObjectName("buttonRescan")
        self.gridLayout.addWidget(self.buttonRescan, 2, 4, 1, 1)
        self.buttonEdit = QtGui.QPushButton(PathDialog)
        self.buttonEdit.setObjectName("buttonEdit")
        self.gridLayout.addWidget(self.buttonEdit, 2, 2, 1, 1)
        self.buttonDelete = QtGui.QPushButton(PathDialog)
        self.buttonDelete.setObjectName("buttonDelete")
        self.gridLayout.addWidget(self.buttonDelete, 2, 3, 1, 1)

        self.retranslateUi(PathDialog)
        QtCore.QMetaObject.connectSlotsByName(PathDialog)

    def retranslateUi(self, PathDialog):
        PathDialog.setWindowTitle(QtGui.QApplication.translate("PathDialog", "Repositories", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("PathDialog", "Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRescan.setText(QtGui.QApplication.translate("PathDialog", "Rescan", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonEdit.setText(QtGui.QApplication.translate("PathDialog", "Edit...", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDelete.setText(QtGui.QApplication.translate("PathDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

