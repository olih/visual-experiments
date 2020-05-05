import os
import sys
import argparse
from fractions import Fraction
from typing import List, Tuple

from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

def stripStringArray(rawlines: str, sep=",")->List[str]:
    return [line.strip() for line in rawlines.split(sep) if line.strip() != ""]

def parseDlmtArray(line: str)-> List[str]:
    return stripStringArray(line.replace("[", "").replace("]", ""), sep=",")

def toDlmtArray(items: List[str], sep=",")->str:
    return "[ {} ]".format(sep.join(items))

# view i:1 lang en-gb xy -1/2 -1/2 width 1/1 height 1/1 -> everything
class DlmtView:
    def __init__(self, id: str, xy: V2d, width: Fraction, height: Fraction, lang: str = "en", description: str = "" ):
        self.id = id
        self.xy = xy
        self.width = width
        self.height = height
        self.lang = lang
        self.description = description
    
    @classmethod
    def from_string(cls, line: str):
        other, description  = line.split("->")
        cmd, viewId, langKey, langId, xyKey, x, y, widthKey, width, heightKey, height = other.split()
        assert cmd == "view", line
        assert langKey == "lang", line
        assert xyKey == "xy", line
        assert widthKey == "width", line
        assert heightKey == "height", line
        
        return cls(id = viewId, xy = V2d.from_string(x + " " + y), width = Fraction(width), height = Fraction(height), lang = langId, description= description.strip())

    def __str__(self):
        return "view {} lang {} xy {} width {} height {} -> {}".format(self.id, self.lang, self.xy, self.width, self.height, self.description)
    
    def __repr__(self):
        return "view {} lang {} xy {} width {} height {} -> {}".format(self.id, self.lang, self.xy, self.width, self.height, self.description)

# tag i:1 lang en-gb same-as [ geospecies:bioclasses/P632y ] -> part of head
class DlmtTagDescription:
    def __init__(self, id: str, same_as: List[str] = [], lang: str = "en", description: str = "" ):
        self.id = id
        self.same_as = same_as
        self.lang = lang
        self.description = description
    
    @classmethod
    def from_string(cls, line: str):
        other, description  = line.split("->")
        cmd, descId, langKey, langId, sameAsKey, sameAsInfo = other.split(" ", 5)
        assert cmd == "tag", line
        assert langKey == "lang", line
        assert sameAsKey == "same-as", line
        
        return cls(id = descId, same_as= parseDlmtArray(sameAsInfo), lang = langId, description= description.strip())

    def __str__(self):
        return "tag {} lang {} same-as {} -> {}".format(self.id, self.lang, toDlmtArray(self.same_as, sep=", "), self.description)
    
    def __repr__(self):
        return "tag {} lang {} same-as {} -> {}".format(self.id, self.lang, toDlmtArray(self.same_as, sep=", "), self.description)
