import time

"""
Autor: Tibor Vanek
UI Zadanie 2 - Eulerov kon (Knight's tour) s Warnsdorffovym pravidlom a rekurzivnym DFS
Oktober 2021
"""

def createBoard(size, start):
    board = [[0 for x in range(size)] for y in range(size)]
    board[start[0]][start[1]] = 1       # nastavi 1 na zaciatocnu poziciu
    return board

def isInBounds(boardSize, position):
    x = position[0]
    y = position[1]
    if x < 0 or x >= boardSize or y < 0 or y >= boardSize:      # ak je mimo sachovnice
        return False
    return True        # else


def checkLegalSteps(board, boardSize, position):
    # vytiahnem X a Y poziciu z Tuple
    x = position[0]
    y = position[1]

    legal_steps = [                     # legalne tahy kona
        (1, 2), (1, -2), (2, 1), (2, -1),
        (-1, 2), (-1, -2), (-2, 1), (-2, -1),
    ]

    # vlozi do listu vsetky mozne kroky, ktore sa daju z tejto pozicie spravit
    possible_positions = []
    for step in legal_steps:
        new_x = x + step[0]
        new_y = y + step[1]
        if isInBounds(boardSize, (new_x, new_y)) and board[new_x][new_y] == 0:  # in bounds a ciel je nepreskumany
            possible_positions.append((new_x, new_y))

    return possible_positions


def getSortedOptions(board, boardSize, possible_positions):
    scores = []     # list listov
    for option in possible_positions:
        list_of_steps = checkLegalSteps(board, boardSize, option)
        score = [option, len(list_of_steps)]    # obsahuje poziciu ako tuple a pocet krokov z nej
        scores.append(score)
    scores = sorted(scores, key=lambda x: x[1])     # usporiadanie krokov od najmensieho, podla intu ([1]) v liste
    return scores


casovy_limit = 15        # v sekundach


def eulerovKon(board, boardSize, curPos, depth, startTime):
    global casovy_limit

    board[curPos[0]][curPos[1]] = depth     # oznacenie cesty kona

    if (time.time() - startTime) > casovy_limit:          # kontrola, ci sme presiahli limit vykonania v sekundach
        print("Time limit exceeded (", str(casovy_limit)+"s )")
        exit()

    if depth == (boardSize * boardSize):    # sme na konci, vypise cas a skonci
        print("-----------------")
        for line in board:
            print(line)
        print("-----------------")
        endTime = time.time()
        # obcas pri malych sachovniciach vypise cas 0.0 s, lebo to trva prilis kratko a zaokruhli sa
        print("Time elapsed:", float(endTime-startTime), "s")
        exit()    # success
    else:           # pokracuje
        possible_positions = checkLegalSteps(board, boardSize, curPos)  # list moznosti
        sorted_options = getSortedOptions(board, boardSize, possible_positions)  # zoradeny list od min. dalsich krokov
        for option in sorted_options:
            option = option[0]      # vytiahne tuple z listu
            eulerovKon(board, boardSize, option, depth+1, startTime)

        # ak som nepresiel celu sachovnicu, a nemam kam dalej ist, nastavim tuto poziciu za nenavstivenu a vynorim sa
        board[curPos[0]][curPos[1]] = 0

    print("-----------------")      # vypis stavu po vynoreni
    for line in board:
        print(line)
    print("-----------------")

def main():
    boardSize = 5   # velkost sachovnice
    start = (0,0)
    board = createBoard(boardSize, start)
    print(str(boardSize)+"x"+str(boardSize))    # vypis velkosti a zaciatocneho stavu
    for line in board:
        print(line)

    startTime = time.time()     # casovac;
    eulerovKon(board, boardSize, start, 1, startTime)


main()
