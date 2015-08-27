__author__ = 'hakon0601'
import Tkinter as tk
import random
from board import Board
from a_star import AStar
import copy
from time import sleep

from Tkinter import *

class Gui(tk.Tk):
    def __init__(self, delay, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("A*")
        self.delay = delay

        self.cell_width = 25
        self.cell_height = 25
        self.path_len = [None, None, None]
        self.search_methods = [None, None, None]
        self.generated_node_count_texts = [None, None, None]
        self.path_len_texts = [None, None, None]

        self.create_menu()

    def create_menu(self):
        self.v = StringVar()
        self.rb0 = tk.Radiobutton(self, text="Board 0", value="board0", variable=self.v)
        self.rb1 = tk.Radiobutton(self, text="Board 1", value="board1", variable=self.v, command=self.start)
        self.rb2 = tk.Radiobutton(self, text="Board 2", value="board2", variable=self.v, command=self.start)
        self.rb3 = tk.Radiobutton(self, text="Board 3", value="board3", variable=self.v, command=self.start)
        self.rb4 = tk.Radiobutton(self, text="Board 4", value="board4", variable=self.v, command=self.start)
        self.rb5 = tk.Radiobutton(self, text="Board 5", value="board5", variable=self.v, command=self.start)

        self.rb0.pack(anchor=W)
        self.rb1.pack(anchor=W)
        self.rb2.pack(anchor=W)
        self.rb3.pack(anchor=W)
        self.rb4.pack(anchor=W)
        self.rb5.pack(anchor=W)

    def destroy_menu(self):
        self.rb0.destroy()
        self.rb1.destroy()
        self.rb2.destroy()
        self.rb3.destroy()
        self.rb4.destroy()
        self.rb5.destroy()

    def start(self):
        self.destroy_menu()

        self.board_best = Board(self.v.get(), False)
        self.board_breadth = copy.deepcopy(self.board_best)
        self.board_depth = copy.deepcopy(self.board_best)
        self.boards = [self.board_best, self.board_breadth, self.board_depth]
        self.a_star_best = AStar("Best-first")
        self.a_star_breadth = AStar("Breadth-first")
        self.a_star_depth = AStar("Depth-first")
        self.a_stars = [self.a_star_best, self.a_star_breadth, self.a_star_depth]
        self.previous_open_lists = [[], [], []]
        self.previous_closed_lists = [[], [], []]

        self.rect = {}
        width = (2 + self.board_best.dim[0])*3*self.cell_width
        height = (self.board_best.dim[0] + 4)*self.cell_height
        self.canvas = tk.Canvas(self, width=width, height=height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        for i in range(len(self.boards)):
            self.a_stars[i].do_first_step(self.boards[i])
        self.draw_board()
        self.run_a_star()

    def run_a_star(self):
        continuing = False
        for i in range(len(self.boards)):
            if not self.a_stars[i].finished:
                result = self.a_stars[i].do_one_step(self.boards[i])
                if not result:
                    print("Failed")
                    self.a_stars[i].finished = True
                    continue
                if result == 1:
                    continuing = True
                else:
                    print("Success")
                    self.a_stars[i].finished = True
                    self.path_len[i] = len(result)
                    self.draw_path(result, i, 0)
                    self.boards[i].print_board()
        self.update_board()
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
