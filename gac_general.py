

class GACGeneral():
    def __init__(self):
        # Tuples with pairs of variables and constraints
        # TODO test if it gets faster by makin this into queue
        self.revise_queue = []

    # Reloads the revise queue with the constraints from the variable in an assumption
    def gac_rerun(self, constraints, variable_dict):
        self.init_revise_queue(constraints, variable_dict)
        self.domain_filtering_loop(variable_dict)

    #TODO bare legg til index til variabel i koen. Ikke hele var
    def init_revise_queue(self, constraints, variable_dict):
        for constr in constraints:
            for variable_key in constr.involved_variables:
                variable = variable_dict[variable_key]
                if len(variable.domain) != 1:
                    self.revise_queue.append((variable, constr))

    def domain_filtering_loop(self, variable_dict):
        while self.revise_queue:
            variable, constr = self.revise_queue.pop()
            # If a variables domain is reduced
            if self.revise(variable, constr, variable_dict):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                    for involved_variable_in_involved_constraint_key in involved_constraint.involved_variables:
                        involved_variable_in_involved_constraint = variable_dict[involved_variable_in_involved_constraint_key]
                        if variable.index != involved_variable_in_involved_constraint.index:
                            self.revise_queue.append((involved_variable_in_involved_constraint, involved_constraint))
