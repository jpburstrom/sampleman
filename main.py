# -*- coding: utf-8 -*-

import os
import sys
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT

from models import *

from mainwindowui import Ui_MainWindow
from filewidgetui import Ui_Dialog
from pathdialogui import Ui_PathDialog

#TODO: .sampleman dir/file in each repository w/ sound metadata

class PathDialog(QtGui.QDialog):
    """Soundfile repository editor."""

    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)

        self.ui = Ui_PathDialog()
        self.ui.setupUi(self)
        
        self.repomodel = RepoModel(self)
        self.ui.treeView.setModel(self.repomodel)
        self.ui.treeView.resizeColumnToContents(0)


        #Setup data
        self.connect(self.ui.buttonAdd, SIGNAL("clicked()"), self.addRepo)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), self.deleteRepo)
        self.connect(self.ui.buttonRescan, SIGNAL("clicked()"), self.rescanRepo)
        self.connect(self.ui.buttonEdit, SIGNAL("clicked()"), self.editRepo)

        #TODO: deactivate delete/rescan when item is not selected

    def addRepo(self):
        """Add new repository.

        """
        path = QtGui.QFileDialog.getExistingDirectory(self, "Add a repository", os.path.expanduser("~"))
        repo = self.repomodel.add_repo(unicode(path))
        if QtGui.QMessageBox.question(
                self, "Question", "Would you like to scan the new repository?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes ) == QtGui.QMessageBox.Yes:
            self.repomodel.scan_repo(repo)
        session.commit()
        self.parent().rebuild()


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
                break
        repo = Repo.get_by(path=unicode(path))
        self.repomodel.scan_repo(repo)

    def editRepo(self):
        """Edit repository paths.
        
        """
        mi = self.ui.treeView.selectedIndexes()[0]
        #FIXME
        #Get repo 
        #find item to edit
        #... (model stuff really)


class MyDialog(QtGui.QDialog):
    """Soundfile attributes edit dialog."""

    def __init__(self, repo, path, *args):
        """Constructor.

        """

        QtGui.QDialog.__init__(self, *args)

        sf = Soundfile.get_from_paths(unicode(repo), unicode(path))
        self.sf = sf

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(path)

        #Setup data
        self.ui.label_5.setText(path)

        metadata = """File format\t\t{0}
Samplerate\t\t{1}
Channels\t\t{2}
Encoding\t\t{3}
Endianness\t\t{4}
Length\t\t{5} s ({6} samples) """.format(
        sf.file_format, sf.samplerate, sf.channels, sf.encoding, sf.endianness, sf.length, sf.nframes)

        tags = ", ".join([t.name for t in sf.tags])

        self.ui.textEditMeta.appendPlainText(metadata)
        self.ui.textEditDescription.appendPlainText(sf.desc or "")
        self.ui.lineEditTags.setText(tags)

        self.connect(self, SIGNAL("accepted()"), self.on_accept)

    def on_accept(self):
        """Commit edits.
        
        """

        self.sf.tagstring = unicode(self.ui.lineEditTags.text()).lower()
        self.sf.desc = unicode(self.ui.textEditDescription.toPlainText())
        session.commit()


class MyWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tagmodel = TagModel(self)
        self.ui.tagView.setModel(self.tagmodel)
        self.filemodel = SoundfileModel(self)
        self.ui.fileView.setModel(self.filemodel)

        self.connect(self.ui.fileView, SIGNAL("doubleClicked(const QModelIndex &)"), self.on_fileView_doubleClick)
        self.connect(self.ui.lineEdit, SIGNAL("returnPressed()"), self.start_search)
        self.connect(self.ui.lineEdit, SIGNAL("textChanged(const QString &)"), self.on_lineEdit_textChanged)
        self.connect(self.ui.tagView, SIGNAL("clicked(const QModelIndex &)"), self.on_tagView_click)
        self.connect(self.ui.actionManage_folders, SIGNAL("triggered()"), self.manage_folders)
        #self.ui.tagView.setRootIndex(0)

    def on_tagView_click(self, mi):
        """Append selected tags to search."""

        f = QtCore.QString()
        [f.append(unicode(mi.data().toString())).append(", ") for mi in self.ui.tagView.selectedIndexes()]
        self.ui.lineEdit.setText(f)

    def on_fileView_doubleClick(self, mi):
        """Open file dialog."""

        d = MyDialog(
                self.filemodel.index(mi.row(), 1).data().toString(),
                self.filemodel.index(mi.row(), 0).data().toString()
                )
        result = d.exec_()
        if result:
            self.filemodel.rebuild()

    def on_lineEdit_textChanged(self, s):
        """Check if current string calls for a new search.
        
        """

        if s.trimmed().endsWith(","):
            self.start_search()

    def manage_folders(self):
        """Open repository dialog.
        
        """

        d = PathDialog(self)
        d.show()

    def start_search(self):
        """Make list from searchbox, and start search.

        """

        searches = [t.strip() for t in unicode(self.ui.lineEdit.text()).split(",") if t.strip()]
        self.filemodel.search(searches)
        self.ui.fileView.resizeColumnToContents(0)

    def rebuild(self):
        """Expensive redo-search-and-redraw-all method."""

        self.filemodel.rebuild()
        self.tagmodel.reload()


initDB()
app = QtGui.QApplication(sys.argv)
w = MyWindow()
w.show()
#w.manage_folders()
sys.exit(app.exec_())
