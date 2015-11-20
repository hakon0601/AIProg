import tkinter as tk
from game2048 import Game2048
from state import State
from time import time
from move_classifier import MoveClassifier
from expectimax import Expectimax
import numpy as np
import json
import copy
import random
import scipy
from math import log, ceil


class Gui(tk.Tk):
    def __init__(self, delay, collect_cases=False, *args, **kwargs):
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
        self.collect_cases = collect_cases
        self.color_dict = self.fill_color_dict()
        if collect_cases:
            self.neural_network_cases = json.load(open("nn_cases_by_nn.txt"))
        self.results = []
        self.start_time = time()
        print("Commands")
        print("t: Test the network classification with a never before seen test set")
        print("tl: Test the network using the training set")
        print("s: Run infinite times using NN")
        print("p: Run 50 games using NN")
        print("r: Run 50 games using a random player")
        print("c: Compare the two runs of 50")
        self.user_control()
        self.start_game()

    def start_game(self):
        if len(self.results) < self.results_length:
        #self.user_control()
        #if True:
            print("run nr", len(self.results))
            self.game_board = Game2048(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            self.board = self.game_board.board
            self.game_board.generate_new_node()
            self.depth = 3
            self.move_count = 0
            self.expectimax = Expectimax()
            self.draw_board()
            self.time = time()
            self.run_algorithm()
        else:
            print(self.results)
            if self.action[0] == "p":
                self.results_from_nn_playing = copy.copy(self.results)
                print("largest tile", max(self.results_from_nn_playing))
                print("average tile", sum(self.results_from_nn_playing)/float(len(self.results_from_nn_playing)))
            elif self.action[0] == "r":
                self.results_from_random_playing = copy.copy(self.results)
                print("largest tile", max(self.results_from_random_playing))
                print("average tile", sum(self.results_from_random_playing)/float(len(self.results_from_random_playing)))
            self.results = []
            self.user_control()
            self.start_game()

    def user_control(self):
        nr_of_training_cases = 10000
        nr_of_test_cases = 1000
        # nodes_in_each_layer = list(map(int, input("Hidden nodes in each layer: ").replace(" ", "").split(",")))
        # print("TanH: 1, Sigmoid: 2, Rectify: 3, Softmax: 4")
        # activation_functions = list(map(int, input("Select activation functions: ").replace(" ", "").split(",")))
        # learning_rate = float(input("learning rate: "))
        # bulk_size = int(input("Bulk size: "))
        nodes_in_each_layer = [700]
        activation_functions = [3, 4]
        learning_rate = 0.02
        number_of_input_nodes = 16
        number_of_output_nodes = 4
        bulk_size = 100
        self.move_classifier = MoveClassifier(nr_of_training_cases=nr_of_training_cases, nr_of_test_cases=nr_of_test_cases,
                                              nr_of_nodes_in_layers=nodes_in_each_layer,
                                              act_functions=activation_functions, lr=learning_rate, number_of_input_nodes=number_of_input_nodes,
                                              number_of_output_nodes=number_of_output_nodes, bulk_size=bulk_size)
        self.move_classifier.preprosessing(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        self.move_classifier.test_preprosessing(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        self.move_classifier.preprosessing(boards=self.move_classifier.test_boards, labels=self.move_classifier.test_labels)
        #self.move_classifier.preprosessing_merging(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        #self.move_classifier.preprosessing_merging(boards=self.move_classifier.test_boards, labels=self.move_classifier.test_labels)

        errors = []

        while True:
            self.action = input("Enter a command or a number to train: ")
            if self.action[0] == "t":
                if len(self.action) == 1:
                    output_activations = self.move_classifier.do_testing(boards=self.move_classifier.test_boards)
                    print("Statistics (test set): \t\t", self.move_classifier.check_result(output_activations, labels=self.move_classifier.test_labels), "%")
                    #test_labels, result = self.move_classifier.do_testing(self.move_classifier.test_boards, self.move_classifier.test_labels)
                    #training_labels, training_result = self.move_classifier.do_testing(self.move_classifier.boards, self.move_classifier.labels)
                elif self.action[1] == "l":
                    output_activations = self.move_classifier.do_testing(boards=self.move_classifier.boards)
                    print("Statistics (training set):\t ", self.move_classifier.check_result(output_activations, labels=self.move_classifier.labels), "%")
            elif self.action[0] == "s":
                self.results_length = float('inf')
                return
            elif self.action[0] == "p" or self.action[0] == "r":
                self.results_length = 50
                return

            elif self.action[0] == "c":
                if len(self.results_from_nn_playing)+len(self.results_from_random_playing) < 100:
                    continue
                print("NN results:\t", self.results_from_nn_playing)
                print("Random results:\t", self.results_from_random_playing)
                print("largest tiles", max(self.results_from_nn_playing),  max(self.results_from_random_playing))
                print("average tiles", sum(self.results_from_nn_playing)/float(len(self.results_from_nn_playing)), sum(self.results_from_random_playing)/float(len(self.results_from_random_playing)))
                p = scipy.stats.ttest_ind(self.results_from_nn_playing, self.results_from_random_playing).pvalue
                print("score: ", max(0,min(7, ceil(-log(p,10)))))
            else:
                errors = self.move_classifier.do_training(epochs=int(self.action), errors=errors)
                output_activations = self.move_classifier.do_testing(boards=self.move_classifier.test_boards)
                print("Statistics (test set):\t\t ", self.move_classifier.check_result(output_activations, labels=self.move_classifier.test_labels), "%")
                output_activations = self.move_classifier.do_testing(boards=self.move_classifier.boards)
                print("Statistics (training set):\t ", self.move_classifier.check_result(output_activations, labels=self.move_classifier.labels), "%")

            print("Total time elapsed: " + str(round((time() - self.start_time)/60, 1)) + " min")


    def run_algorithm(self):
        continuing = True
        if self.game_board.is_game_over():
            largest_tile = self.game_board.get_largest_tile()
            print("largest tile", largest_tile)
            self.results.append(largest_tile)
            if self.collect_cases:
                print("size of training data", len(self.neural_network_cases))
                json.dump(self.neural_network_cases, open("nn_cases_by_nn.txt", 'w'))
            continuing = False
            return self.start_game()
        current_node = State(self.game_board, self.depth)
        self.move_count += 1
        chosen_move = self.expectimax.run_expectimax(current_node, self.depth, -float("inf"), float("inf"), None)
        expectimax_result = self.expectimax.result
        flat_board = current_node.board.board[3] + current_node.board.board[2] + current_node.board.board[1] + current_node.board.board[0]
        if self.collect_cases:
            self.neural_network_cases[str(flat_board)] = expectimax_result
        if self.action[0] == "r":
            chosen_move = self.choose_legal_random_move()
        else:
            result = self.move_classifier.predictor([flat_board])
            chosen_move = self.choose_legal_move_from_nn(result)
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

    def choose_legal_random_move(self):
        while True:
            r = random.randint(0,3)
            if self.game_board.is_move_legal(r):
                return r

    def choose_legal_move_from_nn(self, result):
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
    app = Gui(delay=2, collect_cases=False)
    app.mainloop()