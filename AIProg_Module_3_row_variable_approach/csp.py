import csp_base
import copy

class CSP(csp_base.BaseCSP):
    def __init__(self):
        # Tuples with pairs of variable indexes and constraints
        self.revise_queue = []

    def init_revise_queue(self, constraints, variable_dict):
        for constr in constraints:
            for variable_index in constr.involved_variables:
                self.revise_queue.append((variable_dict[variable_index], constr))

    def domain_filtering_loop(self, variable_dict):
        while self.revise_queue:
            variable, constr = self.revise_queue.pop()
            # If a variables domain is reduced
            if self.revise(variable, constr, variable_dict):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                    for involved_variable_in_involved_constraint in involved_constraint.involved_variables:
                        if variable.index != involved_variable_in_involved_constraint:
                            self.revise_queue.append((variable_dict[involved_variable_in_involved_constraint], involved_constraint))

    # Reduces domain of current variable if constraining variable is singleton domain
    def revise(self, variable, constr, variable_dict):
        reduced = False
        for constraining_variable_index in constr.involved_variables:
            constraining_variable = variable_dict[constraining_variable_index]
            if variable.index != constraining_variable_index and len(constraining_variable.domain) == 1:
                intersecting_value = constraining_variable.domain[0][variable.nr]
                valid_domain = []

                if variable.index == 8 or variable.index == 11:
                    print "----------------------"
                    print "Variable: " + str(variable)
                    print "Constraining variable: " + str(constraining_variable)
                    print "Intersecting value (Constraining variable): " + str(intersecting_value)

                for permutation in variable.domain:
                    if permutation[constraining_variable.nr] == intersecting_value:
                        valid_domain.append(permutation)
                    else:
                        if variable.index == 8 or variable.index == 11:
                            print "Permutation: " + str(permutation)
                            print "Permutation removed"
                        reduced = True
                variable.domain = valid_domain
                if variable.index == 8 or variable.index == 11:
                    print "Valid domain:"
                    print valid_domain
        return reduced
