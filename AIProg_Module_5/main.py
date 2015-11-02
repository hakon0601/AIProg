
from mnist_basics import *

import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann


class ImageRecog():

    # nb = # bits, nh = # hidden nodes (in the single hidden layer)
    # lr = learning rate

    def __init__(self, nr_of_training_images, nb=28*28, nh=700, lr=0.001):
        self.images, self.labels = gen_x_flat_cases(nr_of_training_images)
        #self.images, self.labels = gen_flat_cases()
        self.lrate = lr
        self.build_ann(nb,nh)

    def build_ann(self,nb,nh):
        w1 = theano.shared(np.random.uniform(-.1,.1,size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(-.1,.1,size=(nh,10)))
        input = T.wvector('input')
        target = T.wvector('target')
        b1 = theano.shared(np.random.uniform(-.1,.1,size=nh))
        b2 = theano.shared(np.random.uniform(-.1,.1,size=10))
        x1 = Tann.sigmoid(T.dot(input,w1) + b1)
        x2 = Tann.sigmoid(T.dot(x1,w2) + b2)
        error = T.sum((target - x2)**2)
        params = [w1, b1, w2, b2]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate * g) for p, g in zip(params, gradients)]
        self.predictor = theano.function([input],[x2])
        self.trainer = theano.function([input, target], error, updates=backprop_acts)

    def do_training(self, epochs=1, test_interval=None):
        #graph.start_interactive_mode()
        errors = []
        #if test_interval: self.avg_vector_distances = []
        for i in range(epochs):
            print("epoch: ", i)
            error = 0
            for j in range(len(self.images)):
                if j % 1000 == 0:
                    print("image nr: ", j)
                tar = [0] * 10
                tar[self.labels[j]] = 1
                #tar = theano.shared(tar)

                error += self.trainer(self.images[j], tar)
            print(error)
            print(error/len(self.images))
            errors.append(error)
        #    if test_interval: self.consider_interim_test(i,test_interval)
        #graph.simple_plot(errors,xtitle="Epoch",ytitle="Error",title="")
        #if test_interval:
        #    graph.newfig()
        #    graph.simple_plot(self.avg_vector_distances,xtitle='Epoch',
        #                     ytitle='Avg Hidden-Node Vector Distance',title='')

    def do_testing(self,scatter=True, blind_test_images=None):
        if not blind_test_images:
            self.test_images, self.test_labels = mnist_basics.gen_x_flat_cases(100, type="testing")
            self.preprosessing(self.test_images)
        else:
            self.test_images = blind_test_images
            self.test_labels = None
        hidden_activations = []
        for c in self.test_images:
            end = self.predictor(c)
            hidden_activations.append(end)
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

    def preprosessing(self, feature_sets):
        #Scales images to have values between 0.0 and 1.0 instead of 0 and 255
        for image in range(len(feature_sets)):
            for value in range(len(feature_sets[image])):
                feature_sets[image][value] = feature_sets[image][value]/float(255)


nr_of_training_images = 60000
nr_of_testing_images = 10000
image_recog = ImageRecog(nr_of_training_images)
image_recog.preprosessing(image_recog.images)
image_recog.do_training(epochs=3)
test_labels, result = image_recog.do_testing(nr_of_testing_images)

count = 0
for i in range(len(test_labels)):
    #print image_recog.labels[i]
    #print result[i]
    b = int(test_labels[i]) == np.argmax(result[i])# == max(result[i]))[0][0])
    #print b
    print (test_labels[i])
    print(result[i])
    print(np.argmax(result[i]))
    print(b)
    print ("---")
    if b:
        count += 1
print("statistics:", (count/float(len(test_labels))) * 100)
