import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename

from input_handler import read_file
from state import State
from csp import CSP
from a_star import AStar
from variable import Variable

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Solving nonograms")

        #scenario = "scenarios/scenario_test.txt"

        self.create_menu()

    def create_menu(self):
        # existing boards buttons
        self.info1 = Label(self, text="Choose an existing graph: ")
        self.info1.pack(anchor=W)
        self.v = StringVar()
        self.buttons = [
            tk.Button(self, text="Scenario 0", command=lambda: self.start("scenarios/scenario0.txt")),
            tk.Button(self, text="Scenario 1", command=lambda: self.start("scenarios/scenario1.txt")),
            tk.Button(self, text="Scenario 3", command=lambda: self.start("scenarios/scenario2.txt")),
            tk.Button(self, text="Scenario 4", command=lambda: self.start("scenarios/scenario3.txt")),
            tk.Button(self, text="Scenario 5", command=lambda: self.start("scenarios/scenario4.txt")),
            tk.Button(self, text="Scenario 6", command=lambda: self.start("scenarios/scenario5.txt")),
            tk.Button(self, text="Scenario Test", command=lambda: self.start("scenarios/scenario_test.txt"))
        ]
        for btn in self.buttons:
            btn.pack(anchor=W)

        # # or open a file
        # self.info2 = Label(self, text="Or open file with new board: ")
        # self.info2.pack(anchor=W)
        # self.openFileButton = tk.Button(self, text="Open file", command=self.openFile)
        # self.openFileButton.pack(anchor=W)

    def start(self, scenario):
        self.dimensions, self.variable_dict, self.constraints = read_file(scenario)

        for key, value in self.variable_dict.items() :
            print (key, value)

        initial_state = State(self.constraints, self.variable_dict, CSP())
        initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
        initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

        print ""
        print "refined variable_dict: "
        for key, value in initial_state.variable_dict.items() :
            print (key, value)

        if not initial_state.is_solution_or_contradictory():
            self.astar = AStar()
            self.astar.add_start_state_to_open(initial_state)





if __name__ == "__main__":
    app = Gui()
    app.mainloop()