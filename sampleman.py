# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sampleman.ui'
#
# Created: Sun Feb 14 18:52:34 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(647, 562)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.fileView = QtGui.QListView(self.centralwidget)
        self.fileView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.fileView.setDragEnabled(True)
        self.fileView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.fileView.setAlternatingRowColors(True)
        self.fileView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.fileView.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.fileView.setLayoutMode(QtGui.QListView.Batched)
        self.fileView.setBatchSize(30)
        self.fileView.setObjectName("fileView")
        self.gridLayout.addWidget(self.fileView, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.seekSlider_2 = phonon.Phonon.SeekSlider(self.frame)
        self.seekSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.seekSlider_2.setObjectName("seekSlider_2")
        self.verticalLayout_2.addWidget(self.seekSlider_2)
        self.volumeSlider_2 = phonon.Phonon.VolumeSlider(self.frame)
        self.volumeSlider_2.setObjectName("volumeSlider_2")
        self.verticalLayout_2.addWidget(self.volumeSlider_2)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 647, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen_with = QtGui.QMenu(self.menuFile)
        self.menuOpen_with.setObjectName("menuOpen_with")
        self.menuOpen_copy_with = QtGui.QMenu(self.menuFile)
        self.menuOpen_copy_with.setObjectName("menuOpen_copy_with")
        self.menuExport_as = QtGui.QMenu(self.menuFile)
        self.menuExport_as.setObjectName("menuExport_as")
        self.menuLibrary = QtGui.QMenu(self.menubar)
        self.menuLibrary.setObjectName("menuLibrary")
        self.menuRescan_folders = QtGui.QMenu(self.menuLibrary)
        self.menuRescan_folders.setObjectName("menuRescan_folders")
        self.menuTags = QtGui.QMenu(self.menubar)
        self.menuTags.setObjectName("menuTags")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtGui.QDockWidget(MainWindow)
        self.dockWidget_2.setFeatures(QtGui.QDockWidget.DockWidgetClosable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tagView = QtGui.QListView(self.dockWidgetContents_2)
        self.tagView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tagView.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.tagView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tagView.setObjectName("tagView")
        self.verticalLayout.addWidget(self.tagView)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_2)
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
        self.actionEdit_all = QtGui.QAction(MainWindow)
        self.actionEdit_all.setObjectName("actionEdit_all")
        self.actionEdit_one_by_one = QtGui.QAction(MainWindow)
        self.actionEdit_one_by_one.setObjectName("actionEdit_one_by_one")
        self.actionApp = QtGui.QAction(MainWindow)
        self.actionApp.setObjectName("actionApp")
        self.actionApp_2 = QtGui.QAction(MainWindow)
        self.actionApp_2.setObjectName("actionApp_2")
        self.action_home_johannes = QtGui.QAction(MainWindow)
        self.action_home_johannes.setObjectName("action_home_johannes")
        self.actionPlay = QtGui.QAction(MainWindow)
        self.actionPlay.setCheckable(True)
        self.actionPlay.setObjectName("actionPlay")
        self.menuFile.addAction(self.menuOpen_with.menuAction())
        self.menuFile.addAction(self.menuOpen_copy_with.menuAction())
        self.menuFile.addAction(self.menuExport_as.menuAction())
        self.menuFile.addAction(self.actionPlay)
        self.menuRescan_folders.addAction(self.actionAll_folders)
        self.menuRescan_folders.addSeparator()
        self.menuLibrary.addAction(self.menuRescan_folders.menuAction())
        self.menuLibrary.addAction(self.actionManage_folders)
        self.menuTags.addAction(self.actionEdit_all)
        self.menuTags.addAction(self.actionEdit_one_by_one)
        self.menubar.addAction(self.menuLibrary.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTags.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Sampleman", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOpen_with.setTitle(QtGui.QApplication.translate("MainWindow", "Open with", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOpen_copy_with.setTitle(QtGui.QApplication.translate("MainWindow", "Open copy with", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport_as.setTitle(QtGui.QApplication.translate("MainWindow", "Export as", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLibrary.setTitle(QtGui.QApplication.translate("MainWindow", "Repos", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRescan_folders.setTitle(QtGui.QApplication.translate("MainWindow", "Rescan repos", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTags.setTitle(QtGui.QApplication.translate("MainWindow", "Meta", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_2.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManage_directories.setText(QtGui.QApplication.translate("MainWindow", "Setup folders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAll_folders.setText(QtGui.QApplication.translate("MainWindow", "All folders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManage_folders.setText(QtGui.QApplication.translate("MainWindow", "Manage repos", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_all.setText(QtGui.QApplication.translate("MainWindow", "Edit all", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_one_by_one.setText(QtGui.QApplication.translate("MainWindow", "Edit one by one", None, QtGui.QApplication.UnicodeUTF8))
        self.actionApp.setText(QtGui.QApplication.translate("MainWindow", "App", None, QtGui.QApplication.UnicodeUTF8))
        self.actionApp_2.setText(QtGui.QApplication.translate("MainWindow", "App", None, QtGui.QApplication.UnicodeUTF8))
        self.action_home_johannes.setText(QtGui.QApplication.translate("MainWindow", "/home/johannes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay.setShortcut(QtGui.QApplication.translate("MainWindow", "Space", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import phonon
