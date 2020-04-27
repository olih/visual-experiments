from fractions import Fraction

class V2d:
    def __init__(self, x: Fraction, y: Fraction):
        self.x = x
        self.y = y

    @classmethod
    def from_string(cls, value):
        x, y = value.strip().split(" ")
        return cls(Fraction(x), Fraction(y))

    def __str__(self):
        return "{} {}".format(self.x, self.y)
    
    def __repr__(self):
        return "{} {}".format(self.x, self.y)

    def __add__(self, b):
        return V2d(self.x+b.x, self.y+b.y)

    def __sub__(self, b):
        return V2d(self.x-b.x, self.y-b.y)
    
    def __mul__( self, scalar ):
        return V2d(self.x*scalar, self.y*scalar)

    def square_magnitude(self):
        return self.x**2 + self.y**2

        
# def addPoints (la, lb):
#     length = len(la)
#     return [addPoint(la[i], lb[i]) for i in range(length)]

# def addWeightedPoints (la, lb, weight):
#     length = len(la)
#     return [addPoint(la[i], multiplyPoint(weight, lb[i])) for i in range(length)]