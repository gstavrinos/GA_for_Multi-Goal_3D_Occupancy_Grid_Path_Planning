#!/usr/bin/env python
import copy
from random import randint, shuffle
from point import Point
from path import Path
from numpy import random
from common_point import CommonPoint

debugging = False
#debugging = True

class GeneticAlgorithm(object):
    def __init__(self, population, sigma, mr, ts, sr): # maybe I should add a tournament size, and number of children (?)
        self.population = population
        self.std = sigma
        self.mutation_rate = mr
        self.tournament_size = ts
        self.smoothing_rate = sr
        #self.wall_avoidance_rate = war


    def initialRandomSolutions(self, starting_point, objectives):
        solutions = []
        for i in range(self.population):
            objectives_ = objectives[:]
            prev_x = starting_point.x
            prev_y = starting_point.y
            prev_z = starting_point.z
            total_obj = len(objectives_)
            tmp = []
            tmp.append(starting_point)
            shuffle(objectives_)
            while total_obj > 0:
                allowed_point = False
                next_x = 0
                next_y = 0
                next_z = 0
                minx = prev_x
                maxx = prev_x
                for ii in range(total_obj):
                    if objectives_[0].x < prev_x:
                        minx = prev_x - 1
                    if objectives_[0].x > prev_x:
                        maxx = prev_x + 1

                miny = prev_y
                maxy = prev_y
                for ii in range(total_obj):
                    if objectives_[0].y < prev_y:
                        miny = prev_y - 1
                    if objectives_[0].y > prev_y:
                        maxy = prev_y + 1

                minz = prev_z
                maxz = prev_z
                for ii in range(total_obj):
                    if objectives_[0].z < prev_z:
                        minz = prev_z - 1
                    if objectives_[0].z > prev_z:
                        maxz = prev_z + 1

                available_x = range(minx, maxx+1)
                available_y = range(miny, maxy+1)
                available_z = range(minz, maxz+1)

                while not allowed_point:
                    next_x = available_x[randint(0,len(available_x)-1)]
                    next_y = available_y[randint(0,len(available_y)-1)]
                    next_z = available_z[randint(0,len(available_z)-1)]

                    if not (prev_x == next_x and prev_y == next_y and prev_z == next_z):
                        allowed_point = True

                prev_x = next_x
                prev_y = next_y
                prev_z = next_z
                tmp.append(Point(next_x, next_y, next_z))
                for o in range(total_obj):
                    if next_x == objectives_[0].x and next_y == objectives_[0].y and next_z == objectives_[0].z:
                        total_obj -= 1
                        del objectives_[0]
                        if total_obj > 0:
                            shuffle(objectives_)
                        break
            solutions.append(Path(tmp))
        return solutions


    def crossover(self, path1, path2, objectives):

        tmp = list(set(path1).intersection(path2))
        common_points = []
        for c in tmp:
            common_points.append(CommonPoint(c, path1.index(c), path2.index(c)))
        tmp = []
        common_points.sort(key=lambda x:x.path2_index)

        start_index = 0
        streak = False
        common_points_ = common_points[:]

        i = 1
        # Eliminate consecutive common points
        while i+1 < len(common_points):
            for j in range(i, len(common_points)):
                if common_points[j].path2_index - common_points[i].path2_index <= 1:
                    if j+1 < len(common_points):
                        # Keep the last point of the consecutive points
                        if common_points[j+1].path2_index - common_points[j].path2_index == 1:
                            if common_points[j].point not in objectives:
                                common_points_.remove(common_points[j])
                    i = j
                else:
                    i += 1
                    break

        common_points_1 = common_points_[:]
        common_points_1.sort(key=lambda x:x.path1_index)

        c_tmp = common_points_[:]
        c1_tmp = common_points_1[:]

        if debugging:
            print 'PREVIOUS!'
            for c in common_points_:
                if c.point in objectives:
                    print 'OBJECTIVE!'
                print c
            print '--------------'

        # Eliminate points that are not in the same order (thus, not part of the same sub-path)
        for tc in range(1, len(c_tmp)):
            keep_it = False
            tc1 = c1_tmp.index(c_tmp[tc])
            if c_tmp[tc-1] == c1_tmp[tc1-1]:
                if tc + 1 < len(c_tmp) and tc1 + 1 < len(c1_tmp):
                    if c_tmp[tc+1] == c1_tmp[tc1+1] and c_tmp[tc-1] in common_points_:
                        keep_it = True
            if not keep_it:
                del common_points_[common_points_.index(c_tmp[tc])]
                del common_points_1[common_points_1.index(c1_tmp[tc1])]

        if debugging:
            for c in common_points_:
                if c.point in objectives:
                    print 'OBJECTIVE!'
                print c
            print '--------------'
        

        crossover_point = 0
        if len(common_points_) > 1:
            crossover_point = randint(0, len(common_points_)-1)
            while common_points_[crossover_point] == common_points_1[-1]:
                crossover_point = randint(0, len(common_points_)-2)

        crossover_stop = common_points_1.index(common_points_[crossover_point])+1

        first_half = copy.deepcopy(path2[:common_points_[crossover_point].path2_index])
        new_part = []
        if crossover_stop < len(common_points_1):
            new_part = copy.deepcopy(path1[common_points_[crossover_point].path1_index:common_points_1[crossover_stop].path1_index+1])
        else:
            new_part = copy.deepcopy(path1[common_points_[crossover_point].path1_index:])
        second_half = []
        if crossover_stop < len(common_points_1):
            if not common_points_1[crossover_stop].point == path1[-1]:
                second_half = copy.deepcopy(path2[common_points_1[crossover_stop].path2_index+1:])
        new_path = first_half + new_part + second_half

        if debugging:
            print crossover_point
            print crossover_stop
            print new_path.count(objectives[0])
            print new_path.count(objectives[1])
            print new_path.count(objectives[2])

        return new_path


    def mutation(self, path, gridX, gridY, gridZ, objectives):
        new_path = copy.deepcopy(path)
        for i in range(1,len(new_path)):
            if randint(0,100) > 100-self.mutation_rate and new_path[i] not in objectives:
                p = Point(int(random.normal(new_path[i].x, self.std)), int(random.normal(new_path[i].y, self.std)), int(random.normal(new_path[i].z, self.std)))

                if p.x < 0:
                    p.x = 0
                elif p.x >= gridX:
                    p.x = gridX - 1

                if p.y < 0:
                    p.y = 0
                elif p.y >= gridY:
                    p.y = gridY - 1

                if p.z < 0:
                    p.z = 0
                elif p.z >= gridZ:
                    p.z = gridZ - 1

                if p not in new_path:
                    new_path[i].x = p.x
                    new_path[i].y = p.y
                    new_path[i].z = p.z

        return new_path


    def smoothing(self, path, objectives):
        new_path = copy.deepcopy(path)
        for i in range(1,len(new_path)-1):
            if randint(0,100) > 100-self.smoothing_rate and new_path[i] not in objectives:
                p = Point(int((new_path[i-1].x + new_path[i+1].x)/2),int((new_path[i-1].y + new_path[i+1].y)/2), int((new_path[i-1].z + new_path[i+1].z)/2))
                
                
                if p not in new_path:
                    new_path[i].x = p.x
                    new_path[i].y = p.y
                    new_path[i].z = p.z

        return new_path

# TODO create a wall avoiding function for our children!
    '''
    def wall_avoidance(self, path, occ_grid, gridX, gridY, gridZ, objectives):
        new_path = copy.deepcopy(path)
        i = 0
        p = Point(0, 0, 0)
        while i < len(new_path)-1:
            if randint(0,100) > 100-self.wall_avoidance_rate and new_path[i] not in objectives:
                start_index = 0
                p.x = path[i].x
                p.y = path[i].y
                p.z = path[i].z
                first_time = True
                while occ_grid[p.x][p.y][p.z] > 0 and i+1 < len(new_path):
                    if first_time:
                        start_index = i
                        first_time = False
                    i += 1
                    p.x = path[i].x
                    p.y = path[i].y
                    p.z = path[i].z
                end_index = i - 1
                if start_index > 0:
                    tmp = []
                    for i in range(start_index, end_index+1):

                
                if p not in new_path:
                    new_path[i].x = p.x
                    new_path[i].y = p.y
                    new_path[i].z = p.z

        return new_path
    '''

    def tournament_selection(self, paths):
        winner_index = 0
        best_fitness = -9999999

        for i in range(self.tournament_size):
            rand_index = randint(0, len(paths)-1)
            if paths[rand_index].fitness > best_fitness:
                best_fitness = paths[rand_index].fitness
                winner_index = rand_index

        return winner_index


    def fitness(self, path, occ_grid):
        fitness_ = 0

        for point in path:
            # The closer to an obstacle, the more points lost
            fitness_ += occ_grid[point.x][point.y][point.z] * 10

        fitness_ += len(path)

        return 1.0 / fitness_

