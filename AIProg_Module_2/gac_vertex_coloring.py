from gac_general import GACGeneral


class GACVertexColoring(GACGeneral):
    def __init__(self):
        GACGeneral.__init__(self)

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