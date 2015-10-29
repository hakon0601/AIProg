
from mnist_basics import *

import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann
import mnist_basics


class ImageRecog():

    # nb = # bits, nh = # hidden nodes (in the single hidden layer)
    # lr = learning rate

    def __init__(self, nb=28*28, nh=400, lr=.4):
        self.images, self.labels = mnist_basics.gen_x_flat_cases(800)
#        self.cases = mnist_basics.gen_x_flat_cases(10)
        self.lrate = lr
        self.build_ann(nb,nh,lr)

    def build_ann(self,nb,nh,lr):
        w1 = theano.shared(np.random.uniform(-.1,.1,size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(-.1,.1,size=(nh,10)))
        input = T.dvector('input')
        target = T.dvector('target')
        b1 = theano.shared(np.random.uniform(-.1,.1,size=nh))
        b2 = theano.shared(np.random.uniform(-.1,.1,size=10))
        x1 = Tann.sigmoid(T.dot(input,w1) + b1)
        x2 = Tann.sigmoid(T.dot(x1,w2) + b2)
        error = T.sum((target - x2)**2)
        params = [w1,b1,w2,b2]
        gradients = T.grad(error,params)
        backprop_acts = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]
        self.predictor = theano.function([input],[x2,x1])
        self.trainer = theano.function([input, target],error, updates=backprop_acts)

    def do_training(self, epochs=3, test_interval=None):
        #graph.start_interactive_mode()
        errors = []
        if test_interval: self.avg_vector_distances = []
        for i in range(epochs):
            print "epoch: ", i
            error = 0
            for j in range(len(self.images)):
                print "image nr: ", j
                tar = np.zeros(10)
                tar[self.labels[j]] = 1
                #tar = theano.shared(tar)
                error += self.trainer(self.images[j], tar)
            print error
            errors.append(error)
        #    if test_interval: self.consider_interim_test(i,test_interval)
        #graph.simple_plot(errors,xtitle="Epoch",ytitle="Error",title="")
        #if test_interval:
        #    graph.newfig()
        #    graph.simple_plot(self.avg_vector_distances,xtitle='Epoch',
        #                     ytitle='Avg Hidden-Node Vector Distance',title='')

    def do_testing(self,scatter=True):
        self.test_images, self.test_labels = mnist_basics.gen_x_flat_cases(8000, type="testing")
        hidden_activations = []
        for c in self.test_images:
            end,hact = self.predictor(c)
            hidden_activations.append(end)
        #if scatter: graph.simple_scatter(hidden_activations,radius=8)
        return hidden_activations

image_recog = ImageRecog()
image_recog.do_training()
result = image_recog.do_testing()

count = 0
for i in range(len(image_recog.images)):
    #print image_recog.labels[i]
    #print result[i]
    b = int(image_recog.labels[i]) == int(np.where(result[i] == max(result[i]))[0][0])
    #print b
    if b:
        count += 1
print "statistics:", (count/float(8)) * 100
