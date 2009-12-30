# -*- coding: utf-8 -*-

import os
import sys
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT

from models import *

initDB()

b = Repo.get_by_or_init(path=u"/Users/johannes")
f = Soundfile.get_by_or_init(repo=b, file_path=u"test2.wav")
m = RepoModel()
repo = m.add_repo(u"/Users/johannes/samples/misc")
print f.path
f.desc=u"Fappafdpokasdok"
f.get_data_from_file()
#for tags in [u"foo", u"treo"]:
#    t = Tag.get_by_or_init(name=tags)
#    f.tags.append(t)

sm = SoundfileModel()
#session.delete(repo)
m.scan_repo(repo)
print [s.path for s in Soundfile.query.all()]
#print "foo", f.search(u"desc=Faspp", u"foo", u"channels=2")
#print "foo", f.search( u"foo")

f.taglist = [u"rar"]

print f.tags

session.commit()

for t in Tag.query.all():
    print t.name

