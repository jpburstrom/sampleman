# -*- coding: utf-8 -*-

import os
import sys
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT

from models import *
from settings import SettingsDialog

from mainwindowui import Ui_MainWindow
from filewidgetui import Ui_Dialog

"""
TODO
====

* Högerklickmeny: öppna med... (användardefinierade program)
* exportera filer till viss samplerate & format, definierad av användare. dnd? (eg dnd wavpack-fil till ardour)
* Exportera till...-folder, som sparas mellan sessions.
* Redigera metadata på flera filer samtidigt (slå ihop tags? kopiera beskrivning? hur?)
* Spara sökningar under namn. Kanske ersätta tagrutan, eller som komplement.
* Menyer

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

        d = SettingsDialog(self)
        d.setTab("repositories")
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
