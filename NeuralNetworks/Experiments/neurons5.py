import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from funcs import *

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
                self.layers.append(
                    layer( size = pargs[l],
                           input_size = pargs[l-1] + 1,
                           weight_range = self.weight_range
                    )
                )

    def eval(self, *pargs):
        vector = list(pargs)

        for i,l in enumerate(self.layers):
            output = l.eval( vector + [self.bias] )
            # vector = output
            vector = [ self.margin(x) for x in output ]

        output = [ self.margin(x) for x in output ]
        return output

    def train(self, tset, verbose=False, limit=None):
        iteration = 0
        result = -1
        while result != 0:
        # for i in range(limit):
            iteration += 1
            printif( verbose, '\nIteration: {x}'.format(x=iteration) )
            printif( verbose, '=' * 60 )
            result = 0
            # This for is an epoch
            for x, y in tset:
                # printif( verbose, '-' * 60 )

                ### Feed Forward
                output = self.eval(*x)
                printif( verbose, '\nInput: {x}'.format(x=x) )
                printif( verbose, 'Output:', output, '\nTarget:', y )
                # printif( verbose, 'Match? {x}'.format(x=(output == y)) )
                if output != y:
                    result += 1

                ### Error at the last layer (or at the output)
                cost = cost_prime(output, y)

                ### Backward pass
                for i in range(1, len(self.layers) + 1):
                    cost = self.layers[-i].backprop(cost)

            if result == 0:
                break

            ### Adjustments
            for l in self.layers:
                # l.adjust(self.learning_rate, len(tset))
                l.adjust(self.learning_rate, 1)

            if limit is not None and iteration == limit:
                break
            ### END OF EPOCH

        return iteration, result == 0

class layer():
    def __init__(self, size, input_size, weight_range, *pargs, **kwargs):
        self.input = []
        self.neurons = []
        if size > 0:
            for i in range(size):
                self.neurons.append(
                    neuron(input_size, weight_range)
                )

    def eval(self, vector):
        self.input = vector[:]
        output = []
        for n in self.neurons:
            output.append( n.eval(vector) )

        return output

    def backprop(self, cost):
        if self.input is None:
            return

        costs = [0] * len(self.input)

        for i,n in enumerate(self.neurons):
            c = n.backprop( self.input, cost[i])
            costs = addition(c, costs)

        return costs

    def adjust(self, learning_rate, batch_size):
        for n in self.neurons:
            n.adjust( learning_rate, batch_size )

class neuron():
    def __init__(self, input_size, weight_range = 1, *pargs, **kwargs):
        ''' input_size: number of elements to be received by this neuron '''
        self.weights = [ random_weight( weight_range ) for i in range(input_size) ]
        self.nablas = None

    def eval(self, vector):
        return sigmoid( self.dot(vector) )

    def prime(self, vector):
        return sigmoid_prime( self.dot(vector) )

    def dot(self, vector):
        return dot_product(self.weights, vector)

    def backprop(self, vector, cost):
        z = self.prime(vector)

        delta = z * cost

        # print('delta', delta)
        costs = [0] * len(vector)

        if self.nablas is None:
            self.nablas = [0] * len( self.weights )

        # print('vector', vector)

        for ind, element in enumerate(vector):
            # The error for this input is the delta by the weight
            costs[ind] = delta * self.weights[ind]
            # print(ind, 'cost', costs[ind])

            # The nabla to the current weight is the the delta, by the input
            # element
            nabla = delta * element
            # print(ind, 'nabla', nabla)
            self.nablas[ind] += nabla

        return costs

    def adjust(self, learning_rate, batch_size = 1):
        for i in range( len(self.weights) ):
            adjust = -( learning_rate / batch_size ) * self.nablas[i]
            # print(i, 'adjust', adjust)
            # print(i, 'slope', self.nablas[i])
            self.weights[i] = round( self.weights[i] + adjust, 3 )

        self.nablas = None

tset = [
    ([0,0], [0]),
    ([1,0], [0]),
    ([1,1], [1])
]
