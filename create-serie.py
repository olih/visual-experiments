#!/usr/bin/env python

from hashids import Hashids

hashids = Hashids(salt="Every artist was first an amateur", min_length=8)

def createId():
    with open('counter.txt', 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open('counter.txt', 'w') as wfile:
            wfile.write(str(counter))
            return hashids.encode(counter)

print(createId())