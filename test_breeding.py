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
        obj1 = {
            "constants": "ABC",
            "variables": "IJ",
            "start": "AIAI",
            "rules": [
                {
                    "s": "I",
                    "r": "BCJJ"
                },
                {
                    "s": "J",
                    "r": "ABII"
                }
            ]

        }
        obj2 = {
            "constants": "AD",
            "variables": "JK",
            "start": "DJJD",
            "rules": [
                {
                    "s": "J",
                    "r": "AJJA"
                },
                {
                    "s": "K",
                    "r": "DKDK"
                }
            ]
        }

        product = ProductionGame.from_crossover(obj1, obj2, 30)
        product.produce()
        expected_rules = [
                {
                    "s": "I",
                    "r": "BCJJ"
                },
                {
                    "s": "J",
                    "r": "ABIA"
                },
                {
                    "s": "K",
                    "r": "DKDK"
                }
            ]
        self.assertEqual(product.to_obj()["constants"], "ABCD")
        self.assertEqual(product.to_obj()["variables"], "IJK")
        self.assertEqual(product.to_obj()["start"], "DIAD")
        self.assertEqual(product.to_obj()["rules"], expected_rules)
        


 