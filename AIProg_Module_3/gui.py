from input_handler import read_file
from state import State
from csp import CSP


class Gui():
    def __init__(self, *args, **kwargs):
        scenario = "scenarios/scenario_test.txt"

        # domain = (nr_of_rows, nr_of_columns)
        self.domain, self.variable_dict, self.constraints = read_file(scenario)


        #variable_dict[variable] = variable

        initial_state = State(self.constraints, self.variable_dict, CSP())
        print "initial state"
        print initial_state

        initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
        initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

        print "refined initial state"
        print initial_state



if __name__ == "__main__":
    app = Gui()
    #app.mainloop()