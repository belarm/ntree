#!/usr/bin/env python3

import numpy as np

MAX_DIM = 2**10

e = [2 ** n for n in range(MAX_DIM)]

class ntree(object):
    def __init__(self, minimums, maximums, value=None):
        '''Given the minimum and maximum co-ordinates of an n-dimensional rectangular
        prism, returns a 2**n-tree for sorting points in that space'''
        # There is no intrinsic difference between these, save possibly for the 'sign'
        # of the implied basis vectors, which we should be able to abstract away.
        self.white_corner = minimums
        self.black_corner = maximums

        self.center = minimums + maximums / 2
        self.children = {}
        self.value = value

    @property
    def val(self):
        if self.value is not None:
            return self.value
        else:
            # TODO: We need to return an aggregate of self.children here
            return None

    def route(self, point):
        d = len(point)

        if d > len(self.center):
            # Point is of higher dimensionality than our center; extend center
            shortby = d - len(self.center)
            # convert center to list and use python's list concatenation to lengthen it,
            # then convert back to numpy array
            center = np.array(self.center.tolist() + shortby * [0])
        elif d < len(self.center):
            # Point is of lower dimensionality than our center; contract center
            center = self.center[0:d]
        else:
            # Hey, we got a point of the same dimension as us! Neat!
            center = self.center
        # Grab the relevant portion of our basis diagonal
        basis = e[0:d]

        # We'll need to be able to re-order basis here.
        # NO WE WON'T! Instead, we can change the comparator function used when sorting keys of self.children
        return np.dot((point > center), basis)


n = ntree(np.array([0,0,0,0]),np.array([15,15,15,15]))
# Find the position of a 12-d point in layer 1 of n:
print(n.route(np.array([12,9,9,0,0,0,0,1,0,0,0,1])))
print(n.val)
