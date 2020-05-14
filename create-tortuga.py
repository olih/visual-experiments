import os
import sys
import argparse
from fractions import Fraction
from hashids import Hashids
import json
import glob
from datetime import date
from random import sample, choice, randint
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from breeding import ProductionGame

today = date.today()
BRUSH_WIDTH=34

localDir = os.environ['OLI_LOCAL_DIR']

stencilBaseURL = "https://olih.github.io/stencil/"
authorURL = "https://olih.github.io/stencil/profile.html"


def loadConfAsJson():
    with open('{}/stencil/conf.json'.format(localDir), 'r') as jsonfile:
        return json.load(jsonfile)

jsonConf = loadConfAsJson()

evalDir = jsonConf["stencils"]["evaluation-directory"]
brushDir = jsonConf["stencils"]["brush-directory"]
publishingDir = jsonConf["stencils"]["publishing-directory"]

stencilsHashids = Hashids(salt=jsonConf["stencils"]["salt"], min_length=jsonConf["stencils"]["id-length"])

parser = argparse.ArgumentParser(description = 'Create a tortuga illustration')
parser.add_argument("-f", "--file", help="the file containing the experiments.", required = True)
parser.add_argument("-b", "--brushes", help="the collection of brushes", required = True)
parser.add_argument("-p", "--publish", help="publish the preserved stencils", default = "No")

args = parser.parse_args()

def createStencilId():
    counterFilename = '{}/stencil/stencils-count.txt'.format(localDir)
    with open(counterFilename, 'r') as file:
        data = file.read().replace('\n', '')
        counter = int(data)+1
        with open(counterFilename, 'w') as wfile:
            wfile.write(str(counter))
            return stencilsHashids.encode(counter)

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
        specimen["hid"] = createStencilId()
    return specimen

def publishableSpecimen(specimen):
    hid = specimen["hid"]
    name = "stencil-{}".format(hid)
    stencil = specimen["stencil"]
    summary = specimen["summary"]
    return {
            "content-url json en": "{}{}.json".format(stencilBaseURL, name),
            "name": name,
            "@type": "ImageObject",
            "title en": "Stencil {}".format(name),
            "description en": summary,
            "author-url html en": authorURL,
            "author en": "Olivier Huin",
            "copyright-year": today.strftime("%Y"),
            "license en": "Attribution-ShareAlike 4.0 International",
            "license-url html en": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
            "attribution-name en" : "Olivier Huin",
            "homepage-url markdown en:": "https://github.com/olih/stencil/blob/master/README.md",
            "stencil": stencil,
            "brush-ratio": "1/1",
            "brush-coordinate-system": "system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2"
    }

def lightPublishableSpecimen(specimen):
    hid = specimen["hid"]
    name = "brush-{}".format(hid)
    stencil = specimen["stencil"]
    return {
            "content-url json en": "{}{}.json".format(stencilBaseURL, name),
            "name": name,
            "title en": "Stencil {}".format(name),
            "copyright-year": today.strftime("%Y"),
            "stencil": stencil,
            "brush-ratio": "1/1",
            "brush-coordinate-system": "system cartesian right-dir + up-dir - origin-x 1/2 origin-y 1/2"
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

class Experimenting:
    def __init__(self, name):
        self.name = name
        self.content = {}

    def load(self):
        with open('{}/{}.json'.format(evalDir, self.name), 'r') as jsonfile:
            self.content = json.load(jsonfile)
            self.pool = self.content["mutations"]["pool"]
            self.fractionList= FractionList.from_string(self.pool["fractions"])
            self.init = self.content["mutations"]["init"]
            self.variables = self.content["mutations"]["variables"]
            return self.content   
    
    def saveSpecimenSvg(self, name, specimenData):
        with open('{}/{}.svg'.format(evalDir, name), 'w') as file:  
            file.write(specimenData)
    
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
        product.set_constants("ABLPZ-<>[]").set_vars("IJK")
        product.init_with_random_rules(levels = 2, keyrules = self.pool["rules"])
        product.produce()
        product_obj = product.to_obj()
        brush = toStencil(product.core_chain(), points, fxWeight, tweaks, spaghetti)
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
