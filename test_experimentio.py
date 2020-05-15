import unittest
from experimentio import TagInfo

class TestTagInfo(unittest.TestCase):

    def test_from_shell_string(self):
        self.assertEqual(TagInfo.from_shell_string("eval-2.png\tblue,yellow", ".png"), TagInfo(2, set(["blue", "yellow"])))
        self.assertEqual(TagInfo.from_shell_string("eval-07.png\tblue , yellow ", ".png"), TagInfo(7, set(["blue", "yellow"])))
        self.assertEqual(TagInfo.from_shell_string("eval-07.png\tblue", ".png"), TagInfo(7, set(["blue"])))
        self.assertEqual(TagInfo.from_shell_string("eval-07.png\t blue ", ".png"), TagInfo(7, set(["blue"])))
        self.assertEqual(TagInfo.from_shell_string(" eval-07.png\t", ".png"), TagInfo(7, set([])))
        self.assertEqual(TagInfo.from_shell_string(" eval-07.png \t ", ".png"), TagInfo(7, set([])))

    def test_from_shell_string_list(self):
        tagInfos = TagInfo.from_shell_string_list(["eval-1.png\t", "eval-2.png\tblue,yellow ","eval-3.png\tred"], ".png")
        self.assertEqual(len(tagInfos), 3)
        self.assertEqual(tagInfos[0], TagInfo(1, set([])))
        self.assertEqual(tagInfos[1], TagInfo(2, set(["blue", "yellow"])))
