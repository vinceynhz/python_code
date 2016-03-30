import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

# Write a computer program that counts the number of linearly separable
# Boolean functions of 2, 3, and 4 arguments. Hint: Generate the perceptron
# weights randomly

# Definition 2. Two sets of points A and B in an n-dimensional space are
# called linearly separable if n + 1 real numbers w1, . . . , wn+1 exist,
# such that every point (x1, x2, . . . , xn) in A satisfies 
#       Sum[n, i=1] (wixi) ≥ wn+1 
# and every point (x1, x2, . . ., xn) in B satisfies 
#       Sum[n, i=1] (wixi) < wn+1

import threading

from random import random, randint
from shared.misc import timeit

def generate(size):
    X = []
    f = []
    
    size = 2 ** size
    val = 0
    for i in range(size):
        X.append(val)
        val += 1

    size = 2 ** size
    val = 0
    for i in range( size ):
        f.append(val)
        val += 1

    return X, f

def weights(size):
    # r = [ round( random(), 3 ) for i in range(size + 1) ]
    r = [ randint(0,10) for i in range(size + 1) ]
    # r = [ 0  for i in range(size) ]
    # r.append( round( sum(r) / len(r), 3 ) )
    # r.append( round( 0.5, 3 ) )
    return r

def dot(u, v):
    return sum( a * b for a,b in zip(u,v) )

def func(x, threshold):
    if x > threshold:
        return 1
    else:
        return 0

def train(size, test_set, learning_rate, response, ind):
    print('s', ind)
    w = weights(size)

    counter = 0
    final = 0
        
    while True:
        error_count = 0
        counter += 1

        for input_vector, desired_output in test_set:
            d = dot(input_vector, w[:-1])
            result = func( d, w[-1] )
            error = desired_output - result

            if error != 0:
                error_count += 1
                for index, value in enumerate(input_vector):
                    w[index] = round( w[index] + learning_rate * error * value, 3 )
                w[-1] = round( w[-1] - learning_rate * error, 3 )
        
        if error_count == 0 or counter == 200:
            break

    if counter == 200:
        final = -1
    else:
        final = 1

    response[ind] = final

    print('e', ind, final)

def test(size):
    ''' The strategy to get this thing is first create all the possible
    combinations of inputs and the possible results of all the binary
    functions possible; then for each function create a perceptron that
    will be trained using the inputs.

    If it can be trained under a X amount of epochs then the binary 
    function is linearly separable. I set X to be 200. '''

    X, f = generate(size)
    
    learning_rate = 1
    good_ones = 0
    bad_ones = 0

    for function in f:
    
        w = weights(size)

        # print('f%d' % k, 'initial weights', w)

        test_set = []

        for j in range(2**size):
            x = []
            for i in range(size):
                x.insert(0, ( X[j] & ( 1 << i ) ) >> i )

            t = ( function & ( 1 << j ) ) >> j
            # print('\t', j, '-', x, ':', t)

            test_set.append( (x,t) )

        counter = 0
        # print(len(test_set))
        
        while True:
            error_count = 0
            counter += 1

            for input_vector, desired_output in test_set:
                d = dot(input_vector, w[:-1])
                result = func( d, w[-1] )
                error = desired_output - result

                if error != 0:
                    error_count += 1
                    for index, value in enumerate(input_vector):
                        w[index] = round( w[index] + learning_rate * error * value, 3 )
                    w[-1] = round( w[-1] - learning_rate * error, 3 )
            
            if error_count == 0 or counter == 200:
                break

        # print('f%d' % k, 'final weights', w)
        
        # probably with 100 will work also
        if counter == 200:
            bad_ones += 1
        else:
            good_ones += 1

    return good_ones, bad_ones

def test2(size):
    ''' The strategy to get this thing is first create all the possible
    combinations of inputs and the possible results of all the binary
    functions possible; then for each function create a perceptron that
    will be trained using the inputs.

    If it can be trained under a X amount of epochs then the binary 
    function is linearly separable. I set X to be 200. '''

    X, f = generate(size)
    
    learning_rate = 1
    good_ones = 0
    bad_ones = 0

    inputs = []
    for j in range(2**size):
        
        x = []
        for i in range(size):
            x.insert(0, ( X[j] & ( 1 << i ) ) >> i )

        inputs.append(x)

    for function in f:
    
        w = weights(size)

        test_set = []

        for j in range(2**size):
            t = ( function & ( 1 << j ) ) >> j

            test_set.append( ( inputs[j], t ) )

        counter = 0
        
        while True:
            error_count = 0
            counter += 1

            for input_vector, desired_output in test_set:
                d = dot(input_vector, w[:-1])
                result = func( d, w[-1] )
                error = desired_output - result

                if error != 0:
                    error_count += 1
                    for index, value in enumerate(input_vector):
                        w[index] = round( w[index] + learning_rate * error * value, 3 )
                    w[-1] = round( w[-1] - learning_rate * error, 3 )
            
            if error_count == 0 or counter == 200:
                break

        # print('f%d' % k, 'final weights', w)
        
        # probably with 100 will work also
        if counter == 200:
            bad_ones += 1
        else:
            good_ones += 1

    return good_ones, bad_ones

def test3(size):
    ''' The strategy to get this thing is first create all the possible
    combinations of inputs and the possible results of all the binary
    functions possible; then for each function create a perceptron that
    will be trained using the inputs.

    If it can be trained under a X amount of epochs then the binary 
    function is linearly separable. I set X to be 200. '''

    X, f = generate(size)
    
    learning_rate = 1
    good_ones = 0
    bad_ones = 0

    inputs = []
    for j in range(2**size):
        
        x = []
        for i in range(size):
            x.insert(0, ( X[j] & ( 1 << i ) ) >> i )

        inputs.append(x)

    response = [ 0 for i in range(2**2**size) ]

    for k,function in enumerate(f):

        test_set = []

        for j in range(2**size):
            t = ( function & ( 1 << j ) ) >> j

            test_set.append( ( inputs[j], t ) )

        t = threading.Thread(
            target=train,
            args=(size, test_set, learning_rate, response, k,)
            )

        t.start()

    print('waiting')

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    return response.count(1), response.count(-1)
