from gac_base import BaseGAC


class GAC(BaseGAC):
    def __init__(self):
        # Tuples with pairs of variables and constraints
        self.revise_queue = []

    def gac_rerun(self, constraints, variable_dict):
        self.init_revise_queue(constraints, variable_dict)
        self.domain_filtering_loop(variable_dict)

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

    # Reduces domain of current variable if constraining variables is singleton domains
    def revise(self, variable, constr, variable_dict):
        reduced = False
        for constraining_variable_key in constr.involved_variables:
            if variable.index != constraining_variable_key:
                constraining_variable = variable_dict[constraining_variable_key]
                valid_domain = []
                if len(constraining_variable.domain) != 1:
                    continue
                for value in variable.domain:
                    for constraining_value in constraining_variable.domain:
                        if constr.constraining_func(value, constraining_value):
                            valid_domain.append(value)
                            break
                if len(variable.domain) != len(valid_domain):
                    reduced = True
                variable.domain = valid_domain
        return reduced