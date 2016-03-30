# Common library for shared functions across

### Contents
1. shared
  1. [*misc.py*](#sharedmisc), miscellaneous functions... Semantically I couldn't figure out where to put them
  2. [*vector.py](#sharedvector), vector operations
  3. [*log.py*](#sharedlog), logging functions
2. colors
  1. [*spaces.py*](#colorsspaces), color spaces definitions and transformations between them 
  2. [*colorlib.py*](#colorscolorlib), library for color transformations

### *shared.misc*

The following classes are defined:
* *timeit*, to get the execution time (in ms) of a block of code, see code for usage information

The following methods are defined:

**General**
* *cls*: wrapper of a os.system("cls") call for use in the python interpreter
* *clear*: alias for cls (for when you have been in linux/unix for so long that you mess up your commands)
* *slope*: to calculate the slope between two points *(x1,y1)* and *(x2,y2)*
* *prorate*: when designing layouts in kivy, the percentual position is kinda tricky, this function helps me calculating the proper hints
* *cycle*: cycle an element within the boundaries given, see code for a detailed explanation

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

### *shared.vector*

The following methods are defined:

**Trigonometric functions**
Clean functions: they receive an angle in degrees, convert it to radians (for math functions) and truncate the result to avoid floating point issues
* *ccos*
* *csin*
* *ncos*: negative of the ccos
* *nsin*: negative of the csin

**General**
* *is_same*: check if all elements in a vector are the same
* *truncate*: truncate the elements of a vector to a given value
* *adjust*: change the elements to be 0 based insted of 1 based
* *clean*: remove negative values, floating point and overflows
* *max_index*: get the index of the maximum value in the given input

**Vector to Vector operations**
* *addition*
* *product*: between matrix and vector
* *scalar*
* *distance*
* *magnitude*
* *angle*
* *vor*: elementwise OR between two vectors
* *vand*: elementwise AND between two vectors
* *vadd*: elementwise addition between two vectors

**Vector Rotations**
* *Rx*: rotate from y to z on x
* *iRx*: rotate from z to y on x
* *Ry*: rotate from z to x on y
* *iRy*: rotate from x to z on y
* *Rz*: rotate from x to y on z
* *iRz*: rotate from y to x on z
* *rotate*: wrapper for all rotations

### *shared.log*
The following methods are defined:
* *log*: to log a message with a specific level on a given logger
* *printif*: for conditional (verbose flag-like) printing to console

### *colors.spaces*
The following classes are defined:
* *rgb*: base class for RGB operations, it does not handle alpha channel
* *cmy*: class for CMY operations (mostly transformations to RGB)
* *_trivalue_array (Parent)*: parent class for HSL and HSV, it overrides operators for manipulation of each parameter (Hue, Saturation and Light/Value)
* *hsl (_trivalue_array)*: implements the code to transform from and to RGB
* *hsv (_trivalue_array)*: implements the code to transform from and to RGB

The following methods are defined:
* *_process_args*: method to extract input passed as a list of values, hexadecimal representations or instances of rgb, hsl or hsv, and transform it to a simple list of 3 values

### *colors.colorlib*

The following class is defined:
* *Color*: extension class from rgb (defined in spaces.py), it adds color manipulation methods to create harmonic combinations and xml representation. It implements the calculation of color circle considering RGB as a vectorial space. Working on the paper that explains these calculations and the reasoning behind it.

The following methods are defined:
* *_in_range*: to determine if a value is within a percentual range around a given second value
* *_avg*: to calculate the average between two values
* *_add_color*: to include a given color set in its rgb values to a color circle; if its a value considered to be a red, green or blue, it calculates the sibling color (the one that approximates from the other direction)
* *_rotate*: wrapper of the vector.rotate function that based on the keyword rotates a color to the other two canonical basis (red, green or blue)
* *_get_color*: to extrapolate the complementary colors. If a red, green or blue was initially given, this method will extrapolate the cyan, magenta and yellow; opposite case if a cyan, magenta or yellow was given. (TODO: add reference to the finished paper regarding circle calculation)