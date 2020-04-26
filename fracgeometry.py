from fractions import Fraction

def toStr(a, b):
    return "{} {}".format(a, b)

class V2d:
    def __init__(self, value:str):
        self.value = value
        x, y = value.strip().split(" ")
        self.x = Fraction(x)
        self.y = Fraction(y)
            
    def __str__(self):
        return toStr(self.x, self.y)
    
    def __repr__(self):
        return toStr(self.x, self.y)

    def __add__(self, b):
        return V2d(toStr(self.x+b.x, self.y+b.y))

    def __sub__(self, b):
        return V2d(toStr(self.x-b.x, self.y-b.y))
    
        
def multiplyPoint(weight, a):
    xa, ya = a.strip().split(" ")
    x = Fraction(xa)*Fraction(weight)
    y = Fraction(ya)*Fraction(weight)
    return str(x)+ " "+ str(y)

def midPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction("1/2")*(Fraction(xa)+Fraction(xb))
    y = Fraction("1/2")*(Fraction(ya)+Fraction(yb))
    return str(x)+ " "+ str(y)

def oneThirdPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction("2/3")*Fraction(xa)+Fraction("1/3")*Fraction(xb)
    y = Fraction("2/3")*Fraction(ya)+Fraction("1/3")*Fraction(yb)
    return str(x)+ " "+ str(y)

def twoThirdPoint(a, b):
    xa, ya = a.strip().split(" ")
    xb, yb = b.strip().split(" ")
    x = Fraction("1/3")*Fraction(xa)+Fraction("2/3")*Fraction(xb)
    y = Fraction("1/3")*Fraction(ya)+Fraction("2/3")*Fraction(yb)
    return str(x)+ " "+ str(y)

def addPoints (la, lb):
    length = len(la)
    return [addPoint(la[i], lb[i]) for i in range(length)]

def addWeightedPoints (la, lb, weight):
    length = len(la)
    return [addPoint(la[i], multiplyPoint(weight, lb[i])) for i in range(length)]