#!/usr/bin/env python
import numpy as np
from random import randint
from point import Point

def mapRandomizer(gridX, gridY, gridZ, min, obstacles, goals):
    occ_grid = np.zeros((gridX, gridY, gridZ))
    objectives = []
    for i in range(obstacles):
        minX = randint(0, gridX-min)
        maxX = randint(minX, gridX-1)

        minY = randint(0, gridY-min)
        maxY = randint(minY, gridY-1)

        minZ = randint(0, gridZ-min)
        maxZ = randint(minZ, gridZ-1)
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    occ_grid[x][y][z] = 1

    while len(objectives) < goals:
        x = randint(0,gridX)
        y = randint(0,gridY)
        z = randint(0,gridZ)
        if occ_grid[x][y][z] == 0:
            occ_grid[x][y][z] == 1 # temporarily so that we don't select the same point twice
            objectives.append(Point(x,y,z))
    for i in range(goals):
        occ_grid[objectives[i].x][objectives[i].y][objectives[i].z] = 0

    return occ_grid, objectives

def mapPseudoRandomizer(gridX, gridY, gridZ, thickness, obstacles, goals):
    occ_grid = np.zeros((gridX, gridY, gridZ))
    objectives = []

    x_ = []
    y_ = []
    z_ = []

    for i in range(obstacles):
        ry = randint(0,gridY-thickness-1)
        rz = randint(0,gridZ-thickness-1)
        for j in range(gridX-1):
            for k in range(ry, ry+thickness):
                for l in range(rz, rz+thickness):
                    occ_grid[j][k][l] = 1

    for i in range(obstacles):
        rx = randint(0,gridY-thickness-1)
        rz = randint(0,gridZ-thickness-1)
        for j in range(gridY-1):
            for k in range(rx, rx+thickness):
                for l in range(rz, rz+thickness):
                    occ_grid[k][j][l] = 1

    for i in range(obstacles):
        rx = randint(0,gridX-thickness-1)
        ry = randint(0,gridY-thickness-1)
        for j in range(gridX-1):
            for k in range(rx, rx+thickness):
                for l in range(ry, ry+thickness):
                    occ_grid[k][l][j] = 1

    while len(objectives) < goals:
        x = randint(0,gridX-1)
        y = randint(0,gridY-1)
        z = randint(0,gridZ-1)
        if occ_grid[x][y][z] == 0:
            occ_grid[x][y][z] == 1 # temporarily so that we don't select the same point twice
            objectives.append(Point(x,y,z))
    for i in range(goals):
        occ_grid[objectives[i].x][objectives[i].y][objectives[i].z] = 0

    s_p = Point(randint(0,gridX-1), randint(0,gridZ-1), randint(0,gridZ-1))
    while occ_grid[s_p.x][s_p.y][s_p.z] > 0:
        s_p = Point(randint(0,gridX-1), randint(0,gridZ-1), randint(0,gridZ-1))

    return occ_grid, objectives, s_p

def mapExample():
    gridX = 100
    gridY = 100
    gridZ = 100
    occ_grid = np.zeros((gridX, gridY, gridZ))
    objectives = []
    for i in range(20,30):
        for j in range(40, 50):
            for k in range(10, 15):
                occ_grid[i][j][k] = 1
    for i in range(0,gridX-1):
        for j in range(gridY/2-2, gridY/2+2):
            for k in range(80, 85):
                occ_grid[i][j][k] = 1
    for i in range(0,gridX-1):
        for j in range(gridY/2-20, gridY/2-10):
            for k in range(30, 35):
                occ_grid[i][j][k] = 1
    for i in range(30,35):
        for j in range(0, gridY-1):
            for k in range(50, 60):
                occ_grid[i][j][k] = 1
    for i in range(75,80):
        for j in range(80, 85):
            for k in range(0, gridZ-1):
                occ_grid[i][j][k] = 1

    objectives.append(Point(10,30,50))
    objectives.append(Point(70,90,5))
    objectives.append(Point(90,30,80))

    return occ_grid, objectives


