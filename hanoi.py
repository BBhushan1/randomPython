def move(a, b):
    #print("Move disk from {} to {}!".format(a, b))
    return {"moves": "Move disk from {} to {}!".format(a, b)}


# n: number of discs
# f: from position
# h: is helper position
# t: is target position
i = 0


def hanoi(n, f, h, t):
    global i
    if n == 0:
        pass
    else:
        i += 1;
        hanoi(n - 1, f, t , h)
        print(move(f, t))
        hanoi(n - 1, h, f, t)


hanoi(8, "A", "B", "C")
print("Number of steps: {steps}".format(steps=i))
