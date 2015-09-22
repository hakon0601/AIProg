

class CSP():
    def __init__(self):
        # Tuples with pairs of variable indexes and constraints
        self.revise_queue = []

    def init_revise_queue(self, constraints, variable_dict):
        for constr in constraints:
            for variable in constr.involved_variables:
                self.revise_queue.append((variable_dict[variable.index], constr))

    def domain_filtering_loop(self, variable_dict):
        while self.revise_queue:
            variable, constr = self.revise_queue.pop()
            # If a variables domain is reduced
            if self.revise(variable, constr, variable_dict):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                    for involved_variable_in_involved_constraint in involved_constraint.involved_variables:
                        if variable != variable_dict[involved_variable_in_involved_constraint.index]:
                            self.revise_queue.append((variable_dict[involved_variable_in_involved_constraint.index], involved_constraint))


    # Reduces domain of current variable if constraining variables is singleton domains
    def revise(self, variable, constr, variable_dict):
        for constraining_variable in constr.involved_variables:
            constraining_variable = variable_dict[constraining_variable.index]
            if variable != constraining_variable and len(constraining_variable.domain) == 1 and constraining_variable.domain[0] in variable.domain:
                variable.domain.remove(constraining_variable.domain[0])
                return True
        return False