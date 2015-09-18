

class Constraint():
    def __init__(self, index_1, index_2):
        # Index of vertex on one side, and index of vertex on the other side.
        self.index_1 = index_1
        self.index_2 = index_2

    def __str__(self):
        return str(self.index_1) + " - " + str(self.index_2)

    def __repr__(self):
        return str(self)

    def has_variable(self, variable):
        if self.index_1 == variable.index or self.index_2 == variable.index:
            return True
        return False

    def get_other_variable_index(self, variable):
        if self.index_1 == variable.index:
            return self.index_2
        elif self.index_2 == variable.index:
            return self.index_1
        return None
