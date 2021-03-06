import unittest
from fractions import Fraction
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from tortuga import TortugaConfig, TortugaState, TortugaAction, TortugaProducer, TortugaRuleMaker, TortugaTargetRand, TortugaActionRange

refconfig = TortugaConfig()
refconfig.set_angles_string("0/1 1/4 1/2 3/4").set_magnitudes_string("1 2 3 4 5")
refconfig.set_brush_ids(["i:1", "i:2", "i:3"])
refconfig.set_tags(["", "i:1", "i:2"])
refconfig.set_magnitude_page_ratio_string("1/100").set_scale_magnitude_ratio_string("3/2")
refconfig.set_chain("Z")

class TestTortugaAction(unittest.TestCase):
    def test(self):
        self.assertEqual(TortugaAction.from_string(TortugaAction.to_string(TortugaAction.ANGLE)), TortugaAction.ANGLE)
        self.assertEqual(TortugaAction.from_string(TortugaAction.to_string(TortugaAction.MAGNITUDE)), TortugaAction.MAGNITUDE)
        self.assertEqual(TortugaAction.from_string(TortugaAction.to_string(TortugaAction.BRUSH)), TortugaAction.BRUSH)
        self.assertEqual(TortugaAction.from_string(TortugaAction.to_string(TortugaAction.TAG)), TortugaAction.TAG)
        self.assertEqual(TortugaAction.from_string(TortugaAction.to_string(TortugaAction.NEXT)), TortugaAction.NEXT)
        self.assertEqual(TortugaAction.from_string(TortugaAction.to_string(TortugaAction.PREVIOUS)), TortugaAction.PREVIOUS)

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

    def test_change_tag(self):
        state = TortugaState(refconfig.clone().set_xy_string("10/100 10/100")).set_target(TortugaAction.TAG)
        self.assertEqual(state.create_brushstroke(), "brushstroke i:1 xy 11/100 1/10 scale 3/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 3/25 1/10 scale 3/2 angle 0 tags [ i:1 ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 13/100 1/10 scale 3/2 angle 0 tags [ i:2 ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 7/50 1/10 scale 3/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.PREVIOUS).create_brushstroke(), "brushstroke i:1 xy 3/20 1/10 scale 3/2 angle 0 tags [ i:2 ]")

    def test_amplitude(self):
        state = TortugaState(refconfig.clone().set_xy_string("10/100 10/100")).set_target(TortugaAction.MAGNITUDE)
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 3/25 1/10 scale 3 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 3/20 1/10 scale 9/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 19/100 1/10 scale 6 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.PREVIOUS).create_brushstroke(), "brushstroke i:1 xy 11/50 1/10 scale 9/2 angle 0 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEGATE).create_brushstroke(), "brushstroke i:1 xy 19/100 1/10 scale 9/2 angle 0 tags [  ]")

    def test_angle(self):
        state = TortugaState(refconfig.clone().set_xy_string("10/100 10/100")).set_target(TortugaAction.ANGLE)
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 1/10 11/100 scale 3/2 angle 1/4 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 9/100 11/100 scale 3/2 angle 1/2 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 9/100 1/10 scale 3/2 angle 3/4 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.PREVIOUS).create_brushstroke(), "brushstroke i:1 xy 2/25 1/10 scale 3/2 angle 1/2 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEGATE).create_brushstroke(), "brushstroke i:1 xy 7/100 1/10 scale 3/2 angle -1/2 tags [  ]")
    
    def test_angle_offset(self):
        state = TortugaState(refconfig.clone().set_xy_string("10/100 10/100").set_brushstoke_angle_offset_string("1/5")).set_target(TortugaAction.ANGLE)
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 1/10 11/100 scale 3/2 angle 9/20 tags [  ]")
        self.assertEqual(state.activate_verb(TortugaAction.NEXT).create_brushstroke(), "brushstroke i:1 xy 9/100 11/100 scale 3/2 angle 7/10 tags [  ]")

class TestTortugaProducer(unittest.TestCase):
    def test_produce(self):
        config = refconfig.clone().set_xy_string("10/100 10/100").set_chain("PPPPP")
        producer = TortugaProducer(config)
        self.assertEqual(len(producer.produce()), 5)
    
    def test_produce_brush(self):
        config = refconfig.clone().set_xy_string("10/100 10/100").set_chain("PAB>>P")
        producer = TortugaProducer(config)
        self.assertEqual(producer.produce()[1], "brushstroke i:3 xy 3/25 1/10 scale 3/2 angle 0 tags [  ]")

    def test_produce_restore(self):
        config = refconfig.clone().set_xy_string("10/100 10/100").set_chain("PP[PPP]P")
        producer = TortugaProducer(config)
        brushstokes = producer.produce()
        self.assertEqual(brushstokes[2],brushstokes[-1])
   
    def test_produce_longchain(self):
        config = refconfig.clone().set_xy_string("10/100 10/100").set_chain("PAB>P<APL>P")
        producer = TortugaProducer(config)
        self.assertEqual(len(producer.produce()), 4)

class TestTortugaTargetRand(unittest.TestCase):
    def test_choice(self):
        self.assertEqual(TortugaTargetRand.from_string("L <").choice(), "L<")
        self.assertIn(TortugaTargetRand.from_string("B < >").choice(), ["B<", "B>"])
        self.assertIn(TortugaTargetRand.from_string("A < > Z -").choice(), ["A<", "A>", "AZ", "A-"])

class TestTortugaActionRange(unittest.TestCase):
    def test_choice(self):
        self.assertIn(TortugaActionRange.from_string("B 1 3").choice(), [1, 2, 3])

class TestTortugaRuleMaker(unittest.TestCase):
    def test_make_no_branch(self):
        maker=TortugaRuleMaker()
        maker.set_vars("IJ")
        maker.set_actions_ranges("L 1 3;A 1 3;P 1 4")
        maker.set_supported_targets("L < >;A < > Z")
        made = maker.make()
        self.assertGreaterEqual(len(made[0]), 7 )
        self.assertGreaterEqual(len(made[1][0]["r"]), 7)
        self.assertGreaterEqual(len(made[1][1]["r"]), 7)

    def test_make_branch(self):
        maker=TortugaRuleMaker()
        maker.set_vars("IJ")
        maker.set_actions_ranges("L 1 3;A 1 3;P 1 4;[ 1 3")
        maker.set_supported_targets("L < >;A < >")
        made = maker.make()
        self.assertGreaterEqual(len(made[0]), 8 )
        self.assertTrue("[" in made[0])
        self.assertTrue("]" in made[0])
        self.assertGreaterEqual(len(made[1][0]["r"]), 8)
        self.assertGreaterEqual(len(made[1][1]["r"]), 8)

