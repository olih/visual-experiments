import unittest
from fractions import Fraction
from fracgeometry import V2d

pt0 = "0/1 0/1"
ptA = "1/4 1/3"
ptB = "1/5 1/6"

class TestFracGeometry(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(V2d(ptA)), ptA)

    def test_addVector(self):
        self.assertEqual(str(V2d(pt0) + V2d(ptA)), ptA)
        self.assertEqual(str(V2d(ptA) + V2d(ptB)), "9/20 1/2")
    
    def test_subtractVector(self):
        self.assertEqual(str(V2d(pt0) - V2d(ptA)), "-1/4 -1/3")
        self.assertEqual(str(V2d(ptA) - V2d(pt0)), ptA)
        self.assertEqual(str(V2d(ptA) - V2d(ptB)), "1/20 1/6")

    def test_multiplyVector(self):
        self.assertEqual(str(V2d(ptA)*Fraction("1/3")), "1/12 1/9")
        self.assertEqual((V2d(ptA)*Fraction("2/3")).squareMagnitude(), V2d(ptA).squareMagnitude()*Fraction("4/9"))

   
if __name__ == '__main__':
    unittest.main()