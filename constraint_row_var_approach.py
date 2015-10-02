

class ConstraintRowVarApproach():
    def __init__(self, variable_dict, involved_variables=[]):
        # A cell shared between a row and a column
        # If this cell is true in one, it have to be true in the other.
        # domain = [[True, False, False], [False, True, False], [False, False, True]]
        self.involved_variables = involved_variables
        for variable in involved_variables:
            variable_dict[variable].involved_constraints.append(self)

    def __str__(self):
        s = "c: "
        for v in self.involved_variables:
            s += str(v) + " - "
        s = s[0:-2]
        return s

    def __repr__(self):
        return str(self)
