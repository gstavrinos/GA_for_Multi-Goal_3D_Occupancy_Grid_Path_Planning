#!/usr/bin/env python

class Point(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.z)+"]"

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y and self.z == p.z

    def __hash__(self):
        return hash(str(self))
