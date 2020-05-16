import os
import sys
import argparse
import re
from fractions import Fraction
from typing import List, Tuple, Dict, Set
from enum import Enum, auto
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree

from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

ET.register_namespace('', "http://www.w3.org/2000/svg")
ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")

def strip_string_array(rawlines: str, sep=",")->List[str]:
    return [line.strip() for line in rawlines.split(sep) if line.strip() != ""]

def parse_dlmt_array(line: str)-> List[str]:
    return strip_string_array(line.replace("[", "").replace("]", ""), sep=",")

def parse_dlmt_dict(line: str)-> Dict[str, str]:
    return { part.split(" ")[0]:part.split(" ")[1] for part in parse_dlmt_array(line) }

def to_dlmt_array(items: List[str], sep=",")->str:
    return "[ {} ]".format(sep.join(items))

def to_dlmt_dict(keyvalues: Dict[str, str], sep=",")->str:
    return to_dlmt_array(["{} {}".format(key, value) for key, value in keyvalues.items()], sep)

def strip_unknown(expected, lines):
    return [line for line in lines if expected in line]

def strip_empty(lines):
    return [line.strip() for line in lines if len(line.strip())>0]

def get_prefix(value:str)->str:
    return value.split(":", 2)[0]

PATTERN_NON_ALPHANUM = re.compile('[^a-z0-9_-]')

def as_tidy_name(value: str):
    return PATTERN_NON_ALPHANUM.sub('-', value.lower())

def as_float_string(value):
    return "{:.3f}".format(float(value))

# view i:1 lang en-gb xy 1/2 -1/3 width 1 height 1/2 flags OC tags all but [ i:1,i:2 ] -> everything
class DlmtView:
    def __init__(self, id: str, xy: V2d, width: Fraction, height: Fraction, everything: bool, tags: List[str], flags: str = "O", lang: str = "en", description: str = "" ):
        self.id = id
        self.xy = xy
        self.width = width
        self.height = height
        self.lang = lang
        self.description = description
        self.flags = flags
        self.everything = everything
        self.tags = tags
        self.tags_set = set(tags)
    
    @classmethod
    def from_string(cls, line: str):
        other, description  = line.split("->")
        cmd, viewId, langKey, langId, xyKey, x, y, widthKey, width, heightKey, height, flagsKey, flags, tagsKey, everything, butKey, tagsInfo = other.split(" ", 16)
        assert cmd == "view", line
        assert langKey == "lang", line
        assert xyKey == "xy", line
        assert widthKey == "width", line
        assert heightKey == "height", line
        assert flagsKey == "flags", line
        assert tagsKey == "tags", line
        assert butKey == "but", line
        
        return cls(id = viewId, xy = V2d.from_string(x + " " + y), width = Fraction(width), height = Fraction(height), lang = langId, description= description.strip(), flags = flags, everything = everything == "all", tags = parse_dlmt_array(tagsInfo) )

    def to_string(self):
        everything = "all" if self.everything else "none"
        return "view {} lang {} xy {} width {} height {} flags {} tags {} but {} -> {}".format(self.id, self.lang, self.xy, self.width, self.height, self.flags, everything, to_dlmt_array(self.tags, sep=", ") , self.description)
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.to_string() == str(other)

    def accept_point(self, xy: V2d)->bool:
        return xy.is_inside_rect(xy = self.xy, width = self.width, height = self.height)

    def accept_tags(self, tags: Set[str])->bool:
        if self.everything == True:
            return len(tags.intersection(self.tags_set)) == 0
        else:
            return len(tags.intersection(self.tags_set)) > 0

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
        
        return cls(id = descId, same_as= parse_dlmt_array(sameAsInfo), lang = langId, description= description.strip())

    def to_string(self):
        return "tag {} lang {} same-as {} -> {}".format(self.id, self.lang, to_dlmt_array(self.same_as, sep=", "), self.description)
    
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

    def get_neat_id(self):
        return as_tidy_name(self.id)

# brushstroke i:1 xy 1/15 1/100 scale 1/10 angle 0/1 tags [ i:1 ]
class DlmtBrushstroke:
    def __init__(self, brushid: str, xy: V2d, scale: Fraction, angle: Fraction, tags: List[str] = []):
        self.brushid = brushid
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
        
        return cls(brushid = brushId, xy = V2d.from_string(x + " " + y), scale = Fraction(scale), angle = Fraction(angle), tags = parse_dlmt_array(tagsInfo))

    def to_string(self):
        return "brushstroke {} xy {} scale {} angle {} tags {}".format(self.brushid, self.xy, self.scale, self.angle, to_dlmt_array(self.tags, sep=", "))

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()
        
    def __eq__(self, other):
        return self.to_string() == str(other)

    def get_degree_angle_string(self):
        return as_float_string(self.angle*360)

    def get_scale_string(self):
        return as_float_string(self.scale)

    def get_neat_brush_id(self):
        return as_tidy_name(self.brushid)

    def get_tags_set(self):
        return set(self.tags)


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

# system cartesian right-dir + up-dir -
class DlmtCoordinateSystem:
    def __init__(self, right_dir: AxisDir, up_dir: AxisDir, coordinate_type: CoordinateType):
        self.right_dir = right_dir
        self.up_dir = up_dir
        self.coordinate_type = coordinate_type
    
    @classmethod
    def from_string(cls, line: str):
        systemKey, cartesianKey, rightDirKey, rightDir, upDirKey, upDir = line.split()
        assert systemKey == "system", line
        assert cartesianKey == "cartesian", line
        assert rightDirKey == "right-dir", line
        assert upDirKey == "up-dir", line
        
        return cls(right_dir = AxisDir.from_string(rightDir), up_dir = AxisDir.from_string(upDir), coordinate_type = CoordinateType.from_string(cartesianKey))

    def __str__(self):
        return "system {} right-dir {} up-dir {}".format(CoordinateType.to_string(self.coordinate_type), AxisDir.to_string(self.right_dir), AxisDir.to_string(self.up_dir))
    
    def __repr__(self):
       return "system {} right-dir {} up-dir {}".format(CoordinateType.to_string(self.coordinate_type), AxisDir.to_string(self.right_dir), AxisDir.to_string(self.up_dir))

    def __eq__(self, other):
        return self.right_dir == other.right_dir and self.up_dir == other.up_dir and self.coordinate_type == other.coordinate_type

# system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2
class DlmtBrushCoordinateSystem:
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
        self.brush_page_ratio = Fraction("1/50")
        self.page_coordinate_system = DlmtCoordinateSystem.from_string("system cartesian right-dir + up-dir -")
        self.brush_coordinate_system = DlmtBrushCoordinateSystem.from_string("system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2")
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
        if value != "system cartesian right-dir + up-dir -":
            raise Exception("Page coordinate system not supported yet: "+ value)
        return self.set_page_coordinate_system(DlmtCoordinateSystem.from_string(value))

    def set_brush_coordinate_system(self, value: DlmtBrushCoordinateSystem):
        self.brush_coordinate_system = value
        return self

    def set_brush_coordinate_system_string(self, value: str):
        if value != "system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2":
            raise Exception("Brush coordinate system not supported yet: " + value)
        return self.set_brush_coordinate_system(DlmtBrushCoordinateSystem.from_string(value))

    def set_brush_page_ratio(self, value: Fraction):
        self.brush_page_ratio = value
        return self

    def set_brush_page_ratio_string(self, value: str):
        return self.set_brush_page_ratio(Fraction(value))

    def set_prefixes(self, prefixes: Dict[str, str]):
        self.prefixes = prefixes
        return self
    
    def set_require_sections(self, sections: Dict[str, str]):
        self.require_sections = sections
        return self

    def set_url(self, name: str, media_type: str, lang: str, url: str):
        self.url_refs[(name.strip(), media_type.strip(), lang.strip())] = url.strip()
        return self

    def get_url(self, name: str, media_type: str, lang: str, defaultValue = None):
        return self.url_refs.get((name.strip(), media_type.strip(), lang.strip()), defaultValue)

    def set_text(self, name: str,lang: str, text: str):
        self.text_refs[(name.strip(), lang.strip())] = text.strip()
        return self

    def get_text(self, name: str,lang: str, defaultValue = None):
        return self.text_refs.get((name.strip(), lang.strip()), defaultValue)

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
                result.set_brush_coordinate_system(DlmtBrushCoordinateSystem.from_string(value))
            elif key == "brush-page-ratio":
                result.set_brush_page_ratio(Fraction(value))
            elif key == "id-urn":
                result.set_id_urn(value)
            elif key == "prefixes":
                result.set_prefixes(parse_dlmt_dict(value))
            elif key == "require-sections":
                result.set_require_sections(parse_dlmt_dict(value))
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
        results.append("require-sections: {}".format(to_dlmt_dict(self.require_sections)))
        results.append("prefixes: {}".format(to_dlmt_dict(self.prefixes)))
        results.append("page-coordinate-system: {}".format(self.page_coordinate_system))
        results.append("brush-coordinate-system: {}".format(self.brush_coordinate_system))
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
        thisone = (self.id_urn, self.brush_page_ratio, self.page_coordinate_system, self.brush_coordinate_system, self.prefixes, self.require_sections, self.url_refs, self.text_refs)
        otherone = (other.id_urn, other.brush_page_ratio, other.page_coordinate_system, other.brush_coordinate_system, other.prefixes, other.require_sections, other.url_refs, other.text_refs)
        return thisone == otherone

    def get_short_prefixes(self)->Set[str]:
        return set([key for key, _ in self.prefixes.items()])

    def to_xml_svg(self, lang: str):
        metadata = ET.Element('metadata', attrib = {})
        rdfEl = ET.SubElement(metadata, 'rdf:RDF', attrib = {})
        ccWork = ET.SubElement(rdfEl, 'cc:Work', attrib = {})
        ET.SubElement(ccWork, 'dc:format', attrib = { }).text = "image/svg+xml"
        ET.SubElement(ccWork, 'dc:type', attrib = { "rdf:resource": "http://purl.org/dc/dcmitype/StillImage" })
        ET.SubElement(ccWork, 'dc:title', attrib = { }).text = self.get_text("title", "")
        ET.SubElement(ccWork, 'dc:description', attrib = { }).text = self.get_text("description", lang, "")
        ET.SubElement(ccWork, 'dc:source', attrib = { }).text = "source"
        ET.SubElement(ccWork, 'dc:language', attrib = { }).text = lang
        ET.SubElement(ccWork, 'dc:identifier', attrib = { }).text = self.id_urn
        ET.SubElement(ccWork, 'dc:date', attrib = { }).text = "2020"
        dcCreator = ET.SubElement(ccWork, 'dc:creator', attrib = { })
        ccAgent = ET.SubElement(dcCreator, 'cc:Agent', attrib = { })
        ET.SubElement(ccAgent, 'dc:title', attrib = { }).text = self.get_text("creator", lang, "")
        ET.SubElement(ccWork, 'cc:license', attrib = { "rdf:resource": self. get_url("license-url", "html", lang, "https://creativecommons.org/licenses/by-sa/4.0/legalcode")})
        return metadata



class SvgRenderingConfig:
    
    def __init__(self, headers: DlmtHeaders, view: DlmtView, view_pixel_width: int):
        self.headers = headers
        self.view = view
        self.view_pixel_width = Fraction(view_pixel_width)
        self.zoomk = Fraction(1) / view.width # normalise view width to 1
        self.view_pixel_height = self.zoomk * view.height * self.view_pixel_width
        self.brush_width = self.zoomk * headers.brush_page_ratio * self.view_pixel_width

    def to_page_view_box(self):
        return "0 0 {}".format(V2d(self.view_pixel_width, self.view_pixel_height).to_float_string())

    def to_brush_view_box(self):
        return "{} {}".format(V2d(-self.brush_width/2, -self.brush_width/2).to_float_string(), V2d(self.brush_width, self.brush_width).to_float_string())

    def get_brush_width_string(self):
        return as_float_string(self.brush_width)

class PageBrushstroke:
    def __init__(self, vpath: VPath, tags = Set[str]):
        self.vpath = vpath
        self.tags = tags
    
    def to_string(self):
        return "pbs path {} tags {}".format(self.vpath.to_dalmatian_string(), list(self.tags))
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.vpath == other.vpath and self.tags == other.tags

    def to_xml_svg(self, renderConfig: SvgRenderingConfig):
        element = ET.Element('path', attrib = { "d": self.vpath.to_svg_string(float(renderConfig.view_pixel_width), float(renderConfig.view_pixel_height) ) })
        return element
    
    def zoom_to(self, xy: V2d, width: Fraction):
        return PageBrushstroke(self.vpath.translate(-xy).scale(Fraction(1) / width), self.tags)

class DalmatianMedia:
    
    def __init__(self, headers: DlmtHeaders):
        self.headers = headers
        self.views_dict = {}
        self.tag_descriptions = []
        self.brushstrokes = []
        self.brushes_dict = {}
        
    def __repr__(self):
        return "id: {}, views:{}, tags:{}, brushes:{}, brushstrokes:{}".format(self.headers.id_urn, len(self.views_dict), len(self.tag_descriptions), len(self.brushes_dict), len(self.brushstrokes))
   
    def __eq__(self, other):
        thisone = (self.headers, self.views_dict, self.tag_descriptions, self.brushes_dict, self.brushstrokes)
        otherone = (other.headers, other.views_dict, other.tag_descriptions, other.brushes_dict, other.brushstrokes)
        return thisone == otherone

    def set_views(self, views: List[DlmtView]):
        self.views_dict = {view.id:view for view in views }
        return self
    
    def add_view(self, view: DlmtView):
        self.views_dict[view.id] = view
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
        self.brushes_dict = {brush.id:brush for brush in brushes }
        return self

    def add_brush(self, brush: DlmtBrush):
        self.brushes_dict[brush.id] = brush
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

    def get_brush_by_id(self, brushid: str):
        return self.brushes_dict.get(brushid)

    def get_sorted_brushes(self):
        return sorted([brush for _, brush in self.brushes_dict.items()], key = lambda br: br.id)

    def get_sorted_views(self):
        return sorted([view for _, view in self.views_dict.items()], key = lambda v: v.id)

    def to_obj(self):
        return {
            "headers": self.headers.to_string_list(),
            "views": [str(view) for view in self.get_sorted_views()],
            "tag-descriptions": [str(tag_desc) for tag_desc in self.tag_descriptions],
            "brushes": [str(brush) for brush in self.get_sorted_brushes()],
            "brushstrokes": [str(brushstroke) for brushstroke in self.brushstrokes]
        }

    def to_string_list(self):
        lines = ["section header"]
        lines += self.headers.to_string_list()
        lines += ["--------"]
        lines += ["section views"]
        lines += [str(view) for view in self.get_sorted_views()]
        lines += ["--------"]
        lines += ["section tag-descriptions"]
        lines += [str(tag_desc) for tag_desc in self.tag_descriptions]
        lines += ["--------"]
        lines += ["section brushes"]
        lines += [str(brush) for brush in self.get_sorted_brushes()]
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

    def get_tag_ids(self)->Set[str]:
        return set([tag.id for tag in self.tag_descriptions])

    def get_brush_ids(self)->Set[str]:
        return set([brush.id for _, brush in self.brushes_dict.items()])

    def get_view_ids(self)->Set[str]:
        return set([view.id for _, view in self.views_dict.items()])
    
    def get_used_brush_ids(self)->Set[str]:
        return set([brushstroke.brushid for brushstroke in self.brushstrokes])

    def get_used_tag_ids(self)->Set[str]:
        return set([tagid for brushstroke in self.brushstrokes for tagid in brushstroke.tags])

    def get_used_short_prefixes(self)->Set[str]:
        return set(([get_prefix(same_as) for tag_desc in self.tag_descriptions for same_as in tag_desc.same_as]))
    
    def get_undeclared_short_prefixes(self)->Set[str]:
        return self.get_used_short_prefixes().difference(self.headers.get_short_prefixes())

    def get_undeclared_brush_ids(self)->Set[str]:
        return self.get_used_brush_ids().difference(self.get_brush_ids())

    def get_undeclared_tag_ids(self)->Set[str]:
        return self.get_used_tag_ids().difference(self.get_tag_ids())

    def check_references(self):
        missing_prefixes = self.get_undeclared_short_prefixes()
        missing_brushids = self.get_undeclared_brush_ids()
        missing_tagids = self.get_undeclared_tag_ids()
        results = []
        if len(missing_prefixes) > 0 :
            results.append("Prefixes in tags are not declared: {}".format(list(missing_prefixes)))
        if len(missing_brushids) > 0 :
            results.append("Brush ids in brushstrokes are not declared: {}".format(list(missing_brushids)))
        if len(missing_tagids) > 0 :
            results.append("Tag ids in brushstrokes are not declared: {}".format(list(missing_tagids)))
        return results
    
    def create_page_pixel_coordinate(self, viewid: str, view_pixel_width: int)->SvgRenderingConfig:
        return SvgRenderingConfig(self.headers, self.views_dict[viewid], view_pixel_width)


    def to_page_brushstroke_list(self)-> List[PageBrushstroke]:
        return [ PageBrushstroke(self.get_brush_by_id(bs.brushid).vpath.rotate(bs.angle).scale(self.headers.brush_page_ratio).scale(bs.scale).translate(bs.xy), set(bs.tags)) for bs in self.brushstrokes]

    def page_brushstroke_list_for_view(self, view: DlmtView) -> List[PageBrushstroke]:
        bs4tags = [pbs for pbs in self.to_page_brushstroke_list() if view.accept_tags(pbs.tags)]
        bs4opt = [pbs for pbs in bs4tags if pbs.vpath.is_mostly_inside_rect(view.xy, width = view.width, height = view.height)] if "O" in view.flags else bs4tags
        newbrushstokes = [pbs.zoom_to(view.xy, view.width) for pbs in bs4opt]
        return newbrushstokes

    def page_brushstroke_list_for_view_string(self, view: str) -> List[PageBrushstroke]:
        return self.page_brushstroke_list_for_view(DlmtView.from_string(view))

    def to_xml_svg(self, renderConfig: SvgRenderingConfig)->ElementTree:
        svg = ET.Element('svg', attrib = { 
            "xmlns": "http://www.w3.org/2000/svg",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xmlns:dc": "http://purl.org/dc/elements/1.1/",
            "xmlns:cc": "http://creativecommons.org/ns#",
            "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "xmlns:svg": "http://www.w3.org/2000/svg",
            "viewBox": renderConfig.to_page_view_box()
            })
        svg.append(self.headers.to_xml_svg(lang = "en"))
        for pbs in self.page_brushstroke_list_for_view(renderConfig.view):
            svg.append(pbs.to_xml_svg(renderConfig))
        return ElementTree(svg)

    def to_xml_svg_file(self, renderConfig: SvgRenderingConfig , file_or_filename):
        self.to_xml_svg(renderConfig).write(file_or_filename, encoding='UTF-8')