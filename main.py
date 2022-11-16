from utils import checkHasOnlyOnes, cycleX, cycleY

identifiers = [
    [["!A", "!B", "!C"], ["!A", "!B", "C"]],
    [["!A", "B", "!C"], ["!A", "B", "C"]],
    [["A", "B", "!C"], ["A", "B", "C"]],
    [["A", "!B", "!C"], ["A", "!B", "C"]],
]

mapa = [
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0]
]

groups = []

touched1s = []


def main():
    print("Informe a saída da tabela a medida que forem aparecendo (ordem A - B - C")
    for A in range(2):
        for B in range(2):
            for C in range(2):
                output = int(input(f"{A} - {B} - {C}  : "))

                mapCoords = getCoordsOnTerm(bool(A), bool(B), bool(C))

                mapa[mapCoords[0]][mapCoords[1]] = output

    for i in range(4):
        print(mapa[i])

    equation = makeEquation()

    print(equation)


def makeEquation():
    global groups
    groups = []
    equation = ""

    createSeparationka()

    # GET THE COORDINATES > TEST IF THE IDENTIFIERS FOR EACH COORD IS DIFFERENT -- IF NOT
    # REMOVE FROM THE FIRST TERM > CONCATENATE EVERY LETTER > ADD TO EQUATIOn

    for i in range(len(groups)):
        group = groups[i]
        first_coord = group[0]

        # Equals to first term
        base_term = identifiers[first_coord[0]][first_coord[1]].copy()

        for j in range(len(group)):
            term = identifiers[group[j][0]][group[j][1]]

            for letterIndex in range(len(term)):
                if base_term[letterIndex] != term[letterIndex]:
                    base_term[letterIndex] = ""

        term = "".join(base_term)

        if term != "":
            equation += term

            if i + 1 != len(groups):
                equation += " + "

    return equation


def createSeparationka():

    global groups

    is_all_1 = {mapa[i][j] for j in range(2) for i in range(4)}

    if checkHasOnlyOnes(is_all_1):
        return 1

    # Check for larger groups
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):

            if (i, j) in touched1s or mapa[i][j] == 0:
                continue
            success = createGroups(i, j)

            clearDoubles(success)

    # Second try on groups

    # O FOR DO PYTHON É TÃO BOSTA QUE RETIRAR UM ELEMENTO DO ITERABLE VAI FAZER COM QUE A
    # VARIÁVEL DE CONTROLE ADIANTE UMA CASA
    singleGroups = [x for x in groups if len(x) == 1]

    for e in singleGroups:

        if e not in groups:
            continue

        success = createGroups(e[0][0], e[0][1], False)

        clearDoubles(success)

    clearSingles()

    # Not make pairs based on the ones who already got a group
    # Pair checking

    for i in range(4):
        for j in range(2):
            if (i, j) in touched1s or mapa[i][j] == 0:
                continue
            success = createPairs(i, j)

            clearDoubles(success)

    # Second try on pair checking
    singleGroups = [x for x in groups if len(x) == 1]

    for e in singleGroups:
        if e not in groups:
            continue

        success = createPairs(e[0][0], e[0][1], False)

        clearDoubles(success)


def createGroups(i: int, j: int, toogleTouch: bool = True):

    global groups

    long_line = {mapa[k][j]
                 if (k, j) not in touched1s or not toogleTouch
                 else 0
                 for k in range(4)
                 }

    if checkHasOnlyOnes(long_line):
        group = [(m, j) for m in range(4)]

        touched1s.extend(group)
        groups.append(group)
        return True

    # Check 2x2

    _2x2 = {mapa[cycleY(i + k)][cycleX(j + l)]
            if ((cycleY(i + k), cycleX(j + l)) not in touched1s or not toogleTouch)
            else 0
            for k in range(2) for l in range(2)
            }

    if checkHasOnlyOnes(_2x2):
        group = [(cycleY(i + k), cycleX(j + l))
                 for k in range(2) for l in range(2)]

        touched1s.extend(group)
        groups.append(group)
        return True

    neg_2x2 = {mapa[cycleY(i - k)][cycleX(j - l)]
               if ((cycleY(i - k), cycleX(j - l)) not in touched1s or not toogleTouch)
               else 0
               for k in range(2) for l in range(2)
               }

    if checkHasOnlyOnes(neg_2x2):
        group = [(cycleY(i - k), cycleX(j - l))
                 for k in range(2) for l in range(2)]

        touched1s.extend(group)
        groups.append(group)
        return True

    single = [(i, j)]

    # Else, just make it lonely
    if (single not in groups):
        groups.append(single)
    return False


def createPairs(i: int, j: int, toogleTouch: bool = True):

    global groups

    if (mapa[cycleY(i - 1)][j] == 1 and ((cycleY(i - 1), j) not in touched1s or not toogleTouch)
        and not
        (
            (mapa[cycleY(i - 2)][j] == 1 and (cycleY(i - 2), j) not in touched1s)
        and (mapa[i][cycleX(j - 1)] == 1 and (i, cycleX(j) - 1) not in touched1s)
    )
    ):

        pair = [(i, j), (cycleY(i - 1), j)]

        touched1s.extend(pair)
        groups.append(pair)
        return True

    # Lower vertical
    if (mapa[cycleY(i + 1)][j] == 1 and ((cycleY(i + 1), j) not in touched1s or not toogleTouch)
            and not
            (
                (mapa[cycleY(i + 2)][j] ==
                 1 and (cycleY(i + 2), j) not in touched1s)
        and (mapa[i][cycleX(j + 1)] == 1 and (i, cycleX(j) + 1) not in touched1s)
    )
    ):

        pair = [(i, j), (cycleY(i + 1), j)]

        touched1s.extend(pair)
        groups.append(pair)
        return True

    # Horizontal
    if (mapa[i][cycleX(j + 1)] == 1 and ((cycleY(i + 1), j) not in touched1s or not toogleTouch)):
        pair = [(i, j), (i, cycleX(j + 1))]

        touched1s.extend(pair)
        groups.append(pair)
        return True

    single = [(i, j)]

    # Else, just make it lonely
    if (single not in groups):
        groups.append(single)

    return False


def clearSingles():
    global groups

    for e in groups:
        if len(e) == 1:
            groups.remove(e)


def clearDoubles(success: bool):

    global groups

    if success:
        for tupla in groups[-1]:
            if [tupla] in groups:
                groups.remove([tupla])


def getCoordsOnTerm(A: bool, B: bool, C: bool):

    global identifiers

    _A = ("A" if A else "!A")
    _B = ("B" if B else "!B")
    _C = ("C" if C else "!C")

    term_for_test = _A + _B + _C

    for line in range(len(identifiers)):
        for col in range(len(identifiers[line])):
            currentTerm = "".join(identifiers[line][col])
            if (term_for_test == currentTerm):
                return (line, col)


main()
