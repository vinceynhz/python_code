# Common library for shared functions across

### Contents
1. shared
  1. *misc.py*, miscellaneous functions... Semantically I couldn't figure out where to put them

### *shared.misc*

The following classes are defined:
* *timeit*, to get the execution time (in ms) of a block of code, see code for usage information

The following methods are defined:

**General**
* *cls*: wrapper of a os.system("cls") call for use in the python interpreter
* *clear*: alias for cls (for when you have been in linux/unix for so long that you mess up your commands)
* *slope*: to calculate the slope between two points *(x1,y1)* and *(x2,y2)*
* *prorate*: when designing layouts in kivy, the percentual position is kinda tricky, this function helps me calculating the proper hints

**Binary Data**
* *_print_data*: it receives a bytes or bytearray and formats it into hex/ascii output, useful for binary debugging

[**Bresenham's Line Algorithm**](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)
* *allpoints*: this is the function to call to calculate all pixels in a straight line between two points *(x1,y1)* and *(x2,y2)*
* *switchto*: to transform the given coordinates based on the octant they belong to
* *switchfrom*: to reverse the transformation after the algorithm
* *bresenham*: the algorithm itself
* *octant*: to calculate the octant of a point

**Matrix Scalation**
* *scalematrix*: take a matrix, create partitions and map them to an output matrix of any size
