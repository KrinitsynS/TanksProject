from random import randint

def sum_living_points(world, i, j, live = 1, corners = 1):
    s = 0
    if i > 0:
        if live == world[i - 1][j]:
            s += 1
    if i < len(world) - 1:
        if live == world[i + 1][j]:
            s += 1
    if j > 0:
        if live == world[i][j - 1]:
            s += 1
    if j < len(world[0]) - 1:
        if live == world[i][j + 1]:
            s += 1
    if corners:
        if i > 0 and j > 0:
            if live == world[i - 1][j - 1]:
                s += 1
        if i > 0 and j < len(world[0]) - 1:
            if live == world[i - 1][j + 1]:
                s += 1
        if i < len(world) - 1 and j > 0:
            if live == world[i + 1][j - 1]:
                s += 1
        if i < len(world) - 1 and j < len(world[0]) - 1:
            if live == world[i + 1][j + 1]:
                s += 1
    return s


def generation_world(gen, world, k1, k2):
    for t in range(gen):
        for i in range(len(world)):
            for j in range(len(world[0])):
                s = sum_living_points(world, i, j, k2)
                if world[i][j] == k1 and s in [3, 6, 7, 8]:
                    world[i][j] = k2
                elif world[i][j] == k2 and s not in [3, 4, 6, 7, 8]:
                    world[i][j] = k1
    return world


def walls(world, frequency = 20):
    for i in range(len(world) - 8):
        for j in range(len(world[0]) - 8):
            if world[i][j] == 1:
                if randint(0, frequency) == 1:
                    world[i][j] = 4
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j] == 1:
                s1 = sum_living_points(world, i, j, 4, 0)
                s2 = sum_living_points(world, i, j, 4, 1)
                if s1 == s2 and s1 > 0 and randint(0, 1) == 1:
                    world[i][j] = 4
    return world


def forest_generation(gen, world):
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j] == 1:
                if randint(0, 1) == 1:
                    world[i][j] = 2
    return generation_world(GEN, world, 1, 2)


def coast(gen, world):
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j] == 1 or world[i][j] == 2:
                s1 = sum_living_points(world, i, j, 0)
                if s1 != 0:
                    world[i][j] = 3
            else:
                s2 = sum_living_points(world, i, j, 1)
                s2 += sum_living_points(world, i, j, 2)
                if s2 != 0 and randint(0, 3) == 1:
                    world[i][j] = 3
    return world


GEN = 100
N = 50
M = 100
def gen_all(GEN = 100, N = 50, M = 100):
    #сами острова
    world = [[randint(0, 1) for j in range(M)] for i in range(N)]
    world = generation_world(GEN, world, 0, 1)
    #леса
    world = forest_generation(GEN, world)
    #берега
    world = coast(GEN, world)
    #стены
    world = walls(world)
    
    #запись в файл (вечная)
    f = open('map_world.txt', 'w')
    for i in range(N):
        for j in range(M):
            f.write(str(world[i][j]))
        f.write('\n')
    f.close()

'''
забавный факт:
правила клеточного автомата день ночь очень хорошо подходят для генерации мира
'''
