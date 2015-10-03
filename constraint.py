

class Constraint():
    def __init__(self, variable_dict, involved_variables=[]):
        self.involved_variables = involved_variables
        self.constraining_func = None
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
