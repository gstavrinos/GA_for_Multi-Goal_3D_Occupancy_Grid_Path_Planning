#!/usr/bin/env python

class CommonPoint(object):
    def __init__(self, point, path1_index=0, path2_index=0):
        self.point = point
        self.path1_index = path1_index
        self.path2_index = path2_index

    def __str__(self):
        return str(self.point)+" | "+str(self.path1_index) + " | " + str(self.path2_index)

    def __eq__(self, p):
        return self.point == p.point and self.path1_index == p.path1_index and self.path2_index == p.path2_index