import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from dalmatianmedia import DlmtView, DlmtTagDescription, DlmtBrush

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
