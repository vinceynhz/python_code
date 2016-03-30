import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from math import tanh, exp, atanh, log
from random import random

from shared.misc import cls
from shared.vector import dot_product, addition
from shared.log import printif

### Activation functions
def tanh_prime(x):
    ''' Derivative of the Hyperbolic Tangent function 
    
    When reading around, the Hyperbolic Tangent function can be used instead
    of the sigmoid for activation of the neurons. The tanh is part of the math
    library but not it's derivative (which is used for Backpropagation). 

    This is that derivative. The function goes from -1 to 1, threshold 0. 
    '''
    return 1 - ( tanh(x) ** 2 )

def sigmoid(x):
    ''' Sigmoid Function or Logistic Function

    Probably the most used ones on feed forward back propagation multi layer 
    networks.

    This function goes from 0 to 1, threshold 0.5 '''
    return 1 / ( 1 + exp(-x) )

def sigmoid_prime(x):
    ''' Derivative of the Sigmoid Function
    
    This is the derivative of the sigmoid function shown above, used for
    back propagation '''
    return sigmoid(x) * ( 1 - sigmoid(x) )

### Backprop functions
def cost_func(output, target):
    ''' Mean Squared Error Formula '''
    return ( (target - output) ** 2 ) / 2

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# NOTE: Comment out ONE of these implementations depending on the experiment  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

##### STANDARD VERSION
def cost_prime(output, target):
    ''' Derivative of the quadratic error'''
    return [ output[ind] - target[ind] for ind in range( len(output) ) ]

##### FAHLMAN VERSION
# def cost_prime(output, target):
#     ''' As suggested by Fahlman also, changing the error to grow drastically
#     when the difference between the expected output and the actual one are 
#     bigger, using a modified version of the arc tanh'''

#     return [ catanh( output[ind] - target[ind] ) for ind in range( len(output) ) ]

# def catanh(x):
#     ''' Using the hyperbolic arc tangent from math '''
#     if x >= 1:
#         x = 0.999999
#     elif x <= -1:
#         x = -0.999999
#     return round(atanh(x), 3)

# This one and the one above seem to be the same
def catanh(x):
    ''' Using the logaritmic property of the hyperbolic arc tan '''
    if x >= 0.999999:
        return 17
    elif x <= -0.999999:
        return -17
    else:
        return round(log( (1+x) / (1-x) ), 3)

### Output margin function
def margin1(x, threshold=0.5):
    ''' Using a simple decision on threshold '''
    return 0 if x < threshold else 1

def margin2(x, threshold=0.5):
    ''' Using marginal values around the threshold, as described by Fahlman
    in the same paper '''
    return 0 if x < (threshold - 0.1) else 1 if x > (threshold + 0.1) else x

### Get a random weight functions
def random_weight(wrange=0.5, precision=1):
    ''' To initialize the weights, using python's pseudo random generator '''
    return round( random() * (wrange * 2) - wrange, precision )
