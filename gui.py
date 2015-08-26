__author__ = 'hakon0601'
import Tkinter as tk
import random
import board
import a_star


class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.board = board.Board("board6")
        self.a_star = a_star.AStar()

        self.canvas = tk.Canvas(self, width=1000, height=1000, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = 25
        self.cellheight = 25


        self.rect = {}
        self.draw_board()

        self.a_star.do_first_step(self.board)
        self.redraw(200)

    def redraw(self, delay):
        node = self.a_star.do_one_step(self.board)
        if not node:
            print("Failed")
            return
        if node.type == "G":
            print("Success")
            self.board.reconstruct_path(node)
            self.board.print_board()
            self.draw_board()
        else:
            self.draw_board()
            self.after(delay, lambda: self.redraw(delay))

    def draw_board(self):
        for y in range(self.board.dim[1]):
            for x in range(self.board.dim[0]):
                x1 = x * self.cellwidth
                y1 = self.board.dim[1]*self.cellheight - y * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 - self.cellheight
                if self.board.board[y][x].type == "O":
                    color = "blue"
                elif self.board.board[y][x].type == "X":
                    color = "red"
                if self.board.board[y][x] in self.a_star.open_nodes:
                    color = "gray"
                elif self.board.board[y][x] in self.a_star.closed_nodes:
                    color = "yellow"

                if self.board.board[y][x].type == "G" or self.board.board[y][x].type == "S":
                    color = "black"
                elif self.board.board[y][x].type == "A":
                    color = "green"

                self.rect[y,x] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")

if __name__ == "__main__":
    app = Gui()
    app.mainloop()
