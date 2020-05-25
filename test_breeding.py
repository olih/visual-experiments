import unittest

from breeding import ProductionGame

class TestProductionGame(unittest.TestCase):

    def test_create(self):
        product = ProductionGame(chainlength = 60)
        product.set_constants("LQC").set_vars("IJK")
        product.init_with_random_rules(levels = 2, keyrules = ["L", "QQ", "C"])
        product.produce()
        result = product.to_obj()
        self.assertEqual(len(result["rules"]), 3)
        self.assertGreaterEqual(len(result["chain"]), len(result["core-chain"]))
        self.assertGreaterEqual(len(result["core-chain"]), 60)

    def test_convert(self):
        product = ProductionGame(chainlength = 60)
        product.set_constants("LQC").set_vars("IJK")
        product.init_with_random_rules(levels = 2, keyrules = ["L", "QQ", "C"])
        product.produce()
        self.assertEqual(ProductionGame.from_obj(product.to_obj()), product)


    def test_breeding(self):
        product1 = ProductionGame(chainlength = 60)
        product1.set_constants("LQC").set_vars("IJK")
        product1.init_with_random_rules(levels = 2, keyrules = ["L", "QQ", "C"])
        product1.produce()

        product2 = ProductionGame(chainlength = 60)
        product2.set_constants("LQC").set_vars("IJK")
        product2.init_with_random_rules(levels = 2, keyrules = ["LL", "Q", "CC"])


 