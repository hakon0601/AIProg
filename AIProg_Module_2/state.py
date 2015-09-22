

from math import sqrt
import state_base
import constraint
from copy import deepcopy

class State(state_base.BaseState):
    def __init__(self, constraints, csp):
        self.constraints = constraints
        self.csp = csp
        self.variable_dict = {}
        self.parents = []
        self.h_value = self.calculate_h()
        self.g_value = float("inf")

    def get_f(self):
        return self.g_value + self.h_value

    def calculate_h(self):
        tentative_h = 0
        for variable in self.variable_dict.values():
            tentative_h += (len(variable.domain) - 1)
        return tentative_h


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
        for variable in self.variable_dict.values():
            for value in variable.domain:
                successor_state = State(self.constraints, self.csp)
                successor_variable_dict = deepcopy(self.variable_dict)
                successor_variable_dict[variable.index].domain = [value]
                successor_state.variable_dict = successor_variable_dict

                successor_state.csp.init_revise_queue(self.constraints, successor_state.variable_dict)
                successor_state.csp.domain_filtering_loop(successor_state.variable_dict)
                successor_state.h_value = successor_state.calculate_h()

                successors.append(successor_state)

        return successors

    def movement_cost(self, successor):
        return

    def __eq__(self, other):
        return False

    def __str__(self):
        return

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if self.get_f() < other.get_f():
            return True
        elif self.get_f() > other.get_f():
            return False
        else:
            if self.h_value <= other.h_value:
                return True
            else:
                return False

    def get_best_parent(self):
        return

    def is_solution_or_contradictory(self):
        for variable in self.variable_dict.values():
            # Contradictory
            if len(variable.domain) == 0:
                return True
            # Not a solution
            elif len(variable.domain) != 1:
                return False
        return True