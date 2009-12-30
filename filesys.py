# -*- coding: utf-8 -*-

import os
import mimetypes 

mimetypes.init()
#Add some sound files. Add your own, if you wanna.
mimetypes.add_type("audio/wavpack", ".wv")
mimetypes.add_type("audio/ogg", ".ogg")
mimetypes.add_type("audio/ogg", ".oga")
mimetypes.add_type("audio/ogg", ".spx")
mimetypes.add_type("audio/flac", ".flac")
mimetypes.add_type("audio/other", ".xi")


def scan(root):
    """Recursively scan a root repository for sound files.

    root: root directory to scan.
    
    Generator function, yielding lists of files with relative paths from root.
    """
    root = os.path.abspath(root)
    for path, dirs, files in os.walk(root):
        np = os.path.relpath(path, root)
        yield [os.path.join(np, f) for f in files if "audio" == mimetypes.guess_type(f)[0][:5]]
        
    
for i in scan("/Users/johannes/samples/misc"):
    print i
