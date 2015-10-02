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
            if variable.index != constraining_variable_index:
                valid_domain = []
                if len(constraining_variable.domain) == 1:
                    intersecting_value = constraining_variable.domain[0][variable.nr]
                    # Constraining variable has a singleton domain
                    for permutation in variable.domain:
                        if permutation[constraining_variable.nr] == intersecting_value:
                            valid_domain.append(permutation)
                        else:
                            reduced = True
                    variable.domain = valid_domain
                else:
                    # Domain of constraining variable is not a singleton domain, but if either
                    # 1) none of the permutations in constraining variable has a True value of the intersecting cell
                    # -> remove from variable.domain those permutation that has a True value in intersecting cell
                    # 2) all of the permutations in constraining variable has a True value of the intersecting cell
                    # -> remove from variable.domain those permutation that has a False value in intersecting cell

                    permutation_count = len(constraining_variable.domain)

                    intersecting_value_is_true = 0
                    intersecting_value_is_false = 0

                    for permutation in constraining_variable.domain:
                        if permutation[variable.nr] == True:
                            intersecting_value_is_true += 1
                        elif permutation[variable.nr] == False:
                            intersecting_value_is_false +=1

                    if intersecting_value_is_true == permutation_count or intersecting_value_is_false == permutation_count:
                        for permutation in variable.domain:
                            if intersecting_value_is_true == permutation_count and permutation[constraining_variable.nr] == True:
                                valid_domain.append(permutation)
                            elif intersecting_value_is_false == permutation_count and permutation[constraining_variable.nr] == False:
                                valid_domain.append(permutation)
                            else:
                                reduced = True
                    else:
                        # If constraining variable has permutations that has a mix of True and False for the intersecting cell,
                        # Then we can not reduce variable domain
                        for permutation in variable.domain:
                            valid_domain.append(permutation)
                    variable.domain = valid_domain
        return reduced
