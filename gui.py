__author__ = 'hakon0601'
import Tkinter as tk
import random
import board
import a_star
import copy


class Gui(tk.Tk):
    def __init__(self, filename, delay, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.delay = delay
        self.filename = filename
        self.B = tk.Button(self, text ="Start", command=self.start)
        self.B.pack()

    def start(self):
        self.B.destroy()
        self.board = board.Board(self.filename)
        self.board_breadth = copy.deepcopy(self.board)
        self.board_depth = copy.deepcopy(self.board)
        self.boards = [self.board, self.board_breadth, self.board_depth]
        self.a_star = a_star.AStar("Best-first")
        self.a_star_breadth = a_star.AStar("Breadth-first")
        self.a_star_depth = a_star.AStar("Depth-first")
        self.a_stars = [self.a_star, self.a_star_breadth, self.a_star_depth]
        self.cellwidth = 25
        self.cellheight = 25



        self.canvas = tk.Canvas(self, width=(2 + self.board.dim[0])*3*self.cellwidth, height=self.board.dim[0]*3*self.cellwidth, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        label = tk.Label(self, text="dsa" )
        label.place(relx=1, x=-2, y=2, anchor=tk.CENTER)
        label.pack()


        for i in range(len(self.boards)):
            self.a_stars[i].do_first_step(self.boards[i])


        self.run_astar()


    def run_astar(self):
        continuing = False
        for i in range(len(self.boards)):
            if not self.a_stars[i].finished:
                node = self.a_stars[i].do_one_step(self.boards[i])
                if not node:
                    print("Failed")
                    self.a_stars[i].finished = True
                    continue
                if node.type == "G":
                    print("Success")
                    self.a_stars[i].finished = True
                    self.boards[i].reconstruct_path(node)
                    self.boards[i].print_board()
                    print("Nodes generated: " + str(len(self.a_star.open_nodes) + len(self.a_star.closed_nodes)))
                else:
                    continuing = True
        self.draw_board()
        if continuing:
            self.after(self.delay, lambda: self.run_astar())


    def draw_board(self):
        self.canvas.delete("all")
        for i in range(len(self.boards)):
            offset = (self.board.dim[0] + 1)*self.cellwidth * i
            for y in range(self.board.dim[1]):
                for x in range(self.board.dim[0]):
                    x1 = x * self.cellwidth + offset
                    y1 = self.board.dim[1]*self.cellheight - y * self.cellheight
                    x2 = x1 + self.cellwidth
                    y2 = y1 - self.cellheight
                    if self.boards[i].board[y][x].type == "O":
                        color = "white"
                    elif self.boards[i].board[y][x].type == "X":
                        color = "black"
                    if self.boards[i].board[y][x] in self.a_stars[i].open_nodes:
                        color = "gray"
                    elif self.boards[i].board[y][x] in self.a_stars[i].closed_nodes:
                        color = "red"

                    if self.boards[i].board[y][x].type == "G" or self.boards[i].board[y][x].type == "S":
                        color = "blue"
                    elif self.boards[i].board[y][x].type == "A":
                        color = "green"

                    self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")

if __name__ == "__main__":
    app = Gui("board6", 50)
    app.mainloop()
