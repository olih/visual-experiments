import os
import sys
from hashids import Hashids
import json
import glob
from datetime import date
import json
from typing import List, Tuple, Dict, Set
from enum import Enum, auto


class TypicalDir(Enum):
    EVALUATION = auto()
    PUBLISHING = auto()
    BRUSH = auto()

    @classmethod
    def to_string_key(cls, value):
        if value == TypicalDir.EVALUATION:
            return "evaluation-directory"
        elif value == TypicalDir.PUBLISHING:
            return "publishing-directory"
        elif value == TypicalDir.BRUSH:
            return "brush-directory"
        else:
            return "temp-directory"

def delete_from_string(value: str, deletions: List[str])->str:
    newstr = value
    for deletion in deletions:
        newstr = newstr.replace(deletion, '')
    return newstr

def get_id_from_filename(filename, ext: str = ".svg", prefix: str = "eval-")->int:
    id = delete_from_string(os.path.basename(filename), [prefix, ext])
    return int(id)

def strip_string_array(rawlines: str, sep=",")->List[str]:
    return [line.strip() for line in rawlines.split(sep) if line.strip() != ""]

class TagInfo:
    def __init__(self, id: int, tags: Set[str]):
        self.id = id
        self.tags = tags
   
    def to_string(self):
        return "{} tags {}".format(self.id, self.tags)

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.id == other.id and self.tags == other.tags

    @classmethod
    def from_shell_string(cls, line: str, ext: str = ".svg", prefix: str = "eval-"):
        filename, tagCSV =  line.split("\t")
        id = get_id_from_filename(filename, ext, prefix)
        tags = set(strip_string_array(tagCSV))
        return cls(id, tags)

    @classmethod
    def from_shell_string_list(cls, lines: List[str], ext: str = ".svg", prefix: str = "eval-"):
        return [TagInfo.from_shell_string(line, ext, prefix) for line in lines if "\t" in line]
     

class ExperimentFS:
    def __init__(self, name: str, plural_name: str):
        self.local_dir = os.environ['OLI_LOCAL_DIR']
        self.name = name
        self.plural_name = plural_name
    
    def _load_config(self):
        with open('{}/{}/conf.json'.format(self.name, self.local_dir), 'r') as jsonfile:
            self.config = json.load(jsonfile)
            return self

    def get_directory(self, dirtype: TypicalDir)->str:
        return self.config[self.name][TypicalDir.to_string_key(dirtype)]

    def _load_hasher(self):
        self.hashids = Hashids(salt=self.config[self.plural_name]["salt"], min_length=self.config[self.plural_name]["id-length"])
        return self

    def create_publishing_id(self)->str:
        counterFilename = '{}/{}/{}-count.txt'.format(self.local_dir, self.name, self.plural_name)
        with open(counterFilename, 'r') as file:
            data = file.read().replace('\n', '')
            counter = int(data)+1
            with open(counterFilename, 'w') as wfile:
                wfile.write(str(counter))
                return self.hashids.encode(counter)
    
