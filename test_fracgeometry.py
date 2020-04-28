import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath

pt0 = V2d.from_string("0/1 0/1")
ptA = V2d.from_string("1/4 1/3")
ptB = V2d.from_string("1/5 1/6")
ptC = V2d.from_string("1/7 -1/9")
ptD = V2d.from_string("-1/13 -1/23")
ptE = V2d.from_string("1/17 4/5")
listABCDE = V2dList([ptA, ptB, ptC, ptD, ptE])
listCDE = V2dList([ptC, ptD, ptE])

class TestV2d(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(ptA), "1/4 1/3")

    def test_to_cartesian_string(self):
        self.assertEqual(ptA.to_cartesian_string(100), "(25.000,33.333)")
    
    def test_to_svg_string(self):
        self.assertEqual(ptA.to_svg_string(100), "25.000 -33.333")

    def test_add(self):
        self.assertEqual(str(pt0 + ptA), "1/4 1/3")
        self.assertEqual(str(ptA + ptB), "9/20 1/2")
    
    def test_neg(self):
        self.assertEqual(str(-ptA), "-1/4 -1/3")
        self.assertEqual(str(ptA.neg_x()), "-1/4 1/3")
        self.assertEqual(str(ptA.neg_y()), "1/4 -1/3")
        self.assertEqual(ptA.neg_x().neg_y(), -ptA)
        self.assertEqual(- ptA.neg_x().neg_y(), ptA)

    def test_subtract(self):
        self.assertEqual(pt0 - ptA, - ptA)
        self.assertEqual(str(pt0 - ptA), "-1/4 -1/3")        
        self.assertEqual(str(ptA - pt0), "1/4 1/3")
        self.assertEqual(str(ptA - ptB), "1/20 1/6")

    def test_multiply(self):
        self.assertEqual(str(ptA*Fraction("1/3")), "1/12 1/9")
        self.assertEqual((ptA*Fraction("2/3")).square_magnitude(), ptA.square_magnitude()*Fraction("4/9"))

class TestV2dList(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(listABCDE), "1/4 1/3, 1/5 1/6, 1/7 -1/9, -1/13 -1/23, 1/17 4/5")
    
    def test_to_cartesian_string(self):
        self.assertEqual(listABCDE.to_cartesian_string(100), "(25.000,33.333)(20.000,16.667)(14.286,-11.111)(-7.692,-4.348)(5.882,80.000)")

    def test_to_svg_string(self):
        self.assertEqual(listABCDE.to_svg_string(100), "25.000 -33.333 20.000 -16.667 14.286 11.111 -7.692 4.348 5.882 -80.000")

    def test_add(self):
        sumOfList = listABCDE+listCDE
        self.assertEqual(sumOfList, listCDE+listABCDE)
        self.assertEqual(str(sumOfList), "11/28 2/9, 8/65 17/138, 24/119 31/45, -1/13 -1/23, 1/17 4/5")
        self.assertEqual(sumOfList[0], ptA+ptC)
        self.assertEqual(sumOfList[-1], ptE)

    def test_substract(self):
        substraction = listABCDE - listCDE
        self.assertEqual(substraction, - (listCDE-listABCDE))
        self.assertEqual(substraction[0], ptA-ptC)
        self.assertEqual(substraction[2], ptC-ptE)
        self.assertEqual(substraction[-1], ptE)

    def test_multiply(self):
        self.assertEqual(listCDE* Fraction("1/1"), listCDE)
        self.assertEqual(str(listCDE * Fraction("1/5")),"1/35 -1/45, -1/65 -1/115, 1/85 4/25" )

    def test_neg(self):
        self.assertEqual(listCDE.neg_x().neg_y(), - listCDE)
        self.assertEqual(str(listCDE.neg_x()), "-1/7 -1/9, 1/13 -1/23, -1/17 4/5")

    def test_circular(self):
        self.assertEqual(listCDE.circular()[-1], ptC)
        self.assertEqual(listCDE.circular(), listCDE.extend(V2dList([ptC])))

    def test_to_bigram(self):
        self.assertEqual(listCDE.to_bigram(), [(ptC, ptD), (ptD, ptE)])

class TestVSegment(unittest.TestCase):

    def test_to_dalmatian_string(self):
        self.assertEqual(VSegment.from_line_to(ptC).to_dalmatian_string(), "L 1/7 -1/9")
        self.assertEqual(VSegment.from_move_to(ptA).to_dalmatian_string(), "M 1/4 1/3")
        self.assertEqual(VSegment.from_close().to_dalmatian_string(), "Z")
        self.assertEqual(VSegment.from_cubic_bezier(ptE, ptC, ptD).to_dalmatian_string(), "C "+listCDE.to_dalmatian_string())
        self.assertEqual(VSegment.from_smooth_bezier(ptE, ptC).to_dalmatian_string(), "S 1/7 -1/9 1/17 4/5")
        self.assertEqual(VSegment.from_quadratic_bezier(ptE, ptC).to_dalmatian_string(), "Q 1/7 -1/9 1/17 4/5")

    def test_from_dalmatian_string(self):
        self.assertEqual(VSegment.from_dalmatian_string("Z").to_dalmatian_string(), "Z")
        self.assertEqual(VSegment.from_dalmatian_string("L 1/7 -1/9").to_dalmatian_string(), "L 1/7 -1/9")
        self.assertEqual(VSegment.from_dalmatian_string("M -1/7 -1/9").to_dalmatian_string(), "M -1/7 -1/9")
        self.assertEqual(VSegment.from_dalmatian_string("T 1/4 1/111").to_dalmatian_string(), "T 1/4 1/111")
        self.assertEqual(VSegment.from_dalmatian_string("S 1/4 1/113 1/2 2/113").to_dalmatian_string(), "S 1/4 1/113 1/2 2/113")
        self.assertEqual(VSegment.from_dalmatian_string("Q 1/4 1/115 1/2 2/115").to_dalmatian_string(), "Q 1/4 1/115 1/2 2/115")
        self.assertEqual(VSegment.from_dalmatian_string("C 1/4 1/117 1/2 2/117 3/4 1/39").to_dalmatian_string(), "C 1/4 1/117 1/2 2/117 3/4 1/39")

class TestVPath(unittest.TestCase):

    def test_from_to_dalmatian_string(self):
        dpath = "[ M -1/7 -1/9,L 1/7 -1/9,Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]"
        self.assertEqual(VPath.from_dalmatian_string(dpath).to_dalmatian_string(), dpath)

if __name__ == '__main__':
    unittest.main()