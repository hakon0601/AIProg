import Tkinter as tk
from Tkinter import *
from game2048 import Game2048
from expectimax import Expectimax
from state import State
from time import time
from collections import defaultdict
import json

class Gui(tk.Tk):
    def __init__(self, delay, diagonal=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("2048-solver")
        self.cell_width = self.cell_height = 100
        self.dim = (4, 4)
        self.delay=delay
        self.neural_network_cases = json.load(open("nn_cases.txt"))
        screen_width = self.dim[0]*self.cell_width+1
        screen_height = self.dim[1]*self.cell_height+1
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.bind_keys()

        self.color_dict = self.fill_color_dict()
        self.results = []
        #self.start_game()
        self.game_board = Game2048(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.board = self.game_board.board
        self.game_board.generate_new_node()
        self.draw_board()

    def start_game(self):
        if len(self.results) < 500:
            self.game_board = Game2048(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            self.board = self.game_board.board
            self.game_board.generate_new_node()
            self.depth = 4
            self.move_count = 0
            self.expectimax = Expectimax()
            self.draw_board()
            self.time = time()
            self.run_algorithm()
        else:
            print self.results


    def run_algorithm(self):
        if self.game_board.open_cells_count() < 4:
            self.depth = 3
        else:
            self.depth = 3
        continuing = True
        if self.game_board.is_game_over():
            largest_tile = self.game_board.get_largest_tile()
            print "largest tile", largest_tile
            print "time elapsed: " + str(round(time() - self.time, 1)) + " min"
            self.results.append(largest_tile)
            continuing = False
            print "nr of cases: ", len(self.neural_network_cases)
            json.dump(self.neural_network_cases, open("nn_cases.txt",'w'))
            return self.start_game()
        current_node = State(self.game_board, self.depth)
        self.move_count += 1
        chosen_move = self.expectimax.run_expectimax(current_node, self.depth, -float("inf"), float("inf"), None)
        expectimax_result = self.expectimax.result
        flat_board = current_node.board.board[0] + current_node.board.board[1] + current_node.board.board[2] + current_node.board.board[3]
        self.neural_network_cases[str(flat_board)] = expectimax_result
        #TODO what is this? Continuing
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
        else:
            print "finished because of error in minimax chosen move"
        self.game_board.generate_new_node()
        self.draw_board()
        if continuing:
            self.after(self.delay, lambda: self.run_algorithm())

    def bind_keys(self):
        self.bind('<Up>', lambda event: self.move(self, self.game_board.move_up(), 0))
        self.bind('<Right>', lambda event: self.move(self, self.game_board.move_right(), 1))
        self.bind('<Down>', lambda event: self.move(self, self.game_board.move_down(), 2))
        self.bind('<Left>', lambda event: self.move(self, self.game_board.move_left(), 3))

    def move(self, event, is_moved, direction):
        if is_moved:
            self.game_board.generate_new_node()
            self.draw_board()
            self.f = open('/Users/hakon0601/Dropbox/Python/AIProg/AIProg_Module_5/2048trainingdata.txt', 'a')
            board = ""
            for i in range(3,-1,-1):
                board += (str(self.game_board.board[i][0])) + " "
                board += (str(self.game_board.board[i][1])) + " "
                board += (str(self.game_board.board[i][2])) + " "
                board += (str(self.game_board.board[i][3])) + " "
            board += " "
            board += str(direction)
            self.f.write(board)
            self.f.write("\n")
            self.f.close()

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
            '8192': "light goldenrod",
        }
        return color_dict

if __name__ == "__main__":
    app = Gui(delay=1)
    app.mainloop()