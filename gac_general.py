

class GACGeneral():
    def __init__(self):
        # Tuples with pairs of variables and constraints
        self.revise_queue = []

    # Reloads the revise queue with the constraints from the variable in an assumption
    def gac_rerun(self, constraints, variable_dict):
        self.init_revise_queue(constraints, variable_dict)
        self.domain_filtering_loop(variable_dict)

    def init_revise_queue(self, constraints, variable_dict):
        for constr in constraints:
            for variable_key in constr.involved_variables:
                self.revise_queue.append((variable_key, constr))

    def domain_filtering_loop(self, variable_dict):
        while self.revise_queue:
            variable_key, constr = self.revise_queue.pop()
            variable = variable_dict[variable_key]
            # If a variables domain is reduced
            if self.revise(variable, constr, variable_dict):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                    for involved_variable_in_involved_constraint_key in involved_constraint.involved_variables:
                        if variable.index != involved_variable_in_involved_constraint_key:
                            self.revise_queue.append((involved_variable_in_involved_constraint_key, involved_constraint))
