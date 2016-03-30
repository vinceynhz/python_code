import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from funcs import *

# There can't be a simple artifical intelligence capable of learning its way up
# That particular situation requires a conciousness and self-awareness to
# realize new acquired knowledge

# There are multiple ways to represent the desired output.
# For matters of practicity and educational purposes, let's consider all these
# functions using a x input between 0 and 1

class network():
    def __init__(self, *pargs, learning_rate=0.5, weight_range=0.5, margin_function=1):
        self.layer = []
        self.bias = 1
        self.inputsize = 0
        self.learning_rate = learning_rate
        self.weight_range = weight_range
        self.margin = {
            1 : margin1,
            2 : margin2
        }[margin_function]

        if len(pargs) > 0:
            self.inputsize = pargs[0]
            self.layers = []

            for l in pargs[1:]:
                self.layers.append( layer() )
                for n in range(l):
                    self.layers[-1].add_neuron( self.weight_range )

    def eval(self, *vector, target=None, training=False):
        output = list(vector)

        for layer in self.layers:
            output = layer.eval( output + [self.bias] )
            output = [ self.margin(x) for x in output ]

        # output = [ self.margin(x) for x in output ]

        if target is not None and target != output:
            cost = cost_prime(output, target)
            self.adjust(cost)

        # Here I am adding the margin after the cost calculation for backprop
        return output

    def adjust(self, cost):
        layers = self.layers[:]
        layers.reverse()

        for ind, layer in enumerate(layers):
            cost = layer.adjust( cost, self.learning_rate )

    def train(self, tset, verbose=False, limit=None):
        iteration = 0
        result = -1

        while result != 0:
            iteration += 1
            result = 0

            printif( verbose, '\nIteration: {x}'.format(x=iteration) )
            printif( verbose, '=' * 60)

            for vector, target in tset:

                target = list(target)
                r = self.eval(*vector, target=target)

                printif( verbose, '\nInput: {x}'.format(x=vector) )
                printif( verbose, 'Output:', r, '\nTarget:', target )

                if r != target:
                    result += 1
            if limit is not None and iteration == limit:
                break

        return iteration, result == 0

class layer():
    def __init__( self ):
        self.neurons = []
        self.inputs = []
        self.outputs = []

    def add_neuron(self, weight_range):
        self.neurons.append( neuron(weight_range) )

    def eval(self, vector):
        self.outputs = []

        self.inputs = vector[:]

        for n in self.neurons:
            self.outputs.append( n.eval( vector ) )

        return self.outputs

    def adjust(self, cost, learning_rate):
        costs = [0] * len( self.inputs )
        for ind, n in enumerate(self.neurons):
            result = n.adjust(self.inputs, cost[ind], learning_rate)
            costs = addition( costs, result )

        return costs

class neuron():
    def __init__(self, weight_range):
        self.weights = []
        # self.slopes = []
        # self.old_weights = []
        self.delta = 0
        self.weight_range = weight_range

    def eval(self, vector):
        if len(self.weights) == 0:
            self.weights = [ random_weight( self.weight_range ) for i in range( len(vector) ) ]
            # self.slopes = [ None for i in range( len(vector) ) ]
            # self.old_weights = [ None for i in range( len(vector) )]

        return sigmoid( self.dot(vector) )

    def prime(self, vector):
        return sigmoid_prime( self.dot(vector) )

    def dot(self, vector):
        return dot_product(self.weights, vector)

    def adjust(self, vector, cost, learning_rate):
        z = self.prime( vector )
        self.delta = cost * z

        costs = [0] * len(vector)

        for ind, element in enumerate(vector):
            costs[ind] = self.delta * self.weights[ind]

            adjust = -learning_rate * self.delta * element
            self.weights[ind] = round(self.weights[ind] + adjust, 3) # <<< rounding to 3

        return costs
