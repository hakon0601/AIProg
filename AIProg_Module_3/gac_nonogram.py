from gac_general import GACGeneral


class GACNonogram(GACGeneral):
    def __init__(self):
        GACGeneral.__init__(self)


    # TODO This is the only method in csp that is not general. It should be. Very close to the other gac. can we fix this to make just one gac?
    # Reduces domain of current variable if constraining variable is singleton domain
    def revise(self, variable, constr, variable_dict):
        reduced = False
        for constraining_variable_key in constr.involved_variables:
            if variable.index != constraining_variable_key:
                constraining_variable = variable_dict[constraining_variable_key]
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