

from state import State
import input_handler
from csp import CSP
from a_star import AStar


variable_dict, constraints = input_handler.read_file("graph0.txt")


print(variable_dict)
print(constraints)

initial_state = State(constraints, CSP())
initial_state.variable_dict = variable_dict

a_star = AStar()
a_star.add_open(initial_state)

initial_state.variable_dict[0].domain = [0]
#initial_state.variable_dict[2].domain = [0, 1]

initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

while True:
    if initial_state.is_solution_or_contradictory():
        print "Finished " + str(initial_state.variable_dict)
        exit(1)
    else:
         a_star.do_one_step()



print(initial_state.variable_dict)
