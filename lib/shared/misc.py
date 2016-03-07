import sys

from os import system
from datetime import datetime

class timeit():
    ''' to calculate the execution time (in ms) of a piece of code.

    The class is intended to be used as part of a with block:

    >>> with timeit():
            # add code to time

    At the end of the execution, the time will be printed to std output'''
    def __enter__(self):
        self.start = datetime.now()
        return self

    def __exit__(self, *args):
        self.end = datetime.now()
        self.interval = self.end - self.start
        print(self.interval)

def cls():
    ''' wrapper for os.system('cls') for windows systems '''
    system("cls")

# Alias for cls
clear = cls

#### BINARY DATA FORMATTING AND PRINTING ###
def _print_data(data, stream=sys.stdout):
    ''' this method will format a bunch of bytes into their hex 
    and ASCII representations '''
    line = 0
    output = ""

    for i in range(len(data)):
        # If new line
        if i%16 == 0:
            output += "%04X: " % line
            line += 16

        # Print out the hex byte
        output += "%02X" % data[i]

        # Print the blank space if needed
        if ((i+1)%8) == 0:
            output += "  "
        
        # Print the ascii representations
        if ((i+1)%16) == 0:
            for j in range(i-15, i+1):
                output += "%c" %  data[j] if (data[j] >= 32 and data[j] < 127) else '.'
                if ((j+1) % 8) == 0:
                    output += " "
            
            print(output, file=stream)
            output = ""
        
        # If this is the last byte to be printed
        elif i == len(data) - 1:
            k = 16 - (i+1) % 16
            
            for j in range(k):
                # Print the blank space if needed
                if ((i+j+1)%8) == 0:
                    output += "  "
                output += "   "

            output += "  "
            
            for j in range(i-(i%16), i+1):
                output += "%c" %  data[j] if (data[j] >= 32 and data[j] < 127) else '.'
                if ((j+1) % 8) == 0:
                    output += " "

            for j in range(k):
                # Print the blank space if needed
                if ((i+j+1)%8) == 0:
                    output += " "
                output += " "                

            print(output, file=stream)
        else:
            output += " "

#### BRESENHAM LINE FUNCTIONS ####
# https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
def allpoints(o, p):
    ''' To calculate all pixels between two given points '''
    # normalize the point respect to the origin
    np = [ p[0] - o[0], p[1] - o[1] ]
    # get the octant
    oc = octant(*np)

    # perform the proper change of coordinates
    np = switchto(oc, *np)
    # and get the points for the normalized and switched coords
    points = bresenham(*np)
    # adjust each point back
    for i in range(len(points)):
        # perform the change back to the real coordinates
        tmp = switchfrom(oc, *points[i])
        # and rollback the normalization to the origin
        points[i] = [ o[0] + tmp[0], o[1] + tmp[1] ]

    return points

def switchto(octant, x, y) :
    # based on the octant, change the coordinates for the bresenham algorithm
    return {
        0: [x, y],
        1: [y, x],
        2: [y, -x],
        3: [-x, y],
        4: [-x, -y],
        5: [-y, -x],
        6: [-y, x],
        7: [x, -y]
     }[octant]

def switchfrom(octant, x, y):
    # based on the octant, change the coordinates after the bresenham algorithm
   return {
        0: [x, y],
        1: [y, x],
        2: [-y, x],
        3: [-x, y],
        4: [-x, -y],
        5: [-y, -x],
        6: [y, -x],
        7: [x, -y]
        }[octant]

def bresenham(xi, yi, xo=0, yo=0):
    #  Bresenham algorithm
    result = []
    dx = xi-xo
    dy = yi-yo

    D = 2 * dy - dx

    result.append([xo,yo])
    y = yo

    for x in range(xo+1, xi+1):
        result.append([x,y])
        D = D + ( 2 * dy )
        if D > 0:
            y = y + 1
            D = D - ( 2 * dx )

    return result

def octant(x, y):
    # this thing will calculate the octant given an x and y coordinates
    # Octants:
    #   \2|1/
    #   3\|/0
    #  ---+---
    #   4/|\7
    #   /5|6\
    octant = -1

    if x >= 0 and y >= 0: # first quad
        octant = 0 if x >= y else 1
    elif x < 0 and y >= 0: # second quad
        octant = 2 if abs(x) <= y else 3
    elif x <= 0 and y < 0: # third quad
        octant = 4 if abs(x) >= abs(y) else 5
    elif x > 0 and y < 0: # fourth quad
        octant = 6 if x <= abs(y) else 7

    return octant
#### END OF BRESENHAM FUNCTIONS ####

#### SCALING A MATRIX IN SIZE USING THE METHOD OF SIMPLE EXISTENCE ####
def scalematrix(matrix, currentsize, newsize):
    dx = round(currentsize[0] / newsize[0])
    dy = round(currentsize[1] / newsize[1])
    print('  - dx', dx, 'dy', dy)
    scaled = []

    # this will iterate through the rows in the scaled matrix
    for y in range(newsize[1]):
        # this is my pivot coord y for the original matrix
        py = y * dy
        # this will iterate through the columns in the scaled matrix
        for x in range(newsize[0]):
            # this is my pivot coord x for the original matrix
            px = x * dx

            # rows in original matrix, that correspond to the current coord in
            # the scaled matrix
            found = False
            for j in range(dy):
                # cols in original matrix, that correspond to the current coord
                # in scaled matrix
                for i in range(dx):
                    # let's get a coord
                    coord = [px + i, py + j]
                    # if the coord is existing already in the matrix
                    if coord in matrix:
                        # we don't need to check further, this cell has to be
                        # added
                        found = True
                        break
                if found:
                    break

            if found:
                scaled.append([x,y])

    scaled.sort()
    return scaled

def slope(xo, yo, xi, yi):
    return (yi-yo) / (xi-xo)

def prorate(items):
    current = 1
    result = []
    for item in items:
        result.append(item/current)
        current -= item

    if current > 0:
        result.append(current)

    return result

def cycle(value, upper, lower = 0):
    ''' This function will adjust the value within the boundaries given

    Case 1: The value does not overflow the boundaries

        -oo <----|-------x--------|----> +oo
                low    value      up

        The value is returned

    Case 2: The value overflows outside of the boundary and the overflow (of)
            amount is less than the range amount

                  ~~~~~ range ~~~~~ ~~~ of ~~>
        -oo <----|-----------------|----------x----> +oo
                low               up        value

        OR:

                  <~~ of ~~~ ~~~~~ range ~~~~~
        -oo <----x----------|-----------------|----> +oo
               value       low                up


        The value will be 'bounced' from the exceeded boundary back 
        to within range:

                  ~~~~~ range ~~~~~
                         <~~ of ~~~<<<
        -oo <----|------x----------|----> +oo
                low   value       up

        OR:

                  ~~~~~ range ~~~~~
               >>>~~~ of ~~>
        -oo <----|----------x------|----> +oo
                low       value    up

    Case 3: The value overflows outside of the boundary and the overflow
            amount is greater than the range

                  ~~~~~ range ~~~~~ ~~~~~~~~~ overflow ~~~~~~~~>
        -oo <----|-----------------|----------------------------x----> +oo
                low               up                          value

        OR:

                  <~~~~~~~~ overflow ~~~~~~~~~ ~~~~~ range ~~~~~
        -oo <----x----------------------------|-----------------|----> +oo
               value                         low                up

        The value will be 'bounced' multiple times from boundary to boundary 
        until it falls within the range indicated:

                  ~~~~~ range ~~~~~ 
                  <~~~~~~~~~~~~~~~~<<<
               >>>~~~~~~~~~~>

        -oo <----|-----------x-----|----> +oo
                low        value  up

        OR:

                  ~~~~~ range ~~~~~ 
               >>>~~~~~~~~~~~~~~~~~
                        <~~~~~~~~~~<<<

        -oo <----|-----x-----------|----> +oo
                low  value        up

    '''
    # First, we determine the real range
    rnge = upper + abs(lower)
    # Then we determine the overflow
    overflow = value % rnge
    # Then, how many times the value can fit in the range
    times = value // rnge

    if times == 0:
        if value > upper:
            return value - lower
        else:
            return value

    if times % 2 != 0:
        return upper - overflow - lower

    return lower + overflow
