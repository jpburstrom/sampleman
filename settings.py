# -*- coding: utf-8 -*-

import os
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT

from models import *
from settingsui import Ui_SettingsDialog


class SettingsDialog(QtGui.QDialog):
    """Settings editor."""

    newRepo = QtCore.pyqtSignal(unicode)
    newFolder = QtCore.pyqtSignal(unicode)
    newFormat = QtCore.pyqtSignal(unicode)
    newApp = QtCore.pyqtSignal(unicode)

    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)

        #NB: Repo settings are stored in db. This is for all other settings.
        self._settings = QtCore.QSettings("ljud.org", "Sampleman")

        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self._readSettingsArray("apps", self.ui.listWidget)
        self._readSettingsArray("formats", self.ui.listWidget_2)
        self._readSettingsArray("folders", self.ui.listWidget_3)
        
        self.repomodel = RepoModel(self)
        self.ui.treeView.setModel(self.repomodel)
        self.ui.treeView.resizeColumnToContents(0)

        #Repo-related signals
        self.connect(self.ui.buttonAdd_4, SIGNAL("clicked()"), self.addRepo)
        self.connect(self.ui.buttonDelete_4, SIGNAL("clicked()"), self.deleteRepo)
        self.connect(self.ui.buttonRescan, SIGNAL("clicked()"), self.rescanRepo)
        self.connect(self.ui.buttonEdit, SIGNAL("clicked()"), self.editRepo)
        #TODO: deactivate delete/rescan when item is not selected

        #Application
        self.connect(self.ui.buttonAdd, SIGNAL("clicked()"), self.addApp)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), self.deleteApp)
        self.connect(self.ui.listWidget, SIGNAL("itemChanged(QListWidgetItem *)"), self.appEdited)
        
        #Formats
        self.connect(self.ui.buttonAdd_2, SIGNAL("clicked()"), self.addFormat)
        self.connect(self.ui.buttonDelete_2, SIGNAL("clicked()"), self.deleteFormat)
        self.connect(self.ui.listWidget_2, SIGNAL("itemChanged(QListWidgetItem *)"), self.formatEdited)

        #Folders (For export)
        self.connect(self.ui.buttonAdd_3, SIGNAL("clicked()"), self.addFolder)
        self.connect(self.ui.buttonDelete_3, SIGNAL("clicked()"), self.deleteFolder)
        #self.connect(self.ui.listWidget_3, SIGNAL("itemChanged(QListWidgetItem *)"), self.folderEdited)


    def setTab(self, tab):
        """Set current tab by label, sort of."""

        tabs = ["repositories", "applications", "formats", "folders"]
        self.ui.tabWidget.setCurrentIndex(tabs.index(tab))

    def addRepo(self):
        """Add new repository.

        """
        path = QtGui.QFileDialog.getExistingDirectory(self, "Add a repository", os.path.expanduser("~"))
        if not path:
            return False
        repo = self.repomodel.add_repo(unicode(path))
        if QtGui.QMessageBox.question(
                self, "Question", "Would you like to scan the new repository?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes ) == QtGui.QMessageBox.Yes:
            self.repomodel.scan_repo(repo)
        session.commit()
        self.newRepo.emit(path)

    def deleteRepo(self):
        """Delete selected repository.

        """
        #TODO : dialog box choosing btwn deleting single path and deleting entire repo
        if QtGui.QMessageBox.question(
                self, "Are you sure?", "Delete repository and soundfile data? (This will not remove them from your filesystem)",
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel ) == QtGui.QMessageBox.Ok:
            for mi in self.ui.treeView.selectedIndexes():
                #FIXME: set column to 0 and find path
                if mi.column() == 0:
                    path = mi.data().toString()
                    break
            self.repomodel.delete_repo(unicode(path))
            self.parent().rebuild()
            session.commit()

    def rescanRepo(self):
        """Rescan selected repository.

        """
        for mi in self.ui.treeView.selectedIndexes():
            #FIXME: set column to 0 and find path
            if mi.column() == 0:
                path = mi.data().toString()
                repo = Repo.get_by(path=unicode(path))
                self.repomodel.scan_repo(repo)
                break

    def editRepo(self):
        """Edit repository paths.
        
        """
        print "Edit repo - to implement"
        mi = self.ui.treeView.selectedIndexes()[0]
        #FIXME
        #Get repo 
        #find item to edit
        #... (model stuff really)

    def addApp(self):
        """Add "open with..."-application.

        """
        #listWidget
        self._newListItem(self.ui.listWidget)

    def deleteApp(self):
        """Delete "Open with..."-application.

        """
        items = self._deleteSelected(self.ui.listWidget, "apps")

    def appEdited(self, item):
        text = item.text()
        if not text:
            return
        row = self.ui.listWidget.row(item)
        self._writeSettingsArray("apps", row, text)
        self.newApp.emit(text)

    def addFormat(self):
        """Add file export format.

        """
        self._newListItem(self.ui.listWidget_2)

    def deleteFormat(self):
        """Delete file export format.

        """
        items = self._deleteSelected(self.ui.listWidget_2, "formats")

    def formatEdited(self, item):
        text = item.text()
        if not text:
            return
        row = self.ui.listWidget_2.row(item)
        self._writeSettingsArray("formats", row, text)
        self.newFormat.emit(text)

    def addFolder(self):
        """Add file export folder.

        """
        path = QtGui.QFileDialog.getExistingDirectory(self, "Add an export folder", os.path.expanduser("~"))
        if not path:
            return False
        w = self.ui.listWidget_3
        w.addItem(path)
        i = w.count() - 1
        self._writeSettingsArray("folders", i, path)

    def deleteFolder(self):
        """Delete file export folder.

        """
        items = self._deleteSelected(self.ui.listWidget_3, "folders")

    def folderEdited(self, item):
        text = item.text()
        if not text:
            return
        row = self.ui.listWidget_3.row(item)
        self._writeSettingsArray("folders", row, text)
        self.newFolder.emit(text)

    def _deleteSelected(self, w, key):
        """Delete and return selected items from widget w.
        """
        if w.selectedIndexes() and not self._confirm():
            return None
        li = []
        self._settings.beginGroup(key)
        for item in w.selectedItems():
            row = w.row(item)
            self._settings.remove("{0}".format(row + 1))
            li.append(w.takeItem(row))
            self._settings.setValue("size", self._settings.value("size").toInt()[0] - 1)
        self._settings.endGroup()
        return li
    
    def _confirm(self):
        """Simple annoying confirmation dialog.
        """
        return QtGui.QMessageBox.question(
                self, "Are you sure?", "Are you sure?",
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel ) == QtGui.QMessageBox.Ok

    def _readSettingsArray(self, key, w):
        """Get settings array *key* into QListWidget *w*.
        
        """
        w.clear()
        size = self._settings.beginReadArray(key)
        for i in range(size):
            self._settings.setArrayIndex(i)
            w.addItem(self._settings.value("key").toString())
        self._settings.endArray()

    def _writeSettingsArray(self, key, row, v):
        """Write setting value *v* into array *key*, row *row*.

        """
        #no empty strings, please.
        if not v:
            return
        self._settings.beginWriteArray(key)
        self._settings.setArrayIndex(row)
        self._settings.setValue("key", v)
        self._settings.endArray()

    def _newListItem(self, w):
        """Add new item to w and start editing.
        """

        w.addItem("")
        i = w.count()
        item = w.item(i-1)
        item.setFlags( item.flags() | QtCore.Qt.ItemIsEditable )
        w.editItem(item)
