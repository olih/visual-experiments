#!/usr/bin/env python

import os
from hashids import Hashids
import json
from datetime import date
import argparse

today = date.today()

hashids = Hashids(salt="Every artist was first an amateur", min_length=9)
baseURL = "https://m.olivierhuin.com/i/"
authorURL = "https://m.olivierhuin.com/profile"
licenseURL = "https://creativecommons.org/licenses/by-sa/4.0"

def createId():
    with open('counter.txt', 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open('counter.txt', 'w') as wfile:
            wfile.write(str(counter))
            return hashids.encode(counter)

def splitAndTrim(separator: str, value: str):
    results = map(lambda s: s.strip(), value.split(separator))
    return list(results) if results else []

def mergeKeywords(keywords1: str, keywords2: str):
    k1 = set(splitAndTrim(",", keywords1))
    k2 = set(splitAndTrim(",", keywords2))
    return ",".join(list(k1|k2))

def createBase(slug: str, keywords: str):
    return {
        "baseName": slug.lower() + "-" + createId(),
        "keywords": mergeKeywords(keywords, ""),
        "baseURL": baseURL,
        "author": authorURL,
        "license": licenseURL,
        "creativeWorkStatus": "Draft",
        "colors": "#000000 #ffffff",
        "@type": "ImageObject",
        "encodingFormat": "image/png"
    }

def createName(base, index: int, width: int, height: int):
    return "{}-{}.{}x{}.png".format(base['baseName'], index, width, height)

def createMediaItem(base, index: int, width: int, height: int, title: str, description: str, keywords: str ):
    return {
            "contentUrl": baseURL + createName(base, index, width, height),
            "name": createName(base, index, width, height),
            "@type": base["@type"],
            "headline": title,
            "description": description,
            "abstract": "",
            "keywords": mergeKeywords(base['keywords'], keywords),
            "encodingFormat": base['encodingFormat'],
            "width": "{} px".format(width),
            "height": "{} px".format(height),
            "colors": base['colors'],
            "author": base['author'],
            "datePublished": today.strftime("%Y-%m-%d"),
            "copyrightYear": today.strftime("%Y"),
            "creativeWorkStatus": base['creativeWorkStatus'],
            "license": base['license']
        }

def isNameUnique(jsonContent):
    names = [item['name'] for item in jsonContent['items']]
    return len(names) == len(set(names))

def saveMediaAsJson(baseName: str, jsonContent):
    if isNameUnique(jsonContent):
        with open('creations/{}/media.json'.format(baseName), 'w') as outfile:
            json.dump(jsonContent, outfile, indent=2)
    else:
            print("This unique name is already taken")

def loadMediaAsJson(baseName: str):
    with open('creations/{}/media.json'.format(baseName), 'r') as jsonfile:
        return json.load(jsonfile)
    

parser = argparse.ArgumentParser(description = 'Create or update a new visual experiment')
parser.add_argument("-S", "--slug", help="A slug for the folder name")
parser.add_argument("-B", "--baseName", help="The base name for the experiment")
parser.add_argument("-I", "--index", help="The index for the experiment", type=int)
parser.add_argument("-K", "--keywords", help="A list of keywords separated by coma", default="")
parser.add_argument("-T", "--title", help="A title for the image", default="")
parser.add_argument("-D", "--description", help="A description for the image", default="")
parser.add_argument("-W", "--width", help="The width of the image", type=int, default = 128)
parser.add_argument("-H", "--height", help="The height of the image", type=int, default = 128)
args= parser.parse_args()

if args.slug:
    base = createBase(slug=args.slug, keywords = args.keywords)
    item = createMediaItem(base, index=1, width = args.width, height = args.height, title = args.title, description = args.description, keywords= args.keywords )
    initJson = {
        "count": 1,
        "base": base,
        "items": [item]
    }
    os.mkdir("creations/" + base['baseName'])
    print("Creating "+ base['baseName'])
    saveMediaAsJson(base['baseName'], initJson)

elif args.baseName:
    old = loadMediaAsJson(args.baseName)
    base = old['base']
    index = args.index if args.index else old['count'] + 1
    print("Creating {} with index {}".format(base['baseName'], index))
    item = createMediaItem(base, index=index, width = args.width, height = args.height, title = args.title, description = args.description, keywords= args.keywords)
    newJson = {
        "count": old['count'] if args.index else old['count'] + 1,
        "base": base,
        "items": old['items'] + [item]
    }
    saveMediaAsJson(base['baseName'], newJson)
else:
    print("You need to specify either slug or baseName")


