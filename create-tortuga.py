import os
import sys
import argparse
from fractions import Fraction
from hashids import Hashids
import json
import glob
from datetime import date
from time import sleep, time
from random import sample, choice, randint, shuffle
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
parser.add_argument("-b", "--brushes", help="the collection of brushes", required = False)
parser.add_argument("-p", "--publish", help="publish the preserved stencils", default = "No")
parser.add_argument("-c", "--crossover", help="crossover the breed stencils", default = "No")
parser.add_argument("-m", "--mutation", help="mutate all stencils", default = "No")

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

class BrushDispenser:
    def __init__(self, brushes: List[str]):
        self.brushes = brushes
        self.dispenser = []

    @classmethod
    def from_brush_collection(cls, content):
        brushes = ["ext-id brushes:{} path {}".format(br["name"].strip(), br["brush"]) for br in content["brushes"]]
        return cls(brushes)

    def get_random_brush(self)-> str:
        if len(self.dispenser) == 0:
            self.dispenser = self.brushes.copy()
            shuffle(self.dispenser)
        return self.dispenser.pop()

def crossover_fractions(fractions1: str, fractions2: str)->str:
    fl1 = FractionList.from_string(fractions1)
    fl2 = FractionList.from_string(fractions2)
    cut1 = len(fl1) // 2
    cut2 = len(fl2) // 2
    return str(FractionList(fl1.values[0:cut1] + fl2.values[cut2:]))

def mutate_fraction(fractions1: str, fracpool: FractionList)->str:
    fl1 = FractionList.from_string(fractions1)
    fracts = sorted(fl1.sample(len(fl1)-1)+[fracpool.choice()])
    return str(FractionList(fracts))

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

    def delete_specimen_svg(self):
        oldSvgFiles = glob.glob('{}/eval-*.svg'.format(xpfs.get_directory(TypicalDir.EVALUATION)))
        for filePath in oldSvgFiles:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)


    def save(self):
        with open('{}/{}.json'.format(xpfs.get_directory(TypicalDir.EVALUATION), self.name), 'w') as outfile:
                json.dump(self.content, outfile, indent=2)
    
    def inc_id(self):
        counter = self.content["general"]["counter"]
        counter = counter + 1
        self.content["general"]["counter"] = counter
        return counter
    
    def create_specimen(self):
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
        stencil.add_tag_description_string("tag i:1 lang en same-as [] -> default")
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
        summary = "Stencil manually selected from carefully crafted generations using a Lindenmayer system approach based on angles [ {} ], magnitudes [ {} ] and the rules {} starting with {} resulting in {} brushstokes with a visibility of {:.2%}, correlation of {} and a median range of {}".format(angles, magnitudes, ruleInfo , product_obj["start"], len(brushstokes), float(fitness), correlation, medianpoint.to_float_string())
        return {    
                "id": self.inc_id(),  
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
        stencil.add_tag_description_string("tag i:1 lang en same-as [] -> default")
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
        summary = "Stencil manually selected from carefully crafted generations using a Lindenmayer system approach based on angles [ {} ], magnitudes [ {} ] and the rules {} starting with {} resulting in {} brushstokes with a visibility of {:.2%}, correlation of {} and a median range of {}".format(angles, magnitudes, ruleInfo , product_obj["start"], len(brushstokes), float(fitness), correlation, medianpoint.to_float_string())
        return {    
                "id": self.inc_id(),  
                "product": product_obj,
                "angles": angles,
                "magnitudes": magnitudes,
                "stencil": stencil.to_obj(),
                "summary": summary,
                "tags": ""
        }

    def create_better_specimen(self, attempts: int):
        specimen = self.create_specimen()
        for _ in range(attempts):
            specimen = self.create_specimen()
            print(".", end="", flush=True)
            sleep(0.2) # otherwise overheating
            if specimen is None:
                continue
            print("*", end="")
            break
        return specimen 

    def mutation_specimen(self, specimen):
        # Create L-System
        product = ProductionGame.from_obj(specimen["product"])
        product.produce()
        product_obj = product.to_obj()
        
        # Convert chain to brushstokes
        tortugaconfig = TortugaConfig().set_magnitude_page_ratio(self.init.magnitude_page_ratio)
        tortugaconfig.set_scale_magnitude_ratio_string(self.init.scale_magnitude_ratio)
        tortugaconfig.set_brushstoke_angle_offset(self.init.brushstoke_angle_offset)
        tortugaconfig.set_xy(self.init.xy)
        angles =  mutate_fraction(specimen["angles"], self.pool.angles)
        magnitudes = mutate_fraction(specimen["magnitudes"], self.pool.magnitudes)
        tortugaconfig.set_angles_string(angles)
        tortugaconfig.set_magnitudes_string(magnitudes)
        tortugaconfig.set_brush_ids(self.init.brushids)
        tortugaconfig.set_chain(product.chain)
        brushstokes = TortugaProducer(tortugaconfig).produce()
        bstats = V2dList([bs.xy for bs in brushstokes])
        # Create stencil aka DalmatianMedia
        stencil = DalmatianMedia(DlmtHeaders().set_brush_page_ratio(self.init.brush_page_ratio))
        stencil.add_view_string("view i:1 lang en xy 0 0 width 1 height 1 flags o tags all but [ ] -> everything")
        stencil.add_tag_description_string("tag i:1 lang en same-as [] -> default")
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
        summary = "Stencil manually selected from carefully crafted generations using a Lindenmayer system approach based on angles [ {} ], magnitudes [ {} ] and the rules {} starting with {} resulting in {} brushstokes with a visibility of {:.2%}, correlation of {} and a median range of {}".format(angles, magnitudes, ruleInfo , product_obj["start"], len(brushstokes), float(fitness), correlation, medianpoint.to_float_string())
        return {    
                "id": self.inc_id(),  
                "product": product_obj,
                "angles": angles,
                "magnitudes": magnitudes,
                "stencil": stencil.to_obj(),
                "summary": summary,
                "tags": ""
        }

    def publishable_specimen(self, specimen)->DalmatianMedia:
        name = "stencil-{}".format(specimen["hid"])
        stencil = specimen["stencil"].copy()
        headers = DlmtHeaders()
        headers.set_brush_page_ratio(self.init.brush_page_ratio)
        headers.set_id_urn("olivierhuin/{}/{}".format(self.name, name))
        headers.set_prefixes({"brushes": "https://olih.github.io/brush/", "stencils": "https://olih.github.io/stencil/"})
        headers.set_text("name", "en", name)             
        headers.set_text("title", "en", "Evolved {}".format(name))             
        headers.set_text("license", "en", "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)")
        headers.set_text("attribution-name", "en", "Olivier Huin")
        headers.set_text("brushes-attribution-name", "en", "Olivier Huin")
        headers.set_text("author", "en", "Olivier Huin")
        headers.set_text("description", "en", specimen["summary"])             
        headers.set_url("content-url", "dlmt", "en", "https://olih.github.io/stencil/{}.dlmt".format(name))
        headers.set_url("license-url", "html", "en", "https://creativecommons.org/licenses/by-sa/4.0/legalcode")
        headers.set_url("brushes-license-url", "html", "en", "https://creativecommons.org/licenses/by/4.0/legalcode")
        headers.set_url("author-url", "html", "en", "https://olih.github.io/stencil/profile.html")
        headers.set_url("attribution-url", "html", "en", "https://olih.github.io/stencil/profile.html")
        headers.set_url("brushes-attribution-url", "html", "en", "https://olih.github.io/brush/profile.html")
        headers.set_url("homepage-url", "html", "en", "https://github.com/olih/stencil")
        headers.set_url("repository-url", "html", "en", "https://github.com/olih/stencil")
        headers.set_copyright_year(today.year)
        headers.set_is_family_friendly(True)
        stencil["headers"] = headers.to_string_list()
        media = DalmatianMedia.from_obj(stencil)
        if media.check_references() != []:
            print(media.check_references())
            raise Exception("Invalid format for stencil {}".format(specimen["id"]))
        return media

    def create_better_mutant_specimen(self, refspecimen, attempts: int):
        specimen = self.mutation_specimen(refspecimen)
        for _ in range(attempts):
            specimen = self.mutation_specimen(refspecimen)
            print(".", end="", flush=True)
            sleep(0.4) # otherwise overheating, in addition let's keep it under 2000 mutations
            if specimen is None:
                continue
            print("*", end="")
            break
        return specimen 

    def apply_tags(self):
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
        newspecimens = [ self.create_better_specimen(self.init.specimen_attempts) for _ in range(population) ]
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

    def _specimens_to_dict(self):
        return { specimen["id"]: specimen for specimen in self.content['specimens'] }

    def crossover_population(self):
        all_couples = self._identify_crossover_couples()
        selected_couples = self._next_batch_crossover(self.init.population, all_couples)
        print("Crossover couples left: {}".format(len(self.content["general"]["crossover-couples"])))
        newspecimens = [self.crossover_specimens(self._find_specimen_by_id(couple[0]), self._find_specimen_by_id(couple[1])) for couple in selected_couples]
        validspecimens = [s for s in newspecimens if s is not None]
        self.content['specimens'] = self.content['specimens'] + validspecimens
    
    def _identify_mutation_candidates(self)->List[int]:
        return [ specimen["id"] for specimen in self.content['specimens'] if len(specimen["tags"]) > 0]

    def mutate_population(self):
        by_id = self._specimens_to_dict()
        candids = self._identify_mutation_candidates()
        newspecimens = [ self.create_better_mutant_specimen(by_id[candid], 7) for candid in candids ]
        validspecimens = [s for s in newspecimens if s is not None]
        self.content['specimens'] = self.content['specimens'] + validspecimens

    def _load_brushes_collection(self):
        with open('{}/{}.json'.format(xpfs.get_directory(TypicalDir.BRUSH), args.brushes), 'r') as jsonfile:
            content = json.load(jsonfile)
            dispenser = BrushDispenser.from_brush_collection(content)
            return dispenser

    def mutate_population_with_brushes(self):
        dispenser = self._load_brushes_collection()
        for specimen in self.content['specimens']:
            if "preserve" in specimen["tags"] or len(specimen["tags"]) == 0:
                continue
            specimen["stencil"]["brushes"] = ["brush {} {}".format(brushid, dispenser.get_random_brush()) for brushid in self.init.brushids]
    
    def prepublish(self):
        if not "yes" in args.publish.lower():
            return       
        same_specimens = [specimen for specimen in self.content['specimens'] if not "preserve" in specimen["tags"]]
        preserved_specimens = [xpfs.ensure_publishing_id(specimen) for specimen in self.content['specimens'] if "preserve" in specimen["tags"]]
        self.content['specimens'] = same_specimens + preserved_specimens
            
    def publish(self):
        if not "yes" in args.publish.lower():
            return
        print("Attempting publishing")
        publish_count = 0
        for specimen in self.content['specimens']:
            if not "preserve" in specimen["tags"]:
                continue
            publish_count = publish_count + 1
            stencil = self.publishable_specimen(specimen)
            with open('{}/stencil-{}.dlmt'.format(xpfs.get_directory(TypicalDir.PUBLISHING), specimen["hid"]), 'w') as outfile:
                outfile.write(stencil.to_string())
        print("Published {} stencils to {}".format(publish_count, xpfs.get_directory(TypicalDir.PUBLISHING)))

    def start(self):
        self.apply_tags()
        if "yes" in args.crossover.lower():
            print("Attempting crossover")
            self.crossover_population()
        elif "yes" in args.mutation.lower():
            print("Attempting mutation")
            self.mutate_population()
        elif args.brushes:
            print("Attempting mutating population with brushes")
            self.mutate_population_with_brushes()
        elif "yes" in args.publish.lower():
            self.prepublish()
        else:
            print("Creating new population")
            self.create_new_population()

    def save_svg(self):
        started_svg = time()
        self.delete_specimen_svg()
        specimens = self.content['specimens']
        svg_count = 1
        for specimen in specimens:
            if len(specimen["tags"])>0:
                if not args.brushes:
                    continue
                if args.brushes and "preserve" in specimen["tags"]:
                    continue
            svg_count = svg_count + 1
            stencil = DalmatianMedia.from_obj(specimen["stencil"])
            filename = "{}/eval-{}.svg".format(xpfs.get_directory(TypicalDir.EVALUATION), specimen["id"])
            stencil.to_xml_svg_file(stencil.create_page_pixel_coordinate("i:1", 100), filename)
            print("New: {} : {}".format(specimen["id"], specimen["summary"]))
        finished_svg = time()
        print("Saving to svg took {} seconds thus {} second per specimen".format(finished_svg-started_svg, (finished_svg-started_svg)/svg_count))
    
    def save_everything(self):
        self.save_svg()
        self.save()

experimenting = Experimenting(args.file)
experimenting.load()
experimenting.start()
experimenting.save_everything()
experimenting.publish()
os.system('say Ready')
finished = time()
print("Took {} seconds thus {} second per specimen".format(finished-started, (finished-started)/experimenting.init.population))