import os
import sys
import argparse
from fractions import Fraction
from hashids import Hashids
import json
from random import sample, choice

import dalmatianhelper

localDir = os.environ['OLI_LOCAL_DIR']

def loadConfAsJson():
    with open('{}/stencil/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

evalDir = jsonConf["stencils"]["evaluation-directory"]

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

def saveStencilAsJson(expDirectory, stencilId, jsonContent):
    with open('{}/{}/{}.json'.format(evalDir, expDirectory, stencilId), 'w') as outfile:
            json.dump(jsonContent, outfile, indent=2)

def loadStencilJson(expDirectory, stencilId):
    with open('{}/{}/{}.json'.format(evalDir, expDirectory, stencilId), 'r') as jsonfile:
        return json.load(jsonfile)

def chooseVariable(variables):
    duos = [i+j for i in variables for j in variables]
    trios = [i+j+k for i in variables for j in variables for k in variables]
    quad = [i+j+k+l for i in variables for j in variables for k in variables for l in variables]
    quint = [i+j+k+l+m for i in variables for j in variables for k in variables for l in variables for m in variables]
    return choice([choice(duos), choice(trios), choice(quad), choice(quint)])

def createRule(mutations):
    rules = mutations["pool"]["rules"]
    variables = mutations["variables"]
    strokes = mutations["pool"]["strokes"]
    rvs = choice(rules) + chooseVariable(variables) + choice(strokes)
    vrs = chooseVariable(variables) + choice(rules) + choice(strokes)
    rsv = choice(rules) + choice(strokes) + chooseVariable(variables)
    return choice([rvs, vrs, rsv])

def createSpecimen(general, mutations, crossovers):
    return {
        "experiment-type" : "tortuga",
        "general": general,
        "mutations": mutations,
        "crossovers": crossovers,
        "code": {
            "brushes": sample(mutations["pool"]["brushes"], mutations["init"]["brushes"]),
            "lengths": sample(mutations["pool"]["lengths"].split(), mutations["init"]["lengths"]),
            "angles": sample(mutations["pool"]["angles"].split(), mutations["init"]["angles"]),
            "iterations": mutations["init"]["iterations"],
            "rules": { i:createRule(mutations) for i in mutations["variables"]},
            "start": createRule(mutations)
        }
    }

def initGeneration(expDirectory):
    initcfg = loadStencilJson(expDirectory, "init")
    general = initcfg["general"]
    mutations = initcfg["mutations"]
    crossovers = initcfg["crossovers"]
    for m in range(mutations["init"]["population"]):
        specimen = createSpecimen(general, mutations, crossovers)
        saveStencilAsJson(expDirectory, createStencilId(), specimen)

initGeneration(args.directory)