import os
import sys
import argparse
from fractions import Fraction
from hashids import Hashids
import json

import dalmatianhelper

localDir = os.environ['OLI_LOCAL_DIR']

def loadConfAsJson():
    with open('{}/stencil/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

evalDir = jsonConf["folders"]["evaluation-directory"]

stencilsHashids = Hashids(salt=jsonConf["stencils"]["salt"], min_length=jsonConf["stencils"]["id-length"])

parser = argparse.ArgumentParser(description = 'Create a dead tree branch')
parser.add_argument("-d", "--directory", help="the directory containing the experiment.", required = True)
args = parser.parse_args()

def createStencilId():
    counterFilename = '{}/stencil/stencils-count.txt'.format(localDir)
    with open(counterFilename, 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open(counterFilename, 'w') as wfile:
            wfile.write(str(counter))
            return stencilsHashids.encode(counter)

def saveDeadBranchAsJson(expDirectory, stencilId, jsonContent):
    with open('{}/stencil/{}/{}.json'.format(evalDir, expDirectory, stencilId), 'w') as outfile:
            json.dump(jsonContent, outfile, indent=2)

def loadFoldersJson(expDirectory, stencilId):
    with open('{}/stencil/{}/{}.json'.format(evalDir, expDirectory, stencilId), 'r') as jsonfile:
        return json.load(jsonfile)
