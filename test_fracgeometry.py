import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList

pt0 = V2d.from_string("0/1 0/1")
ptA = V2d.from_string("1/4 1/3")
ptB = V2d.from_string("1/5 1/6")
ptC = V2d.from_string("1/7 -1/9")
ptD = V2d.from_string("-1/13 -1/23")
ptE = V2d.from_string("1/17 4/5")
listABCDE = V2dList([ptA, ptB, ptC, ptD, ptE])

class TestV2d(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(ptA), "1/4 1/3")

    def test_to_cartesian_string(self):
        self.assertEqual(ptA.to_cartesian_string(100), "(25.000,33.333)")

    def test_addVector(self):
        self.assertEqual(str(pt0 + ptA), "1/4 1/3")
        self.assertEqual(str(ptA + ptB), "9/20 1/2")
    
    def test_subtractVector(self):
        self.assertEqual(str(pt0 - ptA), "-1/4 -1/3")
        self.assertEqual(str(ptA - pt0), "1/4 1/3")
        self.assertEqual(str(ptA - ptB), "1/20 1/6")

    def test_multiplyVector(self):
        self.assertEqual(str(ptA*Fraction("1/3")), "1/12 1/9")
        self.assertEqual((ptA*Fraction("2/3")).square_magnitude(), ptA.square_magnitude()*Fraction("4/9"))

class TestV2dList(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(listABCDE), "1/4 1/3,1/5 1/6,1/7 -1/9,-1/13 -1/23,1/17 4/5")
    
    def test_to_cartesian_string(self):
        self.assertEqual(listABCDE.to_cartesian_string(100), "(25.000,33.333)(20.000,16.667)(14.286,-11.111)(-7.692,-4.348)(5.882,80.000)")


if __name__ == '__main__':
    unittest.main()