

def cycleX(x):
    if x >= 2:
        x -= 2
    elif x <= -1:
        x += 2

    return x


def cycleY(y):
    if y >= 4:
        y -= 4
    elif y <= -1:
        y += 4

    return y


def checkHasOnlyOnes(_set: set):
    if len(_set) == 1 and 1 in _set:
        return True
    return False
