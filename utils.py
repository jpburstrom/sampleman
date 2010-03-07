# -*- coding: utf-8 -*-

import os
import sys
import hashlib

from PyQt4.QtCore import QProcess


def md5sum(path):
    """Calculate md5 hash from file."""

    f = open(path)
    h = hashlib.md5()
    while True:
        n = f.read(100000)
        h.update(n)
        if not n:
            break
    f.close()
    return h.hexdigest()

def open_with(app, file):
    """Open file with app."""

    if sys.platform == "darwin":
        QProcess.startDetached("open", [file, "-a", app])
    else:
        QProcess.startDetached(app, [file])




def test():
    for i in xrange(100):
        md5sum("/Users/johannes/test2.wav")

if __name__ == "__main__":
    #import cProfile
    #cProfile.run("test()")
    open_with("/Applications/TwistedWave.app", "")

