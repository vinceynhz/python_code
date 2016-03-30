import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

import png

from array import array
from colors.spaces import hsl, hsv
from shared.vector import dot_product

_corner_weights = [3, -1, -1, -1]
_border_weights = [5, -1, -1, -1, -1, -1]
_weights = [-1, -1, -1, -1, 8, -1, -1, -1, -1]

def greyscale(pixels):
    new = pixels[:]
    # Convert to grayscale
    for row in range(len(pixels)):

        for column in range(0, len(pixels[row]), 4):

            current = pixels[row][ column: column+3 ]
            current = hsv.fromrgb(current)
            current[1] = 0
            current = array('B', hsv.torgb(current) )

            new[row][column: column+3] = current

    return new

def normalize(val):
    return val / 255

def do(filename):
    r = png.Reader(filename)
    width, height, pixels, header = r.read()

    pixels = list(pixels)
    pixels = greyscale(pixels)
    new = pixels[:]

    corners = 0
    top_borders = 0
    bottom_borders = 0
    left_borders = 0
    right_borders = 0

    # Then do the border detection
    for row in range(len(pixels)):
        for column in range(0, len(pixels[row]), 4):
            # top left corner
            #  a b .
            #  c d .
            #  . . .
            if row == 0 and column == 0:
                p = [ 
                      1-pixels[row][column]/255, 
                      1-pixels[row][column+4]/255,
                      1-pixels[row+1][column]/255,
                      1-pixels[row+1][column+4]/255,
                    ]
                w = _corner_weights
                corners += 1
            # bottom left corner
            #  . . .
            #  c d .
            #  a b .
            elif row == len(pixels)-1 and column==0:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row][column+4]/255,
                      1-pixels[row-1][column]/255,
                      1-pixels[row-1][column+4]/255,
                    ]
                w = _corner_weights
                corners += 1
            # top right corner
            #  . b a
            #  . c d
            #  . . .
            elif row == 0 and column == len(pixels[row])-4:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row][column-4]/255,
                      1-pixels[row+1][column-4]/255,
                      1-pixels[row+1][column]/255,
                    ]
                w = _corner_weights
                corners += 1
            # botttom right corner
            #  . . .
            #  . c d
            #  . b a
            elif row == len(pixels)-1 and column == len(pixels[row])-4:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row][column-4]/255,
                      1-pixels[row-1][column-4]/255,
                      1-pixels[row-1][column]/255,
                    ]
                w = _corner_weights
                corners += 1
            # top border
            # . b a c .
            # . d e f .
            # . . . . .
            elif row == 0: 
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row][column-4]/255,
                      1-pixels[row][column+4]/255,
                      1-pixels[row+1][column]/255,
                      1-pixels[row+1][column-4]/255,
                      1-pixels[row+1][column+4]/255,
                    ]
                w = _border_weights
                top_borders += 1
            # bottom border
            # . . . . .
            # . d e f .
            # . b a c .
            elif row == len(pixels)-1:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row][column-4]/255,
                      1-pixels[row][column+4]/255,
                      1-pixels[row-1][column-4]/255,
                      1-pixels[row-1][column]/255,
                      1-pixels[row-1][column+4]/255,
                    ]
                w = _border_weights
                bottom_borders += 1
            # left border
            # . . .
            # b d .
            # a e .
            # c f .
            # . . .
            elif column == 0:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row-1][column]/255,
                      1-pixels[row+1][column]/255,
                      1-pixels[row-1][column+4]/255,
                      1-pixels[row][column+4]/255,
                      1-pixels[row+1][column+4]/255,
                    ]
                w = _border_weights
                left_borders += 1
            # right border
            # . . .
            # . d b
            # . e a
            # . f c
            # . . .
            elif column == len(pixels[row])-4:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row-1][column]/255,
                      1-pixels[row+1][column]/255,
                      1-pixels[row-1][column-4]/255,
                      1-pixels[row][column-4]/255,
                      1-pixels[row+1][column-4]/255,
                    ]
                w = _border_weights
                right_borders += 1
            else:
                p = [
                      1-pixels[row][column]/255,
                      1-pixels[row][column-4]/255,
                      1-pixels[row][column+4]/255,
                      1-pixels[row-1][column-4]/255,
                      1-pixels[row-1][column]/255,
                      1-pixels[row-1][column+4]/255,
                      1-pixels[row+1][column-4]/255,
                      1-pixels[row+1][column]/255,
                      1-pixels[row+1][column+4]/255,
                    ]
                w = _weights

            new_val = dot_product(p,w)

            if new_val >= 0.5:
                new_val = [0] * 3
            else:
                new_val = [255] * 3

            new[row][column:column+3] = array('B', new_val )

    print('width:', width, 'height:', height)
    print('c:', corners, 'tb:', top_borders, 'bb:', bottom_borders, 'lb:', left_borders, 'rb:', right_borders)

    f = open('out.png', 'wb')
    writer = png.Writer(width, height, bitdepth=header['bitdepth'], greyscale=header['greyscale'], alpha=header['alpha'])
    writer.write(f, new)
    f.close()

