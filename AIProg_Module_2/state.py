

from math import sqrt
import state_base
import constraint

class State(state_base.BaseState):
    def __init__(self, constraints):
        self.variable_dict = {}
        self.parents = []
        self.h_value = self.calculate_h()
        self.g_value = float("inf")
        self.constraints = constraints

    def get_f(self):
        return self.g_value + self.h_value

    def calculate_h(self):
        return

    def revise(self):
        for key in self.variable_dict.keys():
            tentative_domain = []
            variable = self.variable_dict[key]
            for value in variable.domain:
                if not self.is_value_breaking_constraints(variable, value):
                    continue
                else:
                    tentative_domain.append(value)
            variable.domain = tentative_domain

    def is_value_breaking_constraints(self, variable, value):
        for constr in self.constraints:
            # Selects the constraints in which the variable appears
            if constr.has_variable(variable):
                other_variable = self.variable_dict[constr.get_other_variable_index(variable)]
                # If the other variable in the constraint has a singelton domain, where the value is equal return True
                if len(other_variable.domain) == 1 and other_variable.domain[0] == value:
                    return True
        return False



    def reconstruct_path(self):
        return

    def generate_successor_nodes(self):
        successors = []
        return successors

    def movement_cost(self, successor):
        return

    def __eq__(self, other):
        return False

    def __str__(self):
        return

    def __repr__(self):
        return self.__str__()

    def get_best_parent(self):
        return
