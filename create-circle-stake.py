import os
import sys
import argparse
from fractions import Fraction
from math import pi, radians, cos, sin

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

parser = argparse.ArgumentParser(description = 'Create circle stake')
parser.add_argument("-r", "--radius", help="the radius of circle (Fraction) first last inc next", default="1/4 1/8 -1/48 1/1")
parser.add_argument("-a", "--angle", help="the angle of circle (Fraction) last inc next", default="1/1 1/64 1/1")
parser.add_argument("-v", "--view", help="Display mode", default="params stake cartesian")
parser.add_argument("-w", "--width", help="the width in pixel", default="10")
args = parser.parse_args()

radiusFirst, radiusLast, radiusInc, radiusNext = [Fraction(v) for v in args.radius.split(" ")]
angleLast, angleInc, angleNext = [Fraction(v) for v in args.angle.split(" ")]


def cosFract(fract):
    numerator = int(1000*cos(radians(360*fract)))
    return Fraction("{}/1000".format(numerator))

def sinFract(fract):
    numerator = int(1000*sin(radians(360*fract)))
    return Fraction("{}/1000".format(numerator))

def pointToCartesian(point, width):
    x, y = point.split(" ")
    xx = float(Fraction(x)*width)
    yy = float(Fraction(y)*width)
    return "({:.3f},{:.3f})".format(xx,yy)

def createFractions():
    results = []
    currentRadius = radiusFirst
    currentRadiusInc = radiusInc*radiusNext
    currentAngle = Fraction(0)
    currentAngleInc = angleInc*angleNext
    more = True
    while more:
        x = currentRadius*cosFract(currentAngle)
        y = currentRadius*sinFract(currentAngle)
        results.append("{} {}".format(x, y))
        currentRadiusInc =   currentRadiusInc*radiusNext
        currentRadius = currentRadius + currentRadiusInc
        currentAngleInc = currentAngleInc*angleNext
        currentAngle = currentAngle + currentAngleInc
        more = currentRadius >= radiusLast and currentAngle <= angleLast
        if not more and "debug" in args.view:
            print("breaking at currentRadius: {} ie {} and currentAngle {} ie {}".format(currentRadius, float(currentRadius), currentAngle, float(currentAngle)))
    return results

fracts = createFractions()
if "params" in args.view:
    print("angle: {}, radius: {}".format(args.angle, args.radius))

if "stake" in args.view:
    row = ",".join(fracts)
    print('"'+row+'",')

if "cartesian" in args.view:
    print("cartesian:")
    print(" ".join([pointToCartesian(f, int(args.width)) for f in fracts]))
