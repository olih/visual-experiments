import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList

pt0 = V2d.from_string("0/1 0/1")
ptStart = V2d.from_string("10/100 10/100")
brushes = ["br1", "br2", "br3"]
amplitudes = [""]

class TestTortugaState(unittest.TestCase):

    def test_create_brushstroke(self):
        self.assertEqual(str(pt0), "1/4 1/3")
