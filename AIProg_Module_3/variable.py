import time


class Variable():
    def __init__(self, index, direction, direction_nr, length, segments=[]):
        self.direction_nr = direction_nr
        self.index = index
        self.direction = direction
        self.length = length
        # Domain is a list of possible permutation lists containing boolean values
        self.domain = self.find_permutations(segments, length)
        self.involved_constraints = []

    def find_permutations(self, segments, length):
        permutations = self.one_segment_permutations(segments=segments, segment_index=0, list_size=length)
        for perm in permutations:
            if len(perm) != length:
                perm += [False for i in range(length - len(perm))]
        return permutations

    def one_segment_permutations(self, segments, segment_index, list_size):
        if segment_index == len(segments):
            return [[]]
        segment_size = segments[segment_index]
        # This domain permutation is invalid if there is not room for all segments
        if segment_size > list_size:
            return -1
        permutations = []
        for i in range(list_size):
            if i + segment_size <= list_size:
                perm = [False for j in range(i)]
                for k in range(i, i + segment_size):
                    perm.append(True)
                more_permutations = self.one_segment_permutations(segments, segment_index=segment_index+1, list_size=list_size-(k+1+1))
                if more_permutations == -1:
                    continue
                for p in more_permutations:
                    if len(p) > 0:
                        new_perm = perm + [False] + p
                    else:
                        new_perm = perm
                    permutations.append(new_perm)
        return permutations

    def __str__(self):
        return str(self.direction) + " - i: " + str(self.index) + " - nr: " + str(self.direction_nr) + " - " + str(self.domain)

    def __repr__(self):
        return str(self)
