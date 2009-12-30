# -*- coding: utf-8 -*-

import os
import hashlib


def md5sum(path):
    f = open(path)
    h = hashlib.md5()
    while True:
        n = f.read(100000)
        h.update(n)
        if not n:
            break
    f.close()
    return h.hexdigest()

def test():
    for i in xrange(100):
        md5sum("/Users/johannes/test2.wav")

if __name__ == "__main__":
    import cProfile
    cProfile.run("test()")
