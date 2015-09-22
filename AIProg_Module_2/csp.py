

class CSP():
    def __init__(self, constraints):
        # Tuples with pairs of variable indexes and constraints
        self.revise_queue = []
        self.init_revise_queue(constraints)

    def init_revise_queue(self, constraints):
        for constr in constraints:
            for variable in constr.involved_variables:
                self.revise_queue.append((variable, constr))

    def domain_filtering_loop(self):
        while self.revise_queue:
            variable, constr = self.revise_queue.pop()
            # If a variables domain is reduced
            if self.revise(variable, constr):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                        for involved_variable_in_involved_constraint in involved_constraint.involved_variables:
                            if variable != involved_variable_in_involved_constraint:
                                self.revise_queue.append((involved_variable_in_involved_constraint, involved_constraint))


    # Reduces domain of current variable if constraining variables is singleton domains
    def revise(self, variable, constr):
        for constraining_variable in constr.involved_variables:
                if variable != constraining_variable and len(constraining_variable.domain) == 1 and constraining_variable.domain[0] in variable.domain:
                    variable.domain.remove(constraining_variable.domain[0])
                    return True
        return False