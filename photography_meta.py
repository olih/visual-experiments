#!/usr/bin/env python

import os
from hashids import Hashids
import json
import argparse
from typing import List, Tuple
from glob import glob
import re
import os.path
from pathlib import Path

localDir = os.environ['OLI_LOCAL_DIR']

def loadConfAsJson():
    with open('{}/photography/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

photographyDir = jsonConf["folders"]["local-parent-directory"]

foldersHashids = Hashids(salt=jsonConf["folders"]["salt"], min_length=15)
mediasHashids = Hashids(salt=jsonConf["medias"]["salt"], min_length=20)

def findDirectories():
    return glob(os.path.join(photographyDir, '*'))

def getDirId(filename):
    if not "--" in filename:
        return None
    else:
        return filename.split("--")[1]

def createFolderId():
    counterFilename = '{}/photography/folders-count.txt'.format(localDir)
    with open(counterFilename, 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open(counterFilename, 'w') as wfile:
            wfile.write(str(counter))
            return foldersHashids.encode(counter)

def createMediaId():
    counterFilename = '{}/photography/medias-count.txt'.format(localDir)
    with open(counterFilename, 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open(counterFilename, 'w') as wfile:
            wfile.write(str(counter))
            return mediasHashids.encode(counter)

def ensureIdForFolders():
    print("Ensuring ids for folders")
    for directory in findDirectories():
        if getDirId(directory) is not None:
            continue
        try:
            dest = "{}--{}".format(directory, createFolderId())
            print("Renaming as %s" % dest)
            os.rename(directory, dest)
        except OSError:
            print ("Renaming  %s failed" % directory)

def findMediaFiles(ext):
    return [y for x in os.walk(photographyDir) for y in glob(os.path.join(x[0], '*.{}'.format(ext)))]

def findAllMediaFiles():
    all = findMediaFiles('jpg') + findMediaFiles('jepg') + findMediaFiles('png')
    return all

def getFileExt(filename):
    return os.path.splitext(filename)[1]

def getParentDirectory(filename):
    return Path(filename).parent

def isSmallMedia(filename):
    return True if "/small-" in filename else False

def isOriginalMedia(filename):
    return True if "/original-" in filename else False

def shouldAddMediaId(filename):
    return False if isSmallMedia(filename) or isOriginalMedia(filename) else True

def ensureIdForMediaFiles():
    print("Ensuring ids for media files")
    for filename in findAllMediaFiles():
        if shouldAddMediaId(filename) is False:
            continue
        try:
            dest = "{}/original-{}{}".format(getParentDirectory(filename), createMediaId(), getFileExt(filename))
            print("Renaming as %s" % dest)
            os.rename(filename, dest)
        except OSError:
            print ("Renaming  %s failed" % filename)


ensureIdForFolders()
ensureIdForMediaFiles()

