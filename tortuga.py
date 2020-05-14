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

class TortugaConfig:
    def __init__(self):
        self.chain = ""
        self.xy = V2d.from_string("0/1 0/1")
        self.angles = FractionList.from_string("0/4 1/4 1/2 3/4")
        self.magnitudes = FractionList.from_string("1 2 3 4")
        self.brushids = ["i:1"]
        self.magnitude_to_brush_scale = FractionList(1)

    def set_chain(self, chain: str):
        self.chain = chain
        return self

    def set_xy(self, xy: V2d):
        self.xy = xy
        return self

    def set_angles(self, angles: List[Fraction]):
        self.angles = angles
        return self

    def set_angles_string(self, value: str):
        return self.set_angles(FractionList.from_string(value))

    def set_magnitudes(self, magnitudes: List[Fraction]):
        self.magnitudes = magnitudes
        return self

    def set_magnitudes_string(self, value: str):
        return self.set_magnitudes(FractionList.from_string(value))

    def set_brush_ids(self, brushids: List[str]):
        self.brushids = brushids
        return self

    def set_magnitude_to_brush_scale(self, value: Fraction):
        self.magnitude_to_brush_scale = value
        return self

class TortugaState:
    def __init__(self, config: TortugaConfig):
        self.config = config
        self.xy = config.xy
        self.previous_xy = config.xy
        self.anglecycle = TortugaCycle(config.angles, 0)
        self.magnitudecycle = TortugaCycle(config.magnitudes, 0)
        self.brushcycle = TortugaCycle(config.brushids, 0)
        self.target = TortugaAction.ANGLE

    def set_target(self, target: TortugaAction):
        self.target = target
        return self

    def set_position(self, xy: V2d, previous_xy: V2d):
        self.previous_xy = previous_xy
        self.xy = xy
        return self

    def set_cycles(self, anglecycle: TortugaCycle[Fraction], amplitudecycle: TortugaCycle[Fraction],  brushcycle: TortugaCycle[str]):
        self.anglecycle = anglecycle
        self.amplitudecycle = amplitudecycle
        self.brushcycle = brushcycle


    def activate_verb(self, verb: TortugaAction):
        target = self.target
        # Angle
        if verb == TortugaAction.NEXT and target == TortugaAction.ANGLE:
            return self.anglecycle.next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.ANGLE:
            return self.anglecycle.previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.ANGLE:
            return self.anglecycle.reset()
        # Length
        if verb == TortugaAction.NEXT and target == TortugaAction.LENGTH:
            return self.magnitudecycle.next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.LENGTH:
            return self.magnitudecycle.previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.LENGTH:
            return self.magnitudecycle.reset()
        # Brush
        if verb == TortugaAction.NEXT and target == TortugaAction.BRUSH:
            return self.brushcycle.next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.BRUSH:
            return self.brushcycle.previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.BRUSH:
            return self.brushcycle.reset()
        else:
            raise Exception("Unexpected verb {} and object {}".format(verb, target))
        
    def clone(self):
        return TortugaState(self.config).set_position(self.xy, self.previous_xy).set_cycles(self.anglecycle, self.magnitudecycle, self.brushcycle).set_target(self.target)
   
    def angle_previous_vector(self):
        if self.xy == self.previous_xy:
            return Fraction(0)
        else:
            delta = self.xy - self.previous_xy
            return delta.get_angle()

    def current_angle(self):
        return self.anglecycle.current() 

    def current_magnitude(self):
        return self.magnitudecycle.current() 

    def current_brush(self):
        return self.brushcycle.current()

    def create_brushstroke(self):
        angle = self.angle_previous_vector() + self.current_angle()
        xy_delta = V2d.from_amplitude_angle(self.current_magnitude, angle)
        new_xy = self.xy + xy_delta
        self.set_xy(new_xy)
        scale = self.current_magnitude() * self.config.magnitude_to_brush_scale
        return DlmtBrushstroke(brushid = self.current_brush(), xy = new_xy, scale = scale, angle = angle, tags=[])



class TortugaProducer:
    def __init__(self, config: TortugaConfig):
        self.config = config
        anyactions = [TortugaAction.from_string(c) for c in config.chain]
        self.actions = [action for action in anyactions if action != TortugaAction.IGNORE]
        self.state = TortugaState(config)
        self.state_stack = deque()

    def save_state(self):
        self.state_stack.append(self.state.clone())

    def restore_state(self):
        if len(self.state_stack) > 0:
            self.state = self.state_stack.pop()
    