# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sampleman.ui'
#
# Created: Mon Dec 28 17:56:08 2009
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(651, 496)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tagView = QtGui.QListView(self.centralwidget)
        self.tagView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tagView.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.tagView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tagView.setObjectName("tagView")
        self.gridLayout.addWidget(self.tagView, 0, 0, 2, 1)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 2)
        self.fileView = QtGui.QTreeView(self.centralwidget)
        self.fileView.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
        self.fileView.setDragEnabled(True)
        self.fileView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.fileView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.fileView.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.fileView.setIndentation(0)
        self.fileView.setRootIsDecorated(False)
        self.fileView.setSortingEnabled(True)
        self.fileView.setExpandsOnDoubleClick(True)
        self.fileView.setObjectName("fileView")
        self.fileView.header().setCascadingSectionResizes(False)
        self.fileView.header().setHighlightSections(True)
        self.fileView.header().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.fileView, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 651, 22))
        self.menubar.setObjectName("menubar")
        self.menuLibrary = QtGui.QMenu(self.menubar)
        self.menuLibrary.setObjectName("menuLibrary")
        self.menuRescan_folders = QtGui.QMenu(self.menuLibrary)
        self.menuRescan_folders.setObjectName("menuRescan_folders")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionTest = QtGui.QAction(MainWindow)
        self.actionTest.setObjectName("actionTest")
        self.actionManage_directories = QtGui.QAction(MainWindow)
        self.actionManage_directories.setObjectName("actionManage_directories")
        self.actionAll_folders = QtGui.QAction(MainWindow)
        self.actionAll_folders.setObjectName("actionAll_folders")
        self.actionManage_folders = QtGui.QAction(MainWindow)
        self.actionManage_folders.setObjectName("actionManage_folders")
        self.menuRescan_folders.addAction(self.actionAll_folders)
        self.menuRescan_folders.addSeparator()
        self.menuLibrary.addAction(self.menuRescan_folders.menuAction())
        self.menuLibrary.addAction(self.actionManage_folders)
        self.menubar.addAction(self.menuLibrary.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Sampleman", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLibrary.setTitle(QtGui.QApplication.translate("MainWindow", "Library", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRescan_folders.setTitle(QtGui.QApplication.translate("MainWindow", "Rescan folders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManage_directories.setText(QtGui.QApplication.translate("MainWindow", "Setup folders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAll_folders.setText(QtGui.QApplication.translate("MainWindow", "All folders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManage_folders.setText(QtGui.QApplication.translate("MainWindow", "Manage folders", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

