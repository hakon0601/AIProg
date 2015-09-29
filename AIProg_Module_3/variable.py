import variabel_base

class Variable(variabel_base.BaseVariabel):
    def __init__(self, spec, index, segment_nr, length, k=0):
        self.index = index
        self.spec = spec
        self.length = length
        self.domain = [x for x in range(k)]
        self.involved_constraints = []
        self.segment_nr = segment_nr
        self.k = k

    def __str__(self):
        return str(self.spec) + " - " + str(self.index) + " - " + str(self.segment_nr) + " - " + str(self.length) + " - " + str(self.domain)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.spec == other.spec and self.index == other.index and self.segment_nr == other.segment_nr:
            return True
        return False