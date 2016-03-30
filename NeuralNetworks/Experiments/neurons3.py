import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

import numpy as np

from funcs import *

# def sigmoid(x):
#     return 1 / ( 1 + np.exp(-x) )
#
# def sigmoid_prime(x):
#     return sigmoid(x) * ( 1 - sigmoid(x) )

def cost_prime(output, target):
    return output - target

sigmoid = np.vectorize(sigmoid)
sigmoid_prime = np.vectorize(sigmoid_prime)

margin1 = np.vectorize(margin1)
margin2 = np.vectorize(margin2)

npround = np.vectorize(round)

class network():
    def __init__(self, *pargs, learning_rate=0.5, weight_range=0.5, margin_function=1):
        self.layers = []
        self.bias = 1
        self.input_size = 0
        self.learning_rate = learning_rate
        self.weight_range = weight_range
        self.margin = {
            1 : margin1,
            2 : margin2
        }[margin_function]

        if len(pargs) > 0:
            self.input_size = pargs[0]

            for l in range( 1, len(pargs[1:])+1 ):
                layer = [ [ random_weight(self.weight_range) for i in range( pargs[l-1] + 1 ) ] for j in range(pargs[l]) ]
                layer = np.array(layer)
                self.layers.append(layer)

    def eval(self, *pargs, training=False):
        if type(pargs[0]) is np.ndarray:
            vector = pargs[0]
        else:
            vector = np.array( [list(pargs)] ).transpose()

        if training:
            inputs = []
        for layer in self.layers:
            vector = np.insert(vector, vector.shape[0], self.bias, 0)
            if training:
                inputs.append(vector)
            vector = layer.dot(vector)
            vector = sigmoid(vector)

        vector = self.margin(vector)

        if training:
            return vector, inputs
        else:
            return vector

    def backprop(self, inputs, cost, batch_size):
        for ind in range(1, len(self.layers) + 1):
            layer = self.layers[-ind]
            vector = inputs[-ind]
            v = layer.dot(vector)
            z = sigmoid_prime(v)
            delta = z * cost
            cost = layer.transpose().dot( delta )
            # to propagate the error, we do not need the bias term
            cost = np.delete(cost, len(cost.shape), 0)
            nabla = []
            for row in delta:
                n = row * vector
                n = np.sum(n, len(n.shape)-1)
                nabla.append(n)
            nabla = np.array(nabla)
            adjust = -( self.learning_rate / batch_size ) * nabla
            self.layers[-ind] = npround( self.layers[-ind] + adjust, 3 )

    def train(self, tset, verbose=False, limit=None):
        test = [ record[0] for record in tset ]
        test = np.array(test).transpose()

        batch_size = len(test)

        target = [ record[1] for record in tset ]
        target = np.array(target).transpose()

        done = False
        iteration = 0
        while not done:
            iteration += 1
            vector = test
            inputs = []

            ### Feed Forward
            output, inputs = self.eval(vector, training=True)
            printif( verbose, '\nInput: {x}'.format(x=vector) )
            printif( verbose, 'Output:', output, '\nTarget:', target )

            done = np.all(output == target)
            if done:
                break

            # Cost at last layer
            cost = cost_prime(output, target)

            # Backpropagation & adjust
            self.backprop(inputs, cost, batch_size)

            if limit is not None and iteration == limit:
                break

        return iteration, done
tset = [
    ([1,1], [1]),
    ([1,0], [0]),
    ([0,0], [0])
]
