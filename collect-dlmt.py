import os
import sys
import argparse
import json
from glob import glob
from typing import List, Tuple, Dict, Set

parser = argparse.ArgumentParser(description = 'Organize dalmatian images in collections')
parser.add_argument("-a", "--action", help="the action (replace, merge, del, list)", required = True)
parser.add_argument("-c", "--collection", help="the file containing the collection", default= None)
parser.add_argument("-m", "--mediadir", help="the directory containing the media files", default= None)
parser.add_argument("-s", "--search", help="the search criteria for the media files", default= "*.dlmt")
parser.add_argument("-k", "--keywords", help="the keywords to process", default= "")
args = parser.parse_args()