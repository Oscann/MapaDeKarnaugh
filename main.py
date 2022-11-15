from utils import cycleX, cycleY

identifiers = [
    [["!A", "!B", "!C"], ["!A", "!B", "C"]],
    [["!A", "B", "!C"], ["!A", "B", "C"]],
    [["A", "B", "!C"], ["A", "B", "C"]],
    [["A", "!B", "!C"], ["A", "!B", "C"]],
]

mapa = [
    [1, 1],
    [1, 1],
    [0, 1],
    [0, 1]
]

groups = []

touched1s = []
touched1s2 = []

# test for:
# all 1 --- done
# long vertical line --- done
# 2 x 2 --- done
# horizontal line --- done
# vertical line --- done

# do:
# equation


def main():
    createSeparationka()
    print(groups)


def makeEquation():
    groups = []
    equation = ""

    createSeparationka()

    # GET THE COORDINATES > TEST IF THE IDENTIFIERS FOR EACH COORD IS DIFFERENT -- IF NOT
    # REMOVE FROM THE FIRST TERM > CONCATENATE EVERY LETTER > ADD TO EQUATION
    for i in range(len(groups)):
        first_coord = groups[i][0]
        first_term = identifiers[first_coord[0]][first_coord[1]]


def checkHasOnlyOnes(_set: set):
    if len(_set) == 1 and 1 in _set:
        return True
    return False


def createSeparationka():

    is_all_1 = {mapa[i][j] for j in range(2) for i in range(4)}

    if checkHasOnlyOnes(is_all_1):
        return 1

    # Check for larger groups
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):

            if (i, j) in touched1s or mapa[i][j] == 0:
                continue
            createGroups(i, j)

    # Second try on groups
    print("Before second try", groups)
    for e in groups:
        if len(e) == 1:
            if (e[0][0], e[0][1]) in touched1s2:
                continue

            result = createGroups(e[0][0], e[0][1], False)

            if result:
                for tupla in groups[-1]:
                    if [tupla] in groups:
                        groups.remove([tupla])

    clearSingles()

    touched1s.extend(touched1s2)

    # Pair checking

    for i in range(4):
        for j in range(2):
            if (i, j) in touched1s or mapa[i][j] == 0:
                continue
            createPairs(i, j)

    for e in groups:
        if len(e) == 1:
            if (e[0][0], e[0][1]) in touched1s2:
                continue
            result = createPairs(e[0][0], e[0][1], False)
            print(result)


def createGroups(i: int, j: int, toogleTouch: bool = True):
    long_line = {mapa[k][j]
                 if (k, j) not in (touched1s if toogleTouch else touched1s2)
                 else 0
                 for k in range(4)
                 }

    if checkHasOnlyOnes(long_line):
        group = [(m, j) for m in range(4)]

        touched1s.extend(group) if toogleTouch else touched1s2.extend(group)
        groups.append(group)
        return True

    # Check 2x2

    _2x2 = {mapa[cycleY(i + k)][cycleX(j + l)]
            if ((cycleY(i + k), cycleX(j + l)) not in (touched1s if toogleTouch else touched1s2))
            else 0
            for k in range(2) for l in range(2)
            }

    if checkHasOnlyOnes(_2x2):
        group = [(cycleY(i + k), cycleX(j + l))
                 for k in range(2) for l in range(2)]

        touched1s.extend(group) if toogleTouch else touched1s2.extend(group)
        groups.append(group)
        return True

    neg_2x2 = {mapa[cycleY(i - k)][cycleX(j - l)]
               if ((cycleY(i - k), cycleX(j - l)) not in (touched1s if toogleTouch else touched1s2))
               else 0
               for k in range(2) for l in range(2)
               }

    if checkHasOnlyOnes(neg_2x2):
        group = [(cycleY(i - k), cycleX(j - l))
                 for k in range(2) for l in range(2)]

        touched1s.extend(group) if toogleTouch else touched1s2.extend(group)
        groups.append(group)
        return True

    # Else, just make it lonely
    single = [(i, j)]
    groups.append(single)
    return False


def createPairs(i: int, j: int, toogleTouch: bool = True):
    if (i, j) in touched1s or mapa[i][j] == 0:
        return True

    if (mapa[cycleY(i - 1)][j] == 1 and ((cycleY(i - 1), j) not in (touched1s if toogleTouch else touched1s2))
        and not
        (
            (mapa[cycleY(i - 2)][j] == 1 and (cycleY(i - 2), j) not in touched1s)
        and (mapa[i][cycleX(j - 1)] == 1 and (i, cycleX(j) - 1) not in touched1s)
    )
    ):

        pair = [(i, j), (cycleY(i - 1), j)]

        touched1s.extend(pair) if toogleTouch else touched1s2.extend(pair)
        groups.append(pair)
        return True

    # Lower vertical
    if (mapa[cycleY(i + 1)][j] == 1 and ((cycleY(i + 1), j) not in (touched1s if toogleTouch else touched1s2))
            and not
            (
                (mapa[cycleY(i + 2)][j] ==
                 1 and (cycleY(i + 2), j) not in touched1s)
        and (mapa[i][cycleX(j + 1)] == 1 and (i, cycleX(j) + 1) not in touched1s)
    )
    ):

        pair = [(i, j), (cycleY(i + 1), j)]

        touched1s.extend(pair) if toogleTouch else touched1s2.extend(pair)
        groups.append(pair)
        return True

    # Horizontal
    if (mapa[i][cycleX(j + 1)] == 1 and ((i, cycleX(j + 1)) not in (touched1s if toogleTouch else touched1s2))):
        print(touched1s)
        pair = [(i, j), (i, cycleX(j + 1))]

        touched1s.extend(pair) if toogleTouch else touched1s2.extend(pair)
        groups.append(pair)
        return True

    # Else, just make it lonely
    single = [(i, j)]
    groups.append(single)

    return False


def clearSingles():
    for e in groups:
        if len(e) == 1:
            groups.remove(e)


main()
