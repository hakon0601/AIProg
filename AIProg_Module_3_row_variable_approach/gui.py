from input_handler import read_file
from state import State
from csp import CSP
from variable import Variable

class Gui():
    def __init__(self, *args, **kwargs):
        scenario = "scenarios/scenario_test.txt"

        # PRE PROSESSING
        # DOMAIN REDUCTION ISOLATED IN ROWS/COLUMNS

        # domain = (nr_of_rows, nr_of_columns)
        self.dimensions, self.variable_dict, self.constraints = read_file(scenario)
        # Make new constraints?

        #print "initial variable_dict: " + str(self.variable_dict)
        for key, value in self.variable_dict.items() :
            print (key, value)

        initial_state = State(self.constraints, self.variable_dict, CSP())
        initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
        initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

        #print "refined variable_dict: " + str(initial_state.variable_dict)
        print ""
        print "refined variable_dict: "
        for key, value in initial_state.variable_dict.items() :
            print (key, value)



    def pre_prosessing(self):
        # Domain reduction in rows and columns isolated
        for constr in self.constraints:
            for variable in constr.involved_variables:
                self.revise_queue.append((variable, constr))



if __name__ == "__main__":
    app = Gui()
    #app.mainloop()