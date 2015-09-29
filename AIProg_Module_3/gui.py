from input_handler import read_file
from state import State
from csp import CSP


class Gui():
    def __init__(self, *args, **kwargs):
        scenario = "scenarios/scenario_test.txt"

        # domain = (nr_of_rows, nr_of_columns)
        self.domain, self.variable_dict, self.constraints = read_file(scenario)

        # init reduce domains so that no segments can be longer than the row/column
        self.no_longer_than_itself()

        initial_state = State(self.constraints, self.variable_dict, CSP())
        print initial_state

        initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
        initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

        print "refined initial state"
        print initial_state


    def no_longer_than_itself(self):
        for variable in self.variable_dict:
            max = 0
            refined_domain = []
            if variable.spec == "row":
                max = self.domain[1]
            elif variable.spec == "column":
                max = self.domain[0]
            for e in variable.domain:
                if max >= variable.length + int(e)+1:
                    refined_domain.append(e)
                else:
                    variable.domain = refined_domain
                    break

    # THis method will not be useful, because they always WILL BE! It will always return true
    # We will never put several.... loll this does not work go to bed fucktard
    def all_involved_variables_are_in_same_row_or_column(self, involved_variables):
        only_rows = True
        only_columns = True
        for variable in involved_variables:
            if variable.spec == "row":
                only_columns = False
            elif variable.spec == "column":
                only_rows = True
        # Returns true if all involved variables is either in a row or in a column
        return (only_rows or only_columns)

if __name__ == "__main__":
    app = Gui()
    #app.mainloop()