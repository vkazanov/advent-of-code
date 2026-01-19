import operator

i1 = "1 + 2 * 3 + 4 * 5 + 6"
i2 = "1 + (2 * 3) + (4 * (5 + 6))"

op2fun = { "+": operator.add, "*": operator.mul }

def tokenize(s):
    for i, c in enumerate(s):
        if c.isspace():
            continue
        elif c.isnumeric():
            yield i, int(c)
        elif c in "+*":
            yield i, op2fun[c]
        else:
            # parens
            yield i, c

def read(tokenizer, depth=0):
    acc = 0
    op = operator.add
    for i, tok in tokenizer:
        if type(tok) == int:
            acc = op(acc, tok)
        elif tok in op2fun.values():
            op = tok
        elif tok == ")":
            return acc
        elif tok == "(":
            acc = op(acc, read(tokenizer))
        else:
            print(tok)
            assert False
    return acc


read(tokenize(i1)) == 71
read(tokenize(i2)) == 51
acc = 0
for s in open("input.txt"):
    acc += read(tokenize(s))
assert(acc == 45283905029161)
