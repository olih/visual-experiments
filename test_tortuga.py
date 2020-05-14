import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from tortuga import TortugaConfig

refconfig = TortugaConfig().set_angles_string("0/1 1/4 1/2 3/4").set_magnitudes_string("1 2 3 4 5").set_brush_ids(["i:1", "i:2", "i:3"]).set_brush_page_ratio_string("1/50").set_magnitude_page_ratio_string("1/100")


class TestTortugaState(unittest.TestCase):

    def test_create_brushstroke(self):
        refconfig.clone().set_xy_string("10/100 10/100").set_chain("A")
