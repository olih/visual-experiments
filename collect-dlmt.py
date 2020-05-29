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

parser = argparse.ArgumentParser(description = 'Organize dalmatian images in collections')
parser.add_argument("-f", "--file", help="the file containing the experiments.", required = True)
parser.add_argument("-b", "--brushes", help="the collection of brushes", required = False)
parser.add_argument("-p", "--publish", help="publish the preserved stencils", default = "No")
parser.add_argument("-c", "--crossover", help="crossover the breed stencils", default = "No")
parser.add_argument("-m", "--mutation", help="mutate all stencils", default = "No")

args = parser.parse_args()