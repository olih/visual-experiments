#!/usr/bin/env python

import os
from hashids import Hashids
import json
from datetime import date
today = date.today()

hashids = Hashids(salt="Every artist was first an amateur", min_length=8)
baseURL = "https://m.olivierhuin.com/i/"
authorURL = "https://m.olivierhuin.com/profile"

def createId():
    with open('counter.txt', 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open('counter.txt', 'w') as wfile:
            wfile.write(str(counter))
            return hashids.encode(counter)

slug = input('What is slug of the series ?')
title = input('What is the title of the work ?')
description = input('What is the description ?')
keywords = input('Some keywords for the image ?')

baseName = slug.lower() + "-" + createId()
os.mkdir("creations/" + baseName)

mediaJson = {
    "count": 1,
    "baseName": baseName,
    "keywords": keywords,
    "items": [
        {
            "contentUrl": "{}{}.1.64x64.png".format(baseURL, baseName),
            "name": "{}.1.64x64.png".format(baseName),
            "@type": "ImageObject",
            "headline": title,
            "description": description,
            "keywords": keywords,
            "encodingFormat": "image/png",
            "width": "64 px",
            "height": "64 px",
            "colors": "#000000 #ffffff",
            "author": authorURL,
            "datePublished": today.strftime("%Y-%m-%d"),
            "copyrightYear": today.strftime("%Y"),
            "creativeWorkStatus": "Draft",
            "license": "https://creativecommons.org/licenses/by-sa/4.0",
        }
    ]
}

def saveMediaAsJson(rows):
    with open('creations/{}/media.json'.format(baseName), 'w') as outfile:
        json.dump(rows, outfile, indent=2)

saveMediaAsJson(mediaJson)