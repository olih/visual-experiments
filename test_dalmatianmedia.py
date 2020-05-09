import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from dalmatianmedia import DlmtView, DlmtTagDescription, DlmtBrush, DlmtBrushstroke, DlmtCoordinateSystem, DlmtBrushCoordinateSystem, DlmtHeaders, DalmatianMedia, PagePixelCoordinate

pt0 = V2d.from_string("0/1 0/1")
ptA = V2d.from_string("1/4 1/3")
ptB = V2d.from_string("1/5 1/6")
ptC = V2d.from_string("1/7 -1/9")
ptD = V2d.from_string("-1/13 -1/23")
ptE = V2d.from_string("1/17 4/5")

class TestDlmtView(unittest.TestCase):

    def test_convert(self):
        line = "view i:1 lang en-gb xy 1/2 -1/3 width 1 height 1/2 -> everything"
        self.assertEqual(str(DlmtView.from_string(line)), line)

class TestDlmtTagDescription(unittest.TestCase):

    def test_convert(self):
        line = "tag i:1 lang en-gb same-as [ geospecies:bioclasses/P632y, geospecies:bioclasses/P631y ] -> part of head"
        self.assertEqual(str(DlmtTagDescription.from_string(line)), line)

class TestDlmtBrush(unittest.TestCase):

    def test_convert(self):
        line = "brush i:1 ext-id brushes:abc3F path [ M -1/3 1/3,L 2/3 1/4,L 1/4 2/3,L -2/3 1/2 ]"
        self.assertEqual(str(DlmtBrush.from_string(line)), line)

class TestDlmtBrushstroke(unittest.TestCase):

    def test_convert(self):
        line = "brushstroke i:1 xy 1/15 1/100 scale 1/10 angle 1/4 tags [ i:1 ]"
        self.assertEqual(str(DlmtBrushstroke.from_string(line)), line)

class TestDlmtCoordinateSystem(unittest.TestCase):

    def test_convert(self):
        line = "system cartesian right-dir + up-dir -"
        self.assertEqual(str(DlmtCoordinateSystem.from_string(line)), line)

class TestDlmtBrushCoordinateSystem(unittest.TestCase):

    def test_convert(self):
        line = "system cartesian right-dir + up-dir - origin-x -1/2 origin-y 1/4"
        self.assertEqual(str(DlmtBrushCoordinateSystem.from_string(line)), line)

class TestDlmtHeaders(unittest.TestCase):

    def test_convert(self):
        headers = DlmtHeaders()
        headers.set_page_coordinate_system_string("system cartesian right-dir + up-dir -")
        headers.set_brush_coordinate_system_string("system cartesian right-dir - up-dir + origin-x 1/4 origin-y 1/5")
        headers.set_brush_page_ratio(Fraction("1/30"))
        headers.set_prefixes({ "prefix1": "http://domain1.com", "prefix2": "http://domain2.com"})
        headers.set_text("license", "en", "Creative Commons")
        headers.set_text("license", "fr", "Creative Communs")
        headers.set_text("title", "en", "Some english title")
        headers.set_text("title", "fr", "Titre en francais")
        headers.set_url("license-url", "html", "en", "https://creativecommons.org/licenses/by-sa/4.0/legalcode")
        headers.set_url("brushes-license-url", "json", "en", "https://creativecommons.org/licenses/by/4.0/legalcode")
        self.assertEqual(DlmtHeaders.from_string_list(headers.to_string_list()), headers)

class TestPagePixelCoordinate(unittest.TestCase):

    def test_to_svg_xy_string(self):
        headers = DlmtHeaders()
        headers.set_page_coordinate_system_string("system cartesian right-dir + up-dir -")
        headers.set_brush_page_ratio(Fraction("1/50"))
        view = DlmtView.from_string("view i:1 lang en-gb xy 20/100 20/100 width 40/100 height 30/100 -> test")
        pagePixelCoord = PagePixelCoordinate(headers, view, 400)
        self.assertEqual(pagePixelCoord.to_page_view_box(), "0 0 400.000 300.000")
        self.assertEqual(pagePixelCoord.to_brush_view_box(), "-10.000 -10.000 20.000 20.000")
        self.assertEqual(pagePixelCoord.brush_width, Fraction(20.0))
        self.assertEqual(pagePixelCoord.to_svg_xy_string(DlmtBrushstroke.from_string("brushstroke i:1 xy 20/100 20/100 scale 1/1 angle 1/1 tags [ i:1 ]")), "0.000 300.000")
        self.assertEqual(pagePixelCoord.to_svg_xy_string(DlmtBrushstroke.from_string("brushstroke i:1 xy 60/100 50/100 scale 1/1 angle 1/1 tags [ i:1 ]")), "400.000 0.000")
        self.assertEqual(pagePixelCoord.to_svg_xy_string(DlmtBrushstroke.from_string("brushstroke i:1 xy 40/100 35/100 scale 1/1 angle 1/1 tags [ i:1 ]")), "200.000 150.000")
        self.assertEqual(pagePixelCoord.to_svg_xy_string(DlmtBrushstroke.from_string("brushstroke i:1 xy 30/100 30/100 scale 1/1 angle 1/1 tags [ i:1 ]")), "100.000 200.000")

class TestDalmatianMedia(unittest.TestCase):

    def test_convert(self):
        headers = DlmtHeaders()
        headers.set_page_coordinate_system_string("system cartesian right-dir + up-dir -")
        headers.set_brush_coordinate_system_string("system cartesian right-dir - up-dir + origin-x 1/4 origin-y 1/5")
        headers.set_brush_page_ratio(Fraction("1/30"))
        headers.set_prefixes({ "prefix1": "http://domain1.com", "prefix2": "http://domain2.com", "geospecies": "http://geospecies"})
        headers.set_text("license", "en", "Creative Commons")
        headers.set_text("license", "fr", "Creative Communs")
        headers.set_text("title", "en", "Some english title")
        headers.set_text("title", "fr", "Titre en francais")
        headers.set_url("license-url", "html", "en", "https://creativecommons.org/licenses/by-sa/4.0/legalcode")
        headers.set_url("brushes-license-url", "json", "en", "https://creativecommons.org/licenses/by/4.0/legalcode")
        media = DalmatianMedia(headers)
        media.add_view_string("view i:1 lang en-gb xy -1/2 -1/2 width 1/1 height 1/1 -> everything")
        media.add_tag_description_string("tag i:1 lang en-gb same-as [ geospecies:bioclasses/P632y ] -> part of head")
        media.add_tag_description_string("tag i:1 lang fr-fr same-as [] -> visage")
        media.add_tag_description_string("tag i:2 lang fr same-as [] -> pied")
        media.add_brush_string("brush i:1 ext-id brushes:abc3F path [ M -1/3 1/3,L 2/3 1/4,L 1/4 2/3,L -2/3 1/2 ]")
        media.add_brush_string("brush i:2 ext-id brushes:abc4F path [ M -1/3 1/3,L 2/3 3/4,L 1/4 2/3,L -2/3 1/2 ]")
        media.add_brushstroke_string("brushstroke i:1 xy 1/15 1/100 scale 1/10 angle 0/1 tags [ i:1 ]")
        media.add_brushstroke_string("brushstroke i:1 xy 2/15 2/100 scale 2/10 angle 0/1 tags [ i:1 ]")
        media.add_brushstroke_string("brushstroke i:1 xy 3/15 3/100 scale 3/10 angle 0/1 tags [ i:1 ]")
        media.add_brushstroke_string("brushstroke i:2 xy 4/15 5/100 scale 5/10 angle 0/1 tags [ i:1, i:2 ]")
        self.assertEqual(DalmatianMedia.from_obj(media.to_obj()), media)
        self.assertEqual(DalmatianMedia.from_string(str(media)), media)
        self.assertEqual(media.get_tag_ids(), set(["i:1", "i:2"]))
        self.assertEqual(media.get_brush_ids(), set(["i:1", "i:2"]))
        self.assertEqual(media.get_view_ids(), set(["i:1"]))
        self.assertEqual(media.get_used_brush_ids(), set(["i:1", "i:2"]))
        self.assertEqual(media.get_used_tag_ids(), set(["i:1", "i:2"]))
        self.assertEqual(media.get_used_short_prefixes(), set(["geospecies"]))
        self.assertEqual(media.check_references(), [])
    
    def test_export_svg(self):
        media = DalmatianMedia(DlmtHeaders().set_brush_page_ratio(Fraction("1/100")))
        media.add_view_string("view i:1 lang en-gb xy 0 0 width 1/1 height 1/1 -> everything")
        media.add_tag_description_string("tag i:1 lang en-gb same-as [] -> default tag")
        media.add_brush_string("brush i:1 ext-id brushes:abc3F path [ M -1/3 1/3, L 1/3 1/3, L 1/3 -1/3, L -1/3 -1/3 ]")
        for i in range(10, 80, 10):
            media.add_brushstroke_string("brushstroke i:1 xy {}/100 50/100 scale 1/1 angle 1/1 tags [ i:1 ]".format(i))
        media.to_xml_svg_file(media.create_page_pixel_coordinate("i:1", 1000), "examples/one.svg")