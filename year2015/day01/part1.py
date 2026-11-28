cnt = 0
for c in open("input.txt", "r").read():
    if c[0] == "(":
        cnt += 1
    elif c[0] == ")":
        cnt -= 1
assert(cnt == 280)
