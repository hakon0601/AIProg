
from mnist_basics import *
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann


class DigitRecognizer():

    def __init__(self, nr_of_training_images, nr_of_hidden_layers, nr_of_nodes_in_layers, act_functions, lr, number_of_input_nodes=28 * 28, no=10, bulk_size=1):
        self.images, self.labels = gen_flat_cases()
        self.test_images, self.test_labels = gen_flat_cases(type="testing")

        self.lrate = lr
        self.bulk_size = bulk_size
        self.build_ann(number_of_input_nodes, no, nr_of_hidden_layers, nr_of_nodes_in_layers, act_functions)

    def build_ann(self, number_of_input_nodes, no, nr_of_hidden_layers, nr_of_nodes_in_layers, act_functions):
        weights = []
        a = theano.shared(np.random.uniform(low=-.1, high=.1, size=(number_of_input_nodes, nr_of_nodes_in_layers[0])))
        weights.append(a)
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
            while j <= len(self.images):
                image_bulk = self.images[i:j]
                # Creating a result bulk with only zeros
                result_bulk = [[0 for i in range(10)] for i in range(self.bulk_size)]
                for k in range(self.bulk_size):
                    label_index = self.labels[i + k]
                    result_bulk[k][label_index] = 1
                i += self.bulk_size
                j += self.bulk_size
                # Provide some feedback while processing images
                if j % (self.bulk_size * 100) == 0:
                    print("image nr: ", j)
                error += self.trainer(image_bulk, result_bulk)
            print("avg error pr image: " + str(error/j))
            errors.append(error)
        return errors

    def do_testing(self, images):
        output_activations = []
        i = 0
        j = self.bulk_size
        while j <= len(images):
            image_group = images[i:j]
            i += self.bulk_size
            j += self.bulk_size
            predictions = self.predictor(image_group)
            # Transform back from bulk to single result
            for activation_vector in predictions:
                output_activations.append(activation_vector)
        return output_activations

    def blind_test(self, images):
        output_activations = self.predictor(images)
        results = []
        for i in range(len(output_activations)):
            answer = np.argmax(output_activations[i])
            results.append(answer)
        return results

    def preprocessing(self, feature_sets):
        #Scales images to have values between 0.0 and 1.0 instead of 0 and 255
        for image in range(len(feature_sets)):
            for value in range(len(feature_sets[image])):
                feature_sets[image][value] = feature_sets[image][value]/float(255)

    # Checking the results against the labels and return a percentage
    def check_result(self, output_activations, labels):
        count = 0
        for i in range(len(output_activations)):
            if int(labels[i]) == np.argmax(output_activations[i]):
                count += 1
        return float((count/float(len(labels))) * 100)




nr_of_training_images = 60000
nr_of_testing_images = 10000

number_of_hidden_layers = int(input("Number of hidden layers: "))
nodes_in_each_layer = list(map(int, input("Hidden nodes in each layer: ").replace(" ", "").split(",")))
print("TanH: 1, Sigmoid: 2, Rectify: 3, Softmax: 4")
activation_functions = list(map(int, input("Select activation functions: ").replace(" ", "").split(",")))
learning_rate = float(input("learning rate: "))
bulk_size = int(input("Bulk size: "))

digit_recog = DigitRecognizer(nr_of_training_images, number_of_hidden_layers, nodes_in_each_layer, activation_functions, learning_rate, bulk_size=bulk_size)
digit_recog.preprocessing(digit_recog.images)
digit_recog.preprocessing(digit_recog.test_images)

# TODO
blind_test_images = None
#digit_recog.preprocessing(blind_test_images)

errors = []

start_time = time()
while True:
    action = input("Enter a integer x to train x epocs, t to test: ")
    if action[0] == "t":
        if len(action) == 1:
            output_activations = digit_recog.do_testing(images=digit_recog.test_images)
            print("Statistics: ", digit_recog.check_result(output_activations, labels=digit_recog.test_labels), "%")
        # Used to test on the large training set of images
        elif action[1] == "l":
            output_activations = digit_recog.do_testing(images=digit_recog.images)
            print("Statistics: ", digit_recog.check_result(output_activations, labels=digit_recog.labels), "%")
        elif action[1] == "a":
            # TODO test the auxiliary data (blind test)
            minor_demo(digit_recog)
            #output_activations = digit_recog.do_testing(images=blind_test_images)
            #print("Result from blind test", digit_recog.blind_test(output_activations))
            pass
    else:
        errors = digit_recog.do_training(epochs=int(action), errors=errors)
        output_activations = digit_recog.do_testing(images=digit_recog.test_images)
        print("Statistics: ", digit_recog.check_result(output_activations, labels=digit_recog.test_labels), "%")
    print("Total time elapsed: " + str((time() - start_time)/60) + " min")
