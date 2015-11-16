import tkinter as tk
from game2048 import Game2048
from state import State
from time import time
from move_classifier import MoveClassifier
import numpy as np

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
        self.user_control()
        self.color_dict = self.fill_color_dict()
        self.results = []
        self.start_game()

    def start_game(self):
        if len(self.results) < 1:
            self.game_board = Game2048(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            self.board = self.game_board.board
            self.game_board.generate_new_node()
            self.depth = 4
            self.move_count = 0
            self.draw_board()
            self.time = time()
            self.run_algorithm()
        else:
            print(self.results)


    def user_control(self):
        nr_of_training_cases = 1000
        nr_of_test_cases = 100
        nr_of_hidden_layers = 1
        nr_of_nodes_in_layers = [80]
        act_functions = [3,4]
        lr = 0.2
        number_of_input_nodes = 16
        number_of_output_nodes = 4
        bulk_size = 1
        self.move_classifier = MoveClassifier(nr_of_training_cases=nr_of_training_cases, nr_of_test_cases=nr_of_test_cases,
                                              nr_of_hidden_layers=nr_of_hidden_layers, nr_of_nodes_in_layers=nr_of_nodes_in_layers,
                                              act_functions=act_functions, lr=lr, number_of_input_nodes=number_of_input_nodes,
                                              number_of_output_nodes=number_of_output_nodes, bulk_size=bulk_size)
        self.move_classifier.preprosessing(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        self.move_classifier.preprosessing(boards=self.move_classifier.test_boards, labels=self.move_classifier.test_labels)

        errors = []

        start_time = time()
        while True:
            action = input("Enter a integer x to train x epocs, t to test: ")
            if action[0] == "t":
                test_labels, result = self.move_classifier.do_testing()
            elif action[0] == "s":
                return
            else:
                #errors = digit_recog.do_training(epochs=int(action), errors=errors)
                results = []
                for i in range(int(action)):
                    errors = self.move_classifier.do_training(epochs=1, errors=errors)
                    test_labels, result = self.move_classifier.do_testing()
                    results.append(float(self.move_classifier.check_result(result)))

                for i in range(len(results)):
                    print(results[i])
            print("Total time elapsed: " + str((time() - start_time)/60) + " min")


    def run_algorithm(self):
        if self.game_board.open_cells_count() < 4:
            self.depth = 3
        else:
            self.depth = 3
        continuing = True
        if self.game_board.is_game_over():
            largest_tile = self.game_board.get_largest_tile()
            print("largest tile", largest_tile)
            print("time elapsed: " + str(round(time() - self.time, 1)) + " min")
            self.results.append(largest_tile)
            continuing = False
            return self.start_game()
        current_node = State(self.game_board, self.depth)
        self.move_count += 1
        #chosen_move = self.expectimax.run_expectimax(current_node, self.depth, -float("inf"), float("inf"), None)
        flat_board = current_node.board.board[3] + current_node.board.board[2] + current_node.board.board[1] + current_node.board.board[0]
        result = self.move_classifier.predictor([flat_board])
        chosen_move = self.get_best_legal_move(result)
        if chosen_move == 0:
            self.game_board.move_left()
        elif chosen_move == 1:
            self.game_board.move_right()
        elif chosen_move == 2:
            self.game_board.move_up()
        elif chosen_move == 3:
            self.game_board.move_down()
        else:
            print("finished because of error in minimax chosen move")
        self.game_board.generate_new_node()
        self.draw_board()
        if continuing:
            self.after(self.delay, lambda: self.run_algorithm())

    def get_best_legal_move(self, result):
        chosen_move = None

        while chosen_move == None or not self.game_board.is_move_legal(chosen_move):
            if chosen_move != None:
                result[0][chosen_move] = -1
            chosen_move = np.argmax(result[0])
        return chosen_move

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
            '8192': "light goldenrod",
        }
        return color_dict

if __name__ == "__main__":
    app = Gui(delay=200)
    app.mainloop()