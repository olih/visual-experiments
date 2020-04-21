import os
import sys
import argparse
from fractions import Fraction

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

parser = argparse.ArgumentParser(description = 'Create fractions')
parser.add_argument("-m", "--min", help="the minimum value (Fraction)", required = True)
parser.add_argument("-M", "--max", help="the maximum value (Fraction)", required = True)
parser.add_argument("-d", "--denom", help="the denominator max value (Int)", required = True)
args = parser.parse_args()

def createFractions(minFrac, maxFrac, denom):
    values = []
    for d in range(denom):
        for i in range(d):
            frac = Fraction("{}/{}".format(i, d))
            if frac >= minFrac and frac <= maxFrac:
                values.append(frac)
    return values
    
results = list(set(createFractions(Fraction(args.min), Fraction(args.max), int(args.denom))))
line = " ".join([str(result) for result in results])

print("Size: {}".format(len(results)))
print(line)

