import os
import sys
import argparse
from fractions import Fraction
from hashids import Hashids
import json
import glob
from datetime import date
from time import sleep, time
from random import sample, choice, randint
from typing import List, Tuple, Dict, Set
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from breeding import ProductionGame
from experimentio import ExperimentFS, TypicalDir
from tortuga import TortugaConfig, TortugaProducer, TortugaRuleMaker
from dalmatianmedia import DlmtView, DlmtTagDescription, DlmtBrush, DlmtBrushstroke, DlmtCoordinateSystem, DlmtBrushCoordinateSystem, DlmtHeaders, DalmatianMedia, SvgRenderingConfig

today = date.today()
started = time()

xpfs = ExperimentFS("stencil", "stencils")
xpfs.load()

parser = argparse.ArgumentParser(description = 'Create a tortuga illustration')
parser.add_argument("-f", "--file", help="the file containing the experiments.", required = True)
parser.add_argument("-b", "--brushes", help="the collection of brushes", required = True)
parser.add_argument("-p", "--publish", help="publish the preserved stencils", default = "No")
parser.add_argument("-c", "--crossover", help="publish the preserved stencils", default = "No")

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
        self.vars: str = content["vars"] # IJ
        self.supported_targets: str = content["supported-targets"]
        self.actions_ranges: str = content["actions-ranges"]
        self.max_chain_length: int = content["max-chain-length"]
        self.specimen_attempts: int = content["specimen-attempts"]
        self.min_median_range: V2d = V2d.from_string(content["min-median-range"])

class XpPoolConf:
    def __init__(self, content):
        self.angles: FractionList = FractionList.from_string(content["angles"])
        self.magnitudes: FractionList = FractionList.from_string(content["magnitudes"])
        self.rules: List[str] = content["rules"]

def crossover_fractions(fractions1: str, fractions2: str)->str:
    fl1 = FractionList.from_string(fractions1)
    fl2 = FractionList.from_string(fractions2)
    cut1 = len(fl1) // 2
    cut2 = len(fl2) // 2
    return str(FractionList(fl1.values[0:cut1] + fl2.values[cut2:]))

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
        product = ProductionGame(chainlength = randint(100, self.init.max_chain_length))
        product.set_constants("ABLPZ-<>[]").set_vars(self.init.vars)
        ruleMaker = TortugaRuleMaker().set_vars(self.init.vars)
        ruleMaker.set_supported_targets(self.init.supported_targets)
        ruleMaker.set_actions_ranges(self.init.actions_ranges)
        product.set_start_and_rules(ruleMaker.make())
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
        bstats = V2dList([bs.xy for bs in brushstokes])
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
        correlation = bstats.get_correlation()
        medianpoint = bstats.get_median_range(8)
        if correlation > 0.9 or correlation < -0.9:
            print("C", end="")
            return None
        if float(fitness) < 0.8:
            print("F", end="")
            return None
        if medianpoint.x < self.init.min_median_range.x:
            print("X", end="")
            return None
        if medianpoint.y < self.init.min_median_range.y:
            print("Y", end="")
            return None
        summary = "Stencil based on angles [ {} ], magnitudes [ {} ] and the rules {} starting with {} resulting in {} brushstokes with a fitness of {:.2%}, correlation of {} and a median range of {}".format(angles, magnitudes, ruleInfo , product_obj["start"], len(brushstokes), float(fitness), correlation, medianpoint.to_float_string())
        return {    
                "id": self.incId(),  
                "product": product_obj,
                "angles": angles,
                "magnitudes": magnitudes,
                "stencil": stencil.to_obj(),
                "summary": summary,
                "tags": ""
        }

    def crossover_specimens(self, specimen1, specimen2):
        # Create L-System
        product = ProductionGame.from_crossover(specimen1["product"], specimen2["product"])
        product.produce()
        product_obj = product.to_obj()
        
        # Convert chain to brushstokes
        tortugaconfig = TortugaConfig().set_magnitude_page_ratio(self.init.magnitude_page_ratio)
        tortugaconfig.set_scale_magnitude_ratio_string(self.init.scale_magnitude_ratio)
        tortugaconfig.set_brushstoke_angle_offset(self.init.brushstoke_angle_offset)
        tortugaconfig.set_xy(self.init.xy)
        angles = crossover_fractions(specimen1["angles"], specimen2["angles"])
        magnitudes = crossover_fractions(specimen1["magnitudes"], specimen2["magnitudes"])
        tortugaconfig.set_angles_string(angles)
        tortugaconfig.set_magnitudes_string(magnitudes)
        tortugaconfig.set_brush_ids(self.init.brushids)
        tortugaconfig.set_chain(product.chain)
        brushstokes = TortugaProducer(tortugaconfig).produce()
        bstats = V2dList([bs.xy for bs in brushstokes])
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
        correlation = bstats.get_correlation()
        medianpoint = bstats.get_median_range(8)
        if correlation > 0.9 or correlation < -0.9:
            print("C", end="")
            return None
        if float(fitness) < 0.8:
            print("F", end="")
            return None
        if medianpoint.x < self.init.min_median_range.x:
            print("X", end="")
            return None
        if medianpoint.y < self.init.min_median_range.y:
            print("Y", end="")
            return None
        summary = "Stencil based on angles [ {} ], magnitudes [ {} ] and the rules {} starting with {} resulting in {} brushstokes with a fitness of {:.2%}, correlation of {} and a median range of {}".format(angles, magnitudes, ruleInfo , product_obj["start"], len(brushstokes), float(fitness), correlation, medianpoint.to_float_string())
        return {    
                "id": self.incId(),  
                "product": product_obj,
                "angles": angles,
                "magnitudes": magnitudes,
                "stencil": stencil.to_obj(),
                "summary": summary,
                "tags": ""
        }

    def createBetterSpecimen(self, attempts: int):
        specimen = self.createSpecimen()
        for _ in range(attempts):
            specimen = self.createSpecimen()
            print(".", end="", flush=True)
            sleep(0.2) # otherwise overheating
            if specimen is None:
                continue
            print("*", end="")
            break
        return specimen 
    
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
            
    def create_new_population(self):
        population = self.init.population
        newspecimens = [ self.createBetterSpecimen(self.init.specimen_attempts) for _ in range(population) ]
        validspecimens = [s for s in newspecimens if s is not None]
        self.content['specimens'] = self.content['specimens'] + validspecimens

    def _next_batch_crossover(self, size: int, initial: List[Tuple] = []):
        if "crossover-couples" not in self.content["general"]:
            self.content["general"]["crossover-couples"] = initial
        remaining_couples = self.content["general"]["crossover-couples"]
        selected = []
        if len(remaining_couples) <= size:
            selected = remaining_couples
            self.content["general"]["crossover-couples"] = []
        else:
            selected = remaining_couples[0:size]
            self.content["general"]["crossover-couples"] = remaining_couples[size:]
        return selected

    def _identify_crossover_couples(self)->List[Tuple]:
        ids = [ specimen["id"] for specimen in self.content['specimens'] if "breed" in specimen["tags"]]
        couples = list(set([(i, j) for i in ids for j in ids]))
        return couples

    def _find_specimen_by_id(self, specimen_id: int):
        specimens = [ specimen for specimen in self.content['specimens'] if specimen["id"] == specimen_id]
        return specimens[0] if len(specimens) == 1 else None

    def crossover_population(self):
        all_couples = self._identify_crossover_couples()
        selected_couples = self._next_batch_crossover(self.init.population, all_couples)
        print("Crossover couples left: {}".format(len(self.content["general"]["crossover-couples"])))
        newspecimens = [self.crossover_specimens(self._find_specimen_by_id(couple[0]), self._find_specimen_by_id(couple[1])) for couple in selected_couples]
        validspecimens = [s for s in newspecimens if s is not None]
        self.content['specimens'] = self.content['specimens'] + validspecimens
    
    def start(self):
        self.applyTags()
        if "yes" in args.crossover.lower():
            self.crossover_population()
        else:
            self.create_new_population()

    def saveSvg(self):
        started_svg = time()
        self.deleteSpecimenSvg()
        specimens = self.content['specimens']
        svg_count = 1
        for specimen in specimens:
            if len(specimen["tags"])>0:
                continue
            svg_count = svg_count + 1
            stencil = DalmatianMedia.from_obj(specimen["stencil"])
            filename = "{}/eval-{}.svg".format(xpfs.get_directory(TypicalDir.EVALUATION), specimen["id"])
            stencil.to_xml_svg_file(stencil.create_page_pixel_coordinate("i:1", 100), filename)
            print("New: {} : {}".format(specimen["id"], specimen["summary"]))
        finished_svg = time()
        print("Saving to svg took {} seconds thus {} second per specimen".format(finished_svg-started_svg, (finished_svg-started_svg)/svg_count))
    
    def saveEverything(self):
        self.saveSvg()
        self.save()

    def publish(self):
        print("Publishing to {}".format(xpfs.get_directory(TypicalDir.PUBLISHING)))

experimenting = Experimenting(args.file)
experimenting.load()
experimenting.start()
experimenting.saveEverything()
os.system('say Ready')
finished = time()
print("Took {} seconds thus {} second per specimen".format(finished-started, (finished-started)/experimenting.init.population))