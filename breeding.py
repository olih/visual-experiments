from random import sample, choice
from typing import List, Tuple

class ProductionRule:
    def __init__(self, search: str, repl: str):
        self.search = search
        self.replace = repl
    
    def __str__(self):
        return "{}:{}".format(self.search, self.replace)
    
    def __repr__(self):
        return "{}:{}".format(self.search, self.replace)
    
    def as_obj(self):
        return { "s": self.search, "r": self.replace }

    @classmethod
    def from_list(cls, objList):
        return [cls(obj["s"],obj["r"] )for obj in objList]

    @classmethod
    def to_list(cls, rules):
        return [rule.as_obj() for rule in rules]

def hideChar(somechar):
    return chr(ord(somechar[0])+1000)

def chooseVariableCombi(vars: str, levels: int):
    variables = [char for char in vars]
    two = choice([i+j for i in variables for j in variables])
    three = choice([i+j+k for i in variables for j in variables for k in variables])
    four = choice([i+j+k+l for i in variables for j in variables for k in variables for l in variables])
    five = choice([i+j+k+l+m for i in variables for j in variables for k in variables for l in variables for m in variables])
    if levels is 2:
        return two
    if levels is 3:
        return choice([two, three])
    if levels is 4:
        return choice([two, three, four])
    if levels is 5:
        return choice([two, three, four, five])
    raise Exception("levels {} are not supported".format(levels))

def createRuleValue(vars: str, levels: int, keyrules: List[str]):
    rv = choice(keyrules) + chooseVariableCombi(vars, levels)
    vr = chooseVariableCombi(vars, levels) + choice(keyrules)
    return choice([rv, vr])

class ProductionGame:
    def __init__(self, chainlength = 50):
        self.rules = []
        self.start = ""
        self.iterations = 0
        self.chain = ""
        self.chainlength = chainlength

    def set_vars(self, variables: str):
        self.variables = variables
        self.variables_list = [char for char in variables]
        return self

    def set_constants(self, constants: str):
        self.constants = constants
        self.constants_list = [char for char in constants]
        return self

    def set_start(self, start: str):
        self.start = start
        return self

    def init_with_random_rules(self, levels: int, keyrules: List[str]):
        self.start = createRuleValue(self.variables, levels, keyrules)
        self.rules = [ ProductionRule(i, createRuleValue(self.variables, levels, keyrules)) for i in self.variables_list]

    def produce(self)->str:
        chain = self.start
        length = 0
        i = 0
        more = True
        while more:
            i = i + 1
            for rule in self.rules:
                chain = chain.replace(rule.search, hideChar(rule.search))
            for rule in self.rules:
                chain = chain.replace(hideChar(rule.search), rule.replace)
            length = len([c for c in chain if c in self.constants_list]) # only usable chars
            more = i < 100 and length < self.chainlength
        self.chain = chain
        self.iterations = i
        return chain

    def core_chain(self):
        usable = [c for c in self.chain if c in self.constants_list]
        newchain =  usable
        while len(newchain)<self.chainlength:
            newchain = newchain + usable
        return newchain[:self.chainlength]

    def to_obj(self):
        return {
            "iterations": self.iterations,
            "constants": self.constants,
            "variables": self.variables,
            "rules": ProductionRule.to_list(self.rules),
            "start": self.start,
            "chain": self.chain,
            "core-chain": "".join(self.core_chain())
        }
