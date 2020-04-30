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
    variables = vars.split("")
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
        self.constants = "L"
        self.variables = "IJK"
        self.rules = []
        self.start = ""
        self.iterations = 3
        self.chain = ""
        self.chainlength = chainlength

    def setVars(self, variables: str):
        self.variables = variables
        return self

    def setConstants(self, constants: str):
        self.constants = constants
        return self

    def setIterations(self, iterations: int):
        self.iterations = iterations
        return self

    def setStart(self, start: str):
        self.start = start
        return self

    def setRules(self, rules: List[ProductionRule]):
        self.rules = rules
        return self

    def randomRules(self, levels: int, keyrules: List[str]):
        self.start = createRuleValue(self.variables, levels, keyrules)
        self.rules = [ {"s": i, "r": createRuleValue(self.variables, levels, keyrules) } for i in self.variables.split("")]

    def produce(self)->str:
        chain = self.start
        for i in range(self.iterations):
            for rule in self.rules:
                chain = chain.replace(rule["s"], hideChar(rule["s"]))
            for rule in self.rules:
                chain = chain.replace(hideChar(rule["s"]), rule["r"])
        self.chain = chain
        return chain

    def core_chain(self):
        keepchars = self.constants.split("")
        usable = [c for c in self.chain if c in keepchars]
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
            "core-chain": self.core_chain()
        }
