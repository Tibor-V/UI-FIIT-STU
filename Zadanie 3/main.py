from random import randrange, shuffle


"""
NOTE: algoritmus funguje len na zakladnej zahradke!
"""

max_fitness = 114   # na default zahrade; pocet_policok - pocet_kamenov
up, left, down, right = (-1, 0), (0, -1), (1, 0), (0, 1)
rock = -1
nasledovnik_number = 0


class Monk:
    def __init__(self, directions, entering_tiles):
        self.fitness = 0
        self.directions = directions
        self.entering_tiles = entering_tiles


def createGarden():    # defaultna zahrada zo zadania
    garden = [[0 for x in range(12)] for y in range(10)]    # inicializuje na 0
    global rock
    garden[2][1] = rock
    garden[4][2] = rock
    garden[3][4] = rock
    garden[1][5] = rock
    garden[6][8] = rock
    garden[6][9] = rock
    return garden


def load_entering_tiles():
    entering_tiles = []

    #nacita pozicie okrajovych policok do listu
    x = y = 0
    pos = (x, y)
    for y in range(y,12):     # horny kraj
        pos = (x,y)
        entering_tiles.append(pos)
    x, y = 9, 0
    for y in range(y,12):     # dolny kraj
        pos = (x,y)
        entering_tiles.append(pos)
    x, y = 1, 0
    for x in range(x,9):     # lavy kraj
        pos = (x,y)
        entering_tiles.append(pos)
    x, y = 1, 11
    for x in range(x,9):     # pravy kraj
        pos = (x,y)
        entering_tiles.append(pos)

    return entering_tiles


def createMonk():
    directions = [up, left, down, right]
    shuffle(directions)

    entering_tiles = load_entering_tiles()
    shuffle(entering_tiles)

    first_monk = Monk(directions, entering_tiles)
    return first_monk


def is_in_corner(position):   # ak sa nachadza v rohu, vrati True; position bude v tuple (x, y)
    x, y = position[0], position[1]
    if x == 0 and (y == 0 or y == 11):
        return True
    elif x == 9 and (y == 0 or y == 11):
        return True
    else:
        return False


def is_in_bounds(x, y):
    return False if (x < 0 or x > 9 or y < 0 or y > 11) else True


def is_on_border(x, y):
    return True if (x == 0 or x == 9 or y == 0 or y == 11) else False


def begin_from_corner(monk, tile_x, tile_y):
    direction_i = 0
    while True:
        if direction_i == 4:  # ked sme presli vsetky directions a nemame kam ist, game over
            return -1   # error, mnich skoncil

        new_x = tile_x + monk.directions[direction_i][0]
        new_y = tile_y + monk.directions[direction_i][1]

        if is_in_bounds(new_x, new_y):
            return monk.directions[direction_i]
        else:
            direction_i += 1
            continue


def print_direction(direction):
    if direction == (-1, 0):
        return "up"
    elif direction == (0, -1):
        return "left"
    elif direction == (1, 0):
        return "down"
    elif direction == (0, 1):
        return "right"
    else:
        return "DIRECTION_UNDEFINED"


def rake_garden(garden, monk):
    """
    dostanem starting position mnicha monk.entering_tiles[0], z toho zoberiem x a y, pozriem ci je roh,
        ak nie, tak direction je oproti stene, t.j. ak zacne na lavom okraji, ide do prava, ak na hornom, ide dole, atd.
        ak je, tak direction je prvy mozny smer zo sorted listu monk.directions
    teraz mam uz urceny smer, odkial mnich zacina. Pocas mnichoveho hrabania  policok na okraji sa upravuje
    monk.entering_tiles tak, ze sa odstrania z listu policka, ktore boli uz pohrabane, aj pri zaciatku noveho hrabania
    treba osetrit, aby sa odpocitalo.
    Pokracuje rovno v jeho smere, az dokial
        pride ku kraju a vyjde z neho, alebo
        narazi na kamen, cize musi zmenit direction. Pozrie sa do monk.directions a skusa, kam moze ist.
            Ak ma volnu aspon jednu cestu, vyberie tu, ktora je v monk.directions skorej
            Ak nema volnu ziadnu cestu, konci hrabanie mnicha a prechadza sa k generovaniu potomkov
    """
    global rock
    global max_fitness
    forbidden_tiles = []
    hrabanie_num = 0
    entering_tiles_i = 0        # index do monk.entering_tiles, posuva sa po pouziti v zahrade
    
    mnich_skoncil = False
    while True:
        # osetrenie toho, ze mnich nesmie zacat z policka, kde uz raz bol
        while monk.entering_tiles[entering_tiles_i] in forbidden_tiles:
            entering_tiles_i += 1   # preskoci vstup, skusa dalej
            if entering_tiles_i > 39:
                mnich_skoncil = 1
                break

        # ak sa mnich zasekol alebo vycerpal vsetky okrajove alebo presiel vsetky
        if mnich_skoncil or entering_tiles_i == 39 or monk.fitness == max_fitness:      # 39 je last index listu
            break

        tile_x = monk.entering_tiles[entering_tiles_i][0]
        tile_y = monk.entering_tiles[entering_tiles_i][1]

        # ak mnich nie je v rohu, ide smerom od steny
        if tile_x == 0 and not is_in_corner( (tile_x, tile_y) ):
            direction = down
        if tile_y == 0 and not is_in_corner( (tile_x, tile_y) ):
            direction = right
        if tile_x == 9 and not is_in_corner( (tile_x, tile_y) ):
            direction = up
        if tile_y == 11 and not is_in_corner( (tile_x, tile_y) ):
            direction = left

        # ak mnich je v rohu
        if is_in_corner((tile_x, tile_y)):
            r_value = begin_from_corner(monk, tile_x, tile_y)
            if r_value == -1:
                mnich_skoncil = True    # nema kam ist z rohu, zasekol sa
                break
            else:                       # else r_value je up, down, left or right
                direction = r_value
        entering_tiles_i += 1

        monk.fitness += 1   # lebo aj zaciatok je pohrabany

        direction_i = 0
        koniec_hrabania_flag = 0
        hrabanie_num += 1
        pohrabane_policka_riadok = 1
        garden[tile_x][tile_y] = hrabanie_num
        #print("zacina sa hrabanie:", hrabanie_num, "akt fitness:", monk.fitness)
        while 1:        # prechadzanie 1ho hrabania zahrady
            new_x = tile_x + direction[0]       # nemal by byt unreferenced
            new_y = tile_y + direction[1]

            # mnich narazil na kamen, urcuje kam sa otoci
            while not is_in_bounds(new_x, new_y) or garden[new_x][new_y] != 0:
                #print()
                if direction_i == 4:
                    mnich_skoncil = True
                    break   # mnich presiel moznosti otocenia ale uz neni kam, konci
                direction = monk.directions[direction_i]
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]
                if not is_in_bounds(new_x, new_y):  # ak by mnich vysiel zo zahrady otocenim
                    if pohrabane_policka_riadok > 1:    # ak uz nieco hrabal v tomto riadku, moze sa otocit von
                        new_x, new_y = tile_x, tile_y
                        break
                    direction_i += 1
                    continue
                direction_i += 1
            if mnich_skoncil:      # ak sa mnich nema uz kam otocit
                break
            direction_i = 0

            # ak je mnich u okraja a v dalsom kroku by vystupil zo zahrady
            if new_x == 0 and direction == up:
                koniec_hrabania_flag = 1
            if new_y == 0 and direction == left:
                koniec_hrabania_flag = 1
            if new_x == 9 and direction == down:
                koniec_hrabania_flag = 1
            if new_y == 11 and direction == right:
                koniec_hrabania_flag = 1

            # if new x neni kamen, prejde sem
            tile_x = new_x
            tile_y = new_y
            if garden[tile_x][tile_y] != hrabanie_num:
                garden[tile_x][tile_y] = hrabanie_num
                monk.fitness += 1
                pohrabane_policka_riadok += 1
            if is_on_border(tile_x, tile_y) and ((tile_x, tile_y) not in forbidden_tiles):
                forbidden_tiles.append((tile_x, tile_y))      # odstrani policko, na ktorom konci
            if koniec_hrabania_flag == 1 or monk.fitness == max_fitness:
                break
    return garden


def create_monk_nasledovnici(monk):       # 40 nasledovnikov z entering_tiles + 4 z directions == 44 total
    list_of_monks = []
    new_entering_tiles = monk.entering_tiles.copy()
    new_directions = monk.directions.copy()
    i = 0
    breakFlag = 0
    # vymienanie vstupnych policok mnicha, directions ostanu
    while breakFlag == 0:     # vygeneruju sa nasledovnici a swapuju sa hodnoty (1. s 2. (prvy nasledovnik), 2. s 3. (druhy) atd.
        if i == len(new_entering_tiles)-1:      # -1 lebo index; posledne policko s prvym polickom
            new_entering_tiles[i], new_entering_tiles[0] = new_entering_tiles[0], new_entering_tiles[i]
            breakFlag = 1
        else:
            new_entering_tiles[i], new_entering_tiles[i+1] = new_entering_tiles[i+1], new_entering_tiles[i]     # swap
        new_monk = Monk(monk.directions, new_entering_tiles)
        list_of_monks.append(new_monk)
        new_entering_tiles = monk.entering_tiles.copy()      # reset list do default
        i += 1
    # vymienanie directions mnicha, entering_tiles ostanu
    breakFlag = i = 0
    while breakFlag == 0:
        if i == len(new_directions)-1:
            new_directions[i], new_directions[0] = new_directions[0], new_directions[i]
            breakFlag = 1
        else:
            new_directions[i], new_directions[i+1] = new_directions[i+1], new_directions[i]
        new_monk = Monk(new_directions, monk.entering_tiles)
        list_of_monks.append(new_monk)
        new_directions = monk.directions.copy()
        i += 1

    global nasledovnik_number
    nasledovnik_number = 1
    # kazdy nasledovnik pohrabe zahradu na zistenie fitness
    for monk in list_of_monks:
        garden = createGarden()
        rake_garden(garden, monk)
        nasledovnik_number += 1
    print("\n\nvygenerovanych", len(list_of_monks), "nasledovnikov")
    for monk in list_of_monks:
        print(monk.fitness, "", end="")
    print()
    return list_of_monks


def fitnessInTabuList(monk, tabuList):  # if tabu list has monks with same fitness, disregard them all
    for genMonk in tabuList:
        if genMonk.fitness == monk.fitness:
            return True
    return False

def tabu_search(first_monk):
    maxTabuSize = 20
    nr_generations = 1
    min_fitness_monk = Monk((), ())         # umely mnich s 0 fitness; na porovnanie s mnichami v generacii

    bestCandidate = first_monk      # best monk in generation
    totalBest = first_monk          # max(parent_monk.fitness, bestCandidate.fitness)
    tabuList = []
    tabuList.append(first_monk)

    while nr_generations < 16 and totalBest.fitness != max_fitness:
        generation = create_monk_nasledovnici(bestCandidate)
        parentMonk = bestCandidate
        bestCandidate = min_fitness_monk
        best_candidate_is_from_curr_gen = False
        for monk in generation:
            if not (monk in tabuList) and not (fitnessInTabuList(monk, tabuList))  and (monk.fitness > bestCandidate.fitness) and (monk.fitness != parentMonk.fitness):
                bestCandidate = monk
                best_candidate_is_from_curr_gen = True
        if not bestCandidate in generation:     # ak vsetci nasledovnici su v tabu_list
            bestCandidate = generation[42]

        if bestCandidate.fitness > totalBest.fitness:
            totalBest = bestCandidate
        tabuList.append(bestCandidate)
        if len(tabuList) > maxTabuSize:
            tabuList.pop(0)
        print("\nBest Candidate from gen",nr_generations,": [",generation.index(bestCandidate),"](",bestCandidate.fitness,")",best_candidate_is_from_curr_gen)
        nr_generations += 1
        print("\ntabu list: ",end="")
        for element in tabuList:
            print(str(element.fitness)+" ",end="")
        print()
    return totalBest


def print_garden(garden):       # pomocna funkcia na prehladnejsi vypis zahrady
    for row in range(10):
        print("[",end="")
        for col in range(12):
            if garden[row][col] >= 0 and garden[row][col] < 10:
                print(" "+str(garden[row][col]),end="")
            else:
                print(str(garden[row][col]),end="")
            if col < 11:
                print(" ",end="")
        print("]")


def main():
    garden = createGarden()
    print("default garden: 12x10")
    print_garden(garden)

    first_monk = createMonk()
    rake_garden(garden, first_monk)

    best_monk = tabu_search(first_monk)
    print("\nBest Fitness found in N generations:", best_monk.fitness)

    #best_monk.fitness = 0
    #bestgarden = createGarden()
    #bestgarden = rake_garden(bestgarden, best_monk)
    #print("Zahrada najlepsieho mnicha:")
    #print_garden(bestgarden)


main()
