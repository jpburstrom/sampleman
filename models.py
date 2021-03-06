# -*- coding: utf-8 -*-

import os
import datetime

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT

from scikits.audiolab import Sndfile
from mutagen.wavpack import WavPackInfo
from mutagen.mp3 import MPEGInfo
from elixir import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import or_, and_

import utils
import filesys
#TODO Possibility to move repo


dbdir=os.path.join(os.path.expanduser("~"),".sampleman")
dbfile=os.path.join(dbdir,"sampleman.sqlite")

def get_by_or_init(cls, if_new_set={}, **params):
	"""Call get_by; if no object is returned, initialize an
	object with the same parameters.  If a new object was
	created, set any initial values."""
	
	result = cls.get_by(**params)
	if not result:
		result = cls(**params)
		result.set(**if_new_set)
	return result

Entity.get_by_or_init = classmethod(get_by_or_init)

class Soundfile(Entity):
    """Database model representing a single soundfile."""

    file_path = Field(Unicode(255),required=True, primary_key=True)
    repo = ManyToOne("Repo", primary_key=True)
    hash = Field(String(16))

    file_format = Field(Unicode(32))
    #libsndfile
    samplerate = Field(Integer)
    channels = Field(Integer)
    encoding = Field(Unicode(16))
    endianness = Field(Unicode(16))
    nframes = Field(Integer)
    #length in sec
    length = Field(Float)
    mtime = Field(DateTime)
    desc = Field(Unicode, default=u"")

    active = Field(Boolean, default=True)
    
    tags = ManyToMany("Tag")

    def get_audiodata_from_file(self):
        """Analyze audio data.

        A quite dirty method, mostly using audiolab Sndfile."""
        ext = os.path.splitext(self.path)[1].lower()
        if ext == ".wv":
            with open(self.path, "r") as f:
                wp = WavPackInfo(f)
            self.file_format = u"wavpack"
            self.samplerate = wp.sample_rate
            self.channels = wp.channels
            #FIXME: set endianness and encoding, right now i don't care
            self.endianness = u"" 
            self.encoding = u""
            self.nframes = wp.nframes
            self.length = wp.length
            return True
        elif ext == ".mp3":
            with open(self.path, "r") as f:
                wp = MPEGInfo(f)
            self.file_format = u"mp3"
            self.samplerate = wp.sample_rate
            self.channels = (wp.mode < 3) + 1
            #FIXME: set endianness, right now i don't care
            self.endianness = u"" 
            #mapping encoding to bitrate
            self.encoding = u"{0}kbps".format(wp.bitrate/1000.)
            #FIXME: nframes?
            self.nframes = 0
            self.length = wp.length
            return True
        else:
            try:
                f = Sndfile(self.path, "r")
                self.file_format = unicode(f.file_format)
                self.samplerate = f.samplerate
                self.channels = f.channels
                self.endianness = unicode(f.endianness)
                self.encoding = unicode(f.encoding)
                self.nframes = f.nframes
                self.length = self.nframes / float(self.samplerate)
                return True
            except IOError:
                print "Error reading {0} - Not an audio file".format(self.path)
                return False



    def get_hash_from_file(self):
        """Calculate and set md5 hash from path."""
        self.hash = utils.md5sum(self.path)

    def get_lmdate_from_file(self):
        """Set last modified time from path."""
        self.mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.path))

    def get_data_from_file(self):
        """Get all data from file.

        Return true if file is audio file, otherwise return false.
        """
        if self.get_audiodata_from_file():
            self.get_lmdate_from_file()
            self.get_hash_from_file()
            return True
        else:
            return False
    
    #Not used?    
    #def add_tags(self, *tags):
    #   """Add tags to soundfile model.

    #   Args: tags to add.
    #   """
    #   ot = [t.name for t in self.tags]
    #   nt = [t for t in tags if t not in ot]
    #   [self.tags.append(Tag.get_by_or_init(name=t)) for t in nt]

    def get_taglist(self):
        """Property getter: get tags as list."""
        return [t.name for t in self.tags]

    def set_taglist(self, tags):
        """Property setter: set tags as list-"""
        tl = self.taglist
        [self.tags.remove(Tag.get_by_or_init(name=t)) for t in tl if t not in tags]
        [self.tags.append(Tag.get_by_or_init(name=t)) for t in tags if t and t not in tl]

    taglist = property(get_taglist, set_taglist)

    def get_tagstring(self):
        """Property getter: get tags as comma-separated string"""
        return ", ".join(self.taglist)

    def set_tagstring(self, s):
        """Property setter: Set tags as comma-separated string"""
        self.taglist = [t.strip() for t in s.split(",")]

    tagstring = property(get_tagstring, set_tagstring)

    def get_path(self):
        """Path propery getter."""
        return os.path.join(self.repo.path, self.file_path)

    path = property(get_path)

    @classmethod
    def get_from_paths(cls, root, path):
        r = Repo.get_by(path=root)
        return cls.get_by(repo=r, file_path=path)

class Tag(Entity):
    """Database model representing a tag."""

    name = Field(Unicode,required=True, unique=True)
    files = ManyToMany("Soundfile", inverse="tags")
    
    def __repr__(self):
        return "Tag: "+self.name

class Repo(Entity):
    """Database model representing a repository.
    
    A repository is a directory that is searched recursively for soundfiles."""

    path = Field(Unicode(255), required=True)
    altpath1 = Field(Unicode(255))
    altpath2 = Field(Unicode(255))
    altpath3 = Field(Unicode(255))
    files = OneToMany("Soundfile", inverse="repo", cascade="all, delete-orphan")

class SoundfileStandardItem(QtGui.QStandardItem):
    """Representing a soundfile inside the SoundfileModel.

    Keeps track of repository path as well as the relative
    path of the soundfile."""

    def __init__(self, repo, ft, *args):
        QtGui.QStandardItem.__init__(self, *args)

        self.repoRole = QtCore.Qt.UserRole + 1
        self.ft = ft
        self.repoData = QtCore.QVariant(repo)

    def data(self, role=QtCore.Qt.DisplayRole):
        """Supply data for the model.
        """

        if role == self.repoRole:
            return self.repoData
        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(u":/ft/icons/{0}.png".format(self.ft))
        else:
            return QtGui.QStandardItem.data(self, role)

    def clone(self):
        return SoundfileStandardItem(self.repoData.toString(), self.ft, self.data().toString())

class SimpleFileModel(QtGui.QStandardItemModel):
    """Drag drop model."""
    def __init__(self, *args):
        QtGui.QStandardItemModel.__init__(self, *args)

    def flags(self, mi):
        """Set flags for drag and drop."""
        defaultFlags = QtGui.QStandardItemModel.flags(self, mi)
        if (mi.isValid()) and mi.column() is 0 :
            return QtCore.Qt.ItemIsDragEnabled | defaultFlags
        else:
            return defaultFlags & QtCore.Qt.ItemIsDragEnabled

    def supportedDropActions(self):
        """Return drag action.
        
        We need this not to accidentally move files."""
        
        return QtCore.Qt.CopyAction

    def mimeData(self, mi):
        """Mime data for DnD."""
        urls = None
        urls = [QtCore.QUrl(self.pathFromIndex(m)) for m in mi]
        mime = QtCore.QMimeData()
        mime.setUrls(urls)
        return mime

    def pathFromIndex(self, mi):
        """Get full file path from QModelIndex."""
        item = self.itemFromIndex(mi)
        repo = unicode(item.data(item.repoRole).toString())
        path = unicode(item.data().toString())
        return os.path.join(repo, path)
    
class SoundfileModel(SimpleFileModel):
    """Soundfile list model."""

    def __init__(self, *args):
        SimpleFileModel.__init__(self, *args)

        self.searchterms = None
        self.rebuild()

        self.connect(self, SIGNAL("itemChanged(QStandardItem)"), self.on_itemChanged)

    def on_itemChanged(self, item):
        pass
        #print item.text()

    def search(self, terms=None, force=False):
        """Search soundfiles.

        terms -- search terms, comma separated. See _search_sounds method.
        force -- force a search, even if terms are the same.
        """
        if terms == self.searchterms and not force:
            return
        self.clear()
        self.searchterms = terms
        if not terms:
            self._build(Soundfile.query.filter_by(active=True).all())
        else:
            self._build(self._search_sounds(*terms))

    def rebuild(self):
        """Force a rebuild of current search."""
        self.search(self.searchterms, True)

    def soundfileFromIndex(self, mi):
        """Get Soundfile model from QModelIndex."""
        item = self.itemFromIndex(mi)
        repo = unicode(item.data(item.repoRole).toString())
        path = unicode(item.data().toString())
        return Soundfile.get_from_paths(repo, path)

    def _build(self, all):
        """Build the list of soundfiles.

        all -- list of Soundfile instances."""
        [self.appendRow(SoundfileStandardItem(t.repo.path, t.file_format, unicode(t.file_path))) for t in all]
    
    def _search_sounds(self, *terms):
        """Search for soundfiles.
        
        Accepts variable number of arguments, each being a single search term ANDed
        to get a search result.

        Terms examples:
        (foo, fum): Search files for content in tags, filename and description
        (desc=Blah,): Search files with description containing "Blah"
        (f=wav,): Search files in wav format

        Terms can be specified with "label=", like this:
        tag/t = tag
        name/n = filename
        desc/d = Description
        channels/c = Channels
        file_format/f = File format
        encoding/e = Encoding
        samplerate/s = Samplerate
        """
        join = False
        #XXX active=True?
        q = Soundfile.query.filter_by(active=True)
        for t in terms:
            if not t:
                return q.all()
            t = t.split("=")
            if len(t) is 1:
                #FIXME: name & tag (& desc) i fritextsök, specificera med prefix.
                #TODO: For later: user settings for free search.
                #TODO: Here, the searches are ANDed. Would be good to have an OR as well.
                st = t[0].lower()
                q = q.outerjoin("tags", aliased=True).filter(or_(
                    Tag.name == st,
                    Soundfile.desc.like(u"%{0}%".format(st)),
                    Soundfile.file_path.like(u"%{0}%".format(st))
                    ))
            elif t[0].lower() in ("tag", "t") :
                q = q.join("tags", aliased=True).filter(Tag.name==t[1].lower())
            elif t[0].lower() in ("name", "n") :
                q = q.filter(Soundfile.file_path.like(u"%{0}%".format(t[1])))
                q = q.filter(Soundfile.desc.like(u"%{0}%".format(t[1])))
            elif t[0].lower() in ("channels", "c"):
                q = q.filter(Soundfile.channels==int(t[1]))
            elif t[0].lower() in  ("file_format", "f"):
                q = q.filter(Soundfile.file_format==t[1])
            elif t[0].lower() in ("encoding", "e"):
                q = q.filter(Soundfile.encoding==t[1].lower())
            elif t[0].lower() in ("samplerate", "r"):
                q = q.filter(Soundfile.samplerate==int(t[1]))
        return q.all()

class TagModel(QtGui.QStandardItemModel):
    """Tag list model."""

    def __init__(self, *args):
        QtGui.QStandardItemModel.__init__(self, *args)
        
        self.reload()

    def reload(self):
        """Reload list of tags."""
        self.clear()
        for t in Tag.query.all():
            self.appendRow(QtGui.QStandardItem(t.name.capitalize()))

class RepoModel(QtGui.QStandardItemModel):
    """Repository paths list model."""

    def __init__(self, *args):
        QtGui.QStandardItemModel.__init__(self, *args)
        
        self.reload()

    def reload(self):
        """Query repos and redraw gui.

        """
        for t in Repo.query.all():
            self.appendRow((QtGui.QStandardItem(t.path), 
                QtGui.QStandardItem(t.altpath1), 
                QtGui.QStandardItem(t.altpath2), 
                QtGui.QStandardItem(t.altpath3)))

    def add_repo(self, path):
        """Add repository to database.
        
        """
        #TODO: No need to check all paths. Also stupid to return existing repo in an add_repo method.
        #Pröva så här: Kolla main path, om den redan finns, returnera None. Annars returnera Repo. Eller?
        try:
            return Repo.query.filter(or_(
                Repo.path==path, 
                Repo.altpath1==path, 
                Repo.altpath2==path, 
                Repo.altpath3==path)).all()[0]
        except IndexError:
            self.appendRow((QtGui.QStandardItem(path), QtGui.QStandardItem(), QtGui.QStandardItem()))
            return Repo(path=path)
        #XXX session.commit()

    def delete_repo(self, path):
        """Delete repository including soundfiles from database.
        
        """
        session.delete(Repo.query.filter_by(path=path).one())
        session.commit()

    def edit_repo(self, oldpath, newpath, col=0):
        """Edit repository path.

        Find oldpath in col (where 0=path, 1=altpath1...) and set it to newpath.
        """
        print "Not implemented"
        #TODO

    def scan_repo(self, repo, rescan=False):
        """Scan repository for new files

        path: repo object
        rescan: If True, analyze all files, including those already in db.
        """
        path = repo.path
        files = []
        s = Soundfile.query.join("repo").filter(Repo.path == path)
        length = s.count()
        for sf in s.all():
            if not os.path.exists(sf.path):
                sf.active = False
                continue
            files.append(sf.path)
        print length
        progress = QtGui.QProgressDialog(u"Rebuilding {0}".format(path), u"Cancel", 0, length, QtGui.qApp.activeWindow()) 
        progress.setWindowModality(QtCore.Qt.WindowModal)
        import random
        i = 0
        if not rescan:
            for lis in filesys.scan(path):
                [Soundfile.get_by_or_init(
                    repo=repo, file_path=p).get_data_from_file() for p in lis if p not in files]
                i += len(lis)
                progress.setValue(i)
        else:
            for lis in filesys.scan(path):
                [Soundfile.get_by_or_init(
                    repo=repo, file_path=p).get_data_from_file() for p in lis]
                i += len(lis)
                progress.setValue(i)
        progress.setValue(length)
        progress.hide()
        session.commit()

            
def initDB():
    #print "initDB"
    # Make sure ~/.pyqtodo exists
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    # Set up the Elixir internal thingamajigs
    metadata.bind = "sqlite:///%s"%dbfile
    metadata.bind.echo = False
    setup_all()
    # And if the database doesn't exist: create it.
    if not os.path.exists(dbfile):
        create_all()

