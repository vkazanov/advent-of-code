import operator

# Grammar
# EXPR -> FACTOR *["*" FACTOR]
# FACTOR -> TERM *["+" TERM]
# TERM -> NUMBER | ( EXPR )

class tokenizer:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def skip_space(self):
        while self.i < len(self.s) and self.s[self.i].isspace():
            self.i += 1

    def peek(self):
        self.skip_space()
        if self.i >= len(self.s):
            return None
        return self.s[self.i]

    def pop(self):
        self.skip_space()
        if self.i >= len(self.s):
            return None

        c = self.s[self.i]
        self.i += 1
        if c.isnumeric():
            return int(c)
        else:
            return c

def eval_expr(tokenizer):
    val = eval_factor(tokenizer)
    while tokenizer.peek() == "*":
        tokenizer.pop()
        val *= eval_factor(tokenizer)
    return val

def eval_factor(tokenizer):
    val = eval_term(tokenizer)
    while tokenizer.peek() == "+":
        tokenizer.pop()
        val += eval_term(tokenizer)
    return val

def eval_term(tokenizer):
    if tokenizer.peek() == "(":
        tokenizer.pop()
        val = eval_expr(tokenizer)
        assert(tokenizer.pop() == ")")
        return val
    else:
        return tokenizer.pop()


# assert(eval_expr(tokenizer("1")) == 1)
# assert(eval_expr(tokenizer("1 * 2")) == 2)
# assert(eval_expr(tokenizer("1 + 2")) == 3)
# assert(eval_expr(tokenizer("1 + 2 * 3")) == 9)
# assert(eval_expr(tokenizer("1 * 2 + 3")) == 5)
# assert(eval_expr(tokenizer("1 + 2 * 3 + 4 * 5 + 6")) == 231)

# assert(eval_expr(tokenizer("(1)")) == 1)
# assert(eval_expr(tokenizer("(1 + 2)")) == 3)
# assert(eval_expr(tokenizer("(1 + 2) * 2")) == 6)
# assert(eval_expr(tokenizer("2 * (1 + 2)")) == 6)
# assert(eval_expr(tokenizer("2 * (1 + 2 * 2)")) == 12)
# assert(eval_expr(tokenizer("8 * 3 + 9 + 3 * 4 * 3")) == 1440)
# assert(eval_expr(tokenizer("5 + (8 * 3 + 9 + 3 * 4 * 3)")) == 1445)
# assert(eval_expr(tokenizer("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")) == 669060)

acc = 0
for s in open("input.txt"):
    acc += eval_expr(tokenizer(s))
print(acc)
assert(acc, 216975281211165)
