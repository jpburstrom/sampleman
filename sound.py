# -*- coding: utf-8 -*-
#ANVÄNDS INTE

import os

from scikits.audiolab import Sndfile

import models

class MySndfile(Sndfile):
    def __init__(self, path, mode):
        ext = os.path.splitext(path)[1].lower()

        self.channels = 0
        self.encoding = None
        self.endianness = None

        
        #self.readonly = True



if __name__ == "__main__":
    f = MySndfile("/Users/johannes/test2.wav", "r")
    print dir(f)
    f.close()
    print "Testing..."
