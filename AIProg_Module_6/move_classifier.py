
import file_handler
import json
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann


class MoveClassifier():

    def __init__(self, nr_of_training_cases, nr_of_test_cases, nr_of_hidden_layers, nr_of_nodes_in_layers, act_functions, lr, number_of_input_nodes=28 * 28, number_of_output_nodes=10, bulk_size=1):
        self.boards, self.labels = file_handler.get_cases(nr_of_training_cases)
        self.test_boards, self.test_labels = file_handler.get_cases(nr_of_test_cases, test=True)

        self.lrate = lr
        self.bulk_size = bulk_size
        self.build_ann(number_of_input_nodes, number_of_output_nodes, nr_of_hidden_layers, nr_of_nodes_in_layers, act_functions)

    def build_ann(self, number_of_input_nodes, no, nr_of_hidden_layers, nr_of_nodes_in_layers, act_functions):
        weights = []
        first_weights = theano.shared(np.random.uniform(low=-.1, high=.1, size=(number_of_input_nodes, nr_of_nodes_in_layers[0])))
        weights.append(first_weights)
        for i in range(1, nr_of_hidden_layers):
            weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(nr_of_nodes_in_layers[i-1], nr_of_nodes_in_layers[i]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(nr_of_nodes_in_layers[-1], no))))

        input = T.fmatrix()
        target = T.fmatrix()

        layers = []
        # First hidden layer
        self.add_layer_activation_function(act_functions[0], layers, input, weights[0])
        # Next layers
        for j in range(nr_of_hidden_layers):
            self.add_layer_activation_function(act_functions[j+1], layers, layers[j], weights[j+1])

        error = T.sum(pow((target - layers[-1]), 2)) # Sum of squared errors
        params = [w for w in weights]
        gradients = T.grad(error, params)
        backprops = self.backprop_acts(params, gradients)

        #self.get_x1 = theano.function(inputs=[input, target], outputs=error, allow_input_downcast=True)
        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
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
            layers.append(T.nnet.softmax(product))

    def backprop_acts (self, params, gradients):
        updates = []
        for p, g in zip(params, gradients):
            updates.append((p, p - self.lrate * g))
        return updates

    def do_training(self, epochs=1, errors=[]):
        starttime = time()
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            i = 0
            j = self.bulk_size
            while j < len(self.boards):
                board_bulk = self.boards[i:j]
                label_bulk = self.labels[i:j]
                i += self.bulk_size
                j += self.bulk_size
                # Provide some feedback while processing boards
                #if j % (self.bulk_size * 100) == 0:
                #    print("board nr: ", j)
                error += self.trainer(board_bulk, label_bulk)
            print("avg error pr board: " + str(error/j))
            errors.append(error)
        return errors

    def do_testing(self):
        hidden_activations = []
        i = 0
        j = self.bulk_size
        while j < len(self.test_boards):
            image_group = self.test_boards[i:j]
            i += self.bulk_size
            j += self.bulk_size
            predictions = self.predictor(image_group)
            # Transform back from bulk to single result
            for res in predictions:
                hidden_activations.append(res)
        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations


    def preprosessing(self, boards, labels):
        #Scales tiles to have values between 0.0 and 1.0 instead of 0 and 255
        for i in range(len(labels)):
            for j in range(len(labels[i])):
                if labels[i][j] == None:
                    labels[i][j] = 0
            boards[i] = json.loads(boards[i])
            sorted_board = sorted(boards[i], reverse=True)
            for j in range(len(boards[i])):
                if boards[i][j] == 0:
                    continue
                rank = sorted_board.index(boards[i][j])
                boards[i][j] = (15 - rank) / 15
                # boards[i][j] = boards[i][j]/float(1024)

            largest_index = labels[i].index(max(labels[i]))
            labels[i] = [0, 0, 0, 0]
            labels[i][largest_index] = 1

    def check_result(self, result):
        count = 0
        for i in range(len(result)):
            a = result[i]
            b = self.test_labels[i]
            if np.argmax(self.test_labels[i]) == np.argmax(result[i]):
                count += 1
        print("statistics:", (count/float(len(self.test_labels))) * 100)
        return float((count/float(len(self.test_labels))) * 100)