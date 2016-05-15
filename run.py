# coding: utf-8

import subprocess
import sys

print sys.argv

#We must redefine it in Py3k if it's not already there
def execfile(file, glob=None, loc=None):
    if glob is None:
        import sys
        glob = sys._getframe().f_back.f_globals
    if loc is None:
        loc = glob

    stream = open(file)
    try:
        contents = stream.read()
    finally:
        stream.close()

    #execute the script (note: it's important to compile first to have the filename set in debug mode)
    exec(compile(contents+"\n", file, 'exec'), glob, loc)


execfile('/home/zh/jettingnoob/alchemist/manage.py')
