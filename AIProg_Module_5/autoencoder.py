
from mnist_basics import *

import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann

# Theano pretty-print
def ppth(obj, fancy=True, graph=False, fid='/Users/hakon0601/Dropbox/Python/AIProg/AIProg_Module_5/',fmt='pdf'):
    if graph: theano.printing.pydotprint(obj,outfile=fid,format=fmt)
    elif fancy: theano.printing.debugprint(obj)
    else: return theano.pp(obj)


def gen_all_bit_cases(num_bits):
    def bits(n):
        s = bin(n)[2:]
        return [int(b) for b in '0'*(num_bits - len(s))+s]
    return [bits(i) for i in range(2**num_bits)]


class AutoEncoder():

    # nb = # bits, nh = # hidden nodes (in the single hidden layer)
    # lr = learning rate

    def __init__(self, nb=3, nh=2, lr=.1):
        self.cases = gen_all_bit_cases(nb)
        self.lrate = lr
        self.build_ann(nb,nh,lr)

    def build_ann(self,nb,nh,lr):
        w1 = theano.shared(np.random.uniform(-.1,.1,size=(nb,nh)))
        w2 = theano.shared(np.random.uniform(-.1,.1,size=(nh,nb)))
        input = T.dvector('input')
        b1 = theano.shared(np.random.uniform(-.1,.1,size=nh))
        b2 = theano.shared(np.random.uniform(-.1,.1,size=nb))
        x1 = Tann.sigmoid(T.dot(input,w1) + b1)
        x2 = Tann.sigmoid(T.dot(x1,w2) + b2)
        error = T.sum((input - x2)**2)
        params = [w1,b1,w2,b2]
        gradients = T.grad(error,params)
        backprop_acts = [(p, p - self.lrate*g) for p,g in zip(params,gradients)]
        self.predictor = theano.function([input],[x2,x1])
        self.trainer = theano.function([input],error, updates=backprop_acts)

    def do_training(self, epochs=1000, test_interval=None):
        #graph.start_interactive_mode()
        errors = []
        if test_interval: self.avg_vector_distances = []
        for i in range(epochs):
            error = 0
            for c in self.cases:
                error += self.trainer(c)
            print error
            errors.append(error)
        #    if test_interval: self.consider_interim_test(i,test_interval)
        #graph.simple_plot(errors,xtitle="Epoch",ytitle="Error",title="")
        #if test_interval:
        #    graph.newfig()
        #    graph.simple_plot(self.avg_vector_distances,xtitle='Epoch',
        #                     ytitle='Avg Hidden-Node Vector Distance',title='')

    def do_testing(self,scatter=True):
        hidden_activations = []
        for c in self.cases:
            end,hact = self.predictor(c)
            hidden_activations.append(end)
        #if scatter: graph.simple_scatter(hidden_activations,radius=8)
        return hidden_activations

autoencoder = AutoEncoder()
autoencoder.do_training()
result = autoencoder.do_testing()

for i in range(8):
    print autoencoder.cases[i]
    print result[i]
