import os
import sys
import argparse
from fractions import Fraction
from collections import deque
from hashids import Hashids
import json
import re
from random import sample, choice

localDir = os.environ['OLI_LOCAL_DIR']
BRUSH_WIDTH=34

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

def loadConfAsJson():
    with open('{}/brush/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

evalDir = jsonConf["brushes"]["evaluation-directory"]

brushesHashids = Hashids(salt=jsonConf["brushes"]["salt"], min_length=jsonConf["brushes"]["id-length"])

parser = argparse.ArgumentParser(description = 'Create brushes')
parser.add_argument("-f", "--file", help="the file containing the experiments.", required = True)
parser.add_argument("-t", "--template", help="the template for visualizing the brush", default = "template-one")
args = parser.parse_args()

def chooseVariable(variables):
    duos = [i+j for i in variables for j in variables]
    trios = [i+j+k for i in variables for j in variables for k in variables]
    return choice([choice(duos), choice(trios)])

def addPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction(xa)+Fraction(xb)
    y = Fraction(ya)+Fraction(yb)
    return str(x)+ " "+ str(y)

def addPoints (la, lb):
    length = len(la)
    return [addPoint(la[i], lb[i]) for i in range(length)]

def applyRulesToChain(rules, start, iterations):
    chain = start
    for i in range(iterations):
        for rule in rules:
            chain = chain.replace(rule["s"], rule["s"].lower())
        for rule in rules:
            chain = chain.replace(rule["s"].lower(), rule["r"])
    return chain

def toBrush(chain, points):
    firstPoint = "M {},".format(points[0])
    otherPoints = points[1:]
    shapes = ",".join(["l {}".format(pt) for pt in otherPoints])
    brush = "[ " +firstPoint + shapes + " ]"
    return brush

def segmentToSvg(segment, width):
    prefix = segment.strip()[0]
    values = segment.strip()[1:].strip().split(" ")
    fvalues = " ".join(["{:.3f}".format(float(Fraction(value)*width)) for value in values])
    return prefix + " " + fvalues

def brushToSvg(brush, width):
    segments =  brush.replace("[","").replace("]", "").strip().split(",")   
    return " ".join([ segmentToSvg(segment, width) for segment in segments])

class Experimenting:
    def __init__(self, name, templateName):
        self.name = name
        self.templateName = templateName
        self.template = ""
        self.content = {}

    def load(self):
        with open('{}/{}.json'.format(evalDir, self.name), 'r') as jsonfile:
            self.content = json.load(jsonfile)
            self.pool = self.content["mutations"]["pool"]
            self.fractions = self.pool["fractions"].split()
            self.init = self.content["mutations"]["init"]
            self.variables = self.content["mutations"]["variables"]
            return self.content
    
    def loadTemplate(self):
        with open('{}/{}.svg'.format(evalDir, self.templateName)) as file:  
            self.template = file.read()
    
    def saveSpecimenSvg(self, name, brushData):
        with open('{}/{}.svg'.format(evalDir, name), 'w') as file:  
            specimenContent = self.template.replace('BRUSH_DATA', brushData)
            file.write(specimenContent)

    def save(self):
        with open('{}/{}.json'.format(evalDir, self.name), 'w') as outfile:
                json.dump(self.content, outfile, indent=2)
    
    def incId(self):
        counter = self.content["general"]["counter"]
        counter = counter + 1
        self.content["general"]["counter"] = counter
        return counter

    def createPoint(self):
        x = Fraction(choice(self.fractions))*choice([1, -1])
        y = Fraction(choice(self.fractions))*choice([1, -1])
        return str(x)+ " "+ str(y)

    def createPoints(self, count):
        return [self.createPoint() for i in range(count)]

    def createRule(self):
        rv = choice(self.pool["rules"]) + chooseVariable(self.variables)
        vr = chooseVariable(self.variables) + choice(self.pool["rules"])
        return choice([rv, vr])

    def createSpecimen(self):
        stake = choice(self.pool["stakes"]).split(",")
        iterations = self.init["iterations"]
        deltas = self.createPoints(len(stake))
        points = addPoints(stake, deltas)
        rules = [ {"s": i, "r":self.createRule() } for i in self.variables]
        start = self.createRule()
        chain = applyRulesToChain(rules, start, iterations)
        brush = toBrush(chain, points)
        brushSvg = brushToSvg(brush, BRUSH_WIDTH)
        return {    
                "id": self.incId(),  
                "iterations": iterations,
                "stake": stake,
                "deltas": deltas,
                "points": points,
                "rules": rules,
                "start": start,
                "chain": chain,
                "brush": brush,
                "brush-svg": brushSvg
        }
    def start(self):
        population = self.init["population"]
        self.content['specimens'] = [ self.createSpecimen() for _ in range(population) ]

    def saveSvg(self):
        specimens = self.content['specimens']
        for specimen in specimens:
            brushSvg = specimen["brush-svg"]
            filename = "eval-{}".format(specimen["id"])
            self.saveSpecimenSvg(filename, brushSvg)


experimenting = Experimenting(args.file, args.template)
experimenting.load()
experimenting.loadTemplate()
experimenting.start()
experimenting.saveSvg()

