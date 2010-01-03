# -*- coding: utf-8 -*-

import os
import sys
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT
from sqlalchemy.orm import join

from models import *
from settings import SettingsDialog

from mainwindowui import Ui_MainWindow
from filewidgetui import Ui_Dialog

"""
TODO
====

* Settings: fixa menyer. Labels? ny setting => signal => uppdatera menyerna
    Vid programstart: befolka menyerna med QSettings
    Vid editering: använd signaler från SettingsDialog
* Högerklickmeny: öppna med... (användardefinierade program)
* Redigera metadata på flera filer samtidigt (slå ihop tags? kopiera beskrivning? hur?)
* exportera filer till viss samplerate & format, definierad av användare. dnd? (eg dnd wavpack-fil till ardour)
* Spara sökningar under namn. Kanske ersätta tagrutan, eller som komplement.

* Add player to Tag editor
* + Keyboard shortcuts

---
* Annotations (importera externa annoteringsformat)
* Internal player: start, stop, volym
* Snapper-funktionalitet (dnd för snippet)
* spara metadata i .sampleman-folder/fil i varje repository (lex git)
"""


class MyDialog(QtGui.QDialog):
    """Soundfile attributes edit dialog."""

    def __init__(self, *items):
        """Constructor.

        """
        
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


        sfs = []
        paths = []
        for item in items:
            repo = item.data(item.repoRole).toString()
            path = item.data().toString()
            paths.append(unicode(path))
            sfs.append(Soundfile.get_from_paths(unicode(repo), unicode(path)))

        self.single = len(sfs) == 1

        path = "\n".join(paths)
        self.setWindowTitle(path)


        #Setup data
        self.ui.label_5.setText(path)

        if self.single:
            sf = sfs[0]
            self.sf = sf
            metadata = """File format\t\t{0}
Samplerate\t\t{1}
Channels\t\t{2}
Encoding\t\t{3}
Endianness\t\t{4}
Length\t\t{5} s ({6} samples) """.format(
        sf.file_format, sf.samplerate, sf.channels, sf.encoding, sf.endianness, sf.length, sf.nframes)
            self.ui.textEditMeta.appendPlainText(metadata)
            self.ui.textEditDescription.appendPlainText(sf.desc or "")
            tags = ", ".join([t.name for t in sf.tags])
            self.ui.lineEditTags.setText(tags)
        else:
            self.ui.textEditMeta.hide()
            self.mergedDesc = list(set([s.desc for s in sfs if s.desc]))
            #ok, det här kan göras i sql också, men orka, typ
            taglist = []
            [taglist.extend(s.tags) for s in sfs]
            self.mergedTags = list(set([t.name for t in taglist]))
        
            self.ui.desc_mergeButton.setEnabled((not not self.mergedDesc))
            self.ui.tags_mergeButton.setEnabled((not not self.mergedTags))

            self.ui.tagsBox.setChecked(False)
            self.ui.descBox.setChecked(False)
        
        self.sfs = sfs

        self.connect(self, SIGNAL("accepted()"), self.on_accepted)

    def on_accepted(self):
        """Commit edits.
        
        """

        if self.ui.tagsBox.isChecked():
            for s in self.sfs:
                s.tagstring = unicode(self.ui.lineEditTags.text()).lower()
        if self.ui.descBox.isChecked():
            for s in self.sfs:
                s.desc = unicode(self.ui.textEditDescription.toPlainText())
        session.commit()
    
    def on_tags_mergeButton_clicked(self):
        self.ui.lineEditTags.setText(", ".join(self.mergedTags))

    def on_desc_mergeButton_clicked(self):
        [self.ui.textEditDescription.appendPlainText(d) for d in self.mergedDesc]


class MyWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settingsDialog = None

        self.tagmodel = TagModel(self)
        self.ui.tagView.setModel(self.tagmodel)
        self.filemodel = SoundfileModel(self)
        self.ui.fileView.setModel(self.filemodel)
        self.ui.fileView.setLayoutMode(self.ui.fileView.Batched)
        self.ui.fileView.setBatchSize(40)

        self._init_menus()

        self.connect(self.ui.lineEdit, SIGNAL("returnPressed()"), self.start_search)
        self.connect(self.ui.lineEdit, SIGNAL("textChanged(const QString &)"), self.on_lineEdit_textChanged)
        self.connect(self.ui.tagView, SIGNAL("clicked(const QModelIndex &)"), self.on_tagView_click)
        self.connect(self.ui.actionManage_folders, SIGNAL("triggered()"), self.manage_folders)

        self.ui.fileView.doubleClicked.connect(self.on_fileView_startEdit)

    def test(self, app):
        #temp
        print app 

    def on_tagView_click(self, mi):
        """Append selected tags to search."""

        f = QtCore.QString()
        [f.append(unicode(mi.data().toString())).append(", ") for mi in self.ui.tagView.selectedIndexes()]
        self.ui.lineEdit.setText(f)

    def on_fileView_startEdit(self, mi, all=False):
        """Open file dialog."""
        items = [self.filemodel.itemFromIndex(m) for m in self.ui.fileView.selectedIndexes()]
        d = MyDialog(*items)
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
        if not self.settingsDialog:
            self._setupSettings()
        self.settingsDialog.setTab("repositories")
        self.settingsDialog.show()

    def start_search(self):
        """Make list from searchbox, and start search.

        """

        searches = [t.strip() for t in unicode(self.ui.lineEdit.text()).split(",") if t.strip()]
        self.filemodel.search(searches)
        #self.ui.fileView.resizeColumnToContents(0)

    def rebuild(self):
        """Expensive redo-search-and-redraw-all method."""

        self.filemodel.rebuild()
        self.tagmodel.reload()

    def _init_menus(self):
        #TODO: remove dummy menu items
        self.ui.menuOpen_with.clear()
        self.ui.menuOpen_copy_with.clear()
        self.ui.menuExport_as.clear()

        self.ui.actionAll_folders.triggered.connect(self.on_repo_rescan)
        for repo in Repo.query.all():
            ac = self.ui.menuRescan_folders.addAction(repo.path) 
            ac.triggered.connect(self.on_repo_rescan)
       
        settings = QtCore.QSettings("ljud.org", "Sampleman")
        size = settings.beginReadArray("apps")
        for i in range(size):
            settings.setArrayIndex(i)
            s = settings.value("key").toString()
            if not s:
                continue
            ac = self.ui.menuOpen_with.addAction(s)
            ac.triggered.connect(self.on_open_with)
            ac = self.ui.menuOpen_copy_with.addAction(s)
            ac.triggered.connect(self.on_open_copy_with)
        settings.endArray()
        size = settings.beginReadArray("folders")
        for i in range(size):
            if not s:
                continue
        settings.endArray()
        size = settings.beginReadArray("formats")
        for i in range(size):
            if not s:
                continue
            settings.setArrayIndex(i)
            s = settings.value("key").toString()
            ac = self.ui.menuExport_as.addAction(s)
            ac.triggered.connect(self.on_export_as)
        settings.endArray()
    
    def on_newRepo(self, s):
        self.ui.menuRescan_folders.addAction(
                s).triggered.connect(self.on_repo_rescan)

    def on_newFolder(self, s):
        pass
        #TODO

    def on_newFormat(self, s):
        self.ui.menuExport_as.addAction(
                s).triggered.connect(self.on_export_as)

    def on_newApp(self, s):
        self.ui.menuOpen_with.addAction(
                s).triggered.connect(self.on_open_with)
        self.ui.menuOpen_copy_with.addAction(
                s).triggered.connect(self.on_open_copy_with)
        
    
    def on_export_as(self):
        #TODO
        print "export"

    def on_open_with(self):
        #TODO
        print "openwith"

    def on_open_copy_with(self):
        #TODO
        print "opencopy"

    def on_repo_rescan(self):
        path = self.sender().text()
        if path == "All folders":
            repos = Repo.query.all()
        else:
            repos = (Repo.get_by(path=unicode(path)),)
        repomodel = RepoModel()
        for repo in repos:
            repomodel.scan_repo(repo)

    def _setupSettings(self):
        self.settingsDialog = SettingsDialog(self)
        self.settingsDialog.newRepo.connect(self.on_newRepo)
        self.settingsDialog.newFolder.connect(self.on_newFolder)
        self.settingsDialog.newFormat.connect(self.on_newFormat)
        self.settingsDialog.newApp.connect(self.on_newApp)


initDB()
app = QtGui.QApplication(sys.argv)
w = MyWindow()
w.show()
#w.manage_folders()
sys.exit(app.exec_())
