from fractions import Fraction
from typing import List, Tuple, Dict, Set, TypeVar, Generic
from enum import Enum, auto
from collections import deque
from random import sample, choice, randint
from fracgeometry import V2d, V2dList, VSegment, VPath, FractionList
from dalmatianmedia import DlmtBrushstroke


T = TypeVar('T')

class TortugaAction(Enum):
    ANGLE = auto()
    MAGNITUDE = auto()
    BRUSH = auto()
    POINT = auto()
    TAG = auto()
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
            return TortugaAction.MAGNITUDE
        elif value == "B":
            return TortugaAction.BRUSH
        elif value == "T":
            return TortugaAction.TAG
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
            return TortugaAction.NEGATE
        else:
            return TortugaAction.IGNORE

    @classmethod
    def to_string(cls, value):
        if value == TortugaAction.ANGLE:
            return "A"
        elif value == TortugaAction.MAGNITUDE:
            return "L"
        elif value == TortugaAction.BRUSH:
            return "B"
        elif value == TortugaAction.TAG:
            return "T"
        elif value == TortugaAction.POINT:
            return "P"
        elif value == TortugaAction.NEXT:
            return ">"
        elif value == TortugaAction.PREVIOUS:
            return "<"
        elif value == TortugaAction.RESET:
            return "Z"
        elif value == TortugaAction.SAVE:
            return "["
        elif value == TortugaAction.RESTORE:
            return "]"
        elif value == TortugaAction.NEGATE:
            return "-"
        else:
            return ""

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
        self.tags = ["i:1"]
        self.magnitude_page_ratio = Fraction("1/100")
        self.scale_magnitude_ratio = Fraction("1/1")
        self.brushstoke_angle_offset = Fraction(0)

    def __eq__(self, other):
        thisone = (self.chain, self.xy, self.angles, self.magnitudes, self.tags, self.brushids, self.magnitude_page_ratio, self.scale_magnitude_ratio, self.brushstoke_angle_offset )
        otherone = (other.chain, other.xy, other.angles, other.magnitudes,self.tags, other.brushids, other.magnitude_page_ratio, other.scale_magnitude_ratio, other.brushstoke_angle_offset )
        return thisone == otherone

    def clone(self):
         cfg = TortugaConfig()
         cfg.set_chain(self.chain)
         cfg.set_xy(self.xy)
         cfg.set_angles(self.angles)
         cfg.set_magnitudes(self.magnitudes)
         cfg.set_brush_ids(self.brushids)
         cfg.set_tags(self.tags)
         cfg.set_magnitude_page_ratio(self.magnitude_page_ratio)
         cfg.set_scale_magnitude_ratio(self.scale_magnitude_ratio)
         cfg.set_brushstoke_angle_offset(self.brushstoke_angle_offset)
         return cfg

    def set_chain(self, chain: str):
        self.chain = chain
        return self

    def set_xy(self, xy: V2d):
        self.xy = xy
        return self

    def set_xy_string(self, value: str):
        return self.set_xy(V2d.from_string(value))

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

    def set_tags(self, tags: List[str]):
        self.tags = tags
        return self

    def set_magnitude_page_ratio(self, value: Fraction):
        self.magnitude_page_ratio = value
        return self

    def set_magnitude_page_ratio_string(self, value: str):
        return self.set_magnitude_page_ratio(Fraction(value))

    def set_scale_magnitude_ratio(self, value: Fraction):
        self.scale_magnitude_ratio = value
        return self

    def set_scale_magnitude_ratio_string(self, value: str):
        return self.set_scale_magnitude_ratio(Fraction(value))

    def set_brushstoke_angle_offset(self, value: Fraction):
        self.brushstoke_angle_offset = value
        return self
    
    def set_brushstoke_angle_offset_string(self, value: str):
        return self.set_brushstoke_angle_offset(Fraction(value))


class TortugaState:
    def __init__(self, config: TortugaConfig):
        self.config = config
        self.xy = config.xy
        self.previous_xy = config.xy
        self.anglecycle = (TortugaCycle(config.angles, 0), TortugaCycle([1, -1]))
        self.magnitudecycle = (TortugaCycle(config.magnitudes, 0), TortugaCycle([1, -1]))
        self.brushcycle = TortugaCycle(config.brushids, 0)
        self.tagcycle = TortugaCycle(config.tags, 0)
        self.target = TortugaAction.ANGLE

    def set_target(self, target: TortugaAction):
        self.target = target
        return self

    def set_position(self, xy: V2d, previous_xy: V2d):
        self.previous_xy = previous_xy
        self.xy = xy
        return self

    def set_cycles(self, anglecycle: (TortugaCycle[Fraction], TortugaCycle[int]), amplitudecycle: (TortugaCycle[Fraction],  TortugaCycle[int]),  brushcycle: TortugaCycle[str], tagcycle: TortugaCycle[str]):
        self.anglecycle = anglecycle
        self.amplitudecycle = amplitudecycle
        self.brushcycle = brushcycle
        self.tagcycle = tagcycle
        return self

    def activate_verb(self, verb: TortugaAction):
        target = self.target
        # Angle
        if verb == TortugaAction.NEXT and target == TortugaAction.ANGLE:
            self.anglecycle[0].next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.ANGLE:
            self.anglecycle[0].previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.ANGLE:
            self.anglecycle[0].reset()
        elif verb == TortugaAction.NEGATE and target == TortugaAction.ANGLE:
            self.anglecycle[1].next()
        # Length
        elif verb == TortugaAction.NEXT and target == TortugaAction.MAGNITUDE:
            self.magnitudecycle[0].next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.MAGNITUDE:
            self.magnitudecycle[0].previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.MAGNITUDE:
            self.magnitudecycle[0].reset()
        elif verb == TortugaAction.NEGATE and target == TortugaAction.MAGNITUDE:
            self.magnitudecycle[1].next()
        # Brush
        elif verb == TortugaAction.NEXT and target == TortugaAction.BRUSH:
            self.brushcycle.next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.BRUSH:
            self.brushcycle.previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.BRUSH:
            self.brushcycle.reset()
        # Tag
        elif verb == TortugaAction.NEXT and target == TortugaAction.TAG:
            self.tagcycle.next()
        elif verb == TortugaAction.PREVIOUS and target == TortugaAction.TAG:
            self.tagcycle.previous()
        elif verb == TortugaAction.RESET and target == TortugaAction.TAG:
            self.tagcycle.reset()
        else:
            raise Exception("Unexpected verb {} and target {}".format(verb, target))
        return self
        
    def clone(self):
        return TortugaState(self.config).set_position(self.xy, self.previous_xy).set_cycles(self.anglecycle, self.magnitudecycle, self.brushcycle, self.tagcycle).set_target(self.target)
   
    def angle_previous_vector(self):
        if self.xy == self.previous_xy:
            return Fraction(0)
        else:
            delta = self.xy - self.previous_xy
            return delta.get_angle()

    def current_angle(self):
        return self.anglecycle[0].current() 

    def sign_angle(self):
        return self.anglecycle[1].current() 

    def current_magnitude(self):
        return self.magnitudecycle[0].current()

    def sign_magnitude(self):
        return self.magnitudecycle[1].current()

    def current_brush(self):
        return self.brushcycle.current()

    def current_tag(self):
        return self.tagcycle.current()

    def create_brushstroke(self):
        angle = self.angle_previous_vector() + self.sign_angle()*self.current_angle()
        xy_delta = V2d.from_amplitude_angle(self.current_magnitude()*self.config.magnitude_page_ratio*self.sign_magnitude(), angle)
        new_xy = self.xy + xy_delta
        self.set_position(new_xy, self.xy)
        scale = self.current_magnitude() * self.config.scale_magnitude_ratio
        brush_angle = angle + self.config.brushstoke_angle_offset
        tags = [] if self.current_tag() == "" else [self.current_tag()]
        return DlmtBrushstroke(brushid = self.current_brush(), xy = new_xy, scale = scale, angle = brush_angle, tags= tags)



class TortugaProducer:
    def __init__(self, config: TortugaConfig):
        self.config = config
        anyactions = [TortugaAction.from_string(c) for c in config.chain]
        self.actions = [action for action in anyactions if action != TortugaAction.IGNORE]
        self.state = TortugaState(config)
        self.state_stack = deque()

    def _save_state(self):
        self.state_stack.append(self.state.clone())

    def _restore_state(self):
        if len(self.state_stack) > 0:
            self.state = self.state_stack.pop()
    
    def _reset_state(self):
        self.state_stack = deque()

    def produce(self)->List[DlmtBrushstroke]:
        results = []
        for action in self.actions:
            if action in [TortugaAction.ANGLE, TortugaAction.MAGNITUDE, TortugaAction.BRUSH]:
                self.state.set_target(action)
            elif action in [TortugaAction.NEGATE, TortugaAction.NEXT, TortugaAction.PREVIOUS, TortugaAction.RESET]:
                self.state.activate_verb(action)
            elif action == TortugaAction.POINT:
                brushstoke = self.state.create_brushstroke()
                results.append(brushstoke)
            elif action == TortugaAction.SAVE:
                self._save_state()
            elif action == TortugaAction.RESTORE:
                self._restore_state()

        return results

class TortugaTargetRand:
    def __init__(self):
        self.target = TortugaAction.IGNORE
        self.verbs = [TortugaAction.IGNORE]

    def set_target(self, target: TortugaAction):
        self.target = target
        return self

    def set_verbs(self, verbs: List[TortugaAction]):
        self.verbs = verbs
        return self

    @classmethod
    def from_string(cls, value: str):
        target, other = value.split(":",1)
        verbs = [TortugaAction.from_string(term) for term in other.split(" ") if term in "<>Z-" ]
        rule = cls()
        rule.set_target(TortugaAction.from_string(target))
        rule.set_verbs(verbs)
        return rule

    def choice(self)->str:
       return  "".join([ TortugaAction.to_string(p) for p in [self.target, choice(self.verbs)] ])

        

class TortugaRuleMaker:
    def __init__(self):
        self.variables_list = ["I"]
        self.supported_targets = {
            "L": [">", "<"]
        }
    
    def set_vars(self, variables: str):
        self.variables_list = [char for char in variables]
        return self

    def set_supported(self, supported: str):
        supported.split(" ")

    def make(self)->(str, List):
        return ("", [{}])


    
