import sys

# to make available all the other code
# the route has to be modified for environment's code

sys.path.append('$CODE_DIR\\_lib')
# sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

'''
    This module contains multiple functions to operate vectors and matrices
'''
from math import sqrt, acos, cos, sin, pi, radians
from shared.misc import cycle

### TRIGONOMETRIC FUNCTIONS ###
def ccos(angle):
    """ Clean cosinus: angle in degrees,
    result truncated to reduce floating point issues """
    return round( cos(radians(angle)), 2 )

def csin(angle):
    """ Clean sinus: angle in degrees,
    result truncated to reduce floating point issues """
    return round( sin(radians(angle)), 2 )

def nsin(angle):
    """ Clean negative sinus: angle in degrees,
    result truncated to reduce floating point issues """
    return -1 * csin(angle)

def ncos(angle):
    """ Clean negative cosinus: angle in degrees,
    result truncated to reduce floating point issues """
    return -1 * ccos(angle)

#Value used to convert between radians and degrees
to_degrees = 180 / pi

### MISC FUNCTIONS ###
def is_same(vector):
    ''' check if all the elements in the vector are the same '''
    if len(vector) == 1:
        return True

    v = vector[0]
    for i in vector[1:]:
        if i != v:
            return False

    return True

# Vector operations
def addition(vector1, vector2):
    return [ u + v for u,v in zip(vector1, vector2) ]
    # return [ value + vector2[i] for i,value in enumerate(vector1) ]

def product(matrix, vector):
    ''' matrix by vector '''
    result = []
    for row in matrix:
        result.append( scalar(row, vector) )
    return result

def scalar(vector1, vector2):
    ''' scalar product '''
    # product = 0
    # for ind,val in enumerate(vector1):
    #     product += val * vector2[ind]
    # return product
    return sum( u * v for u, v in zip(vector1, vector2))

dot_product = scalar

def truncate(vector, value):
    ''' truncate values in a vector '''
    return [ i if i < value else value for i in vector ]

def adjust(vector):
    ''' adjustment to 0 based elements in a vector '''
    return [ i-1 for i in vector ]

def clean(vector): 
    ''' eliminate negatives, floating points, and overflow '''
    return [ cycle(abs(int(value)), 255) for value in vector ]

def distance(vector1, vector2):
    ''' calculate the distance between two vectors '''
    temp = [ v * vector2[i] for i,v in enumerate(vector1) ]
    d = 0
    for v in temp:
        d += v
    return sqrt( d )

def magnitude(vector):
    ''' calculate the magnitude of a vecto
    which can be understood as the distance to itself '''
    return distance(vector, vector)

def angle(vector1, vector2):
    ''' calculate the angle between two vectors '''
    s = scalar(vector1, vector2)
    m = magnitude(vector1) * magnitude(vector2)
    return acos( s / m ) * to_degrees

# Rotations
def Rx(vector, angle): 
    ''' Rotate from y to z, on x '''
    matrix = [
               [1, 0, 0],
               [0, ccos(angle), nsin(angle)],
               [0, csin(angle), ccos(angle)]
             ]
    return product( matrix, vector )

def iRx(vector, angle): 
    ''' Rotate from z to y, on x '''
    matrix = [
               [1, 0, 0],
               [0, ccos(angle), csin(angle)],
               [0, nsin(angle), ccos(angle)]
             ]
    return product( matrix, vector )

def Ry(vector, angle): 
    ''' Rotate from z to x, on y '''
    matrix = [
                [ccos(angle), 0, csin(angle)],
                [0,1,0],
                [nsin(angle), 0, ccos(angle)]
             ]
    return product(matrix, vector)

def iRy(vector, angle):
    ''' Rotate from x to z, on y '''
    matrix = [
            [ccos(angle), 0, nsin(angle)],
            [0,1,0],
            [csin(angle), 0, ccos(angle)]
         ]
    return product(matrix, vector)

def Rz(vector, angle): 
    ''' Rotate from x to y, on z '''
    matrix = [
                [ccos(angle), nsin(angle), 0],
                [csin(angle), ccos(angle), 0],
                [0, 0, 1]
             ]
    return product(matrix, vector)

def iRz(vector, angle):
    ''' Rotate from y to x, on z '''
    matrix = [
                [ccos(angle), csin(angle), 0],
                [nsin(angle), ccos(angle), 0],
                [0, 0, 1]
             ]
    return product(matrix, vector)

def rotate(vector, axis, angle):
    ''' wrapper of rotations '''
    return{
        'x'  : Rx,
        'y'  : Ry,
        'z'  : Rz,
        'ix' : iRx,
        'iy' : iRy,
        'iz' : iRz
    }[axis](vector, angle)

def vor(vector1, vector2):
    ''' apply an OR logical operation to the elements in two given vectors '''
    if type(vector2) is list:
        return [ v | vector2[i] for i,v in enumerate(vector1) ]
    else:
        return [ v | vector2 for i,v in enumerate(vector1) ]

def vand(vector1, vector2):
    ''' apply an AND logical operation to the elements in two given vectors '''
    if type(vector2) is list:
        return [ v & vector2[i] for i,v in enumerate(vector1) ]
    else:
        return [ v & vector2 for i,v in enumerate(vector1) ]

def vadd(vector1, vector2):
    ''' elementwise addition of elements in two vectors, haddamard addition '''
    if type(vector2) is list:
        return [ ( v + vector2[i] ) / 2 for i,v in enumerate(vector1) ]
    else:
        return [ ( v + vector2 ) / 2 for i,v in enumerate(vector1) ]

def max_index(*pargs):
    """ a) get the maximum value of the array
    b) get the index of the first ocurrence """
    if len(pargs) > 1:
        array = list(pargs)
    else:
        array = pargs[0]
    return array.index( max(array) )
