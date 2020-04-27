import unittest
from fractions import Fraction
from fracgeometry import V2d

pt0 = V2d.from_string("0/1 0/1")
ptA = V2d.from_string("1/4 1/3")
ptB = V2d.from_string("1/5 1/6")

class TestFracGeometry(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(ptA), "1/4 1/3")

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

   
if __name__ == '__main__':
    unittest.main()