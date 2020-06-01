from random import sample, choice
from typing import List, Tuple

class ProductionRule:
    def __init__(self, search: str, repl: str):
        self.search = search
        self.replace = repl
    
    def __eq__(self, other):
        return self.search == other.search and self.replace == other.replace

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

def createRuleValue(vars: str, levels: int, keyrules: List[str])->str:
    rv = choice(keyrules) + chooseVariableCombi(vars, levels)
    vr = chooseVariableCombi(vars, levels) + choice(keyrules)
    return choice([rv, vr])

def merge_string(str1: str, str2: str)->str:
    s1 = set([c for c in str1])
    s2 = set([c for c in str2])
    s = sorted(list(s1.union(s2)))
    return "".join(s)

def crossover_string(str1: str, str2: str)->str:
    cut1 = len(str1) //4
    cut2 = len(str2) //4
    center = str1[cut1:-cut1]
    left = str2[:cut2]
    right = str2[-cut2:]
    return left + center + right

class ProductionGame:
    def __init__(self, chainlength = 50):
        self.rules = []
        self.start = ""
        self.iterations = 0
        self.chain = ""
        self.chainlength = chainlength

    def __eq__(self, other):
        thisone = (self.variables, self.constants, self.start, self.rules)
        otherone = (other.variables, other.constants, other.start, other.rules)
        return thisone == otherone

    def to_string(self):
        return "vars {} const {} start {} rules {}".format(self.variables, self.constants, self.start, self.rules)

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

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

    def set_rules(self, rules: List[ProductionRule]):
        self.rules = rules
        return self

    def set_rules_as_objs(self, rules: List):
        return self.set_rules(ProductionRule.from_list(rules))

    def set_start_and_rules(self, start_and_rules: (str,  List)):
        '''Sets a tuple with a tuple with the start and rules as obj (not ProductionRule)'''
        self.set_start(start_and_rules[0])
        self.set_rules_as_objs(start_and_rules[1])
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
    @classmethod
    def from_obj(cls, content, chainlength = None):
        constants = content["constants"]
        variables = content["variables"]
        rules = content["rules"]
        start = content["start"]
        length = chainlength if chainlength else len(content.get("chain", ""))
        product = cls(length)
        product.set_vars(variables)
        product.set_constants(constants)
        product.set_start(start)
        product.set_rules_as_objs(rules)
        return product

    @classmethod
    def from_crossover(cls, content1, content2, chainlength = None):
        constants = merge_string(content1["constants"], content2["constants"])
        variables = merge_string(content1["variables"], content2["variables"])
        start = crossover_string(content1["start"], content2["start"])
        length = chainlength if chainlength else max(len(content1.get("chain", "")), len(content2.get("chain", "")))
        rules1_dict = {r["s"]: r["r"] for r in content1["rules"]}
        rules2_dict = {r["s"]: r["r"] for r in content2["rules"]}
        rules = [{"s": r["s"], "r": crossover_string(r["r"], rules2_dict[r["s"]]) if r["s"] in rules2_dict  else r["r"] } for r in content1["rules"]]
        for key, value in rules2_dict.items():
            if key not in rules1_dict:
               rules.append({ "s": key, "r": value }) 
        product = cls(length)
        product.set_vars(variables)
        product.set_constants(constants)
        product.set_start(start)
        product.set_rules_as_objs(rules)
        return product


