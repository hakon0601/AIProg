

from state import State
import input_handler

variable_dict, constraints = input_handler.read_file("graph-color-1.txt")


print(variable_dict)
print(constraints)

initial_state = State(constraints)
initial_state.variable_dict = variable_dict

initial_state.revise()
print(initial_state.variable_dict)

