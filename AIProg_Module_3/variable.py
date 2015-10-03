import variabel_base
from copy import deepcopy


class Variable(variabel_base.BaseVariabel):
    def __init__(self, index, direction, direction_nr, length, segments=[]):
        self.direction_nr = direction_nr
        self.index = index
        self.direction = direction
        self.length = length
        # Domain is a list of possible permutation lists containing boolean values
        self.domain = self.find_permutations(segments, length)
        self.involved_constraints = []


    # TODO rewrite this method as it is stolen code
    def find_permutations(self, segments, length):
        if len(segments) == 0:
            return [[False for bool in range(length)]]

        permutations = []

        for start in range(length - segments[0] + 1):
            permutation = []
            for x in range(start):
                permutation.append(False)
            for x in range(start, start + segments[0]):
                permutation.append(True)
            x = start + segments[0]
            if x < length:
                permutation.append(False)
                x += 1
            if x == length and len(segments) == 0:
                permutations.append(permutation)
                break
            sub_start = x
            sub_rows = self.find_permutations(segments[1:len(segments)], length - sub_start)
            for sub_row in sub_rows:
                sub_permutation = deepcopy(permutation)
                for x in range(sub_start, length):
                    sub_permutation.append(sub_row[x - sub_start])
                permutations.append(sub_permutation)
        return permutations

    def __str__(self):
        return str(self.direction) + " - i: " + str(self.index) + " - nr: " + str(self.direction_nr) + " - " + str(self.domain)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.direction == other.direction and self.index == other.index and self.direction_nr == other.direction_nr:
            return True
        return False