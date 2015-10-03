import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename

import input_handler
from AIProg_Module_2.gac import GAC
from a_star_graph import AStar
from state import State


class Gui(tk.Tk):
    def __init__(self, delay, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("GAC with A*")
        self.delay = delay
        self.oval_radius = 15
        self.color_dict = {0: "blue", 1: "green", 2: "red", 3: "black", 4: "gray", 5: "yellow"}

        self.create_menu()

    def create_menu(self):
        # existing boards buttons
        self.info1 = Label(self, text="Choose an existing graph: ")
        self.info1.pack(anchor=W)
        self.v = StringVar()
        self.buttons = [
            tk.Button(self, text="Graph 0", command=lambda: self.start("graphs/graph0.txt")),
            tk.Button(self, text="Graph 1", command=lambda: self.start("graphs/graph1.txt")),
            tk.Button(self, text="Graph color 1", command=lambda: self.start("graphs/graph-color-1.txt")),
            tk.Button(self, text="Graph color 2", command=lambda: self.start("graphs/graph-color-2.txt")),
            tk.Button(self, text="Rand 50 - 4", command=lambda: self.start("graphs/rand-50-4-color1.txt")),
            tk.Button(self, text="Rand 100 - 4", command=lambda: self.start("graphs/rand-100-4-color1.txt")),
            tk.Button(self, text="Rand 100 - 6", command=lambda: self.start("graphs/rand-100-6-color1.txt")),
            tk.Button(self, text="Spiral 500 - 4", command=lambda: self.start("graphs/spiral-500-4-color1.txt"))
        ]
        for btn in self.buttons:
            btn.pack(anchor=W)

        # or open a file
        self.info2 = Label(self, text="Or open file with new board: ")
        self.info2.pack(anchor=W)
        self.openFileButton = tk.Button(self, text="Open file", command=self.openFile)
        self.openFileButton.pack(anchor=W)

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

    def destroy_menu(self):
        for btn in self.buttons:
            btn.destroy()

        self.info1.destroy()
        self.info2.destroy()
        self.openFileButton.destroy()


    def start(self, filename):
        # destroy menu when algorithm illustrations begins
        self.destroy_menu()
        print filename

        self.nodes = {}

        variable_dict, constraints = input_handler.read_file(filename)
        initial_state = State(constraints, variable_dict, GAC())
        print "init State: " + str(initial_state)
        initial_state.csp.init_revise_queue(initial_state.constraints, initial_state.variable_dict)
        initial_state.csp.domain_filtering_loop(initial_state.variable_dict)

        self.screen_width = self.winfo_screenwidth() - 100
        self.screen_height = self.winfo_screenheight() - 200
        print (self.screen_width, self.screen_height)
        self.normalize_coordinates(initial_state)
        print "normalized init State: " + str(initial_state)
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # add back and cancel buttons to display
        self.backButton = tk.Button(self,text='back', command=self.back)
        self.cancelButton = tk.Button(self,text='Cancel', command=self.cancel)
        self.backButton.pack()
        self.cancelButton.pack()

        self.draw_board(initial_state)

        if not initial_state.is_solution_or_contradictory():
            self.a_star = AStar()
            self.a_star.add_start_state_to_open(initial_state)
            self.run_a_star()


    def back(self):
        # goes back to menu

        # destroy current gui elements
        for widget in self.winfo_children():
            widget.destroy()
        # TODO restart counts

        # back to menu
        self.create_menu()

    def cancel(self):
        # destroy window. quit program.
        self.destroy()

    def draw_board(self, initial_state):
        self.canvas.delete("all")
        for variable in initial_state.variable_dict.values():
            x1 = variable.x
            y1 = variable.y + self.oval_radius
            x2 = x1 + self.oval_radius
            y2 = y1 - self.oval_radius
            color = "white"
            if len(variable.domain) == 1:
                color = self.color_dict[variable.domain[0]]
            self.nodes[variable.index] = self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags="rect")

        for constraint in initial_state.constraints:
            x1 = initial_state.variable_dict[constraint.involved_variables[0]].x + self.oval_radius/2
            y1 = initial_state.variable_dict[constraint.involved_variables[0]].y + self.oval_radius/2
            x2 = initial_state.variable_dict[constraint.involved_variables[1]].x + self.oval_radius/2
            y2 = initial_state.variable_dict[constraint.involved_variables[1]].y + self.oval_radius/2
            self.canvas.create_line(x1, y1, x2, y2)

    def update_board(self, state):
        for variable in state.variable_dict.values():
            if len(variable.domain) == 1:
                self.canvas.itemconfig(self.nodes[variable.index], fill=self.color_dict[variable.domain[0]])

    def normalize_coordinates(self, initial_state):
        old_min_x = float("inf")
        old_min_y = float("inf")
        old_max_x = 0
        old_max_y = 0
        for variable in initial_state.variable_dict.values():
            if variable.x <= old_min_x:
                old_min_x = variable.x
            if variable.x >= old_max_x:
                old_max_x = variable.x
            if variable.y <= old_min_y:
                old_min_y = variable.y
            if variable.y >= old_max_y:
                old_max_y = variable.y
        old_range_x = old_max_x - old_min_x
        old_range_y = old_max_y - old_min_y

        new_range_x = self.screen_width - self.oval_radius
        new_range_y = self.screen_height - self.oval_radius
        for variable in initial_state.variable_dict.values():
            variable.x = (variable.x - old_min_x) / old_range_x * new_range_x
            variable.y = (variable.y - old_min_y) / old_range_y * new_range_y


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

if __name__ == "__main__":
    app = Gui(delay=50)
    app.mainloop()
