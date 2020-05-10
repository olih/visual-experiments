import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList

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

    def test_rotate(self):
        self.assertEqual(ptA.rotate(Fraction("1/2")), - ptA)
        self.assertEqual(ptA.rotate(Fraction("1/4")), V2d.from_string("-1/3 1/4"))
        self.assertEqual(ptA.rotate(Fraction("-1/4")), V2d.from_string("1/3 -1/4"))
 
class TestV2dList(unittest.TestCase):

    def test_create(self):
        self.assertEqual(str(listABCDE), "1/4 1/3, 1/5 1/6, 1/7 -1/9, -1/13 -1/23, 1/17 4/5")
    
    def test_to_cartesian_string(self):
        self.assertEqual(listABCDE.to_cartesian_string(100), "(25.000,33.333)(20.000,16.667)(14.286,-11.111)(-7.692,-4.348)(5.882,80.000)")

    def test_to_from_dalmatian_string(self):
        self.assertEqual(listABCDE.to_dalmatian_string(), "1/4 1/3 1/5 1/6 1/7 -1/9 -1/13 -1/23 1/17 4/5")
        self.assertEqual(V2dList.from_dalmatian_string(listABCDE.to_dalmatian_string()),listABCDE)
        self.assertEqual(V2dList.from_dalmatian_string(listABCDE.to_dalmatian_string(";"), ";"),listABCDE)
    
    def test_to_dalmatian_list(self):
        self.assertEqual(listABCDE.to_dalmatian_list(), ["1/4 1/3","1/5 1/6","1/7 -1/9","-1/13 -1/23", "1/17 4/5"])
        self.assertEqual(V2dList.from_dalmatian_list(listABCDE.to_dalmatian_list()), listABCDE)

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

    def test_slice(self):
        self.assertEqual(listCDE[0], ptC)
        self.assertEqual(listCDE[-1], ptE)
        self.assertEqual(listCDE[0:2], [ptC, ptD])
        self.assertEqual(listABCDE[:4:2], [ptA, ptC])

    def test_to_bigram(self):
        self.assertEqual(listCDE.to_bigram(), [(ptC, ptD), (ptD, ptE)])

    def test_mirror(self):
        self.assertEqual(listCDE.clone(), listCDE)
        self.assertEqual(listCDE.reverse(),V2dList([ptE, ptD, ptC]))
        self.assertEqual(listCDE.mirror(), V2dList([ptC, ptD, ptE, ptE, ptD, ptC]))

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

    def test_to_svg_string(self):
        dpu = 100
        self.assertEqual(VSegment.from_line_to(ptC).to_svg_string(dpu), "L 14.286 11.111")
        self.assertEqual(VSegment.from_move_to(ptA).to_svg_string(dpu), "M 25.000 -33.333")
        self.assertEqual(VSegment.from_close().to_svg_string(dpu), "Z")
        self.assertEqual(VSegment.from_cubic_bezier(ptE, ptC, ptD).to_svg_string(dpu), "C 14.286 11.111 -7.692 4.348 5.882 -80.000")
        self.assertEqual(VSegment.from_smooth_bezier(ptE, ptC).to_svg_string(dpu), "S 14.286 11.111 5.882 -80.000")
        self.assertEqual(VSegment.from_quadratic_bezier(ptE, ptC).to_svg_string(dpu), "Q 14.286 11.111 5.882 -80.000")
    
    def test_rotate(self):
        r90 = Fraction("1/4")
        self.assertEqual(VSegment.from_close().rotate(r90), VSegment.from_close())
        self.assertEqual(VSegment.from_line_to(ptA).rotate(r90).to_dalmatian_string(), "L -1/3 1/4")
        self.assertEqual(VSegment.from_cubic_bezier(ptE, ptC, ptD).rotate(r90).to_dalmatian_string(), "C 1/9 1/7 1/23 -1/13 -4/5 1/17")

    def test_translate(self):
        self.assertEqual(VSegment.from_close().translate(ptE), VSegment.from_close())
        self.assertEqual(VSegment.from_line_to(ptA).translate(ptB).to_dalmatian_string(), "L 9/20 1/2")
        self.assertEqual(VSegment.from_cubic_bezier(ptE, ptC, ptD).translate(ptB).to_dalmatian_string(), "C 12/35 1/18 8/65 17/138 22/85 29/30")

class TestFractionList(unittest.TestCase):

    def test_create(self):
        fractlist = "1/4 -1/3 1/5 1/6 4/5"
        self.assertEqual(str(FractionList.from_string(fractlist)), fractlist)

    def test_choice(self):
        fractlist = FractionList.from_string("1/4 -1/3 1/5 1/6 4/5")
        self.assertEqual(fractlist.signed_sample(2, ";").count(";"), 1)
        self.assertEqual(len(fractlist.signed_sample_list(3)), 3)


class TestVPath(unittest.TestCase):

    def test_from_to_dalmatian_string(self):
        dpath = "[ M -1/7 -1/9,L 1/7 -1/9,Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]"
        self.assertEqual(VPath.from_dalmatian_string(dpath).to_dalmatian_string(), dpath)

    def test_to_core_cartesian_string(self):
        vpath = VPath.from_dalmatian_string("[ M -1/7 -1/9,L 1/7 -1/9,Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]")
        self.assertEqual(vpath.to_core_cartesian_string(100, ";"), "(-14.286,-11.111);(14.286,-11.111);(50.000,1.739);(25.000,0.901);(75.000,2.564);(50.000,1.770)")
        self.assertEqual(len(vpath.to_core_cartesian_string(100, ";").split(";")), len(vpath)-1)

    def test_to_core_svg_string(self):
        vpath = VPath.from_dalmatian_string("[ M -1/7 -1/9,L 1/7 -1/9,Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]")
        self.assertEqual(vpath.to_core_svg_string(100), "M -14.286 11.111 L 14.286 11.111 L 50.000 -1.739 L 25.000 -0.901 L 75.000 -2.564 L 50.000 -1.770 Z")

    def test_to_svg_string(self):
        vpath = VPath.from_dalmatian_string("[ M -1/7 -1/9,L 1/7 -1/9,Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]")
        self.assertEqual(vpath.to_svg_string(100), "M -14.286 11.111 L 14.286 11.111 Q 25.000 -0.870 50.000 -1.739 T 25.000 -0.901 C 25.000 -0.855 50.000 -1.709 75.000 -2.564 S 25.000 -0.885 50.000 -1.770 Z")

    def test_action_frequency(self):
        vpath = VPath.from_dalmatian_string("[ M -1/7 -1/9,L 1/7 -1/9, L 1/7 -1/11, Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]")
        self.assertEqual(vpath.action_frequency(), { "M": 1, "L": 2, "Q": 1, "T": 1, "C": 1, "S": 1, "Z": 1, "E": 0, "Total": 8})

    def test_rotate(self):
        r90 = Fraction("1/4")
        r180 = Fraction("1/2")
        vpath = VPath.from_dalmatian_string("[ M -1/7 -1/9,L 1/7 -1/9, L 1/7 -1/11, Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]")
        self.assertEqual(vpath.rotate(r90).rotate(r90).rotate(r90).rotate(r90), vpath)
        self.assertEqual(vpath.rotate(r90).rotate(r90), vpath.rotate(r180))
        self.assertEqual(vpath.rotate(r180).to_dalmatian_string(), "[ M 1/7 1/9,L -1/7 1/9,L -1/7 1/11,Q -1/4 -1/115 -1/2 -2/115,T -1/4 -1/111,C -1/4 -1/117 -1/2 -2/117 -3/4 -1/39,S -1/4 -1/113 -1/2 -2/113,Z ]")

    def test_translate(self):
        vpath = VPath.from_dalmatian_string("[ M -1/7 -1/9,L 1/7 -1/9, L 1/7 -1/11, Q 1/4 1/115 1/2 2/115,T 1/4 1/111,C 1/4 1/117 1/2 2/117 3/4 1/39,S 1/4 1/113 1/2 2/113,Z ]")
        self.assertEqual(vpath.translate(ptE).translate(-ptE), vpath)

if __name__ == '__main__':
    unittest.main()