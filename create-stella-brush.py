import os
import sys
import argparse
from fractions import Fraction
from collections import deque
from hashids import Hashids
import json
import re
import glob
from random import sample, choice, randint
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from breeding import ProductionGame
from datetime import date

today = date.today()

localDir = os.environ['OLI_LOCAL_DIR']
BRUSH_WIDTH=34

brushBaseURL = "https://olih.github.io/brush/"
authorURL = "https://olih.github.io/brush/profile.html"

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

def loadConfAsJson():
    with open('{}/brush/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

evalDir = jsonConf["brushes"]["evaluation-directory"]
publishingDir = jsonConf["brushes"]["publishing-directory"]

brushesHashids = Hashids(salt=jsonConf["brushes"]["salt"], min_length=jsonConf["brushes"]["id-length"])

parser = argparse.ArgumentParser(description = 'Create brushes')
parser.add_argument("-f", "--file", help="the file containing the experiments.", required = True)
parser.add_argument("-t", "--template", help="the template for visualizing the brush", default = "template-one")
parser.add_argument("-p", "--publish", help="publish the preserved brushes", default = "No")
args = parser.parse_args()

def createBrushId():
    counterFilename = '{}/brush/brushes-count.txt'.format(localDir)
    with open(counterFilename, 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open(counterFilename, 'w') as wfile:
            wfile.write(str(counter))
            return brushesHashids.encode(counter)

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
    
def offsetActionToSegment(action, ptStart:V2d, ptEnd:V2d, fxWeight, tweaks: FractionList) -> VSegment:
    offset = (ptEnd - ptStart).rotate(Fraction("1/4"))*Fraction("1/5")*tweaks[4]
    newStart =  ptStart + offset # slightly inconsistent but should impact control points
    newEnd = ptEnd + offset
    return actionToSegment(action, newStart, newEnd, fxWeight, tweaks)

def toBrush(corechain, points, fxWeight, tweaks, spaghetti: bool)-> VPath:
    firstSegment = VSegment.from_move_to(points[0])
    lastSegment = actionToSegment(corechain[-1], points[-1], points[0], fxWeight, FractionList.from_string(tweaks[0]))
    otherlength = len(points)-1
    segments = []
    if spaghetti:
        forwardsegments = [firstSegment] + [ actionToSegment(corechain[i], points[i], points[i+1], fxWeight, FractionList.from_string(tweaks[i+1])) for i in range(otherlength)]
        backwardsegments = [ offsetActionToSegment(corechain[i], points[i], points[i+1], fxWeight, FractionList.from_string(tweaks[i+1])) for i in range(otherlength-1, 0, -1)]
        segments = forwardsegments + backwardsegments
    else:
        segments = [firstSegment] + [ actionToSegment(corechain[i], points[i], points[i+1], fxWeight, FractionList.from_string(tweaks[i+1])) for i in range(otherlength)] + [lastSegment]

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

def messup_stake(stake: V2dList):
    if randint(1, 7) is 1:
        return stake
    newstake = stake.clone()
    if randint(1, 4) is 1:
        newstake = newstake.reverse()
    if randint(1, 10) is 1:
        newstake = newstake.mirror()

    length = len(stake)
    endslice = randint(4, length)
    inc = randint(1, 4)
    newstake = V2dList(newstake[:endslice:inc])
    
    if len(newstake)<5:
        return messup_stake(stake)
    else:
        return newstake

def addHidToSpecimen(specimen):
    if not "hid" in specimen:
        specimen["hid"] = createBrushId()
    return specimen

def publishableSpecimen(specimen):
    hid = specimen["hid"]
    name = "brush-{}".format(hid)
    brush = specimen["brush"]
    summary = specimen["summary"]
    return {
            "content-url json en": "{}{}.json".format(brushBaseURL, name),
            "name": name,
            "@type": "ImageObject",
            "title en": "Brush {}".format(name),
            "description en": summary,
            "author-url html en": authorURL,
            "author en": "Olivier Huin",
            "copyright-year": today.strftime("%Y"),
            "license en": "Attribution 4.0 International",
            "license-url html en": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "attribution-name en" : "Olivier Huin",
            "homepage-url markdown en:": "https://github.com/olih/brush/blob/master/README.md",
            "brush": brush,
            "brush-ratio": "1/1",
            "brush-coordinate-system": "system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2"
    }

def lightPublishableSpecimen(specimen):
    hid = specimen["hid"]
    name = "brush-{}".format(hid)
    brush = specimen["brush"]
    return {
            "content-url json en": "{}{}.json".format(brushBaseURL, name),
            "name": name,
            "title en": "Brush {}".format(name),
            "copyright-year": today.strftime("%Y"),
            "brush": brush,
    }
def savePublishableSpecimen(name, specimenData):
        with open('{}/{}.json'.format(publishingDir, name), 'w') as outfile:  
            json.dump(specimenData, outfile, indent=2)

def publishSpecimens(specimens):
    for specimen in specimens:
        if not "hid" in specimen:
            continue
        publishable = publishableSpecimen(specimen)
        savePublishableSpecimen(publishable["name"], publishable)

def publishCurrentCollection(collname, specimens):
    publishables = [lightPublishableSpecimen(specimen) for specimen in specimens if "hid" in specimen]
    collections = {
            "name": collname,
            "author-url html en": authorURL,
            "author en": "Olivier Huin",
            "license en": "Attribution 4.0 International",
            "license-url html en": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "attribution-name en" : "Olivier Huin",
            "homepage-url markdown en:": "https://github.com/olih/brush/blob/master/README.md",
            "brush-ratio": "1/1",
            "brush-coordinate-system": "system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2",
            "brushes": publishables
    }
    with open('{}/coll-{}.json'.format(publishingDir, collname), 'w') as outfile:  
            json.dump(collections, outfile, indent=2)  
        

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
        stake = messup_stake(V2dList.from_dalmatian_string(choice(self.pool["stakes"]), sep=","))
        spaghetti = randint(1, 2) is 1
        fxWeight = FractionList.from_string(self.pool["fx-weights"]).choice()
        deltas = V2dList.from_dalmatian_list(self.fractionList.signed_sample_list(len(stake), 2))
        tweaks = self.fractionList.signed_sample_list(len(stake), 5)
        points = stake + (deltas*fxWeight)
        product = ProductionGame(chainlength = len(points) -1)
        product.set_constants("ZMLCQST").set_vars("IJK")
        product.init_with_random_rules(levels = 2, keyrules = self.pool["rules"])
        product.produce()
        product_obj = product.to_obj()
        brush = toBrush(product.core_chain(), points, fxWeight, tweaks, spaghetti)
        frequency_info = ", ".join(["{}:{}".format(k,v) for k, v in brush.action_frequency().items()])
        ruleInfo = ", ".join([r["s"] + "->" + r["r"] for r in product_obj["rules"]])
        summary = "Brush based on a stake of {} points, a weight of {} and the following rules {} starting with {} resulting in frequency {}".format(len(stake), fxWeight, ruleInfo , product_obj["start"], frequency_info)
        return {    
                "id": self.incId(),  
                "fx-weight": str(fxWeight),
                "stake": stake.to_dalmatian_list(),
                "spaghetti": spaghetti,
                "deltas": deltas.to_dalmatian_list(),
                "tweaks": tweaks,
                "points": points.to_dalmatian_list(),
                "product": product_obj,
                "brush": brush.to_dalmatian_string(),
                "brush-svg": brush.to_svg_string(BRUSH_WIDTH),
                "brush-cartesian": brush.to_core_cartesian_string(BRUSH_WIDTH),
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
                print('Saved', specimen["summary"])
        bestspecimens = [specimen for specimen in specimens if len(specimen["tags"])> 0 ]
        if "yes" in args.publish.lower():
            bestspecimens = [addHidToSpecimen(specimen) for specimen in self.content['specimens'] if "preserve" in specimen["tags"] ]
        print("Total saved {}".format(len(bestspecimens)))
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
            print('New', specimen["summary"])
    
    def saveEverything(self):
        self.saveSvg()
        self.save()

    def publish(self):
        print("Publishing to {}".format(publishingDir))
        publishSpecimens(self.content['specimens'])
        publishCurrentCollection(self.name, self.content['specimens'])

experimenting = Experimenting(args.file, args.template)
experimenting.load()
experimenting.start()
experimenting.saveEverything()
if "yes" in args.publish.lower():
    experimenting.publish()

