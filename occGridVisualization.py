#!/usr/bin/env python
from mayavi import mlab

figure = None
path_plot = None

def occGridVisualization(occ_grid, starting_point, objectives, path, first_path):
    x = []
    y = []
    z = []
    v = []
    objx = []
    objy = []
    objz = []
    pathx = []
    pathy = []
    pathz = []
    pathx_ = []
    pathy_ = []
    pathz_ = []

    for i in range(len(occ_grid)):
        for j in range(len(occ_grid[i])):
            for k in range(len(occ_grid[i][j])):
                if occ_grid[i][j][k] > 0:
                    x.append(i)
                    y.append(j)
                    z.append(k)
                    v.append(1 - occ_grid[i][j][k])

    for i in range(len(objectives)):
        objx.append(objectives[i].x)
        objy.append(objectives[i].y)
        objz.append(objectives[i].z)

    for i in range(len(path)):
        pathx.append(path[i].x)
        pathy.append(path[i].y)
        pathz.append(path[i].z)

    for i in range(len(first_path)):
        pathx_.append(first_path[i].x)
        pathy_.append(first_path[i].y)
        pathz_.append(first_path[i].z)

    figure = mlab.figure('Occupancy Grid', bgcolor=(1, 1, 1), fgcolor = (0.2, 0.2, 0.2))
    mlab.points3d(x, y, z, v, mode='cube', colormap='black-white', scale_mode='none', scale_factor='1')
    mlab.points3d(objx, objy, objz, mode='cube', color=(1, 0, 0), scale_mode='none', scale_factor='1')
    mlab.points3d(starting_point.x, starting_point.y, starting_point.z, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='1')
    mlab.axes(extent=[0, len(occ_grid), 0, len(occ_grid),0, len(occ_grid)])
    mlab.plot3d(pathx, pathy, pathz, color=(0, 0, 1))
    mlab.plot3d(pathx_, pathy_, pathz_, color=(0, 1, 0))
    #mlab.axes()
    mlab.show()

