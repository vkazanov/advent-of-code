
def has_entered(inp):
    prev, this = 0, 0
    for i, c in enumerate(inp, start=1):
        prev = this
        if c[0] == "(":
            this += 1
        elif c[0] == ")":
            this -= 1

        if this < 0 and this < prev:
            break
    return i

assert(has_entered("(") == 1)
assert(has_entered("()())") == 5)

assert(has_entered(open("input.txt", "r").read().strip()) == 1797)
