from collections import defaultdict
import file_handler
import json
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann
from math import log2



class MoveClassifier():

    def __init__(self, nr_of_training_cases, nr_of_test_cases, nr_of_nodes_in_layers, act_functions, lr, number_of_input_nodes, number_of_output_nodes, bulk_size=1):
        self.boards, self.labels = file_handler.get_cases(nr_of_training_cases)
        self.test_boards, self.test_labels = file_handler.get_cases(nr_of_test_cases, test=True)

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

            print("avg error pr board: " + str(error/len(self.boards)))
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

    def preprosessing(self, boards, labels):
        # Kan bruke potens verdien til alle of bare dele pa det overste
        for i in range(len(boards)):
            boards[i] = list(map(int, boards[i].replace("[", "").replace("]", "").split(", ")))
            largest = float(log2(max(boards[i])))
            for j in range(len(boards[i])):
                if boards[i][j] != 0:
                    boards[i][j] =  log2(boards[i][j]) / largest

            # Create label array
            largest_index = labels[i].index(max(labels[i]))
            labels[i] = [0, 0, 0, 0]
            labels[i][largest_index] = 1
        #self.preprosessing_merging(boards, labels)

    def preprosessing_merging(self, boards, labels):
        for i in range(len(boards)):
            boards[i] = list(map(int, boards[i].replace("[", "").replace("]", "").split(", ")))
            square_board = [boards[i][0:4], boards[i][4:8], boards[i][8:12], boards[i][12:16]]
            for y in range(4):
                for x in range(4):
                    current = square_board[y][x]
                    possible_merges = 0
                    neighbors = 0
                    w = 0
                    n = 0
                    e = 0
                    s = 0
                    # West
                    if x > 0:
                        w = square_board[y][x - 1]
                        neighbors += 1
                        if w != 0 and current == w:
                            possible_merges += 1
                    # North
                    if (y > 0):
                        n = square_board[y - 1][x]
                        neighbors += 1
                        if n != 0 and current == n:
                            possible_merges += 1
                    # East
                    if x < 3:
                        e = square_board[y][x + 1]
                        neighbors += 1
                        if e != 0 and current == e:
                            possible_merges += 1
                    # South
                    if (y < 3):
                        s = square_board[y + 1][x]
                        neighbors += 1
                        if s != 0 and current == s:
                            possible_merges += 1
                    #current_new_value = (1 - (current - w)**2) + (1 - (current - n)**2) + (1 - (current - e)**2) + (1 - (current - s)**2)
                    current_new_value = possible_merges/neighbors
                    boards[i][y*4 + x] = current_new_value

            # Create label array
            largest_index = labels[i].index(max(labels[i]))
            labels[i] = [0, 0, 0, 0]
            labels[i][largest_index] = 1


    def test_preprosessing(self, boards, labels):
        board_count_dict = defaultdict(int)
        labels_count_dict = defaultdict(int)
        for i in range(len(boards)):
            board_count_dict[str(boards[i])] += 1
            labels_count_dict[str(labels[i])] += 1
        print("number of boards", len(boards))
        print("number of boards in dict", len(board_count_dict.keys()))
        print("times left", labels_count_dict[str([1, 0, 0, 0])])
        print("times right", labels_count_dict[str([0, 1, 0, 0])])
        print("times up", labels_count_dict[str([0, 0, 1, 0])])
        print("times down", labels_count_dict[str([0, 0, 0, 1])])

    def neigbour_merge(self, board, k):
        neigbour_count = 0
        neigbours_that_can_merge = 0
        tile = board[k]
        if not (k+1)%4 == 0:
            # tile right
            neigbour_count += 1
            if tile==board[k+1]:
                neigbours_that_can_merge+=1
        if not k%4 == 0:
            # tile left
            neigbour_count += 1
            if tile==board[k-1]:
                neigbours_that_can_merge+=1
        if k>4:
            # tile above
            neigbour_count += 1
            if tile==board[k-4]:
                neigbours_that_can_merge+=1
        if k<12:
            # tile above
            neigbour_count += 1
            if tile==board[k+4]:
                neigbours_that_can_merge+=1
        # print(board)
        # print(k)
        # print(neigbour_count)
        # print(neigbours_that_can_merge)
        return neigbour_count, neigbours_that_can_merge

    def check_result(self, output_activations, labels):
        count = 0
        for i in range(len(output_activations)):
            if np.argmax(labels[i]) == np.argmax(output_activations[i]):
                count += 1
        return float((count/float(len(labels))) * 100)

