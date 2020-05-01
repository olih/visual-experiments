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
from breeding import ProductionGame

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


def actionToSegment(action, ptStart, ptEnd, fxWeight, tweaks) -> VSegment:
    # not fully sure the calculations are what we really expect
    oneThird = ptStart + ((ptEnd-ptStart)*Fraction("1/3")) 
    twoThird = ptStart + ((ptEnd-ptStart)*Fraction("2/3"))
    halfway = ptStart + ((ptEnd-ptStart)*Fraction("1/2"))
    if action is "L":
        return VSegment.from_line_to(ptEnd)
    if action is "T":
        return VSegment.from_fluid_bezier(ptEnd)
    if action is "C":
        startCtlPt = oneThird + (V2d(tweaks[0], tweaks[1])* fxWeight)
        endCtlPt = twoThird + (V2d(tweaks[2], tweaks[3])* fxWeight)
        return VSegment.from_cubic_bezier(ptEnd, startCtlPt, endCtlPt)
    if action is "S":
        ctlPt = halfway + (V2d(tweaks[0], tweaks[1])* fxWeight)
        return VSegment.from_smooth_bezier(ptEnd, ctlPt)
    if action is "Q":
        ctlPt = halfway + (V2d(tweaks[0], tweaks[1])* fxWeight)
        return VSegment.from_quadratic_bezier(ptEnd, ctlPt)
    

def toBrush(corechain, points, fxWeight, tweaks)-> VPath:
    firstPoint = VSegment.from_move_to(points[0])
    otherlength = len(points)-1
    segments = [firstPoint] + [ actionToSegment(corechain[i], points[i], points[i+1], fxWeight, FractionList.from_string(tweaks[i+1])) for i in range(otherlength)]
    return VPath(segments)

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
    
    def createSpecimen(self):
        stake = V2dList.from_dalmatian_string(choice(self.pool["stakes"]), sep=",")
        fxWeight = FractionList.from_string(self.pool["fx-weights"]).choice()
        deltas = V2dList.from_dalmatian_list(self.fractionList.signed_sample_list(len(stake), 2))
        tweaks = self.fractionList.signed_sample_list(len(stake), 5)
        points = stake + (deltas*fxWeight)
        product = ProductionGame(chainlength = len(points) -1)
        product.set_constants("ZMLCQST").set_vars("IJK")
        product.init_with_random_rules(levels = 2, keyrules = self.pool["rules"])
        product.produce()
        product_obj = product.to_obj()
        brush = toBrush(product.core_chain(), points, fxWeight, tweaks)
        summary = "Brush based on a stake of {} points, a weight of {} and the following rules {} starting with {}".format(len(stake), fxWeight, ", ".join([r["s"] + "->" + r["r"] for r in product_obj["rules"]]), product_obj["start"])
        return {    
                "id": self.incId(),  
                "fx-weight": str(fxWeight),
                "stake": stake.to_dalmatian_list(),
                "deltas": deltas.to_dalmatian_list(),
                "tweaks": tweaks,
                "points": points.to_dalmatian_list(),
                "product": product_obj,
                "brush": brush.to_dalmatian_string(),
                "brush-svg": brush.to_svg_string(BRUSH_WIDTH),
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

