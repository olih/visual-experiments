import os
import sys
import argparse
import json
from glob import glob
from datetime import date
from time import sleep, time
from typing import List, Tuple, Dict, Set
from dalmatianmedia import DlmtView, DalmatianMedia, SvgRenderingConfig

today = date.today()
started = time()

parser = argparse.ArgumentParser(description = 'Convert a Dalmatian Mask Tape media')
parser.add_argument("-i", "--indirectory", help="Directory containing the Dalmatian Mask Tape media files", required = True)
parser.add_argument("-o", "--outdirectory", help="Output directory", required = True)
parser.add_argument("-f", "--format", help="Image format (svg, png)", default = "svg")
parser.add_argument("-p", "--prefix", help="Prefix for the generated media files", default = "")
parser.add_argument("-W", "--width", help="The width of generated bitmap in pixels.", required = True)
parser.add_argument("-v", "--view", help="The view to export (default, cropped, i:0...)", default = "default")
parser.add_argument("-b", "--background", help="Background color", default = "white")
args = parser.parse_args()

dlmtfiles = glob("{}/*.dlmt".format(args.indirectory))

default_view = DlmtView.from_string("view i:1 lang en xy 0 0 width 1 height 1 flags o tags all but [  ] -> everything")

def read_dlmt_file(filename: str)->DalmatianMedia:
    with open(filename, 'r') as dlmtfile:
        return DalmatianMedia.from_string(dlmtfile.read())

def write_png(filename: str, color: str):
    os.popen("inkscape --export-type=png --export-background '{}' {}".format(color, filename))

def write_media(media: DalmatianMedia):
    filename = "{}/{}{}.svg".format(args.outdirectory,args.prefix, media.headers.get_text("name", "en"))
    if args.view == "default":
        media.to_xml_svg_file(media.create_page_pixel_coordinate_with_view(int(args.width), default_view), filename)
    elif args.view == "cropped":
        rect = media.get_brushstokes_points().get_containing_rect()
        cropped_view = DlmtView.from_string("view i:2 lang en xy {} width {} height {} flags o tags all but [  ] -> cropped ".format(rect.xy, rect.width, rect.height))
        media.to_xml_svg_file(media.create_page_pixel_coordinate_with_view(int(args.width), cropped_view), filename)
    else:
        media.to_xml_svg_file(media.create_page_pixel_coordinate(args.view, int(args.width)), filename)
    if "png" in args.format:
        write_png(filename, args.format)

for filename in dlmtfiles:
    media = read_dlmt_file(filename)
    write_media(media)
    print(".", end="", flush=True)

finished = time()
print("Took {} seconds thus {} second per specimen".format(finished-started, (finished-started)/len(dlmtfiles)))