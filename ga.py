#!/usr/bin/env python
import numpy as np
from path import Path
from point import Point
import genetic_algorithm as ga
from quicksort import quickSort
from occGridVisualization import occGridVisualization
from map_tools import mapRandomizer, mapPseudoRandomizer, mapExample

path = []
gridX = 100
gridY = 100
gridZ = 100
thickness = 5
occ_grid = None
objectives = []
no_of_objectives = 5
obstacles_per_axis = 3
starting_point = Point(0,0,0)

if __name__ == "__main__":
    # Create a 3D Occupancy Grid
    print '\033[94m Generating random occupancy grid and objectives... \033[0m'
    occ_grid, objectives, starting_point = mapPseudoRandomizer(gridX, gridY, gridZ, thickness, obstacles_per_axis, no_of_objectives)

    alg = ga.GeneticAlgorithm(500, 0.00001, 5, 2, 40)

    print '\033[94m Generating random initial solutions... \033[0m'
    paths = alg.initialRandomSolutions(starting_point, objectives)

    max_generations = 25000 # We should better wait for convergence

    for p in range(len(paths)):
        paths[p].fitness = alg.fitness(paths[p].points, occ_grid)

    max_p = max(paths, key=lambda x:x.fitness)

    max_f = 0
    count = 0

    for i in range(max_generations):
        quickSort(paths)
        if max_f < paths[0].fitness:
            max_f = paths[0].fitness
            count = 0
            print '\033[94m Current maximum fitness:\033[0m\033[92m ' + str(max_f) + '\033[0m\033[94m, Generation:\033[0m\033[92m ' + str(i) +' \033[0m'
        else:
            count += 1
            if count >= 2000:
                # Looks like the algorithm converged (or won't ever converge!)
                break

        p1 = alg.tournament_selection(paths)
        p2 = alg.tournament_selection(paths)

        new_path = []
        # Always crossover (cr = 1)
        new_path1 = alg.crossover(paths[p1].points, paths[p2].points, objectives)
        new_path2 = alg.crossover(paths[p2].points, paths[p1].points, objectives)

        new_path1 = alg.mutation(new_path1, gridX, gridY, gridZ, objectives)
        new_path1 = alg.smoothing(new_path1, objectives)

        new_path2 = alg.mutation(new_path2, gridX, gridY, gridZ, objectives)
        new_path2 = alg.smoothing(new_path2, objectives)

        new_path1_ = Path(new_path1)
        new_path1_.fitness = alg.fitness(new_path1_.points, occ_grid)
        paths[-1] = new_path1_

        new_path2_ = Path(new_path2)
        new_path2_.fitness = alg.fitness(new_path2_.points, occ_grid)
        paths[-1] = new_path2_

    occGridVisualization(occ_grid, starting_point, objectives, paths[0].points, max_p.points)