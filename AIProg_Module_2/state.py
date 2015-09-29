from copy import deepcopy
from sys import setrecursionlimit

import state_base

setrecursionlimit(10000)

class State(state_base.BaseState):
    def __init__(self, constraints, variable_dict, csp):
        self.constraints = constraints
        self.csp = csp
        self.variable_dict = variable_dict
        self.parent = None
        self.children = []
        self.h_value = float("inf")
        self.g_value = float("inf")

    def get_f(self):
        return self.g_value + self.h_value

    def getID(self):
        return self.__hash__()

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
        path = [self]
        while path[-1].parent:
            path.append(path[-1].parent)
        return list(reversed(path))

    def generate_successor_nodes(self):
        successors = []
        # Generate one successor for every possible singleton domain for each variable
        variable_with_smallest_domain = None
        for variable in self.variable_dict.values():
            if (not variable_with_smallest_domain or len(variable.domain) < len(variable_with_smallest_domain.domain)):
                if len(variable.domain) != 1:
                    variable_with_smallest_domain = variable
        print "variable with smallest domain: " + str(variable_with_smallest_domain)
        for value in variable_with_smallest_domain.domain:
            successor_variable_dict = deepcopy(self.variable_dict)

            # Enforcing the assumption by reducing the domain of the assumed
            # variable to a singleton set (only one value)
            successor_variable_dict[variable_with_smallest_domain.index].domain = [value]
            successor_state = State(self.constraints, successor_variable_dict, self.csp)

            # = GAC rerun
            successor_state.csp.init_revise_queue(self.constraints, successor_state.variable_dict)
            successor_state.csp.domain_filtering_loop(successor_state.variable_dict)

            # Calulate h after domain reductions
            successor_state.h_value = successor_state.calculate_h()

            successors.append(successor_state)
        return successors

    def movement_cost(self, successor):
        return 1

    def __eq__(self, other):
        # If all domains of the corresponding variables in the two states are the same, they are the same state
        for key in self.variable_dict.keys():
            if not set(self.variable_dict[key].domain) == set(other.variable_dict[key].domain):
                return False
        return True

    def __str__(self):
        return str(self.variable_dict) + " h: " + str(self.h_value) + " - g: " + str(self.g_value)

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

    def __hash__(self):
        return hash(repr(sorted(self.variable_dict.items())))

    def is_solution_or_contradictory(self):
        for variable in self.variable_dict.values():
            # Contradictory
            if len(variable.domain) == 0:
                return True
            # Not a solution
            elif len(variable.domain) != 1:
                return False
        return True