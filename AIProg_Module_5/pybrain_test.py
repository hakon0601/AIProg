from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain import TanhLayer
import theano

net = buildNetwork(2, 3, 1, bias=True, hiddenclass=TanhLayer)

#res = net.activate([2, 1])
#print res

ds = SupervisedDataSet(2, 1)

ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (0,))

#for inp, target in ds:
#    print inp, target

#print ds['input']
trainer = BackpropTrainer(net, ds)

print net.activate([0, 1])

for i in range(2000):
    print trainer.train()

print net.activate([0, 0])
print net.activate([0, 1])
print net.activate([1, 0])
print net.activate([1, 1])


#print trainer.trainUntilConvergence()

