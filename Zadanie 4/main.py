import random
import math
#import numpy as np
import matplotlib.pyplot as plt
import time


zafarbene_body_1 = []
zafarbene_body_3 = []
zafarbene_body_7 = []
zafarbene_body_15 = []

class Bod:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


"""
R: [500, 600], [900, 2000], [3200, 2800], [2500, 1600] a [3000, 3600]

G: [9500, 600], [+9100, 2000], [+6800, 2600], [+7500, 1600] a [+7000, 3600]

B: [500, +9400], [900, +8000], [3200, +7400], [2500, +8400] a [3000, +6400]

P: [+9500, +9400], [+9100, +8000], [+6800, +7400], [+7500, +8400] a [+7000, +6400]

 R body by mali byť generované s 99% pravdepodobnosťou s X < 5500 a Y < 5500
 G body by mali byť generované s 99% pravdepodobnosťou s X > 4500 a Y < 5500
 B body by mali byť generované s 99% pravdepodobnosťou s X < 5500 a Y > 4500
 P body by mali byť generované s 99% pravdepodobnosťou s X > 4500 a Y > 4500
"""


def getHexColor(color):     # farba na plotovanie cez matplotlib
    if color == "R":
        return '#FF0000'
    elif color == "G":
        return '#00FF00'
    elif color == "B":
        return '#0000FF'
    elif color == "P":
        return '#7E2F8E'


def add_to_priestor(X, Y, color):
    global MAP
    global zafarbene_body_1
    MAP[X][Y] = color
    # add initial points to all lists
    zafarbene_body_1.append(Bod(X, Y, color))
    zafarbene_body_3.append(Bod(X, Y, color))
    zafarbene_body_7.append(Bod(X, Y, color))
    zafarbene_body_15.append(Bod(X, Y, color))

def create_training_data():
    # red
    add_to_priestor(500, 600, "R")
    add_to_priestor(900, 2000, "R")
    add_to_priestor(3200, 2800, "R")
    add_to_priestor(2500, 1600, "R")
    add_to_priestor(3000, 3600, "R")
    # green
    add_to_priestor(9500, 600, "G")
    add_to_priestor(9100, 2000, "G")
    add_to_priestor(6800, 2600, "G")
    add_to_priestor(7500, 1600, "G")
    add_to_priestor(7000, 3600, "G")
    # blue
    add_to_priestor(500, 9400, "B")
    add_to_priestor(900, 8000, "B")
    add_to_priestor(3200, 7400, "B")
    add_to_priestor(2500, 8400, "B")
    add_to_priestor(3000, 6400, "B")
    # purple
    add_to_priestor(9500, 9400, "P")
    add_to_priestor(9100, 8000, "P")
    add_to_priestor(6800, 7400, "P")
    add_to_priestor(7500, 8400, "P")
    add_to_priestor(7000, 6400, "P")


def k_smallest_values(k, list):    # find k smallest values in list, ex. [(356, "r"), (841, "g"), (22,"r")] with key [0]
    k_smallest = []
    ignored_elements = []
    for i in range(k):
        min = (99999, "")
        for element in list:
            if element[0] < min[0] and (element not in ignored_elements):
                min = element
        k_smallest.append(min)
        ignored_elements.append(min)
    return k_smallest


def classify_forEach_k(X, Y):
    color_1 = classify(X, Y, 1, zafarbene_body_1)
    color_3 = classify(X, Y, 3, zafarbene_body_3)
    color_7 = classify(X, Y, 7, zafarbene_body_7)
    color_15 = classify(X, Y, 15, zafarbene_body_15)

    zafarbene_body_1.append(Bod(X, Y, color_1))
    zafarbene_body_3.append(Bod(X, Y, color_3))
    zafarbene_body_7.append(Bod(X, Y, color_7))
    zafarbene_body_15.append(Bod(X, Y, color_15))

    list_of_colors = [color_1, color_3, color_7, color_15]
    return list_of_colors

def classify(X, Y, k, pole_zafarbene):
    distances_list = []     # list, do ktoreho si ulozim vsetky vzdialenosti bodov
    zafarbene_body = pole_zafarbene

    # euklidovska vzdialenost vypocitana pre kazdy bod (CURRENT BOD od vsetkych ostatnych postupne, do listu)
    for point in zafarbene_body:
        euclidean_distance = math.sqrt( ((X - point.x)**2) + ((Y - point.y)**2) )
        color_of_point = point.color
        distances_list.append((euclidean_distance, color_of_point))     # tuple with 2 parts

    k_smallest = k_smallest_values(k, distances_list)
    r_count = g_count = b_count = p_count = 0
    maximum = (0, "")
    for point in k_smallest:
        if point[1] == "R":
            r_count += 1
            if maximum[0] < r_count:
                maximum = (r_count,"R")
        elif point[1] == "G":
            g_count += 1
            if maximum[0] < g_count:
                maximum = (g_count,"G")
        elif point[1] == "B":
            b_count += 1
            if maximum[0] < b_count:
                maximum = (b_count,"B")
        elif point[1] == "P":
            p_count += 1
            if maximum[0] < p_count:
                maximum = (p_count,"P")
    classified_color = maximum[1]
    return classified_color


def urci_chybovost(og_color, classified_colors, chybovost):     # vypocita uspesnost pre farby z k
    for i in range(4):
        if classified_colors[i] != og_color:
            chybovost[i] += 1
    return chybovost


EMPTY_SLOT = '0'        # nezafarbene miesto v poli
MAP = [[EMPTY_SLOT for x in range(10000)] for y in range(10000)]         # 10 000 x 10 000
create_training_data()

points_per_color = 1250
pole_k = [1, 3, 7, 15]

# plt canvas
fig, ax = plt.subplots(2, 2)
PLT_TITLE = "Pocet bodov: "+str(points_per_color*4)
plt.suptitle(PLT_TITLE)

print("Map initialized, ",end="")
chyby = 0
print("starting clock")
t_start = time.time()
chybovost = [0, 0, 0, 0]

for i in range(points_per_color + 1):     # 0 - points_per_color; (1 red -> 1 green -> 1 blue -> 1 purple) -> repeat
    # generate red
    probability = random.randint(1, 100)
    if probability < 99:    # ak vysla 99% pravdepodobnost, generujeme v stvorci tejto farby
        og_color = "R"
        point_x = random.randint(0, 5500)
        point_y = random.randint(0, 5500)
        while MAP[point_x][point_y] != EMPTY_SLOT:      # ak by bol duplikat
            point_x = random.randint(0, 5500)
            point_y = random.randint(0, 5500)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]     # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)
    elif probability == 100:  # trafilo 1%, bod je generovany v celom poli
        og_color = "R"
        point_x = random.randint(0, 9999)
        point_y = random.randint(0, 9999)
        while MAP[point_x][point_y] != EMPTY_SLOT:  # ak by bol duplikat
            point_x = random.randint(0, 9999)
            point_y = random.randint(0, 9999)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)

    # generate green
    probability = random.randint(1, 100)
    if probability < 99:  # ak vysla 99% pravdepodobnost, generujeme v stvorci tejto farby
        og_color = "G"
        point_x = random.randint(4500, 9999)
        point_y = random.randint(0, 5500)
        while MAP[point_x][point_y] != EMPTY_SLOT:  # ak by bol duplikat
            point_x = random.randint(4500, 9999)
            point_y = random.randint(0, 5500)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)
    elif probability == 100:  # trafilo 1%, bod je generovany v celom poli
        og_color = "G"
        point_x = random.randint(0, 9999)
        point_y = random.randint(0, 9999)
        while MAP[point_x][point_y] != EMPTY_SLOT:  # ak by bol duplikat
            point_x = random.randint(0, 9999)
            point_y = random.randint(0, 9999)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)

    # generate blue
    probability = random.randint(1, 100)
    if probability < 99:  # ak vysla 99% pravdepodobnost, generujeme v stvorci tejto farby
        og_color = "B"
        point_x = random.randint(0, 5500)
        point_y = random.randint(4500, 9999)
        while MAP[point_x][point_y] != EMPTY_SLOT:  # ak by bol duplikat
            point_x = random.randint(0, 5500)
            point_y = random.randint(4500, 9999)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)
    elif probability == 100:  # trafilo 1%, bod je generovany v celom poli
        og_color = "B"
        point_x = random.randint(0, 9999)
        point_y = random.randint(0, 9999)
        while MAP[point_x][point_y] != EMPTY_SLOT:  # ak by bol duplikat
            point_x = random.randint(0, 9999)
            point_y = random.randint(0, 9999)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)

    # generate purple
    probability = random.randint(1, 100)
    if probability < 99:
        og_color = "P"
        point_x = random.randint(4500, 9999)
        point_y = random.randint(4500, 9999)
        while MAP[point_x][point_y] != EMPTY_SLOT:
            point_x = random.randint(4500, 9999)
            point_y = random.randint(4500, 9999)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)
    elif probability == 100:  # trafilo 1%, bod je generovany v celom poli
        og_color = "P"
        point_x = random.randint(0, 9999)
        point_y = random.randint(0, 9999)
        while MAP[point_x][point_y] != EMPTY_SLOT:  # ak by bol duplikat
            point_x = random.randint(0, 9999)
            point_y = random.randint(0, 9999)
        color_list = classify_forEach_k(point_x, point_y)
        MAP[point_x][point_y] = color_list[0]  # zaradenie do mapy
        chybovost = urci_chybovost(og_color, color_list, chybovost)

    if (i % 500 == 0) and i != 0:
        print(">500 points generated")


t_end = time.time()
t_result = float(t_end - t_start)
print("done, time elapsed:",round(t_result, 4),"s ...plotting")
zu = len(zafarbene_body_1)
print(points_per_color*4, "bodov  vygenerovanych,", points_per_color, "per color")
print("pocet chyb:"
      "\nK=1:",chybovost[0],"->", round(((zu-chybovost[0])/zu) * 100),"% uspesnost"
      "\nK=3:",chybovost[1],"->", round(((zu-chybovost[1])/zu) * 100),"% uspesnost"
      "\nK=7:",chybovost[2],"->", round(((zu-chybovost[2])/zu) * 100),"% uspesnost"
      "\nK=15:",chybovost[3],"->", round(((zu-chybovost[3])/zu) * 100),"% uspesnost"
      )

for data in zafarbene_body_1:
    ax[0, 0].plot(data.x, data.y, marker=".", color=getHexColor(data.color))
    ax[0, 0].set_title("K = 1")
for data in zafarbene_body_3:
    ax[0, 1].plot(data.x, data.y, marker=".", color=getHexColor(data.color))
    ax[0, 1].set_title("K = 3")
for data in zafarbene_body_7:
    ax[1, 0].plot(data.x, data.y, marker=".", color=getHexColor(data.color))
    ax[1, 0].set_title("K = 7")
for data in zafarbene_body_15:
    ax[1, 1].plot(data.x, data.y, marker=".", color=getHexColor(data.color))
    ax[1, 1].set_title("K = 15")


fig.tight_layout()
plt.savefig("knn")

#plt.show()

print("END")
