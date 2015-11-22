from time import time
import copy
import requests
from random import randint
import numpy as np

from file_handler import *
from move_classifier import MoveClassifier
from game2048 import Game2048
from expectimax import Expectimax
from state import State


class GameController():

    NR_OF_TRAINING_CASES = 7000
    NR_OF_TEST_CASES = 833

    def __init__(self, collect_cases=False, depth=3):
        self.collect_cases = collect_cases
        self.depth = depth
        if collect_cases:
            self.neural_network_cases = load_cases()
            self.expectimax = Expectimax()
        self.results_from_nn_playing = []
        self.results_from_random_playing = []
        self.results = []
        self.results_from_random_playing = [112]*50
        self.start_time = time()
        self.print_commands()
        self.setup_network(use_default=True)
        self.user_control()
        self.start_game()

    def start_game(self):
        if len(self.results) < self.results_length:
            print("run nr", len(self.results))
            self.game_board = Game2048(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            self.board = self.game_board.board
            self.game_board.generate_new_node()
            self.move_count = 0
            #self.draw_board()
            self.time = time()
            self.run_algorithm()
        else:
            print(self.results)
            print("Largest tile", max(self.results))
            print("Average tile", sum(self.results)/float(len(self.results)))
            if self.action[0] == "p":
                self.results_from_nn_playing = copy.copy(self.results)
            elif self.action[0] == "r":
                self.results_from_random_playing = copy.copy(self.results)
            elif self.action[0] == "c":
                self.results_from_nn_playing = copy.copy(self.results)
                self.print_comparison()
            self.results = []
            self.user_control()
            self.start_game()

    def setup_network(self, use_default=False):
        nr_of_training_cases = GameController.NR_OF_TRAINING_CASES
        nr_of_test_cases = GameController.NR_OF_TEST_CASES
        if use_default:
            nodes_in_each_layer = [700]
            activation_functions = [3, 4]
            learning_rate = 0.02
            number_of_input_nodes = 24
            number_of_output_nodes = 4
            bulk_size = 1
        else:
            nodes_in_each_layer = list(map(int, input("Hidden nodes in each layer: ").replace(" ", "").split(",")))
            print("TanH: 1, Sigmoid: 2, Rectify: 3, Softmax: 4")
            activation_functions = list(map(int, input("Select activation functions: ").replace(" ", "").split(",")))
            learning_rate = float(input("learning rate: "))
            bulk_size = int(input("Bulk size: "))

        self.move_classifier = MoveClassifier(nr_of_training_cases=nr_of_training_cases,
                                              nr_of_test_cases=nr_of_test_cases,
                                              nr_of_nodes_in_layers=nodes_in_each_layer,
                                              act_functions=activation_functions, lr=learning_rate,
                                              number_of_input_nodes=number_of_input_nodes,
                                              number_of_output_nodes=number_of_output_nodes,
                                              bulk_size=bulk_size)

        extra_nodes = self.move_classifier.preprocessing_row_column(boards=self.move_classifier.boards)
        extra_test_nodes = self.move_classifier.preprocessing_row_column(boards=self.move_classifier.test_boards)

        self.move_classifier.preprocessing(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        self.move_classifier.preprocessing(boards=self.move_classifier.test_boards, labels=self.move_classifier.test_labels)
        #self.move_classifier.test_preprocessing(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        #self.move_classifier.preprocessing_merging(boards=self.move_classifier.boards, labels=self.move_classifier.labels)
        #self.move_classifier.preprocessing_merging(boards=self.move_classifier.test_boards, labels=self.move_classifier.test_labels)

        self.move_classifier.add_extra_nodes(self.move_classifier.boards, extra_nodes)
        self.move_classifier.add_extra_nodes(self.move_classifier.test_boards, extra_test_nodes)
        self.errors = []

    def user_control(self):
        while True:
            self.action = input("Enter a command or a number to train: ")
            # Test classification percentage using both the test set and training set
            if self.action[0] == "t":
                self.test_percentage_training_and_test_set()
            # Play forever
            elif self.action[0] == "s":
                self.results_length = float('inf')
                return
            # Play 50 games, using the neural net p or a random player r
            elif self.action[0] == "p" or self.action[0] == "r":
                self.results_length = 50
                return
            # Run the grading function
            elif self.action[0] == "c":
                if len(self.results_from_nn_playing) < 50:
                    self.results_length = 50
                    return
                else:
                    self.print_comparison()
            elif self.action[0] == "l":
                self.collect_cases = not self.collect_cases
                if self.collect_cases:
                    self.neural_network_cases = load_cases()
                    self.expectimax = Expectimax()
            else:
                self.errors = self.move_classifier.do_training(epochs=int(self.action), errors=self.errors)
                self.test_percentage_training_and_test_set()

            print("Total time elapsed: " + str(round((time() - self.start_time)/60, 1)) + " min")


    def run_algorithm(self):
        self.continuing = True
        if self.game_board.is_game_over():
            self.conclude_game()
            return self.start_game()
        current_node = State(self.game_board, self.depth)
        self.move_count += 1
        flat_board = current_node.board.board[3] + current_node.board.board[2] + current_node.board.board[1] + current_node.board.board[0]
        if self.collect_cases:
            self.gather_case_and_result_using_expectimax(current_node, flat_board)
        if self.action[0] == "r":
            chosen_move = self.choose_legal_random_move()
        else:
            extra_nodes = self.move_classifier.preprocessing_row_column(boards=[flat_board])
            self.move_classifier.preprocessing(boards=[flat_board], labels=None)
            flat_board = self.move_classifier.add_extra_nodes([flat_board], extra_nodes)[0]

            output_activations = self.move_classifier.predictor([flat_board])
            chosen_move = self.choose_legal_move_from_nn(output_activations)

        self.do_move(chosen_move)
        self.game_board.generate_new_node()

    def do_move(self, chosen_move):
        if chosen_move == 0:
            self.game_board.move_left()
        elif chosen_move == 1:
            self.game_board.move_right()
        elif chosen_move == 2:
            self.game_board.move_up()
        elif chosen_move == 3:
            self.game_board.move_down()

    def conclude_game(self):
        self.continuing = False
        largest_tile = self.game_board.get_largest_tile()
        print("Largest tile", largest_tile)
        self.results.append(largest_tile)
        print("Average tile", sum(self.results)/float(len(self.results)))
        if self.collect_cases:
            print("size of training data", len(self.neural_network_cases))
            dump_cases(self.neural_network_cases)

    def choose_legal_random_move(self):
        while True:
            r = randint(0,3)
            if self.game_board.is_move_legal(r):
                return r

    def choose_legal_move_from_nn(self, result):
        chosen_move = None

        while chosen_move == None or not self.game_board.is_move_legal(chosen_move):
            if chosen_move != None:
                result[0][chosen_move] = -1
            chosen_move = np.argmax(result[0])
        return chosen_move

    def gather_case_and_result_using_expectimax(self, current_node, flat_board):
        self.expectimax.run_expectimax(current_node, self.depth, -float("inf"), float("inf"), None)
        self.neural_network_cases[str(flat_board)] = self.expectimax.result

    def welch(self, list1, list2):
        params = {"results": str(list1) + " " + str(list2), "raw": "1"}
        resp = requests.post('http://folk.ntnu.no/valerijf/6/', data=params)
        return resp.text


    def test_percentage_training_and_test_set(self):
        output_activations = self.move_classifier.do_testing(boards=self.move_classifier.test_boards)
        print("Statistics (test set): \t\t", self.move_classifier.check_result(output_activations, labels=self.move_classifier.test_labels), "%")
        output_activations = self.move_classifier.do_testing(boards=self.move_classifier.boards)
        print("Statistics (training set):\t ", self.move_classifier.check_result(output_activations, labels=self.move_classifier.labels), "%")

    def print_comparison(self):
        print("NN results:\t", self.results_from_nn_playing)
        print("Random results:\t", self.results_from_random_playing)
        print("largest tiles", max(self.results_from_nn_playing),  max(self.results_from_random_playing))
        print("average tiles", sum(self.results_from_nn_playing)/float(len(self.results_from_nn_playing)), sum(self.results_from_random_playing)/float(len(self.results_from_random_playing)))
        points = self.welch(self.results_from_random_playing, self.results_from_nn_playing)
        print("points", points)

    def print_commands(self):
        print("Commands")
        print("t: Test the network classification using both the test set and the training set")
        print("L toggle case collection. Currently: ", self.collect_cases)
        print("s: Run infinite times using NN")
        print("p: Run 50 games using NN")
        print("r: Run 50 games using a random player")
        print("c: Compare the two runs of 50")