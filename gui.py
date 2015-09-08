__author__ = 'hakon0601'
import Tkinter as tk
import random
from board import Board
from a_star import AStar
import copy
from time import sleep
from tkFileDialog import askopenfilename

from Tkinter import *

class Gui(tk.Tk):
    def __init__(self, delay, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("A*")
        self.delay = delay
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
        self.rb0 = tk.Button(self, text="Board 0", command=lambda:self.start("board0.txt"))
        self.rb1 = tk.Button(self, text="Board 1", command=lambda:self.start("board1.txt"))
        self.rb2 = tk.Button(self, text="Board 2", command=lambda:self.start("board2.txt"))
        self.rb3 = tk.Button(self, text="Board 3", command=lambda:self.start("board3.txt"))
        self.rb4 = tk.Button(self, text="Board 4", command=lambda:self.start("board4.txt"))
        self.rb5 = tk.Button(self, text="Board 5", command=lambda:self.start("board5.txt"))
        self.rb0.pack(anchor=W)
        self.rb1.pack(anchor=W)
        self.rb2.pack(anchor=W)
        self.rb3.pack(anchor=W)
        self.rb4.pack(anchor=W)
        self.rb5.pack(anchor=W)

        # or open a file
        self.info2 = Label(self, text="Or open file with new board: ")
        self.info2.pack(anchor=W)
        self.openFileButton = tk.Button(self, text="Open file", command=self.openFile)
        self.openFileButton.pack(anchor=W)

    def openFile(self):
        filename = askopenfilename(parent=self)
        print "filename"
        print filename
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
        self.rb0.destroy()
        self.rb1.destroy()
        self.rb2.destroy()
        self.rb3.destroy()
        self.rb4.destroy()
        self.rb5.destroy()
        self.info1.destroy()
        self.info2.destroy()
        self.openFileButton.destroy()

    def start(self, boardnumber):
        # destroy menu when algorithm illustrations begins
        self.destroy_menu()

        # instances of the board, one for each search algorithm
        self.board_best = Board(str(boardnumber), False)
        self.board_breadth = copy.deepcopy(self.board_best)
        self.board_depth = copy.deepcopy(self.board_best)
        self.boards = [self.board_best, self.board_breadth, self.board_depth]

        # initialize AStar instances for the search algorithms
        self.a_star_best = AStar("Best-first")
        self.a_star_breadth = AStar("Breadth-first")
        self.a_star_depth = AStar("Depth-first")

        # add them to a list with all AStar instances
        self.a_stars = [self.a_star_best, self.a_star_breadth, self.a_star_depth]
        self.previous_open_lists = [[], [], []]
        self.previous_closed_lists = [[], [], []]

        self.rect = {}
        width = (2 + self.board_best.dim[0])*3*self.cell_width
        height = (self.board_best.dim[0] + 4)*self.cell_height
        self.canvas = tk.Canvas(self, width=width, height=height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # add back and cancel buttons to display
        self.backButton = tk.Button(self,text='back', command=self.back)
        self.cancelButton = tk.Button(self,text='Cancel', command=self.cancel)
        self.backButton.pack()
        self.cancelButton.pack()

        # do first step for all AStar instances
        for i in range(len(self.boards)):
            self.a_stars[i].do_first_step(self.boards[i])
        
        self.draw_board()
        self.run_a_star()

    def back(self):
        # goes back to menu

        # destroy current gui elements
        for widget in self.winfo_children():
            widget.destroy()

        # restart counts
        self.generated_node_count_texts[0] = "?"
        self.generated_node_count_texts[1] = "?"
        self.generated_node_count_texts[2] = "?"
        self.path_len[0] = 0
        self.path_len[1] = 0
        self.path_len[2] = 0

        # back to menu
        self.create_menu()
    
    def cancel(self):
        # destroy window. quit program.
        self.destroy()

    def run_a_star(self):
        continuing = False
        # go through the boards (one for each search algorithm)
        for i in range(len(self.boards)):
            # if the algorithm is not finished upon the board, do one iteration of the algorithm
            if not self.a_stars[i].finished:
                result = self.a_stars[i].do_one_step(self.boards[i])
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
                    self.path_len[i] = len(result)
                    self.draw_path(result, i, 0)
                    self.boards[i].print_board()
        self.update_board()
        # as long as at least one of the algorithms is not finished, 
        # run_a_star will be called over and over again
        if continuing:
            self.after(self.delay, lambda: self.run_a_star())

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(len(self.boards)):
            offset_x = (self.board_best.dim[0] + 1)*self.cell_width * i
            offset_y = self.cell_height
            for y in range(self.board_best.dim[1]):
                for x in range(self.board_best.dim[0]):
                    x1 = x * self.cell_width + offset_x
                    y1 = self.board_best.dim[1]*self.cell_height - y * self.cell_height + offset_y
                    x2 = x1 + self.cell_width
                    y2 = y1 - self.cell_height
                    if self.boards[i].board[y][x].type == "O":
                        color = "white"
                    elif self.boards[i].board[y][x].type == "X":
                        color = "black"
                    elif self.boards[i].board[y][x].type == "G" or self.boards[i].board[y][x].type == "S":
                        color = "blue"
                    elif self.boards[i].board[y][x].type == "A":
                        color = "green"

                    self.rect[i,y,x] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")
            self.draw_text(i)

    def draw_text(self, i):
        offset_x = (self.board_best.dim[0] + 1)*self.cell_width * i
        self.search_methods[i] = self.canvas.create_text(offset_x, 0, anchor=tk.NW)
        self.canvas.itemconfig(self.search_methods[i], text=self.a_stars[i].search_method)
        self.canvas.index(self.search_methods[i], 12)
        self.generated_node_count_texts[i] = self.canvas.create_text(offset_x, (self.board_best.dim[0] + 1)*self.cell_height, anchor=tk.NW)
        self.canvas.itemconfig(self.generated_node_count_texts[i], text="Number of generated nodes: " + str(len(self.a_stars[i].open_nodes) + len(self.a_stars[i].closed_nodes)))
        self.canvas.index(self.generated_node_count_texts[i], 13)
        self.path_len_texts[i] = self.canvas.create_text((self.board_best.dim[0] + 1)*self.cell_width * i, (self.board_best.dim[0] + 2)*self.cell_height, anchor=tk.NW)
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
        for i in range(len(self.boards)):
            offset_x = (self.board_best.dim[0] + 1)*self.cell_width * i
            offset_y = self.cell_height
            changed_in_open = [node for node in self.a_stars[i].open_nodes if node not in self.previous_open_lists]
            changed_in_closed = [node for node in self.a_stars[i].closed_nodes if node not in self.previous_closed_lists]
            self.previous_open_lists = self.a_stars[i].open_nodes
            self.previous_closed_lists = self.a_stars[i].closed_nodes
            for node in changed_in_open:
                x1 = node.x * self.cell_width + offset_x
                y1 = self.board_best.dim[1]*self.cell_height - node.y * self.cell_height + offset_y
                x2 = x1 + self.cell_width
                y2 = y1 - self.cell_height
                self.canvas.itemconfig(self.rect[i, node.y, node.x], fill="gray")
            for node in changed_in_closed:
                x1 = node.x * self.cell_width + offset_x
                y1 = self.board_best.dim[1]*self.cell_height - node.y * self.cell_height + offset_y
                x2 = x1 + self.cell_width
                y2 = y1 - self.cell_height
                self.canvas.itemconfig(self.rect[i, node.y, node.x], fill="red")
            self.update_text(i)

    def draw_path(self, path, i, j):
        offset_x = (self.board_best.dim[0] + 1)*self.cell_width * i
        node = path[j]
        x1 = node.x * self.cell_width + offset_x
        y1 = self.board_best.dim[1]*self.cell_height - node.y * self.cell_height + self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 - self.cell_height

        self.canvas.create_oval(x1,y1,x2,y2, fill="green", tags="oval")
        if j < (len(path) - 1):
            self.after(100, lambda: self.draw_path(path, i, j+1))


if __name__ == "__main__":
    app = Gui(5)
    app.mainloop()
