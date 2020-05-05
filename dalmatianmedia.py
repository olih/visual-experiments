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

# brush i:1 ext-id brushes:abc3F path [ M -1/3 1/3, l 2/3 0/1, l 0/1 2/3, l -2/3 0/1 ]
class DlmtBrush:
    def __init__(self, id: str, ext_id:str, vpath: VPath):
        self.id = id
        self.ext_id = ext_id
        self.vpath = vpath
    
    @classmethod
    def from_string(cls, line: str):
        cmd, brushId, extIdKey, extId, pathKey, other = line.split(" ", 5 )
        assert cmd == "brush", line
        assert extIdKey == "ext-id", line
        assert pathKey == "path", line
        
        return cls(id = brushId, ext_id = extId, vpath = VPath.from_dalmatian_string(other))

    def __str__(self):
        return "brush {} ext-id {} path {}".format(self.id, self.ext_id, self.vpath.to_dalmatian_string())
    
    def __repr__(self):
        return "brush {} ext-id {} path {}".format(self.id, self.ext_id, self.vpath.to_dalmatian_string())

# brushstroke i:1 xy 1/15 1/100 scale 1/10 angle 0/1 tags [ i:1 ]
class DlmtBrushstroke:
    def __init__(self, id: str, xy: V2d, scale: Fraction, angle: Fraction, tags: List[str] = []):
        self.id = id
        self.xy = xy
        self.scale = scale
        self.angle = angle
        self.tags = tags
    
    @classmethod
    def from_string(cls, line: str):
        cmd, brushId, xyKey, x, y, scaleKey, scale, angleKey, angle, tagsKey, tagsInfo = line.split(" ", 10 )
        assert cmd == "brushstroke", line
        assert xyKey == "xy", line
        assert scaleKey == "scale", line
        assert angleKey == "angle", line
        assert tagsKey == "tags", line
        
        return cls(id = brushId, xy = V2d.from_string(x + " " + y), scale = Fraction(scale), angle = Fraction(angle), tags = parseDlmtArray(tagsInfo))

    def __str__(self):
        return "brushstroke {} xy {} scale {} angle {} tags {}".format(self.id, self.xy, self.scale, self.angle, toDlmtArray(self.tags, sep=", "))
    
    def __repr__(self):
        return "brushstroke {} xy {} scale {} angle {} tags {}".format(self.id, self.xy, self.scale, self.angle, toDlmtArray(self.tags, sep=", "))
