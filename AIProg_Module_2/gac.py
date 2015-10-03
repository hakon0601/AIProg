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
            for variable in constr.involved_variables:
                self.revise_queue.append((variable_dict[variable], constr))

    def domain_filtering_loop(self, variable_dict):
        while self.revise_queue:
            variable, constr = self.revise_queue.pop()
            # If a variables domain is reduced
            if self.revise(variable, constr, variable_dict):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                    for involved_variable_in_involved_constraint in involved_constraint.involved_variables:
                        if variable != variable_dict[involved_variable_in_involved_constraint]:
                            self.revise_queue.append((variable_dict[involved_variable_in_involved_constraint], involved_constraint))


    # Reduces domain of current variable if constraining variables is singleton domains
    def revise(self, variable, constr, variable_dict):
        reduced = False
        for constraining_variable in constr.involved_variables:
            constraining_variable = variable_dict[constraining_variable]
            if variable.index != constraining_variable.index:
                valid_domain = []
                # TODO I think you can drop this entire code chunk if constraining domain is not a singleton???
                for value in variable.domain:
                    for constraining_value in constraining_variable.domain:
                        if constr.constraining_func(value, constraining_value):
                            valid_domain.append(value)
                            break
                if len(variable.domain) != len(valid_domain):
                    reduced = True
                variable.domain = valid_domain

                #if len(constraining_variable.domain) == 1 and constraining_variable.domain[0] in variable.domain:
                #    variable.domain.remove(constraining_variable.domain[0])
                #    return True
        return reduced