import unittest
from dalmatiancollection import DlmtCollectionItem, DlmtCollection

alpha = DlmtCollectionItem("alpha", set(["jupiter", "moon"]))
bravo = DlmtCollectionItem("bravo", set([]))
charlie = DlmtCollectionItem("charlie", set(["moon"]))
delta = DlmtCollectionItem("delta", set(["saturn"]))
fox = DlmtCollectionItem("fox", set(["mercury"]))
golf = DlmtCollectionItem("golf", set(["pluto"]))
hotel = DlmtCollectionItem("hotel", set(["pluto"]))

collec_alpha_delta = DlmtCollection().set_items([alpha, bravo, charlie, delta])
collec_fox_golf = DlmtCollection().set_items([fox, golf])
collec_golf_hotel = DlmtCollection().set_items([golf, hotel])
collec_all = DlmtCollection().set_items([alpha, bravo, charlie, delta, golf, hotel])

class TestDlmtCollection(unittest.TestCase):

    def test_add(self):
        newcollect = collec_alpha_delta.clone().add_item(hotel)
        self.assertEqual(newcollect.get_item_by_name("hotel"), hotel)
   
    def test_remove(self):
       actual = collec_alpha_delta.clone().remove_item_by_name("bravo")
       self.assertEqual(len(actual), 3)
       self.assertEqual(actual, DlmtCollection().set_items([alpha, charlie, delta]))
    
    def test_convert(self):
        self.assertEqual(DlmtCollection.from_obj(collec_alpha_delta.to_obj()), collec_alpha_delta)

    def test_add_keywords(self):
        c = collec_alpha_delta.clone()
        self.assertEqual(c.add_keywords("alpha", set(["moon"])).get_item_by_name("alpha").keywords, set(["jupiter", "moon"]))
        self.assertEqual(c.add_keywords("bravo", set(["earth"])).get_item_by_name("bravo").keywords, set(["earth"]))
        self.assertEqual(c.add_keywords("charlie", set(["earth"])).get_item_by_name("charlie").keywords, set(["moon", "earth"]))
 
    def test_remove_keywords(self):
        c = collec_alpha_delta.clone()
        self.assertEqual(c.remove_keywords("alpha", set(["moon"])).get_item_by_name("alpha").keywords, set(["jupiter"]))
        self.assertEqual(c.remove_keywords("bravo", set(["moon"])).get_item_by_name("bravo").keywords, set([]))
        self.assertEqual(c.remove_keywords("charlie", set(["moon"])).get_item_by_name("charlie").keywords, set([]))
        self.assertEqual(c.remove_keywords("delta", set(["moon"])).get_item_by_name("delta").keywords, set(["saturn"]))

    def test_add_keywords_for_all(self):
        newcollect = collec_alpha_delta.clone().add_keywords_for_all(set(["moon"]))
        self.assertTrue(newcollect.get_item_by_name("alpha").has_keyword("moon"))
        self.assertTrue(newcollect.get_item_by_name("bravo").has_keyword("moon"))
        self.assertTrue(newcollect.get_item_by_name("charlie").has_keyword("moon"))

    def test_remove_keywords_for_all(self):
        newcollect = collec_alpha_delta.clone().remove_keywords_for_all(set(["moon"]))
        self.assertFalse(newcollect.get_item_by_name("alpha").has_keyword("moon"))
        self.assertFalse(newcollect.get_item_by_name("bravo").has_keyword("moon"))
        self.assertFalse(newcollect.get_item_by_name("charlie").has_keyword("moon"))
        self.assertFalse(newcollect.get_item_by_name("delta").has_keyword("moon"))

    def test_find_matching(self):
        self.assertEqual(collec_alpha_delta.find_matching_names(set(["moon"])), ["alpha", "charlie"] )
        self.assertEqual(collec_alpha_delta.find_not_matching_names(set(["moon"])), ["bravo", "delta"] )
        self.assertEqual(collec_alpha_delta.find_matching_names(set(["saturn"])), ["delta"])
        self.assertEqual(collec_alpha_delta.find_matching_names(set(["other"])), [] )

    def test_merge_and_split(self):
        self.assertEqual(collec_alpha_delta+collec_golf_hotel, collec_all)
        self.assertEqual(collec_all.split(set(["pluto"])), (collec_golf_hotel, collec_alpha_delta))