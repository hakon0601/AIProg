import Tkinter as tk
import random
from board import Board
from a_star import AStar
import copy
from time import sleep
from tkFileDialog import askopenfilename
import state

from Tkinter import *

class Gui(tk.Tk):
    def __init__(self, delay, diagonal=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("A*")
        self.delay = delay
        self.diagonal = diagonal
        self.cells = None
        self.cell_width = 25
        self.cell_height = 25
        # path length for the different search methods, added when/if algorithm is finished
        self.path_len = [None, None, None]
        # search methods that will run simultaneously
        self.search_methods = [None, None, None]
        # gui text for node count and path length
        self.generated_node_count_texts = [None, None, None]
        self.path_len_texts = [None, None, None]

        self.create_menu()

    def create_menu(self):
        # existing boards buttons
        self.info1 = Label(self, text="Choose an existing board: ")
        self.info1.pack(anchor=W)
        self.v = StringVar()
        self.buttons = [
            tk.Button(self, text="Board 0", command=lambda:self.start("board0.txt")),
            tk.Button(self, text="Board 1", command=lambda:self.start("board1.txt")),
            tk.Button(self, text="Board 2", command=lambda:self.start("board2.txt")),
            tk.Button(self, text="Board 3", command=lambda:self.start("board3.txt")),
            tk.Button(self, text="Board 4", command=lambda:self.start("board4.txt")),
            tk.Button(self, text="Board 5", command=lambda:self.start("board5.txt"))
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
        # instantiate the board
        self.board = Board(filename, self.diagonal)

        self.cells = {}

        # initialize AStar instances for the search algorithms
        self.a_stars = [AStar("Best-first"), AStar("Breadth-first"), AStar("Depth-first")]

        # Dictionary containing all the graphic rectangle objects, indexed by (i, x, y) where i is the index
        # of that board-display and x and y are coordinates on that board
        # Number of boards times their width plus one cells in between each
        screen_width = (self.board.dim[0] + len(self.a_stars) - 1)*len(self.a_stars)*self.cell_width
        screen_height = (self.board.dim[1] + 4)*self.cell_height
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # add back and cancel buttons to display
        self.backButton = tk.Button(self,text='back', command=self.back)
        self.cancelButton = tk.Button(self,text='Cancel', command=self.cancel)
        self.backButton.pack()
        self.cancelButton.pack()

        self.draw_board()

        # Adding the start state to open-list for all AStar instances
        for i in range(len(self.a_stars)):
            start_state = state.State(self.board.start[0], self.board.start[1], self.board)
            self.a_stars[i].add_start_state_to_open(start_state)

        self.run_a_star()

    def back(self):
        # goes back to menu

        # destroy current gui elements
        for widget in self.winfo_children():
            widget.destroy()

        # restart counts
        self.generated_node_count_texts = [None, None, None]
        self.path_len = [None, None, None]

        # back to menu
        self.create_menu()
    
    def cancel(self):
        # destroy window. quit program.
        self.destroy()

    def run_a_star(self):
        continuing = False
        # go through the boards (one for each search algorithm)
        for i in range(len(self.a_stars)):
            # if the algorithm is not finished with the board, do one iteration of the algorithm
            if not self.a_stars[i].finished:
                result = self.a_stars[i].do_one_step()
                if not result:
                    # there are no more nodes in open nodes -> algorithm did not reach goal, fail
                    print("Failed")
                    self.a_stars[i].finished = True
                    continue
                if result == 1:
                    # the algorithm is not finished
                    continuing = True
                else:
                    print("Success")
                    self.a_stars[i].finished = True
                    self.path_len[i] = round(result[-1].g_value * 10, 2)
                    self.draw_path(result, i, 0)
        self.update_board()
        # as long as at least one of the algorithms is not finished, 
        # run_a_star will be called over and over again
        if continuing:
            self.after(self.delay, lambda: self.run_a_star())

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(len(self.a_stars)):
            offset_x = (self.board.dim[0] + 1)*self.cell_width * i
            offset_y = self.cell_height
            for y in range(self.board.dim[1]):
                for x in range(self.board.dim[0]):
                    # Positioning the corners of the cells
                    x1 = x * self.cell_width + offset_x
                    y1 = self.board.dim[1]*self.cell_height - y * self.cell_height + offset_y
                    x2 = x1 + self.cell_width
                    y2 = y1 - self.cell_height
                    # Coloring cells depending on type
                    cell_type = self.board.board[y][x]
                    if cell_type == "O":
                        color = "white"
                    elif cell_type == "X":
                        color = "black"
                    elif cell_type == "G" or cell_type == "S":
                        color = "blue"
                    # Creates a rectangle object on the canvas and adds it to the cells dictionary
                    self.cells[i, y, x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect")
            self.draw_text(i)

    def draw_text(self, i):
        offset_x = (self.board.dim[0] + 1)*self.cell_width * i
        # Creating text items for labeling search methods
        self.search_methods[i] = self.canvas.create_text(offset_x, 0, anchor=tk.NW)
        self.canvas.itemconfig(self.search_methods[i], text=self.a_stars[i].search_method)
        self.canvas.index(self.search_methods[i], 12)

        self.generated_node_count_texts[i] = self.canvas.create_text(offset_x, (self.board.dim[0] + 1)*self.cell_height, anchor=tk.NW)
        self.canvas.itemconfig(self.generated_node_count_texts[i], text="Number of generated nodes: " + str(len(self.a_stars[i].open_nodes) + len(self.a_stars[i].closed_nodes)))
        self.canvas.index(self.generated_node_count_texts[i], 13)

        self.path_len_texts[i] = self.canvas.create_text((self.board.dim[0] + 1)*self.cell_width * i, (self.board.dim[0] + 2)*self.cell_height, anchor=tk.NW)
        self.canvas.itemconfig(self.path_len_texts[i], text="")
        self.canvas.index(self.path_len_texts[i], 14)

    def update_text(self, i):
        for i in range(3):
            self.canvas.itemconfig(self.search_methods[i], text=self.a_stars[i].search_method)
            self.canvas.itemconfig(self.generated_node_count_texts[i], text="Number of generated nodes: " + str(len(self.a_stars[i].open_nodes) + len(self.a_stars[i].closed_nodes)))
            if self.path_len[i] == 0:
                self.canvas.itemconfig(self.path_len_texts[i], text="Length of path: None")
            else:
                self.canvas.itemconfig(self.path_len_texts[i], text="Length of path: " + str(self.path_len[i]))

    def update_board(self):
        for i in range(len(self.a_stars)):
            offset_x = (self.board.dim[0] + 1)*self.cell_width * i
            offset_y = self.cell_height
            for node in self.a_stars[i].open_nodes:
                # Avoid drawing over start and goal
                if node.g_value == 0 or node.h_value == 0:
                    continue
                x1 = node.x * self.cell_width + offset_x
                y1 = self.board.dim[1]*self.cell_height - node.y * self.cell_height + offset_y
                x2 = x1 + self.cell_width
                y2 = y1 - self.cell_height
                self.canvas.itemconfig(self.cells[i, node.y, node.x], fill="gray")
            for node in self.a_stars[i].closed_nodes:
                # Avoid drawing over start and goal
                if node.g_value == 0 or node.h_value == 0:
                    continue
                x1 = node.x * self.cell_width + offset_x
                y1 = self.board.dim[1]*self.cell_height - node.y * self.cell_height + offset_y
                x2 = x1 + self.cell_width
                y2 = y1 - self.cell_height
                self.canvas.itemconfig(self.cells[i, node.y, node.x], fill="red")
            self.update_text(i)

    def draw_path(self, path, i, j):
        offset_x = (self.board.dim[0] + 1)*self.cell_width * i
        node = path[j]
        x1 = node.x * self.cell_width + offset_x
        y1 = self.board.dim[1]*self.cell_height - node.y * self.cell_height + self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 - self.cell_height

        self.canvas.create_oval(x1,y1,x2,y2, fill="green", tags="oval")
        if j < (len(path) - 1):
            self.after(100, lambda: self.draw_path(path, i, j+1))


if __name__ == "__main__":
    app = Gui(delay=50, diagonal=False)
    app.mainloop()
