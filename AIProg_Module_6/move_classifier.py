from collections import defaultdict
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann
from math import log2

from file_handler import *


class MoveClassifier():

    def __init__(self, nr_of_training_cases, nr_of_test_cases, nr_of_nodes_in_layers, act_functions, lr, number_of_input_nodes, number_of_output_nodes, bulk_size=1):
        self.boards, self.labels = process_cases_for_nn(nr_of_training_cases)
        self.test_boards, self.test_labels = process_cases_for_nn(nr_of_test_cases, test=True)

        self.lrate = lr
        self.bulk_size = bulk_size
        self.build_ann(number_of_input_nodes, number_of_output_nodes, nr_of_nodes_in_layers, act_functions)

    def build_ann(self, number_of_input_nodes, nr_of_output_nodes, nr_of_nodes_in_layers, act_functions):
        weights = []
        first_weights = theano.shared(np.random.uniform(low=-.1, high=.1, size=(number_of_input_nodes, nr_of_nodes_in_layers[0])))
        weights.append(first_weights)
        for i in range(1, len(nr_of_nodes_in_layers)):
            weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(nr_of_nodes_in_layers[i-1], nr_of_nodes_in_layers[i]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(nr_of_nodes_in_layers[-1], nr_of_output_nodes))))

        input = T.fmatrix()
        target = T.fmatrix()

        layers = []
        # First hidden layer
        self.add_layer_activation_function(act_functions[0], layers, input, weights[0])
        # Next layers
        for j in range(len(nr_of_nodes_in_layers)):
            self.add_layer_activation_function(act_functions[j+1], layers, layers[j], weights[j+1])

        error = T.sum(pow((target - layers[-1]), 2)) # Sum of squared errors
        params = [w for w in weights]
        gradients = T.grad(error, params)
        backprops = self.backprop_acts(params, gradients)

        #self.get_x1 = theano.function(inputs=[input, target], outputs=error, allow_input_downcast=True)
        self.trainer = theano.function(inputs=[input, target], outputs=[error, layers[-1]], updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=layers[-1], allow_input_downcast=True)

    def add_layer_activation_function(self, act_func, layers, layer, weight):
        product = T.dot(layer, weight)
        if act_func == 1:
            # TanH
            layers.append(T.tanh(product))
        elif act_func == 2:
            # Sigmoid
            layers.append(Tann.sigmoid(product))
        elif act_func == 3:
            # Rectify
            layers.append(T.maximum(0, product))
        elif act_func == 4:
            # Softmax
            layers.append(T.nnet.softmax(product))

    def backprop_acts (self, params, gradients):
        updates = []
        for p, g in zip(params, gradients):
            updates.append((p, p - self.lrate * g))
        return updates

    def do_training(self, epochs=1, errors=[]):
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            i = 0
            j = self.bulk_size
            while j <= len(self.boards):
                board_bulk = self.boards[i:j]
                label_bulk = self.labels[i:j]
                i += self.bulk_size
                j += self.bulk_size
                # Provide some feedback while processing boards
                #if j % (self.bulk_size * 100) == 0:
                #    print("board nr: ", j)
                err, act_out = self.trainer(board_bulk, label_bulk)
                error += err

            print("avg error pr board: " + str(error/(len(self.boards))))
            errors.append(error)
        return errors

    def do_testing(self, boards):
        output_activations = []
        i = 0
        j = self.bulk_size
        while j <= len(boards):
            # TODO just do this in a simple for loop not bulks
            board_group = boards[i:j]
            i += self.bulk_size
            j += self.bulk_size
            predictions = self.predictor(board_group)
            # Transform back from bulk to single result
            for activation_vector in predictions:
                output_activations.append(activation_vector)
        return output_activations

    def preprocessing(self, boards, labels=None):
        # Uses the logarithmical value and divides by the larges tile to map to a value in the range [0, 1]
        for i in range(len(boards)):
            largest = float(log2(max(boards[i])))
            for j in range(len(boards[i])):
                if boards[i][j] != 0:
                    boards[i][j] = log2(boards[i][j]) / largest

            if labels:
                # Create label array
                largest_index = labels[i].index(max(labels[i]))
                labels[i] = [0, 0, 0, 0]
                labels[i][largest_index] = 1

    def preprocessing_row_column(self, boards):
        # Adds 8 extra nodes, one for each row/column.
        # Each node represents the the number of tiles you can merge on a row/column and their logaritmical normalized value
        processed_board = []
        for b in range(len(boards)):
            extra_nodes = []
            for i in range(4):
                extra_nodes.append(self.row_column_score(boards[b][4*i:4*(i+1)]) / 2.0)
            for j in range(4):
                extra_nodes.append(self.row_column_score(boards[b][j::4]) / 2.0)
            processed_board.append(boards[b] + extra_nodes)
        return processed_board

    def row_column_score(self, vector):
        score = 0.0
        for i in range(len(vector)-1):
            if vector[i] == 0:
                break
            for j in range(i+1, len(vector)):
                if vector[i] == vector[j]:
                    score += vector[i]
                    break
                elif not vector[j] == 0:
                    break
        return score

    def test_preprocessing(self, boards, labels):
        board_count_dict = defaultdict(int)
        labels_count_dict = defaultdict(int)
        for i in range(len(boards)):
            board_count_dict[str(boards[i])] += 1
            labels_count_dict[str(labels[i])] += 1
        print("number of boards", len(boards))
        print("number of boards in dict", len(board_count_dict.keys()))
        print("times left", labels_count_dict[str([1, 0, 0, 0])], "\t", labels_count_dict[str([1, 0, 0, 0])] / float(len(boards)), "%")
        print("times right", labels_count_dict[str([0, 1, 0, 0])], "\t", labels_count_dict[str([0, 1, 0, 0])] / float(len(boards)), "%")
        print("times up", labels_count_dict[str([0, 0, 1, 0])], "\t", labels_count_dict[str([0, 0, 1, 0])] / float(len(boards)), "%")
        print("times down", labels_count_dict[str([0, 0, 0, 1])], "\t", labels_count_dict[str([0, 0, 0, 1])] / float(len(boards)), "%")

    def check_result(self, output_activations, labels):
        count = 0
        for i in range(len(output_activations)):
            if np.argmax(labels[i]) == np.argmax(output_activations[i]):
                count += 1
        return float((count/float(len(labels))) * 100)

