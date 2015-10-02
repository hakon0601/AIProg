import variabel_base


class Variable(variabel_base.BaseVariabel):
    def __init__(self, index, direction, line_index, segment_nr, length, k=0):
        self.index = index
        self.direction = direction
        self.length = length
        self.domain = [x for x in range(k)]
        self.involved_constraints = []
        self.segment_nr = segment_nr
        self.k = k
        self.prune_longer_than_max(k)

    def prune_longer_than_max(self, max):
        refined_domain = []
        for value in self.domain:
            if self.length + int(value) <= max:
                refined_domain.append(value)
            else:
                self.domain = refined_domain
                break

    def __str__(self):
        return str(self.direction) + " - " + str(self.index) + " - " + str(self.segment_nr) + " - " + str(self.length) + " - " + str(self.domain)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.direction == other.spec and self.index == other.index and self.segment_nr == other.segment_nr:
            return True
        return False