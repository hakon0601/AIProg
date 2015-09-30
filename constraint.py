

class Constraint():
    def __init__(self, variable_dict, involved_variables=[]):
        # Index of vertex on one side, and index of vertex on the other side.
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

    def get_other(self, variable):
        if variable == self.involved_variables[0]:
            return self.involved_variables[1]
        elif variable == self.involved_variables[1]:
            return self.involved_variables[0]
        else:
            print "Error in constraint.get_other"
            return None

    def all_involved_vars_are_in_same_line(self):
        only_rows = True
        only_columns = True
        for variable in self.involved_variables:
            if variable.spec == "row":
                only_columns = False
            elif variable.spec == "column":
                only_rows = False
        # Returns true if all involved variables is either in a row or in a column
        return (only_rows or only_columns)