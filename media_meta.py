#!/usr/bin/env python

import os
from hashids import Hashids
import json
from datetime import date
import argparse
from typing import List, Tuple

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

def createBucket(name: str):
    return name[0:3] + name.split('.')[0][-1] + "/"

def createMediaItem(base, index: int, width: int, height: int, title: str, description: str, keywords: str ):
    name = createName(base, index, width, height)
    return {
            "contentUrl": baseURL + createBucket(name) + name,
            "name": name,
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

def addMediaItem(baseName: str, dimensions: List[Tuple[int,int]], title: str, description: str, keywords: str ):
    old = loadMediaAsJson(baseName)
    base = old['base']
    index = old['count'] + 1
    items = map(lambda d: createMediaItem(base, index=index, width = d[0], height = d[1], title =title, description = description, keywords= keywords), dimensions)
    newJson = {
        "count": old['count'] + 1,
        "base": base,
        "items": old['items'] + items
    }
    saveMediaAsJson(base['baseName'], newJson)
    return index