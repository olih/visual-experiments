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
    
    def __mul__( self, scalar ):
        return V2d(toStr(self.x*scalar, self.y*scalar))

    def squareMagnitude(self):
        return self.x**2 + self.y**2

        
def addPoints (la, lb):
    length = len(la)
    return [addPoint(la[i], lb[i]) for i in range(length)]

def addWeightedPoints (la, lb, weight):
    length = len(la)
    return [addPoint(la[i], multiplyPoint(weight, lb[i])) for i in range(length)]