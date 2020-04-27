from fractions import Fraction
from typing import List

class V2d:
    def __init__(self, x: Fraction, y: Fraction):
        self.x = x
        self.y = y

    @classmethod
    def from_string(cls, value: str):
        x, y = value.strip().split(" ")
        return cls(Fraction(x), Fraction(y))

    def __str__(self):
        return "{} {}".format(self.x, self.y)
    
    def to_cartesian_string(self, dpu: int):
        return "({:.3f},{:.3f})".format(float(self.x*dpu), float(self.y*dpu))

    def __repr__(self):
        return "{} {}".format(self.x, self.y)

    def __add__(self, b):
        return V2d(self.x+b.x, self.y+b.y)

    def __sub__(self, b):
        return V2d(self.x-b.x, self.y-b.y)
    
    def __mul__( self, scalar: Fraction):
        return V2d(self.x*scalar, self.y*scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __neg__(self):
        return V2d(self.x*-1, self.y*-1)

    def square_magnitude(self):
        return self.x**2 + self.y**2

class V2dList:
    
    def __init__(self, values: List[V2d] ):
         self.values = values.copy()
    
    def __str__(self):
        return ", ".join([str(value) for value in self.values])
    
    def __repr__(self):
        return ", ".join([str(value) for value in self.values])

    def length(self):
        return len(self.values)
    
    def __len__(self):
        return len(self.values)
    
    def __eq__(self, other):
        return self.values == other.values

    def to_cartesian_string(self, dpu: int, sep=""):
        return sep.join([ value.to_cartesian_string(dpu) for value in self.values])

    @classmethod
    def ljust(cls, v2dlist, length: int, filler: V2d = V2d.from_string("0/1 0/1")):
        values = v2dlist.values.copy()
        while len(values)<length:
            values.append(filler)
        return cls(values)
    
    def __getitem__(self, index):
        return self.values[index]
    
    def __neg__(self):
        return V2dList([- value for value in self.values])

    def __add__(self, b):
        maxlength = max(self.length(), b.length())
        aa = V2dList.ljust(self, maxlength).values
        bb = V2dList.ljust(b, maxlength).values
        return V2dList([aa[i] + bb[i] for i in range(maxlength)])

    def __sub__(self, b):
        maxlength = max(self.length(), b.length())
        aa = V2dList.ljust(self, maxlength).values
        bb = V2dList.ljust(b, maxlength).values
        return V2dList([aa[i] - bb[i] for i in range(maxlength)])

    def __mul__( self, scalar: Fraction):
       return V2dList([value * scalar for value in self.values])
