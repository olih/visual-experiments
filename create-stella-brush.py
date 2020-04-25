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

def substractPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction(xa)-Fraction(xb)
    y = Fraction(ya)-Fraction(yb)
    return str(x)+ " "+ str(y)

def multiplyPoint(weight, a):
    xa, ya = a.strip().split(" ")
    x = Fraction(xa)*Fraction(weight)
    y = Fraction(ya)*Fraction(weight)
    return str(x)+ " "+ str(y)

def midPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction("1/2")*(Fraction(xa)+Fraction(xb))
    y = Fraction("1/2")*(Fraction(ya)+Fraction(yb))
    return str(x)+ " "+ str(y)

def oneThirdPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction("2/3")*Fraction(xa)+Fraction("1/3")*Fraction(xb)
    y = Fraction("2/3")*Fraction(ya)+Fraction("1/3")*Fraction(yb)
    return str(x)+ " "+ str(y)

def twoThirdPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction("1/3")*Fraction(xa)+Fraction("2/3")*Fraction(xb)
    y = Fraction("1/3")*Fraction(ya)+Fraction("2/3")*Fraction(yb)
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

def normChain(chain, length):
    usable = [c for c in chain if c in ["L","T", "C", "S", "Q"]]
    newchain =  usable
    while len(newchain)<length:
        newchain = newchain + usable
    return newchain[:length]

def actionToSegment(action, ptStart, ptEnd, fxWeight, tweaks):
    oneThird = oneThirdPoint(ptStart, ptEnd)
    twoThird = twoThirdPoint(ptStart, ptEnd)
    halfway = midPoint(ptStart, ptEnd)
    if action is "L":
        return "l {}".format(ptEnd)
    if action is "T":
        return "t {}".format(ptEnd)
    if action is "C":
        startCtlPt = addPoint(oneThird, multiplyPoint(fxWeight,tweaks[0] + " " +tweaks[1]))
        endCtlPt = addPoint(twoThird, multiplyPoint(fxWeight,tweaks[2] + " " +tweaks[3]))
        return "c {} {} {}".format(startCtlPt, endCtlPt, ptEnd)
    if action is "S":
        ctlPt = addPoint(halfway, multiplyPoint(fxWeight,tweaks[0] + " " +tweaks[1]))
        return "s {} {}".format(ctlPt, ptEnd)
    if action is "Q":
        ctlPt = addPoint(halfway, multiplyPoint(fxWeight,tweaks[0] + " " +tweaks[1]))
        return "q {} {}".format(ctlPt, ptEnd)
    

def toBrush(chain, points, fxWeight, tweaks):
    firstPoint = "M {},".format(points[0])
    otherlength = len(points)-1
    usableChain = normChain(chain, otherlength)
    shapes = ",".join([ actionToSegment(usableChain[i], points[i], points[i+1], fxWeight, tweaks[i+1].split(" ")) for i in range(otherlength)])
    brush = "[ " +firstPoint + shapes + " ]"
    return brush

def segmentToSvg(segment, width):
    prefix = segment.strip()[0]
    values = segment.strip()[1:].strip().split(" ")
    fvalues = " ".join(["{:.3f}".format(float(Fraction(value)*width)) for value in values])
    return prefix + " " + fvalues

def brushToSvg(brush, width):
    segments =  brush.replace("[","").replace("]", "").strip().split(",")   
    svgPath = " ".join([ segmentToSvg(segment, width) for segment in segments])
    return "{} Z".format(svgPath)

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

    def createTweak(self):
        a = Fraction(choice(self.fractions))*choice([1, -1])
        b = Fraction(choice(self.fractions))*choice([1, -1])
        c =  Fraction(choice(self.fractions))*choice([1, -1])
        d =  Fraction(choice(self.fractions))*choice([1, -1])
        e =  Fraction(choice(self.fractions))*choice([1, -1])
        return " ".join([str(a), str(b), str(c), str(d), str(e)])

    def createPoints(self, count):
        return [self.createPoint() for i in range(count)]
    
    def createTweaks(self, count):
        return [self.createTweak() for i in range(count)]

    def createRule(self):
        rv = choice(self.pool["rules"]) + chooseVariable(self.variables)
        vr = chooseVariable(self.variables) + choice(self.pool["rules"])
        return choice([rv, vr])

    def createSpecimen(self):
        stake = choice(self.pool["stakes"]).split(",")
        iterations = self.init["iterations"]
        fxWeight = choice(self.pool["fx-weights"].split(" "))
        deltas = self.createPoints(len(stake))
        tweaks = self.createTweaks(len(stake))
        points = addPoints(stake, deltas)
        rules = [ {"s": i, "r":self.createRule() } for i in self.variables]
        start = self.createRule()
        chain = applyRulesToChain(rules, start, iterations)
        brush = toBrush(chain, points, fxWeight, tweaks)
        brushSvg = brushToSvg(brush, BRUSH_WIDTH)
        return {    
                "id": self.incId(),  
                "iterations": iterations,
                "fx-weight": fxWeight,
                "stake": stake,
                "deltas": deltas,
                "tweaks": tweaks,
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

