

class Constraint():
    def __init__(self, involved_variables=[]):
        # Index of vertex on one side, and index of vertex on the other side.
        self.involved_variables = involved_variables
        for variable in involved_variables:
            variable.involved_constraints.append(self)

    def __str__(self):
        s = ""
        for v in self.involved_variables:
            s += str(v.index) + " - "
        s = s[0:-2]
        return s

    def __repr__(self):
        return str(self)
'''
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
'''