from fractions import Fraction
from typing import List, Tuple
from enum import Enum, auto

class V2d:
    def __init__(self, x: Fraction, y: Fraction):
        self.x = x
        self.y = y

    @classmethod
    def from_string(cls, value: str):
        x, y = value.strip().split(" ")
        return cls(Fraction(x), Fraction(y))

    def clone(self):
        return V2d(self.x, self.y)

    def __str__(self):
        return "{} {}".format(self.x, self.y)
    
    def to_dalmatian_string(self):
        return "{} {}".format(self.x, self.y)
    
    def to_cartesian_string(self, dpu: int):
        return "({:.3f},{:.3f})".format(float(self.x*dpu), float(self.y*dpu))

    def to_svg_string(self, dpu: int):
        return "{:.3f} {:.3f}".format(float(self.x*dpu), float(self.y*dpu*-1))

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
    
    def neg_x(self):
        return V2d(self.x*-1, self.y)

    def neg_y(self):
        return V2d(self.x, self.y*-1)

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

    def to_svg_string(self, dpu: int, sep=" "):
        return sep.join([ value.to_svg_string(dpu) for value in self.values])

    def to_dalmatian_string(self):
        return " ".join([ value.to_dalmatian_string() for value in self.values])
    
    @classmethod
    def from_dalmatian_string(cls, somestr: str):
        fractions = [Fraction(value) for value in somestr.strip().split(" ")]
        return [V2d(fractions[2*i], fractions[2*i+1]) for i in range(len(fractions)//2)]

    @classmethod
    def ljust(cls, v2dlist, length: int, filler: V2d = V2d.from_string("0/1 0/1")):
        values = [value.clone() for value in v2dlist.values]
        while len(values)<length:
            values.append(filler)
        return cls(values)
    
    def __getitem__(self, index):
        return self.values[index]
    
    def __neg__(self):
        return V2dList([- value.clone() for value in self.values])

    def neg_x(self):
        return V2dList([value.clone().neg_x() for value in self.values])

    def neg_y(self):
        return V2dList([value.clone().neg_y() for value in self.values])

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

    def __mul__(self, scalar: Fraction):
       return V2dList([value.clone() * scalar for value in self.values])

    def extend(self, other):
       return V2dList(self.values.copy()+other.values.copy())

    def append(self, value: V2d):
        newvalues = self.values.copy()
        newvalues.append(value)
        return V2dList(newvalues)

    def circular(self):
        return self.append(self.values[0])

    def to_bigram(self)->List[Tuple[V2d, V2d]]:
        return [(self.values[i], self.values[i+1]) for i in range(len(self.values)-1)]

class SegmentShape(Enum):
    CLOSE_PATH = auto()
    MOVE_TO = auto()
    LINE_TO = auto()
    CUBIC_BEZIER = auto()
    SMOOTH_BEZIER = auto()
    QUADRATIC_BEZIER = auto()
    FLUID_BEZIER = auto()
    NOT_SUPPORTED = auto()
    
    @classmethod
    def from_string(cls, value: str):
        if value is "Z":
            return SegmentShape.CLOSE_PATH
        elif value is "M":
            return SegmentShape.MOVE_TO
        elif value is "L":
            return SegmentShape.LINE_TO
        elif value is "C":
            return SegmentShape.CUBIC_BEZIER
        elif value is "S":
            return SegmentShape.SMOOTH_BEZIER
        elif value is "Q":
            return SegmentShape.QUADRATIC_BEZIER
        elif value is "T":
            return SegmentShape.FLUID_BEZIER
        else:
            return SegmentShape.NOT_SUPPORTED
    
    @classmethod
    def to_string(cls, value):
        if value is SegmentShape.CLOSE_PATH:
            return "Z"
        elif value is SegmentShape.MOVE_TO:
            return "M"
        elif value is SegmentShape.LINE_TO:
            return "L"
        elif value is SegmentShape.CUBIC_BEZIER:
            return "C"
        elif value is SegmentShape.SMOOTH_BEZIER:
            return "S"
        elif value is SegmentShape.QUADRATIC_BEZIER:
            return "Q"
        elif value is SegmentShape.FLUID_BEZIER:
            return "T"
        else:
            return "E"

    @classmethod
    def count_of_points(cls, value):
        if value is SegmentShape.CLOSE_PATH:
            return 0
        elif value is SegmentShape.MOVE_TO:
            return 1
        elif value is SegmentShape.LINE_TO:
            return 1
        elif value is SegmentShape.CUBIC_BEZIER:
            return 3
        elif value is SegmentShape.SMOOTH_BEZIER:
            return 2
        elif value is SegmentShape.QUADRATIC_BEZIER:
            return 2
        elif value is SegmentShape.FLUID_BEZIER:
            return 1
        else:
            return 0


class VSegment:
    def __init__(self, action: SegmentShape = SegmentShape.NOT_SUPPORTED, pt: V2d = None, pt1: V2d = None, pt2: V2d = None):
        self.action = action
        self.pt = pt
        self.pt1 = pt1
        self.pt2 = pt2
    
    @classmethod
    def from_close(cls):
        return cls(SegmentShape.CLOSE_PATH)    

    @classmethod
    def from_move_to(cls, pt):
        return cls(SegmentShape.MOVE_TO, pt)    
    
    @classmethod
    def from_line_to(cls, pt):
        return cls(SegmentShape.LINE_TO, pt)

    @classmethod
    def from_cubic_bezier(cls, pt, pt1, pt2):
        return cls(SegmentShape.CUBIC_BEZIER, pt, pt1, pt2)

    @classmethod
    def from_smooth_bezier(cls, pt, pt1):
        return cls(SegmentShape.SMOOTH_BEZIER, pt, pt1)

    @classmethod
    def from_quadratic_bezier(cls, pt, pt1):
        return cls(SegmentShape.QUADRATIC_BEZIER, pt, pt1)

    @classmethod
    def from_fluid_bezier(cls, pt):
        return cls(SegmentShape.FLUID_BEZIER, pt)

    def to_dalmatian_string(self):
        action_str = SegmentShape.to_string(self.action)
        if self.action is SegmentShape.CLOSE_PATH:
            return "{}".format(action_str)
        elif self.action in [SegmentShape.MOVE_TO, SegmentShape.LINE_TO, SegmentShape.FLUID_BEZIER] :
            return "{} {}".format(action_str, self.pt.to_dalmatian_string())
        elif self.action in [ SegmentShape.SMOOTH_BEZIER, SegmentShape.QUADRATIC_BEZIER]:
            return "{} {} {}".format(action_str, self.pt1.to_dalmatian_string(), self.pt.to_dalmatian_string())
        elif self.action is SegmentShape.CUBIC_BEZIER:
            return "{} {} {} {}".format(action_str, self.pt1.to_dalmatian_string(), self.pt2.to_dalmatian_string(), self.pt.to_dalmatian_string())
        else:
            return "E"
    
    @classmethod
    def from_dalmatian_string(cls, dstr):
        if dstr is "Z":
            return VSegment.from_close()
        action = SegmentShape.from_string(dstr.strip()[0])
        points = V2dList.from_dalmatian_string(dstr.strip()[1:])
        length = len(points)
        if action is SegmentShape.MOVE_TO and length is 1 :
            return VSegment.from_move_to(points[0])
        elif action is SegmentShape.LINE_TO and length is 1 :
            return VSegment.from_line_to(points[0])
        elif action is SegmentShape.FLUID_BEZIER and length is 1 :
            return VSegment.from_fluid_bezier(points[0])
        elif action is SegmentShape.SMOOTH_BEZIER and length is 2:
            return VSegment.from_smooth_bezier(points[1], points[0])
        elif action is SegmentShape.QUADRATIC_BEZIER and length is 2:
            return VSegment.from_quadratic_bezier(points[1], points[0])
        elif action is SegmentShape.CUBIC_BEZIER and length is 3:
            return VSegment.from_cubic_bezier(points[2], points[0], points[1])
        else:
            return VSegment()


    def __str__(self):
        return self.to_dalmatian_string()
    
    def __repr__(self):
        return self.to_dalmatian_string()

class VPath:
    def __init__(self, segments: List[VSegment]):
        self.segments = segments

    def __str__(self):
        return str(self.segments)
    
    def __repr__(self):
        return str(self.segments)

    def length(self):
        return len(self.segments)
    
    def __len__(self):
        return len(self.segments)
    
    def __eq__(self, other):
        return self.segments == other.segments

    def to_dalmatian_string(self):
        core = ",".join([segment.to_dalmatian_string() for segment in self.segments])
        return "[ {} ]".format(core)
    
    @classmethod
    def from_dalmatian_string(cls, dstr):
        parts =  dstr.replace("[","").replace("]", "").strip().split(",")
        segments = [VSegment.from_dalmatian_string(segment) for segment in parts]
        return cls(segments)

    def core_points(self):
        return [segment.pt for segment in self.segments if SegmentShape.count_of_points(segment.action)>0]

    def to_core_cartesian_string(self, dpu: int, sep=""):
        return sep.join([point.to_cartesian_string(dpu) for point in self.core_points()])

    def to_core_svg_string(self, dpu: int):
        return " ".join(["L {}".format(point.to_svg_string(dpu)) for point in self.core_points()]).replace("L", "M", 1) + " Z"