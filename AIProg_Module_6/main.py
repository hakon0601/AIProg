
from AIProg_Module_5.mnist_basics import *
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann


class Game2048Neural():

    # nb = # bits, nh = # hidden nodes (in the single hidden layer)
    # lr = learning rate

    def __init__(self, nb=28*28, nh=700, lr=0.001):
        #self.images, self.labels = gen_x_flat_cases(600)
        self.cases = self.read_training_data()
        print(self.cases)
        self.lrate = lr
        self.build_ann(nb,nh)

    def build_ann(self,nb,nh):
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh,10)))
        input = T.dvector('input')
        target = T.wvector('target')
        b1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=nh))
        b2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=10))
        x1 = T.maximum((T.dot(input,w1) + b1), 0.)
        x2 = T.maximum((T.dot(x1,w2) + b2), 0.)
        error = T.sum(pow((target - x2), 2))
        params = [w1, b1, w2, b2]
        gradients = T.grad(error, params)
        backprops = self.backprop_acts(params, gradients)

        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=[x2], allow_input_downcast=True)

    def backprop_acts (self, params, gradients):
        updates = []
        for p, g in zip(params, gradients):
            updates.append((p, p - self.lrate * g))
        return updates

    def do_training(self, epochs=1, test_interval=None, errors=[]):
        #graph.start_interactive_mode()
        #if test_interval: self.avg_vector_distances = []
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            for j in range(len(self.images)):
                if j % 10000 == 0:
                    print("image nr: ", j)
                tar = [0] * 10
                tar[self.labels[j]] = 1
                #tar = theano.shared(tar)

                error += self.trainer(self.images[j], tar)
            print(error)
            print("avg error pr image: " + str(error/len(self.images)))
            errors.append(error)
        return errors

    def do_testing(self,scatter=True, blind_test_images=None):
        if not blind_test_images:
            self.test_images, self.test_labels = gen_x_flat_cases(100, type="testing")
            self.preprosessing(self.test_images)
        else:
            self.test_images = blind_test_images
            self.test_labels = None
        hidden_activations = []
        for c in self.test_images:
            end = self.predictor(c)
            hidden_activations.append(end)
        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations

    def blind_test(self, images):
        raw_results = self.do_testing(blind_test_images=images)
        results = []
        for i in range(len(raw_results)):
            highest_value = int(np.where(raw_results[i] == max(raw_results[i]))[0][0])
            results.append(highest_value)
        #Returns a list with the classifications of the images
        return results

    def check_result(self, result):
        count = 0
        for i in range(len(self.test_labels)):
            b = int(self.test_labels[i]) == np.argmax(result[i])# == max(result[i]))[0][0])
            if b:
                count += 1
        print("statistics:", (count/float(len(self.test_labels))) * 100)

    def read_training_data(self):
        training_data = []
        file = open("2048trainingdata.txt", "r")
        #training_data = file.read().splitlines()
        for line in file.readlines():
            training_data.append(line)

        file.close()
        return training_data

game2048Neural = Game2048Neural()

errors = []

# while True:
#     starttime = time()
#     action = input("Press 1 to train, 2 to test, r to set learning rate: ")
#     if action == "r":
#         image_recog.lrate = float(input("Enter a new learning rate: "))
#     elif int(action) == 1:
#         errors = image_recog.do_training(epochs=1, errors=errors)
#     elif int(action) == 2:
#         test_labels, result = image_recog.do_testing(nr_of_testing_images)
#     else:
#         errors = image_recog.do_training(epochs=int(action), errors=errors)


