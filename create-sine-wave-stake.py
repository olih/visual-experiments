import os
import sys
import argparse
from fractions import Fraction
from math import pi, radians, sin

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

parser = argparse.ArgumentParser(description = 'Create sinusoidal stake')
parser.add_argument("-a", "--amplitude", help="the peak deviation of the function from zero (Fraction) first last inc next", default="1/4 1/8 -1/48 1/1")
parser.add_argument("-p", "--period", help="the period (Fraction) last inc next", default="1/1 1/64 1/1")
parser.add_argument("-v", "--view", help="Display mode", default="params stake cartesian")
parser.add_argument("-w", "--width", help="the width in pixel", default="10")
args = parser.parse_args()

amplitudeFirst, amplitudeLast, amplitudeInc, amplitudeNext = [Fraction(v) for v in args.amplitude.split(" ")]
periodLast, periodInc, periodNext = [Fraction(v) for v in args.period.split(" ")]


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
    currentAmplitude = amplitudeFirst
    currentAmplitudeInc = amplitudeInc*amplitudeNext
    currentPeriod = Fraction(0)
    currentPeriodInc = periodInc*periodNext
    more = True
    while more:
        x = -amplitudeFirst + 2*amplitudeFirst*currentPeriod/periodLast
        y = currentAmplitude*sinFract(currentPeriod)
        results.append("{} {}".format(x, y))
        currentAmplitudeInc =   currentAmplitudeInc*amplitudeNext
        currentAmplitude = currentAmplitude + currentAmplitudeInc
        currentPeriodInc = currentPeriodInc*periodNext
        currentPeriod = currentPeriod + currentPeriodInc
        more = currentAmplitude >= amplitudeLast and currentPeriod <= periodLast
        if not more and "debug" in args.view:
            print("breaking at currentAmplitude: {} ie {} and currentPeriod {} ie {}".format(currentAmplitude, float(currentAmplitude), currentPeriod, float(currentPeriod)))
    return results

fracts = createFractions()
if "params" in args.view:
    print("period: {}, amplitude: {}".format(args.period, args.amplitude))

if "stake" in args.view:
    row = ",".join(fracts)
    print('"'+row+'",')

if "cartesian" in args.view:
    print("cartesian:")
    print(" ".join([pointToCartesian(f, int(args.width)) for f in fracts]))