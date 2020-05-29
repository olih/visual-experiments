from typing import List, Tuple, Dict, Set
import json
import glob

def strip_string_array(rawlines: str)->List[str]:
    return [line.strip() for line in rawlines.split(",") if line.strip() != ""]

def join_set(values: Set[str])->str:
    return ",".join(list(values))

class DlmtCollectionItem:
    def __init__(self, name: str, keywords: Set[str]):
        self.name = name
        self.keywords = keywords
   
    def to_string(self):
        return "{} keywords {}".format(self.name, self.keywords)

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

    @classmethod
    def from_obj(cls, content):
        keywords = strip_string_array(content["keywords"])
        return cls(content["name"], set(keywords))

    def to_obj(self):
        return { "name": self.name, "keywords": join_set(self.keywords)}

noItem = DlmtCollectionItem("", [])

class DlmtCollection:
    def __init__(self, items: List[DlmtCollectionItem]):
        self.items = [i.clone() for i in items]
        self.items_dict = {i.name:i for i in self.items}

    def __len__(self):
        return len(self.items)

    def __eq__(self, other):
        return self.items == other.items and self.items_dict == other.items_dict

    def clone(self):
        return DlmtCollection(self.items)

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
        keywords = self.get_item_by_name(name).keywords
        self.set_keywords(name, keywords.difference(rmkeywords))
        return self

    @classmethod
    def from_obj(cls, arrcontent):
        items = [DlmtCollectionItem.from_obj(i) for i in arrcontent]
        return cls(items)

    def to_obj(self):
        return [ i.to_obj() for i in self.items ]

