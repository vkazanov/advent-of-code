from io import StringIO
import pprint
from util import cstr, COLOR, FORMAT
from dataclasses import dataclass

# inp = open("input-test-1.txt")
inp = open("input-1.txt")

@dataclass
class Seq:
    value: list
    def __init__(self, value):
        self.value = value

@dataclass
class Alt:
    value: list
    def __init__(self, value):
        self.value = value

rules = {}

def parse(rule_line):
    idx, right = rule_line.split(": ")
    idx = int(idx)
    if " | " not in right:
        rules[idx] = Seq(parse_seq(right))
    else:
        rules[idx] = Alt([Seq(parse_seq(alt)) for alt in right.split(" | ")])

def parse_seq(seq_line):
    res = []
    for c in seq_line.split(" "):
        if c.isnumeric():
            res.append(int(c))
        else:
            res.append(c[1:-1])
    return res

for line in inp:
    line = line.strip()
    if not line: break
    parse(line)

def expand_rule(rule):
    match rule:
        case int(n):
            return expand_rule(rules[rule])
        case str(s):
            return rule
        case Seq(l):
            return Seq(list(expand_rule(r) for r in l))
        case Alt(l):
            return Alt(list(expand_rule(r) for r in l))
        case _:
            assert False
    return rule

rule = expand_rule(rules[0])

def check(line, rule, i=0):
    match rule:
        case str(r):
            return r == line[i], i + 1

        case Seq(rule_seq):
            next_i = i
            for r_i, r in enumerate(rule_seq):
                this_res, next_i = check(line, r, next_i)
                if not this_res:
                    return False, next_i
            return True, next_i

        case Alt(rule_alt):
            for r in rule_alt:
                this_res, next_i = check(line, r, i)
                if this_res:
                    return True, next_i
            return False, i

        case _:
            assert False
    return False, i

counter = 0
for line in inp:
    line = line.strip()
    res, l = check(line, rule)
    if res and l == len(line): counter += 1
print(counter)
assert(counter == 162)
