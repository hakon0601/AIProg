import variabel_base
from copy import deepcopy


class Variable(variabel_base.BaseVariabel):
    def __init__(self, index, direction, direction_nr, length, segments=[]):
        self.nr = direction_nr
        self.index = index
        self.direction = direction
        self.length = length
        # Domain is a list of possible permutation lists containing boolean values
        self.domain = self.find_permutations(segments, length)
        self.involved_constraints = []

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

    def create_domain(self, segments, length):
        '''
        domain = []
        while True:
            permutation = [[False for bool in range(length)] for a in range(length)]
            for segment in segments:
                for i in range(length):
                    if i + segment <= length and :
                        for j in range(segment):
                            permutation[i + j] = True
        '''
        if sum(segments) > length:
            return []
        result = []
        if not segments:
            result.append([False for bool in range(length)])
        else:
            place_first = self.create_domain(segments[1:], length - segments[0] - 1)

            for rest in place_first:
                result.append(list.extend([True for bool in range(segments[0])], rest))

            skip_first = self.create_domain(segments, length - 1)
            for rest in skip_first:
                result.append(list.extend([False], rest))

        return result

    def __str__(self):
        return str(self.direction) + " - i: " + str(self.index) + " - nr: " + str(self.nr) + " - " + str(self.domain)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.direction == other.direction and self.index == other.index and self.nr == other.nr:
            return True
        return False