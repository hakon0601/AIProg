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
                self.revise_queue.append((variable_dict[variable_key], constr))

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


    # TODO This is the only method in csp that is not general. It should be. Very close to the other gac. can we fix this to make just one gac?
    # Reduces domain of current variable if constraining variable is singleton domain
    def revise(self, variable, constr, variable_dict):
        reduced = False
        for constraining_variable_index in constr.involved_variables:
            constraining_variable = variable_dict[constraining_variable_index]
            if variable.index != constraining_variable_index:
                valid_domain = []
                for permutation in variable.domain:
                    # Remove a permutation from the domain if no permutation in the
                    # constricting domain has the same value in the intersecting cell
                    for constraining_permutation in constraining_variable.domain:
                        if constr.constraining_func(permutation[constraining_variable.direction_nr], constraining_permutation[variable.direction_nr]):
                            valid_domain.append(permutation)
                            break
                if len(variable.domain) != len(valid_domain):
                    reduced = True
                variable.domain = valid_domain
        return reduced