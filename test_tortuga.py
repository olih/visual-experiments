import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from tortuga import TortugaConfig, TortugaState, TortugaAction

refconfig = TortugaConfig().set_angles_string("0/1 1/4 1/2 3/4").set_magnitudes_string("1 2 3 4 5").set_brush_ids(["i:1", "i:2", "i:3"]).set_magnitude_page_ratio_string("1/100").set_scale_magnitude_ratio_string("3/2").set_chain("Z")

class TestTortugaState(unittest.TestCase):
    def test_clone_config(self):
        self.assertEqual(refconfig.clone(), refconfig)

    def test_change_brush(self):
        state = TortugaState(refconfig.clone().set_xy_string("10/100 10/100")).set_target(TortugaAction.BRUSH)
        self.assertEqual(state.create_brushstroke(), "brushstroke i:1 xy 11/100 1/10 scale 3/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:2 xy 3/25 1/10 scale 3/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:3 xy 13/100 1/10 scale 3/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 7/50 1/10 scale 3/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.PREVIOUS).create_brushstroke(), "brushstroke i:3 xy 3/20 1/10 scale 3/2 angle 0 tags [  ]")

    def test_amplitude(self):
        state = TortugaState(refconfig.clone().set_xy_string("10/100 10/100")).set_target(TortugaAction.AMPLITUDE)
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 3/25 1/10 scale 3 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 3/20 1/10 scale 9/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 19/100 1/10 scale 6 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.PREVIOUS).create_brushstroke(), "brushstroke i:1 xy 11/50 1/10 scale 9/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEGATE).create_brushstroke(), "brushstroke i:1 xy 19/100 1/10 scale 9/2 angle 0 tags [  ]")
