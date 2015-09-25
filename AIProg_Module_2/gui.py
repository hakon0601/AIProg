

from state import State
import input_handler
from csp import CSP
from a_star import AStar


variable_dict, constraints = input_handler.read_file("spiral-500-4-color1.txt")



initial_state = State(constraints, variable_dict, CSP())

print "init State: " + str(initial_state)

#initial_state.variable_dict[0].domain = [0]
#initial_state.variable_dict[2].domain = [0, 1]

initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

print "refined init State: " + str(initial_state)

a_star = AStar()
a_star.add_start_state_to_open(initial_state)


def run_a_star():
    # if the algorithm is not finished with the board, do one iteration of the algorithm
    result = a_star.do_one_step()
    if not result:
        # there are no more nodes in open nodes -> algorithm did not reach goal, fail
        print("Failed")
        return
    elif result == 1:
        # the algorithm is not finished
        #self.update_board()
        # run_a_star will be called over and over again
        #self.after(500, lambda: run_a_star())
        run_a_star()
    else:
    # Result is a reconstructed path of states from start to goal
        print("Success")
        print "Path length: " + str(round(result[-1].g_value * 10, 2))
        #self.draw_path(result, i, 0)


run_a_star()