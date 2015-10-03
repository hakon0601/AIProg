import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename

import input_handler
from csp_state import CSPState
from gac import GAC
from a_star_graph import AStar
from variable import Variable


class Gui(tk.Tk):
    def __init__(self, delay, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.delay = delay
        self.title("Solving nonograms")
        self.cells = {}
        self.cell_width = 25
        self.cell_height = 25

        constraint_function = input_handler.makefunc(["x", "y"], "for i in range(y): print x")
        print "jrfsd" + str(constraint_function(1, 5))

        self.create_menu()

    def create_menu(self):
        self.info1 = Label(self, text="Choose an existing scenario: ")
        self.info1.pack(anchor=W)
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

         # or open a file
        self.info2 = Label(self, text="Or open file with new scenario: ")
        self.info2.pack(anchor=W)
        self.openFileButton = tk.Button(self, text="Open file", command=self.openFile)
        self.openFileButton.pack(anchor=W)

    def start(self, scenario):
        self.cells = {}
        self.destroy_menu()
        self.dimensions, self.variable_dict, self.constraints = input_handler.read_file(scenario)

        initial_state = CSPState(self.constraints, self.variable_dict, GAC())
        initial_state.gac.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
        initial_state.gac.domain_filtering_loop(initial_state.variable_dict)

        screen_width = (self.dimensions[0] + 2)*self.cell_width
        screen_height = (self.dimensions[1] + 2)*self.cell_height
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        self.backButton = tk.Button(self,text='back', command=self.back)
        self.cancelButton = tk.Button(self,text='Cancel', command=self.cancel)
        self.backButton.pack()
        self.cancelButton.pack()

        self.draw_board(initial_state)

        if not initial_state.is_solution_or_contradictory():
            self.a_star = AStar()
            self.a_star.add_start_state_to_open(initial_state)
            self.run_a_star()

    def draw_board(self, initial_state):
        self.canvas.delete("all")
        print "dim " + str(self.dimensions)
        offset_x = self.cell_width
        offset_y = self.cell_height
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                x1 = x * self.cell_width + offset_x
                y1 = self.dimensions[1]*self.cell_height - y * self.cell_height + offset_y
                x2 = x1 + self.cell_width
                y2 = y1 - self.cell_height
                self.cells[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")

        self.update_board(initial_state)

    def update_board(self, state):
        for variable in state.variable_dict.values():
            if len(variable.domain) == 1:
                if variable.direction == "row":
                    for i in range(self.dimensions[0]):
                        if variable.domain[0][i]:
                            self.canvas.itemconfig(self.cells[i, variable.direction_nr], fill="blue")
                else:
                    for i in range(self.dimensions[1]):
                        if variable.domain[0][i]:
                            self.canvas.itemconfig(self.cells[variable.direction_nr, i], fill="blue")

    def run_a_star(self):
        print "running astar"
        continuing = False
        # if the algorithm is not finished with the board, do one iteration of the algorithm
        if not self.a_star.finished:
            result = self.a_star.do_one_step()
            if not result:
                # there are no more nodes in open nodes -> algorithm did not reach goal, fail
                print("Failed")
                return
            if result.h_value != 0:
                # the algorithm is not finished
                continuing = True
            else:
                print("Success")
                self.a_star.finished = True
        self.update_board(result)
        # as long as at least one of the algorithms is not finished,
        # run_a_star will be called over and over again
        if continuing:
            self.after(self.delay, lambda: self.run_a_star())

    def destroy_menu(self):
        for btn in self.buttons:
            btn.destroy()

        self.info1.destroy()
        self.info2.destroy()
        self.openFileButton.destroy()

    def openFile(self):
        filename = askopenfilename(parent=self)
        f = open(filename)
        f.read()
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        # start with chosen file
        self.start(filename)

    def back(self):
        # goes back to menu

        # destroy current gui elements
        for widget in self.winfo_children():
            widget.destroy()
        # back to menu
        self.create_menu()

    def cancel(self):
        # destroy window. quit program.
        self.destroy()



if __name__ == "__main__":
    app = Gui(delay=50)
    app.mainloop()