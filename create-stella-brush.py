import os
import sys
import argparse
from fractions import Fraction
from collections import deque
from hashids import Hashids
import json
import re
import glob
from random import sample, choice
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList

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

def getYSign(idx):
    return 1 if idx % 2 is 0 else -1

def segmentToSvg(segment, width):
    prefix = segment.strip()[0]
    values = segment.strip()[1:].strip().split(" ")
    length = len(values)
    fvalues = " ".join(["{:.3f}".format(getYSign(i)*float(Fraction(values[i])*width)) for i in range(length)])
    return prefix + " " + fvalues

def brushToSvg(brush, width):
    segments =  brush.replace("[","").replace("]", "").strip().split(",")   
    svgPath = " ".join([ segmentToSvg(segment, width) for segment in segments])
    return "{} Z".format(svgPath)


def getFilename(filename):
    return os.path.basename(filename)

def getIdFromFilename(filename):
    filename = getFilename(filename)
    id = filename.replace('eval-','').replace('.svg','')
    return int(id)

def asTagInfo(line):
    if not "\t" in line:
        return { "tags": []}
    filename, tagCSV =  line.split("\t")
    return {"id": getIdFromFilename(filename), "tags": tagCSV }

def extractIdWithTags():
    stream = os.popen("tag -l {}/eval-*".format(evalDir))
    lines = stream.readlines()
    tagInfoLines = [asTagInfo(line.strip()) for line in lines ]
    withTags = { tagInfo["id"]: tagInfo["tags"] for tagInfo in  tagInfoLines if len(tagInfo["tags"])>0 }
    return withTags

class Experimenting:
    def __init__(self, name, templateName):
        self.name = name
        self.templateName = templateName
        self.template = ""
        self.content = {}

    def loadTemplate(self):
        with open('{}/{}.svg'.format(evalDir, self.templateName)) as file:  
            self.template = file.read()

    def load(self):
        self.loadTemplate()
        with open('{}/{}.json'.format(evalDir, self.name), 'r') as jsonfile:
            self.content = json.load(jsonfile)
            self.pool = self.content["mutations"]["pool"]
            self.fractionList= FractionList.from_string(self.pool["fractions"])
            self.init = self.content["mutations"]["init"]
            self.variables = self.content["mutations"]["variables"]
            return self.content   
    
    def saveSpecimenSvg(self, name, brushData):
        with open('{}/{}.svg'.format(evalDir, name), 'w') as file:  
            specimenContent = self.template.replace('BRUSH_DATA', brushData)
            file.write(specimenContent)
    
    def deleteSpecimenSvg(self):
        oldSvgFiles = glob.glob('{}/eval-*.svg'.format(evalDir))
        for filePath in oldSvgFiles:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)


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
        stake = V2dList.from_dalmatian_string(choice(self.pool["stakes"]).split(","))
        iterations = self.init["iterations"]
        fxWeight = FractionList.from_string(self.pool["fx-weights"]).choice()
        deltas = self.createPoints(len(stake))
        tweaks = self.createTweaks(len(stake))
        points = addWeightedPoints(stake, deltas, fxWeight)
        rules = [ {"s": i, "r":self.createRule() } for i in self.variables]
        start = self.createRule()
        chain = applyRulesToChain(rules, start, iterations)
        brush = toBrush(chain, points, fxWeight, tweaks)
        brushSvg = brushToSvg(brush, BRUSH_WIDTH)
        summary = "Brush based on a stake of {} points, a weight of {} and the following rules {} starting with {}".format(len(stake), fxWeight, ", ".join([r["s"] + "->" + r["r"] for r in rules]), start)
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
                "brush-svg": brushSvg,
                "summary": summary,
                "tags": ""
        }
    def applyTags(self):
        specimens = self.content['specimens']
        idWithTags = extractIdWithTags()
        for specimen in specimens:
            specimenId = specimen["id"]
            if specimenId in idWithTags:
                specimen["tags"] = idWithTags[specimenId]
        bestspecimens = [specimen for specimen in specimens if len(specimen["tags"])> 0 ]
        self.content['specimens'] = bestspecimens
            
    def createNewPopulation(self):
        population = self.init["population"]
        newspecimens = [ self.createSpecimen() for _ in range(population) ]
        self.content['specimens'] = self.content['specimens'] + newspecimens
 
    def start(self):
        self.applyTags()
        self.createNewPopulation()

    def saveSvg(self):
        self.deleteSpecimenSvg()
        specimens = self.content['specimens']
        for specimen in specimens:
            if len(specimen["tags"])>0:
                continue
            brushSvg = specimen["brush-svg"]
            filename = "eval-{}".format(specimen["id"])
            self.saveSpecimenSvg(filename, brushSvg)
            print(specimen["summary"])
    
    def saveEverything(self):
        self.saveSvg()
        self.save()

experimenting = Experimenting(args.file, args.template)
experimenting.load()
experimenting.start()
experimenting.saveEverything()

