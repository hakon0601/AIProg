from mnist_basics import *

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain import TanhLayer

nr_of_cases = 10

images, labels = gen_flat_cases()

net = buildNetwork(784, 60, 10, bias=True, hiddenclass=TanhLayer)

ds = SupervisedDataSet(784, 10)

for i in range(10): #len(images)):
    expected_res = [0 for i in range(10)]
    expected_res[labels[i]] = 1
    ds.addSample(images[i], expected_res)

trainer = BackpropTrainer(net, ds)

print "result 0", [(net.activate(images[i]), labels[i]) for i in range(10)]

for i in range(200):
    print i
    print trainer.train()

print "result 1", [(net.activate(images[i]), labels[i]) for i in range(10)]
