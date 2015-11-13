
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann
import file_handler
import json


class MoveClassifier():

    # nb = # bits, nh = # hidden nodes (in the single hidden layer)
    # lr = learning rate

    def __init__(self, nr_of_training_cases, nr_of_test_cases, nb=16, nh=10000, no=4, lr=0.001, bulk_size=1):
        self.boards, self.labels = file_handler.get_cases(nr_of_training_cases)
        self.test_boards, self.test_labels = file_handler.get_cases(nr_of_test_cases, test=True)
        #self.images, self.labels = gen_flat_cases()
        self.lrate = lr
        self.bulk_size = bulk_size
        self.build_ann(nb, nh, no)

    def floatX(self, X):
        return np.asarray(X, dtype=theano.config.floatX)

    def build_ann(self, nb, nh, no):
        w1 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nb, nh)))
        w2 = theano.shared(np.random.uniform(low=-.1, high=.1, size=(nh, no)))
        input = T.wmatrix()
        target = T.fmatrix()
        x1 = Tann.sigmoid(T.dot(input,w1))
        x2 = Tann.sigmoid(T.dot(x1,w2))
        error = T.sum(pow((target - x2), 2))
        params = [w1, w2]
        gradients = T.grad(error, params)
        backprops = self.backprop_acts(params, gradients)

        self.get_x1 = theano.function(inputs=[input, target], outputs=error, allow_input_downcast=True)
        self.trainer = theano.function(inputs=[input, target], outputs=error, updates=backprops, allow_input_downcast=True)
        self.predictor = theano.function(inputs=[input], outputs=x2, allow_input_downcast=True)

    def backprop_acts (self, params, gradients):
        updates = []
        for p, g in zip(params, gradients):
            updates.append((p, p - self.lrate * g))
        return updates

    def do_training(self, epochs=1, test_interval=None, errors=[]):
        starttime = time()
        #graph.start_interactive_mode()
        #if test_interval: self.avg_vector_distances = []
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            i = 0
            j = self.bulk_size
            while j < len(self.boards):
                image_group = self.boards[i:j]
                result_group = self.labels[i:j]
                i += self.bulk_size
                j += self.bulk_size
            #for j in range(len(self.images)):
                if j % (self.bulk_size * 1000) == 0:
                    print("image nr: ", j)
                #tar = [0] * 10
                #tar[self.labels[j]] = 1
                #tar = theano.shared(tar)
                #hhh = self.get_x1(image_group, result_group)
                #print("hh")
                error += self.trainer(image_group, result_group)
            print(error)
            print("avg error pr image: " + str(error/j))
            errors.append(error)
        print("Training time: " + str((round(time()-starttime, 1))) + " sec")
        return errors

    def do_testing(self, blind_test_images=None):
        if blind_test_images is not None:
            self.test_images = blind_test_images
            self.test_labels = None

        hidden_activations = []
        i = 0
        j = self.bulk_size
        while j < len(self.test_boards):
            board_group = self.test_boards[i:j]
            i += self.bulk_size
            j += self.bulk_size
            end = self.predictor(board_group)
            for res in end:
                hidden_activations.append(res)
        '''
        for c in self.test_images:
            end = self.predictor(c)
            hidden_activations.append(end)
        '''
        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations

    def blind_test(self, images):
        #Raw images is a list with sublist of raw_images
        self.preprosessing(images)
        raw_results = self.do_testing(blind_test_images=images)
        results = []
        for i in range(len(raw_results)):
            highest_value = int(np.where(raw_results[i] == max(raw_results[i]))[0][0])
            results.append(highest_value)
        #Returns a list with the classifications of the images
        return results

    def preprosessing(self, boards, labels):
        #Scales images to have values between 0.0 and 1.0 instead of 0 and 255
        for i in range(len(labels)):
            for j in range(len(labels[i])):
                if labels[i][j] == None:
                    labels[i][j] = 0
            boards[i] = json.loads(boards[i])
            for j in range(len(boards[i])):
                boards[i][j] = boards[i][j]/float(1024)
            largest_index = labels[i].index(max(labels[i]))
            labels[i] = [0, 0, 0, 0]
            labels[i][largest_index] = 1

    def check_result(self, result):
        count = 0
        for i in range(len(result)):
            #print image_recog.labels[i]
            #print result[i]
            b = np.argmax(self.test_labels[i]) == np.argmax(result[i])# == max(result[i]))[0][0])
            #print b
            # print (test_labels[i])
            # print(result[i])
            # print(np.argmax(result[i]))
            # print(b)
            # print ("---")
            if b:
                count += 1
        print("statistics:", (count/float(len(self.test_labels))) * 100)

'''
nr_of_training_cases = 600000
nr_of_test_cases = 10000
move_classifier = MoveClassifier(nr_of_training_cases, bulk_size=100)
move_classifier.preprosessing(boards=move_classifier.boards, labels=move_classifier.labels)
move_classifier.preprosessing(boards=move_classifier.test_boards, labels=move_classifier.test_labels)


errors = []

starttime = time()
while True:
    action = input("Press 1 to train, 2 to test, r to set learning rate: ")
    if int(action) == 1:
        errors = move_classifier.do_training(epochs=1, errors=errors)
    elif int(action) == 2:
        test_labels, result = move_classifier.do_testing()
    else:
        errors = move_classifier.do_training(epochs=int(action), errors=errors)
    print("Total time elapsed: " + str(round((time() - starttime)/60, 1)) + " min")
'''

