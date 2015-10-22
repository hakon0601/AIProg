import Tkinter as tk
from Tkinter import *
from game2048 import Game2048
from minimax import Minimax
from state import State

class Gui(tk.Tk):
    def __init__(self, delay, diagonal=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("2048-solver")
        self.cell_width = self.cell_height = 50
        self.dim = (4, 4)
        self.delay=delay
        screen_width = self.dim[0]*self.cell_width+1
        screen_height = self.dim[1]*self.cell_height+1
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        #self.bind_keys()

        self.color_dict = self.fill_color_dict()
        self.game_board = Game2048()
        self.board = self.game_board.board
        self.game_board.generate_new_node()
        self.depth = 4
        self.move_count = 0
        self.minimax = Minimax()

        self.draw_board()
        self.run_algorithm()
        #print "instances of State: " + str(State._ids)

    def run_algorithm(self):
        if self.game_board.open_cells_count() < 4:
            self.depth = 4
        else:
            self.depth = 4
        continuing = True
        if self.game_board.is_game_over():
            print "finished cause game_board is gameover"
            continuing = False
        current_node = State(self.game_board, self.depth)
        self.move_count += 1
        chosen_move = self.minimax.minimax_alpha_beta(current_node, self.depth, -float("inf"), float("inf"), None)
        if chosen_move == None:
            Continuing = False
        elif chosen_move == 0:
            Continuing = False
        elif chosen_move == "left":
            self.game_board.move_left()
        elif chosen_move == "right":
            self.game_board.move_right()
        elif chosen_move == "up":
            self.game_board.move_up()
        elif chosen_move == "down":
            self.game_board.move_down()
            # if not self.game_board.move_left():
            #     if not self.game_board.move_up():
            #         if not self.game_board.move_right():
            #             self.game_board.move_down()
        else:
            print "finished because of error in minimax chosen move"
        self.game_board.generate_new_node()
        self.draw_board()
        if continuing:
            self.after(self.delay, lambda: self.run_algorithm())

    def bind_keys(self):
        self.bind('<Up>', lambda event: self.move(self, self.game_board.move_up()))
        self.bind('<Down>', lambda event: self.move(self, self.game_board.move_down()))
        self.bind('<Right>', lambda event: self.move(self, self.game_board.move_right()))
        self.bind('<Left>', lambda event: self.move(self, self.game_board.move_left()))

    def move(self, event, is_moved):
        if is_moved:
            self.game_board.generate_new_node()
            self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(self.dim[1]):
                for x in range(self.dim[0]):
                    x1 = x * self.cell_width
                    y1 = self.dim[1]*self.cell_height - y * self.cell_height
                    x2 = x1 + self.cell_width
                    y2 = y1 - self.cell_height
                    cell_type = self.board[y][x]
                    text = str(self.board[y][x])
                    color = self.color_dict[str(self.board[y][x])]
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect")
                    if cell_type != 0:
                        self.canvas.create_text(x1+self.cell_width/2, y1-self.cell_height/2, text=text)

    def fill_color_dict(self):
        color_dict = {
            '0': "white",
            '2': "lemon chiffon",
            '4': "peach puff",
            '8': "sandy brown",
            '16': "dark orange",
            '32': "salmon",
            '64': "tomato",
            '128': "khaki",
            '256': "khaki",
            '512': "red",
            '1024': "light goldenrod",
            '2048': "firebrick",
            '4096': "dim grey",
        }
        return color_dict

if __name__ == "__main__":
    app = Gui(delay=50)
    app.mainloop()