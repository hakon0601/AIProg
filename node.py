__author__ = 'hakon0601'


class Node():
    def __init__(self, x, y, h_value):
        self.x = x
        self.y = y
        self.type = 'O'
        self.parent = None
        self.h_value = h_value
        self.g_value = float("inf")
        self.f_value = float("inf")

    def get_f(self):
        return self.g_value + self.h_value

    def __str__(self):
        return self.type + " - (" + str(self.x) + ", " + str(self.y) + ")"

    '''
    Type O is free node
    Type X is obstacle node
    Type G is goal node
    Type S is start node
    '''