import os
import sys
import argparse
from fractions import Fraction
from typing import List, Tuple, Dict
from enum import Enum, auto

from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

def stripStringArray(rawlines: str, sep=",")->List[str]:
    return [line.strip() for line in rawlines.split(sep) if line.strip() != ""]

def parseDlmtArray(line: str)-> List[str]:
    return stripStringArray(line.replace("[", "").replace("]", ""), sep=",")

def parseDlmtDict(line: str)-> Dict[str, str]:
    return { part.split(" ")[0]:part.split(" ")[1] for part in parseDlmtArray(line) }

def toDlmtArray(items: List[str], sep=",")->str:
    return "[ {} ]".format(sep.join(items))

def toDlmtDict(keyvalues: Dict[str, str], sep=",")->str:
    return toDlmtArray(["{} {}".format(key, value) for key, value in keyvalues.items()], sep)

def strip_unknown(expected, lines):
    return [line for line in lines if expected in line]

def strip_empty(lines):
    return [line.strip() for line in lines if len(line.strip())>0]

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

    def to_string(self):
        return "view {} lang {} xy {} width {} height {} -> {}".format(self.id, self.lang, self.xy, self.width, self.height, self.description)
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.to_string() == str(other)

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

    def to_string(self):
        return "tag {} lang {} same-as {} -> {}".format(self.id, self.lang, toDlmtArray(self.same_as, sep=", "), self.description)
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.to_string() == str(other)

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

    def to_string(self):
        return "brush {} ext-id {} path {}".format(self.id, self.ext_id, self.vpath.to_dalmatian_string())
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.to_string() == str(other)

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

    def to_string(self):
        return "brushstroke {} xy {} scale {} angle {} tags {}".format(self.id, self.xy, self.scale, self.angle, toDlmtArray(self.tags, sep=", "))

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()
        
    def __eq__(self, other):
        return self.to_string() == str(other)

class AxisDir(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    NOT_SUPPORTED = auto()
    
    @classmethod
    def from_string(cls, value: str):
        if value == "+":
            return AxisDir.POSITIVE
        elif value == "-":
            return AxisDir.NEGATIVE
        else:
            return AxisDir.NOT_SUPPORTED
    
    @classmethod
    def to_string(cls, value):
        if value == AxisDir.POSITIVE:
            return "+"
        elif value == AxisDir.NEGATIVE:
            return "-"
        else:
            return "E"

class CoordinateType(Enum):
    CARTESIAN = auto()
    POLAR = auto()
    NOT_SUPPORTED = auto()
    
    @classmethod
    def from_string(cls, value: str):
        if value == "cartesian":
            return CoordinateType.CARTESIAN
        elif value == "polar":
            return CoordinateType.POLAR
        else:
            return CoordinateType.NOT_SUPPORTED
    
    @classmethod
    def to_string(cls, value):
        if value == CoordinateType.CARTESIAN:
            return "cartesian"
        elif value == CoordinateType.POLAR:
            return "polar"
        else:
            return "E"

# system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2
class DlmtCoordinateSystem:
    def __init__(self, right_dir: AxisDir, up_dir: AxisDir, origin_x: Fraction, origin_y: Fraction, coordinate_type: CoordinateType):
        self.right_dir = right_dir
        self.up_dir = up_dir
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.coordinate_type = coordinate_type
    
    @classmethod
    def from_string(cls, line: str):
        systemKey, cartesianKey, rightDirKey, rightDir, upDirKey, upDir, originXKey, originX, originYKey, originY = line.split()
        assert systemKey == "system", line
        assert cartesianKey == "cartesian", line
        assert rightDirKey == "right-dir", line
        assert upDirKey == "up-dir", line
        assert originXKey == "origin-x", line
        assert originYKey == "origin-y", line
        
        return cls(right_dir = AxisDir.from_string(rightDir), up_dir = AxisDir.from_string(upDir), origin_x = Fraction(originX), origin_y = Fraction(originY), coordinate_type = CoordinateType.from_string(cartesianKey))

    def __str__(self):
        return "system {} right-dir {} up-dir {} origin-x {} origin-y {}".format(CoordinateType.to_string(self.coordinate_type), AxisDir.to_string(self.right_dir), AxisDir.to_string(self.up_dir), self.origin_x, self.origin_y)
    
    def __repr__(self):
       return "system {} right-dir {} up-dir {} origin-x {} origin-y {}".format(CoordinateType.to_string(self.coordinate_type), AxisDir.to_string(self.right_dir), AxisDir.to_string(self.up_dir), self.origin_x, self.origin_y)

    def __eq__(self, other):
        return self.right_dir == other.right_dir and self.up_dir == other.up_dir and self.origin_x == other.origin_x and self.origin_y == other.origin_y and self.coordinate_type == other.coordinate_type

class DlmtHeaders:
    def __init__(self):
        self.id_urn = ""
        self.brush_ratio = Fraction("1/1")
        self.page_ratio = Fraction("1/1")
        self.brush_page_ratio = Fraction("1/50")
        self.page_coordinate_system = DlmtCoordinateSystem.from_string("system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2")
        self.brush_coordinate_system = DlmtCoordinateSystem.from_string("system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2")
        self.prefixes = { "github": "https://github.com/" }
        self.require_sections  = {i: "0.5" for i in ["header", "views", "tag-descriptions", "brushes", "brushstrokes"]}
        self.url_refs = { }
        self.text_refs = { }

    def set_id_urn(self, value: str):
        self.id_urn = value
        return self

    def set_page_coordinate_system(self, value: DlmtCoordinateSystem):
        self.page_coordinate_system = value
        return self

    def set_page_coordinate_system_string(self, value: str):
        return self.set_page_coordinate_system(DlmtCoordinateSystem.from_string(value))

    def set_brush_coordinate_system(self, value: DlmtCoordinateSystem):
        self.brush_coordinate_system = value
        return self

    def set_brush_coordinate_system_string(self, value: str):
        return self.set_brush_coordinate_system(DlmtCoordinateSystem.from_string(value))

    def set_page_ratio(self, value: Fraction):
        self.page_ratio = value
        return self

    def set_brush_ratio(self, value: Fraction):
        self.brush_ratio = value
        return self 

    def set_brush_page_ratio(self, value: Fraction):
        self.brush_page_ratio = value
        return self
    
    def set_prefixes(self, prefixes: Dict[str, str]):
        self.prefixes = prefixes
        return self
    
    def set_require_sections(self, sections: Dict[str, str]):
        self.require_sections = sections
        return self

    def set_url(self, name: str, media_type: str, lang: str, url: str):
        self.url_refs[(name.strip(), media_type.strip(), lang.strip())] = url.strip()
        return self

    def set_text(self, name: str,lang: str, text: str):
        self.text_refs[(name.strip(), lang.strip())] = text.strip()
        return self

    @classmethod
    def from_string_list(cls, lines: str):
        result = cls()
        for line in lines:
            rawkey, rawvalue = line.split(":", 1)
            key = rawkey.strip()
            value = rawvalue.strip()
            if key == "page-coordinate-system":
                result.set_page_coordinate_system(DlmtCoordinateSystem.from_string(value))
            elif key == "brush-coordinate-system":
                result.set_brush_coordinate_system(DlmtCoordinateSystem.from_string(value))
            elif key == "page-ratio":
                result.set_page_ratio(Fraction(value))
            elif key == "brush-ratio":
                result.set_brush_ratio(Fraction(value))
            elif key == "brush-page-ratio":
                result.set_brush_page_ratio(Fraction(value))
            elif key == "id-urn":
                result.set_id_urn(value)
            elif key == "prefixes":
                result.set_prefixes(parseDlmtDict(value))
            elif key == "require-sections":
                result.set_require_sections(parseDlmtDict(value))
            elif key.count(" ") == 1:
                name, lang = key.split()
                if name in ["license", "attribution-name", "brushes-license", "brushes-attribution-name", "title", "description"]:
                    result.set_text(name, lang, value)
            elif key.count(" ") == 2:
                name, media_type, lang = key.split()
                supported_media = ["html", "json", "rdf", "markdown", "nt", "ttl", "json-ld", "csv"]
                if name in ["license-url", "attribution-url", "brushes-license-url", "brushes-attribution-url", "metadata-url", "homepage-url"] and media_type in supported_media:
                    result.set_url(name, media_type, lang, value)
            else:
                raise Exception("Header key [{}] is not supported".format(key))
        return result
    
    def to_string_list(self)->List[str]:
        results = []
        results.append("id-urn: {}".format(self.id_urn))
        results.append("require-sections: {}".format(toDlmtDict(self.require_sections)))
        results.append("prefixes: {}".format(toDlmtDict(self.prefixes)))
        results.append("page-coordinate-system: {}".format(self.page_coordinate_system))
        results.append("brush-coordinate-system: {}".format(self.brush_coordinate_system))
        results.append("page-ratio: {}".format(self.page_ratio))
        results.append("brush-ratio: {}".format(self.brush_ratio))
        results.append("brush-page-ratio: {}".format(self.brush_page_ratio))
        for keydata, value in self.text_refs.items():
            results.append("{} {}: {}".format(keydata[0], keydata[1], value))
        for keydata, value in self.url_refs.items():
            results.append("{} {} {}: {}".format(keydata[0], keydata[1], keydata[2], value))
        return results

    def to_string(self)->str:
        return "\n".join(self.to_string_list())

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()
    
    def __eq__(self, other):
        thisone = (self.id_urn, self.brush_ratio, self.page_ratio, self.brush_page_ratio, self.page_coordinate_system, self.brush_coordinate_system, self.prefixes, self.require_sections, self.url_refs, self.text_refs)
        otherone = (other.id_urn, other.brush_ratio, other.page_ratio, other.brush_page_ratio, other.page_coordinate_system, other.brush_coordinate_system, other.prefixes, other.require_sections, other.url_refs, other.text_refs)
        return thisone == otherone



class DalmatianMedia:
    
    def __init__(self, headers: DlmtHeaders):
        self.headers = headers
        self.views = []
        self.tag_descriptions = []
        self.brushes = []
        self.brushstrokes = []
        
    def __repr__(self):
        return "id: {}, views:{}, tags:{}, brushes:{}, brushstrokes:{}".format(self.headers.id_urn, len(self.views), len(self.tag_descriptions), len(self.brushes), len(self.brushstrokes))
   
    def __eq__(self, other):
        thisone = (self.headers, self.views, self.tag_descriptions, self.brushes, self.brushstrokes)
        otherone = (other.headers, other.views, other.tag_descriptions, other.brushes, other.brushstrokes)
        return thisone == otherone

    def set_views(self, views: List[DlmtView]):
        self.views = views
        return self
    
    def add_view(self, view: DlmtView):
        self.views.append(view)
        return self

    def add_view_string(self, view: str):
        return self.add_view(DlmtView.from_string(view))

    def set_tag_descriptions(self, tag_descriptions: List[DlmtTagDescription]):
        self.tag_descriptions = tag_descriptions
        return self

    def add_tag_description(self, tag_description: DlmtTagDescription):
        self.tag_descriptions.append(tag_description)
        return self

    def add_tag_description_string(self, tag_description: str):
        return self.add_tag_description(DlmtTagDescription.from_string(tag_description))

    def set_brushes(self, brushes: List[DlmtBrush]):
        self.brushes = brushes
        return self

    def add_brush(self, brush: DlmtBrush):
        self.brushes.append(brush)
        return self

    def add_brush_string(self, brush: str):
        return self.add_brush(DlmtBrush.from_string(brush))

    def set_brushstrokes(self, brushstrokes: List[DlmtBrushstroke]):
        self.brushstrokes = brushstrokes
        return self

    def add_brushstroke(self, brushstroke: DlmtBrushstroke):
        self.brushstrokes.append(brushstroke)
        return self

    def add_brushstroke_string(self, brushstroke: str):
        return self.add_brushstroke(DlmtBrushstroke.from_string(brushstroke))

    def to_obj(self):
        return {
            "headers": self.headers.to_string_list(),
            "views": [str(view) for view in self.views],
            "tag-descriptions": [str(tag_desc) for tag_desc in self.tag_descriptions],
            "brushes": [str(brush) for brush in self.brushes],
            "brushstrokes": [str(brushstroke) for brushstroke in self.brushstrokes]
        }

    def to_string_list(self):
        lines = ["section header"]
        lines += self.headers.to_string_list()
        lines += ["--------"]
        lines += ["section views"]
        lines += [str(view) for view in self.views]
        lines += ["--------"]
        lines += ["section tag-descriptions"]
        lines += [str(tag_desc) for tag_desc in self.tag_descriptions]
        lines += ["--------"]
        lines += ["section brushes"]
        lines += [str(brush) for brush in self.brushes]
        lines += ["--------"]
        lines += ["section brushstrokes"]
        lines += [str(brushstroke) for brushstroke in self.brushstrokes]
        return lines
    
    def to_string(self)->str:
        return "\n".join(self.to_string_list())
    
    def __str__(self):
        return self.to_string()
    
    @classmethod
    def from_obj(cls, mediaobj):
        headers = DlmtHeaders.from_string_list(mediaobj["headers"])
        views = [DlmtView.from_string(view) for view in mediaobj["views"]]
        tag_descriptions = [DlmtTagDescription.from_string(tagdesc) for tagdesc in mediaobj["tag-descriptions"]]
        brushes = [DlmtBrush.from_string(brush) for brush in mediaobj["brushes"]]
        brushstrokes = [DlmtBrushstroke.from_string(brushstroke) for brushstroke in mediaobj["brushstrokes"]]
        return cls(headers).set_views(views).set_tag_descriptions(tag_descriptions).set_brushes(brushes).set_brushstrokes(brushstrokes)

    @classmethod
    def from_string(cls, content):
        headersStr, viewsStr, tagDescriptionsStr, brushesStr, brushstrokesStr = content.split('--------')
        headers = strip_empty(headersStr.splitlines())
        views = strip_empty(viewsStr.splitlines())
        tagDescriptions = strip_empty(tagDescriptionsStr.splitlines())
        brushes = strip_empty(brushesStr.splitlines())
        brushstrokes = strip_empty(brushstrokesStr.splitlines())
        assert headers[0] == "section header", headers[0]
        assert views[0] == "section views", views[0]
        assert tagDescriptions[0] == "section tag-descriptions", tagDescriptions[0]
        assert brushes[0] == "section brushes", brushes[0]
        assert brushstrokes[0] == "section brushstrokes", brushstrokes[0]
        dlmtheaders = DlmtHeaders.from_string_list(strip_unknown(":", headers[1:]))
        dlmtviews = [DlmtView.from_string(view) for view in strip_unknown("view ", views[1:])]
        dlmttag_descriptions = [DlmtTagDescription.from_string(tagdesc) for tagdesc in strip_unknown("tag ", tagDescriptions[1:])]
        dlmtbrushes = [DlmtBrush.from_string(brush) for brush in strip_unknown("brush ", brushes[1:])]
        dlmtbrushstrokes = [DlmtBrushstroke.from_string(brushstroke) for brushstroke in strip_unknown("brushstroke ", brushstrokes[1:])]
        return cls(dlmtheaders).set_views(dlmtviews).set_tag_descriptions(dlmttag_descriptions).set_brushes(dlmtbrushes).set_brushstrokes(dlmtbrushstrokes)