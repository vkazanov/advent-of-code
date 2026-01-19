import pprint
from functools import lru_cache
from dataclasses import dataclass

@dataclass
class Ref: i: int

@dataclass
class Seq: parts: tuple

@dataclass
class Alt: options: tuple

def parse_rule(rule_line):
    lhs, rhs = rule_line.split(": ")
    return int(lhs), parse_alt(rhs) if " | " in rhs else parse_seq(rhs)

def parse_alt(alt_line):
    return Alt(tuple(parse_seq(opt) for opt in alt_line.split(" | ")))

def parse_seq(seq_line):
    return Seq(tuple(Ref(int(c)) if c.isdigit() else c[1:-1] for c in seq_line.split()))

def check(line, rules):

    def match_node(node, i):
        match node:
            case str(c):
                return frozenset((i + 1,)) if i < len(line) and c == line[i] else frozenset()

            case Seq(rule_seq):
                positions = {i}
                for r in rule_seq:
                    positions = {p2 for p in positions for p2 in match_node(r, p)}
                    if not positions:
                        break
                return frozenset(positions)

            case Alt(options):
                return frozenset(p2 for opt in options for p2 in match_node(opt, i))

            case Ref(rule_i):
                return match_rule(rule_i, i)

            case _:
                raise TypeError(f"Invalid rule: {node!r}")

    @lru_cache(maxsize=None)
    def match_rule(rule_i, i):
        return match_node(rules[rule_i], i)

    return len(line) in match_rule(0, 0)

# inp = open("input-test-2.txt")
inp = open("input-2.txt")

rule_block, input_block = inp.read().split("\n\n")
all_rules = dict(parse_rule(line) for line in rule_block.splitlines())
counter = sum(check(line.strip(), all_rules) for line in input_block.splitlines())

print(counter)
assert(counter == 267)
