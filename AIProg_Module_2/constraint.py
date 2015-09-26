

class Constraint():
    def __init__(self, variable_dict, involved_variables=[]):
        # Index of vertex on one side, and index of vertex on the other side.
        self.involved_variables = involved_variables
        for variable in involved_variables:
            variable_dict[variable].involved_constraints.append(self)

    def __str__(self):
        s = ""
        for v in self.involved_variables:
            s += v + " - "
        s = s[0:-2]
        return s

    def __repr__(self):
        return str(self)
