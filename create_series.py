#!/usr/bin/env python

import os
import argparse
from media_meta import createBase, createMediaItem, loadMediaAsJson, saveMediaAsJson

parser = argparse.ArgumentParser(description = 'Create a new visual experiment')
parser.add_argument("-S", "--slug", help="A slug for the folder name", required = True)
parser.add_argument("-K", "--keywords", help="A list of keywords separated by coma", default="")
args= parser.parse_args()

base = createBase(slug=args.slug, keywords = args.keywords)
initJson = {
    "count": 0,
    "base": base,
    "items": []
}
os.mkdir("creations/" + base['baseName'])
print("Creating "+ base['baseName'])
saveMediaAsJson(base['baseName'], initJson)


