import os
import sys
import argparse
from fractions import Fraction
from hashids import Hashids
import json
import glob
from datetime import date
from random import sample, choice, randint
from typing import List, Tuple, Dict, Set
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from breeding import ProductionGame
from experimentio import ExperimentFS, TypicalDir
from tortuga import TortugaConfig, TortugaProducer
from dalmatianmedia import DlmtView, DlmtTagDescription, DlmtBrush, DlmtBrushstroke, DlmtCoordinateSystem, DlmtBrushCoordinateSystem, DlmtHeaders, DalmatianMedia, SvgRenderingConfig

today = date.today()

xpfs = ExperimentFS("stencil", "stencils")
xpfs.load()

parser = argparse.ArgumentParser(description = 'Create a tortuga illustration')
parser.add_argument("-f", "--file", help="the file containing the experiments.", required = True)
parser.add_argument("-b", "--brushes", help="the collection of brushes", required = True)
parser.add_argument("-p", "--publish", help="publish the preserved stencils", default = "No")

args = parser.parse_args()

class XpInitConf:
    def __init__(self, content):
        self.population: int = content["population"]
        self.angles: int = content["angles"]
        self.magnitudes:int = content["magnitudes"]
        self.brushids: List[str] = content["brushids"]
        self.brushes: List[str] = content["brushes"]
        self.xy: V2d = V2d.from_string(content["xy"])
        self.magnitude_page_ratio: Fraction = Fraction(content["magnitude-page-ratio"]) # 1/100
        self.brush_page_ratio: Fraction = Fraction(content["brush-page-ratio"]) # 1/100 better to keep consistent across stencils
        self.scale_magnitude_ratio: Fraction = Fraction(content["scale-magnitude-ratio"]) # 1
        self.brushstoke_angle_offset: Fraction = Fraction(content["brushstoke-angle-offset"]) # 0

class XpPoolConf:
    def __init__(self, content):
        self.angles: FractionList = FractionList.from_string(content["angles"])
        self.magnitudes: FractionList = FractionList.from_string(content["magnitudes"])
        self.rules: List[str] = content["rules"]


class Experimenting:
    def __init__(self, name):
        self.name = name
        self.content = {}

    def load(self):
        with open('{}/{}.json'.format(xpfs.get_directory(TypicalDir.EVALUATION), self.name), 'r') as jsonfile:
            self.content = json.load(jsonfile)
            self.pool = XpPoolConf(self.content["mutations"]["pool"])
            self.init = XpInitConf(self.content["mutations"]["init"])
            return self.content   
        
    def deleteSpecimenSvg(self):
        oldSvgFiles = glob.glob('{}/eval-*.svg'.format(xpfs.get_directory(TypicalDir.EVALUATION)))
        for filePath in oldSvgFiles:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)


    def save(self):
        with open('{}/{}.json'.format(xpfs.get_directory(TypicalDir.EVALUATION), self.name), 'w') as outfile:
                json.dump(self.content, outfile, indent=2)
    
    def incId(self):
        counter = self.content["general"]["counter"]
        counter = counter + 1
        self.content["general"]["counter"] = counter
        return counter
    
    def createSpecimen(self):
        # Create L-System
        product = ProductionGame(chainlength = randint(30, 700))
        product.set_constants("ABLPZ-<>[]").set_vars("IJK")
        product.init_with_random_rules(levels = 4, keyrules = self.pool.rules)
        product.produce()
        product_obj = product.to_obj()
        
        # Convert chain to brushstokes
        tortugaconfig = TortugaConfig().set_magnitude_page_ratio(self.init.magnitude_page_ratio)
        tortugaconfig.set_scale_magnitude_ratio_string(self.init.scale_magnitude_ratio)
        tortugaconfig.set_brushstoke_angle_offset(self.init.brushstoke_angle_offset)
        tortugaconfig.set_xy(self.init.xy)
        angles = self.pool.angles.sample_as_string(self.init.angles)
        magnitudes = self.pool.magnitudes.sample_as_string(self.init.magnitudes)
        tortugaconfig.set_angles_string(angles)
        tortugaconfig.set_magnitudes_string(magnitudes)
        tortugaconfig.set_brush_ids(self.init.brushids)
        tortugaconfig.set_chain(product.chain)
        brushstokes = TortugaProducer(tortugaconfig).produce()
        
        # Create stencil aka DalmatianMedia
        stencil = DalmatianMedia(DlmtHeaders().set_brush_page_ratio(self.init.brush_page_ratio))
        stencil.add_view_string("view i:1 lang en xy 0 0 width 1 height 1 flags o tags all but [ ] -> everything")
        stencil.add_tag_description_string("tag i:1 lang en same-as [] -> default tag")
        for brush in self.init.brushes:
            stencil.add_brush_string(brush)
        stencil.set_brushstrokes(brushstokes)
        allbr = stencil.page_brushstroke_list_for_view_string("view i:1 lang en xy 0 0 width 1 height 1 flags o tags all but [ ] -> everything")
        fitbr = stencil.page_brushstroke_list_for_view_string("view i:1 lang en xy 0 0 width 1 height 1 flags O tags all but [ ] -> everything")
        fitness = Fraction(len(fitbr), len(allbr))
        ruleInfo = ", ".join([r["s"] + "->" + r["r"] for r in product_obj["rules"]])
        summary = "Stencil based on {} angles, {} magnitudes and on the rules {} starting with {} resulting in {} brushstokes with a fitness of {}".format(len(angles), len(magnitudes), ruleInfo , product_obj["start"], len(brushstokes), fitness)
        return {    
                "id": self.incId(),  
                "product": product_obj,
                "angles": angles,
                "magnitudes": magnitudes,
                "stencil": stencil.to_obj(),
                "summary": summary,
                "tags": ""
        }
    
    def applyTags(self):
        specimens = self.content['specimens']
        idWithTags = xpfs.search_eval_file_id_tags(".svg")
        for specimen in specimens:
            specimenId = specimen["id"]
            if not specimenId in idWithTags:
                continue
            filetags = idWithTags[specimenId]
            if len(filetags.tags) == 0:
                continue
            specimen["tags"] = " ".join(list(filetags.tags))
            print('Saved', specimen["summary"])
        bestspecimens = [specimen for specimen in specimens if len(specimen["tags"])> 0 ]
        if "yes" in args.publish.lower():
            bestspecimens = [xpfs.ensure_publishing_id(specimen) for specimen in self.content['specimens'] if "preserve" in specimen["tags"] ]
        print("Total saved {}".format(len(bestspecimens)))
        self.content['specimens'] = bestspecimens
            
    def createNewPopulation(self):
        population = self.init.population
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
            stencil = DalmatianMedia.from_obj(specimen["stencil"])
            filename = "{}/eval-{}.svg".format(xpfs.get_directory(TypicalDir.EVALUATION), specimen["id"])
            stencil.to_xml_svg_file(stencil.create_page_pixel_coordinate("i:1", 100), filename)
            print("New: {} : {}".format(specimen["id"], specimen["summary"]))
    
    def saveEverything(self):
        self.saveSvg()
        self.save()

    def publish(self):
        print("Publishing to {}".format(xpfs.get_directory(TypicalDir.PUBLISHING)))

experimenting = Experimenting(args.file)
experimenting.load()
experimenting.start()
experimenting.saveEverything()
