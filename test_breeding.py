import unittest

from breeding import ProductionRule, ProductionGame

class TestProductionGame(unittest.TestCase):

    def test_create(self):
        product = ProductionGame(chainlength = 60)
        product.set_constants("LQC").set_vars("IJK")
        product.init_with_random_rules(levels = 2, keyrules = ["L", "QQ", "C"])
        product.set_start("MI")
        product.produce()
        result = product.to_obj()
        self.assertEqual(len(result["rules"]), 3)
        self.assertGreaterEqual(len(result["chain"]), len(result["core-chain"]))
        self.assertGreaterEqual(len(result["core-chain"]), 60)

 