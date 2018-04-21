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
        if len(minimums) != len(maximums):
            raise ValueError("Mimimums and maximums must be the same length(dimension)")
        self.minimums = minimums
        self.maximums = maximums

        self.center = (minimums + maximums) / 2
        self.radii = (maximums - minimums) / 2
        self.children = {}
        self._value = value

    @property
    def val(self):
        # Should it be an error to evaluate the val of a branch node?
        if self._value is not None:
            return self._value
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
        # Right now, this implies Z-order
        return np.dot((point > center), basis)

    @property
    def isleaf(self):
        # Python dictionaries evaluate to false when empty
        return bool(self.children)

    # def child_bounding_box(self, child):
    #     ls = []
    #     hs = []
    #     for l,c,h in zip(self.minimums, self.center, self.maximums):
    #
    #     for bool(int(b)) in reversed('{:b}'.format(child)):
    #         if


    def child_bounding_box(self, child):
        '''Given the index of a child, returns the center of said child's space'''
         # HACK
        bits = [int(b) for b in reversed('{:b}'.format(child))]
        bits += (len(self.center) - len(bits)) * [0]
        bitvec = np.array(bits)
        # bitvec = bitvec * 2 - 1 # {0,1} -> {-1,1}
        # In each dimension, take an average weighted by 3/4 towards the child node to find the new center
        newmin = self.minimums + self.radii * bitvec
        newmax = newmin + self.radii
        return newmin, newmax
        # h = []
        #
        # return ((2 + bitvec) * self.maximums + (2 - bitvec) * self.minimums) / 4

    # np.array([int(_) for _ in reversed("{:b}".format(n-1))],dtype=np.bool)
        # pass


    def add(self, point):
        if self.isleaf:
            # Need to move our current value to a child and become a branch node
            self.children[self.route(self._value)] = ntree(..., ..., self._value)
            self._value = None




n = ntree(np.array([0,0,0,0]),np.array([16,16,16,16]))
# Find the position of a 12-d point in layer 1 of n:
print(n.route(np.array([12,9,9,0,0,0,0,1,0,0,0,1])))
print(n.radii)
print(n.center)
for i in range(16):
    print(n.child_bounding_box(i))
