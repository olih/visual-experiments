from typing import List, Tuple, Dict, Set
import json
import glob
import os

def strip_string_array(rawlines: str)->List[str]:
    return [line.strip() for line in rawlines.split(",") if line.strip() != ""]

def join_set(values: Set[str])->str:
    return ",".join(list(values))

def to_dlmt_array(items: Set[str], sep=",")->str:
    return "[ {} ]".format(sep.join(list(items)))

class DlmtCollectionItem:
    def __init__(self, name: str, keywords: Set[str]):
        self.name = name
        self.keywords = keywords
   
    def to_string(self):
        return "name {} keywords {}".format(self.name, to_dlmt_array(self.keywords))

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        thisone = (self.name, self.keywords)
        otherone = (other.name, other.keywords)
        return thisone == otherone

    def clone(self):
        return DlmtCollectionItem(self.name, self.keywords)

    def set_keywords(self, keywords: Set[str]):
        self.keywords = keywords.copy()
        return self

    def has_keywords(self):
        return len(self.keywords) > 0

    def has_keyword(self, keyword: str)->bool:
        return keyword in self.keywords

    def match_keywords(self, keywords: Set[str]):
        return keywords.issubset(self.keywords)

    @classmethod
    def from_obj(cls, content):
        keywords = strip_string_array(content["keywords"])
        return cls(content["name"], set(keywords))

    def to_obj(self):
        return { "name": self.name, "keywords": join_set(self.keywords)}

    @classmethod
    def from_shell_string(cls, line: str):
        filename, tagCSV =  line.split("\t")
        name, _ = os.path.basename(filename).split(".", 1)
        keywords = set(strip_string_array(tagCSV))
        return cls(name, keywords)


noItem = DlmtCollectionItem("", [])

class DlmtCollection:
    def __init__(self):
        self.items = []
        self.items_dict = {}
    
    def to_string(self):
        return ";".join(sorted([item.to_string() for item in self.items]))

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.to_string() == other.to_string()
    
    def length(self):
        return len(self.items)
    
    def __len__(self):
        return self.length()

    def __add__(self, b):
        newitems = self.items + b.items
        return DlmtCollection().set_items(newitems)

    def clone(self):
        return DlmtCollection().set_items(self.items)

    def add_item(self, item: DlmtCollectionItem):
        self.items.append(item)
        self.items_dict[item.name] = item
        return self

    def set_items(self, items: List[DlmtCollectionItem]):
        self.items = [i.clone() for i in items]
        self.items_dict = {i.name:i for i in self.items}
        return self

    def get_item_by_name(self, name: str)->DlmtCollectionItem:
        return self.items_dict.get(name, noItem.clone())

    def remove_item_by_name(self, name: str):
        if name in self.items_dict:
            del self.items_dict[name]
        self.items = list(filter(lambda i: i.name != name, self.items))
        return self

    def set_item(self, item: DlmtCollectionItem):
        self.remove_item_by_name(item.name)
        self.add_item(item.clone())
        return self

    def set_keywords(self, name: str,  keywords: Set[str]):
       return self.set_item(DlmtCollectionItem(name, keywords))

    def add_keywords(self, name: str, addkeywords: Set[str]):
        keywords = self.get_item_by_name(name).keywords
        self.set_keywords(name, keywords.union(addkeywords))
        return self

    def remove_keywords(self, name: str, rmkeywords: Set[str]):
        keywords = self.get_item_by_name(name).keywords.copy()
        for kw in rmkeywords:
            if kw in keywords:
                keywords.remove(kw)
        self.set_keywords(name, keywords)
        return self

    def add_keywords_for_all(self, addkeywords: Set[str]):
        for item in self.items:
            self.add_keywords(item.name, addkeywords)
        return self

    def remove_keywords_for_all(self, rmkeywords: Set[str]):
        for item in self.items:
            self.remove_keywords(item.name, rmkeywords)
        return self

    def find_matching_items(self, keywords: Set[str])->List[DlmtCollectionItem]:
        return [ item for item in self.items if item.match_keywords(keywords)]

    def find_not_matching_items(self, keywords: Set[str])->List[DlmtCollectionItem]:
        return [ item for item in self.items if not item.match_keywords(keywords)]
    
    def find_matching_names(self, keywords: Set[str])->List[DlmtCollectionItem]:
        return [ item.name for item in self.find_matching_items(keywords)]

    def find_not_matching_names(self, keywords: Set[str])->List[DlmtCollectionItem]:
        return [ item.name for item in self.find_not_matching_items(keywords)]

    def split(self, keywords: Set[str])->Tuple:
        a = self.find_matching_items(keywords)
        b = self.find_not_matching_items(keywords)
        return (DlmtCollection().set_items(a), DlmtCollection().set_items(b))

    @classmethod
    def from_obj(cls, arrcontent):
        items = [DlmtCollectionItem.from_obj(i) for i in arrcontent]
        return cls().set_items(items)

    def to_obj(self):
        return [ i.to_obj() for i in self.items ]
