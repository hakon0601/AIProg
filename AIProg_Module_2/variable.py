

class Variable():
    def __init__(self, index, x, y, k):
        self.index = index
        self.x = x
        self.y = y
        self.domain = [x for x in range(k)]
        self.involved_constraints = []

    def __str__(self):
        #return str(self.index) + " - " + str(self.domain)
        return str(self.index) + " - (" + str(self.x) + "," + str(self.y) + ") - " + str(self.domain)

    def __repr__(self):
        return str(self)
