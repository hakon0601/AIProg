import state_base
from copy import deepcopy


class CSPState(state_base.BaseState):
    def __init__(self, constraints, variable_dict, gac):
        self.constraints = constraints
        self.gac = gac
        self.variable_dict = variable_dict
        self.parent = None
        self.children = []
        self.h_value = float("inf")
        self.g_value = float("inf")

    def get_f(self):
        return self.g_value + self.h_value

    def calculate_h(self):
        tentative_h = 0
        for variable in self.variable_dict.values():
            tentative_h += (len(variable.domain) - 1)
        return tentative_h

    def reconstruct_path(self):
        path = [self]
        while path[-1].parent:
            path.append(path[-1].parent)
        return list(reversed(path))

    def generate_successor_nodes(self):
        successors = []
        # Generate one successor for every possible singleton domain of the variable with the smallest domain
        variable_with_smallest_domain = self.get_variable_with_smallest_domain()
        for value in variable_with_smallest_domain.domain:
            successor_variable_dict = deepcopy(self.variable_dict)

            # Reducing the domain of the variable to a singleton set
            successor_variable_dict[variable_with_smallest_domain.index].domain = [value]
            successor_state = CSPState(self.constraints, successor_variable_dict, self.gac)

            # GAC rerun on the newly generated successor
            self.gac.gac_rerun(successor_state.constraints, successor_state.variable_dict)

            # Calulate h after domain reductions
            successor_state.h_value = successor_state.calculate_h()

            successors.append(successor_state)
        return successors

    def movement_cost(self, successor):
        return 1

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

    def is_solution_or_contradictory(self):
        for variable in self.variable_dict.values():
            # Contradictory
            if len(variable.domain) == 0:
                return True
            # Not a solution
            elif len(variable.domain) != 1:
                return False
        return True

    def get_variable_with_smallest_domain(self):
        variable_with_smallest_domain = None
        for variable in self.variable_dict.values():
            if not variable_with_smallest_domain or len(variable.domain) < len(variable_with_smallest_domain.domain):
                if len(variable.domain) != 1:
                    variable_with_smallest_domain = variable
        return variable_with_smallest_domain
