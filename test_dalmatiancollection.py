import unittest
from dalmatiancollection import DlmtCollectionItem, DlmtCollection

alpha = DlmtCollectionItem("alpha", set(["jupiter", "moon"]))
bravo = DlmtCollectionItem("bravo", set([]))
charlie = DlmtCollectionItem("charlie", set(["moon"]))
delta = DlmtCollectionItem("delta", set(["saturn"]))
fox = DlmtCollectionItem("fox", set(["mercury"]))
golf = DlmtCollectionItem("golf", set(["pluto"]))
hotel = DlmtCollectionItem("hotel", set(["pluto"]))

collec_alpha_delta = DlmtCollection([alpha, bravo, charlie, delta])
collec_fox_golf = DlmtCollection([fox, golf])

class TestDlmtCollection(unittest.TestCase):

    def test_add(self):
        newcollect = collec_alpha_delta.clone().add_item(hotel)
        self.assertEqual(newcollect.get_item_by_name("hotel"), hotel)
   
    def test_remove(self):
       actual = collec_alpha_delta.clone().remove_item_by_name("bravo")
       self.assertEqual(len(actual), 3)
       self.assertEqual(actual, DlmtCollection([alpha, charlie, delta]))
    
    def test_convert(self):
        self.assertEqual(DlmtCollection.from_obj(collec_alpha_delta.to_obj()), collec_alpha_delta)

    def test_add_keywords(self):
        newcollect = collec_alpha_delta.clone().add_keywords("charlie", set(["earth"]))
        self.assertEqual(newcollect.get_item_by_name("charlie"), DlmtCollectionItem("charlie", set(["moon", "earth"])))
 
    def test_remove_keywords(self):
        newcollect = collec_alpha_delta.clone().remove_keywords("alpha", set(["moon"]))
        self.assertEqual(newcollect.get_item_by_name("alpha"), DlmtCollectionItem("alpha", set(["jupiter"])))
