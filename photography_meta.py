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
import subprocess

localDir = os.environ['OLI_LOCAL_DIR']

def loadConfAsJson():
    with open('{}/photography/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

photographyDir = jsonConf["folders"]["local-parent-directory"]
photographyImgDir = "{}/img".format(photographyDir)
photographyDataDir = "{}/data".format(photographyDir)

foldersHashids = Hashids(salt=jsonConf["folders"]["salt"], min_length=15)
mediasHashids = Hashids(salt=jsonConf["medias"]["salt"], min_length=20)

def findDirectories():
    return glob(os.path.join(photographyImgDir, '*'))

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
    return [y for x in os.walk(photographyImgDir) for y in glob(os.path.join(x[0], '*.{}'.format(ext)))]

def findAllMediaFiles():
    all = findMediaFiles('jpg') + findMediaFiles('jpeg') + findMediaFiles('png')
    return all

def findMediaIds(folderName):
    return [getFilename(filename).replace("original-", "") for filename in glob(os.path.join("{}/{}".format(photographyImgDir, folderName), 'original-*'))]

def getFileExt(filename):
    return os.path.splitext(filename)[1]

def getFilename(filename):
    return os.path.basename(filename)

def getParentDirectory(filename):
    return Path(filename).parent

def isSmallMedia(filename):
    return True if "/small-" in filename else False

def isOriginalMedia(filename):
    return True if "/original-" in filename else False

def shouldAddMediaId(filename):
    return False if isOriginalMedia(filename) else True

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

def asTagInfo(line):
    if not "\t" in line:
        folder = getFilename(line)
        dirId = getDirId(folder)
        return { "id": dirId, "folder": folder, "tags": [], "items": []}
    filename, tagCSV =  line.split("\t")
    tags = tagCSV.split(",")
    folder = getFilename(filename)
    dirId = getDirId(folder)
    mediaIds = findMediaIds(folder)
    return {"id": dirId,  "folder": folder, "tags": tags, "items": mediaIds }

def saveFoldersMetaAsJson(jsonContent):
    with open('{}/folders.json'.format(photographyDataDir), 'w') as outfile:
            json.dump(jsonContent, outfile, indent=2)

def saveMediaTagsAsJson(jsonContent):
    with open('{}/media-tags.json'.format(photographyDataDir), 'w') as outfile:
            json.dump(jsonContent, outfile, indent=2)

def saveMediaGroupAsJson(groupId, jsonContent):
    with open('{}/group-{}.json'.format(photographyDataDir, groupId), 'w') as outfile:
            json.dump(jsonContent, outfile, indent=2)

def extractTags():
    stream = os.popen("tag -l {}/*".format(photographyImgDir))
    lines = stream.readlines()
    tagInfoLines = [asTagInfo(line.strip()) for line in lines ]
    saveFoldersMetaAsJson(tagInfoLines)
# ensureIdForFolders()
# ensureIdForMediaFiles()

def loadFoldersJson():
    with open('{}/folders.json'.format(photographyDataDir), 'r') as jsonfile:
        return json.load(jsonfile)

def loadMediaTagsAsJson():
    with open('{}/media-tags.json'.format(photographyDataDir), 'r') as jsonfile:
        return json.load(jsonfile)

def fileTagsForFolder(folderInfo):
    tags = folderInfo["tags"]
    folder = folderInfo["folder"]
    return [ { "item": item, "folder": folder, "tags": tags} for item in folderInfo["items"]]
    

def tagsByFile():
    foldersJson = loadFoldersJson()
    mediaTags = [fileTagsForFolder(folder) for folder in foldersJson]
    flatMediaTags= [item for sublist in mediaTags for item in sublist]
    saveMediaTagsAsJson(flatMediaTags)

def organizeGroup(group, mediaTags):
    return [mediaItem for mediaItem in mediaTags if group["name"] in mediaItem["tags"]]

def organizeByGroup():
    mediaTags = loadMediaTagsAsJson()
    groups = jsonConf["groups"]
    for group in groups:
        groupMediaTags = organizeGroup(group, mediaTags)
        saveMediaGroupAsJson(group["id"], groupMediaTags)

extractTags()
tagsByFile()
organizeByGroup()