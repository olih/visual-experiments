from fractions import Fraction
from typing import List, Tuple, Dict, Set, TypeVar, Generic
from enum import Enum, auto
from collections import deque
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from dalmatianmedia import DlmtBrushstroke


T = TypeVar('T')

class TortugaAction(Enum):
    ANGLE = auto()
    LENGTH = auto()
    BRUSH = auto()
    POINT = auto()
    NEXT = auto()
    PREVIOUS = auto()
    RESET = auto()
    SAVE = auto()
    RESTORE = auto()
    NEGATE = auto()
    IGNORE = auto()
    
    @classmethod
    def from_string(cls, value: str):
        if value == "A":
            return TortugaAction.ANGLE
        elif value == "L":
            return TortugaAction.LENGTH
        elif value == "B":
            return TortugaAction.BRUSH
        elif value == "P":
            return TortugaAction.POINT
        elif value == ">":
            return TortugaAction.NEXT
        elif value == "<":
            return TortugaAction.PREVIOUS
        elif value == "Z":
            return TortugaAction.RESET
        elif value == "[":
            return TortugaAction.SAVE
        elif value == "]":
            return TortugaAction.RESTORE
        elif value == "-":
            return TortugaAction.NEXT
        else:
            return TortugaAction.IGNORE

class TortugaCycle(Generic[T]):
    def __init__(self, values: List[T], idx: int = 0):
        self.values = values
        self.idx = idx
    
    def clone(self)->T:
        return TortugaCycle(self.values.copy(), self.idx)

    def next(self)->T:
        idx = self.idx + 1
        if idx >= len(self.values):
           idx = 0
        self.idx = idx
        return self.values[idx]

    def previous(self)->T:
        idx = self.idx - 1
        if idx < 0 :
           idx = len(self.values) -1
        self.idx = idx
        return self.values[idx]

    def reset(self)->T:
        self.idx = 0
        return self.values[0]

    def current(self)->T:
        return self.values[self.idx]

class TortugaState:
    def __init__(self, xy: V2d, previous_xy: V2d, anglecycle: TortugaCycle[Fraction], lengthcycle: TortugaCycle[Fraction], brushcycle: TortugaCycle[str], verb: TortugaAction, obj: TortugaAction, length_to_brush_scale: Fraction):
        self.xy = xy
        self.previous_xy = previous_xy
        self.anglecycle = anglecycle
        self.lengthcycle = lengthcycle
        self.brushcycle = brushcycle
        self.current_verb = verb
        self.current_obj = obj
        self.length_to_brush_scale = length_to_brush_scale
    
    def clone(self):
        return TortugaState(self.xy, self.previous_xy, self.anglecycle.clone(), self.lengthcycle.clone(), self.brushcycle.clone(), verb = self.current_verb, obj = self.current_obj, length_to_brush_scale = self.length_to_brush_scale)

    def process_verb_obj(self):
        verb = self.current_verb
        obj = self.current_obj
        # Angle
        if verb == TortugaAction.NEXT and obj == TortugaAction.ANGLE:
            return self.anglecycle.next()
        elif verb == TortugaAction.PREVIOUS and obj == TortugaAction.ANGLE:
            return self.anglecycle.previous()
        elif verb == TortugaAction.RESET and obj == TortugaAction.ANGLE:
            return self.anglecycle.reset()
        # Length
        if verb == TortugaAction.NEXT and obj == TortugaAction.LENGTH:
            return self.lengthcycle.next()
        elif verb == TortugaAction.PREVIOUS and obj == TortugaAction.LENGTH:
            return self.lengthcycle.previous()
        elif verb == TortugaAction.RESET and obj == TortugaAction.LENGTH:
            return self.lengthcycle.reset()
        # Brush
        if verb == TortugaAction.NEXT and obj == TortugaAction.BRUSH:
            return self.brushcycle.next()
        elif verb == TortugaAction.PREVIOUS and obj == TortugaAction.BRUSH:
            return self.brushcycle.previous()
        elif verb == TortugaAction.RESET and obj == TortugaAction.BRUSH:
            return self.brushcycle.reset()
        else:
            raise Exception("Unexpected verb {} and object {}".format(verb, obj))
    
    def current_angle(self):
        return self.anglecycle.current() 

    def angle_previous_vector(self):
        if self.xy == self.previous_xy:
            return Fraction(0)
        else:
            delta = self.xy - self.previous_xy
            return delta.get_angle()

    def current_length(self):
        return self.lengthcycle.current() 

    def current_brush(self):
        return self.brushcycle.current()

    def set_verb(self, verb: TortugaAction):
        self.current_verb = verb
        return self

    def set_obj(self, obj: TortugaAction):
        self.current_obj = obj
        return self

    def set_xy(self, xy: V2d):
        self.previous_xy = self.xy
        self.xy = xy
        return self

    def create_brushstroke(self):
        angle = self.angle_previous_vector() + self.current_angle()
        xy_delta = V2d.from_amplitude_angle(self.current_length, angle)
        new_xy = self.xy + xy_delta
        self.set_xy(new_xy)
        scale = self.current_length * self.length_to_brush_scale
        return DlmtBrushstroke(brushid = self.current_brush(), xy = new_xy, scale = scale, angle = angle, tags=[])



class TortugaProducer:
    def __init__(self, chain: str, xy: V2d,  angles: List[Fraction], lengths: List[Fraction], brushids: List[str], length_to_brush_scale: Fraction):
        self.chain = chain
        self.xy = xy
        self.angles = angles
        self.lengths = lengths
        self.brushids = brushids
        self.length_to_brush_scale = length_to_brush_scale
        anyactions = [TortugaAction.from_string(c) for c in chain]
        self.actions = [action for action in anyactions if action != TortugaAction.IGNORE]
        self.state = TortugaState(xy, xy, TortugaCycle(angles), TortugaCycle(lengths), TortugaCycle(brushids), verb = TortugaAction.RESTORE, obj = TortugaAction.BRUSH, length_to_brush_scale = length_to_brush_scale)
        self.state_stack = deque()

    def save_state(self):
        self.state_stack.append(self.state.clone())

    def restore_state(self):
        if len(self.state_stack) > 0:
            self.state = self.state_stack.pop()
    