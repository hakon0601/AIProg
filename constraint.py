

class Constraint():
    def __init__(self, variable_dict, involved_variables=[]):
        # Index of vertex on one side, and index of vertex on the other side.
        self.involved_variables = involved_variables
        for variable in involved_variables:
            variable_dict[variable].involved_constraints.append(self)

    def __str__(self):
        s = ""
        for v in self.involved_variables:
            s += str(v) + " - "
        s = s[0:-2]
        return s

    def __repr__(self):
        return str(self)

    def is_breaking(self, variable, e):
        if variable != self.involved_variables[0] and variable != self.involved_variables[1]:
            "Something happend in constraints"

        first_var = None
        second_var = None
        var_segment_nr = int(variable.segment_nr)

        if variable == self.involved_variables[0] and var_segment_nr < int(self.involved_variables[1].segment_nr):
            first_var = variable
            second_var = self.involved_variables[1]

        elif variable == self.involved_variables[1] and var_segment_nr< int(self.involved_variables[0].segment_nr):
            first_var = variable
            second_var = self.involved_variables[0]

        elif variable == self.involved_variables[0] and var_segment_nr > int(self.involved_variables[1].segment_nr):
            first_var = self.involved_variables[1]
            second_var = variable

        elif variable == self.involved_variables[1] and var_segment_nr > int(self.involved_variables[0].segment_nr):
            first_var = self.involved_variables[0]
            second_var = variable

        if variable == first_var:
            # first var
            if e <= (int(first_var.k) - int(first_var.length) - int(second_var.length) - 1):
                return False
            else:
                # Is breaking
                print ""
                print "variable is first"
                print "inv0: " + str(self.involved_variables[0])
                print "inv1: " + str(self.involved_variables[1])
                print "e: " + str(e)
                print "domain: " + str(first_var.k)
                print "length first: " + str(first_var.length)
                print "length second: " + str(second_var.length)
                print "e is bigger than " + str(int(first_var.k) - int(first_var.length) - int(second_var.length) - 1)
                return True

        elif variable == second_var:
            # second var
            if e > first_var.length:
                return False
            else:
                # Is breaking
                print ""
                print "variable is second"
                print "inv0: " + str(self.involved_variables[0])
                print "inv1: " + str(self.involved_variables[1])
                print "e: " + str(e)
                print "domain: " + str(first_var.k)
                print "length first: " + str(first_var.length)
                print "length second: " + str(second_var.length)
                print "e is smaller or alike " + str(first_var.length)
                return True
        else:
            print "error in Constraint class"