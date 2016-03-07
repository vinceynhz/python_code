import sys

# to make available all the other code
# the route has to be modified for environment's code

sys.path.append('$CODE_DIR\\_lib')
# sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from shared.vector import max_index

def _process_args(*pargs):
    ''' Method to parse whatever is passed in pargs, into a three element list.

    It allows integers, hexadecimal values, hexadecimal strings, other lists or
    tuples and other existent objects.
    '''
    result = [0] * 3

    # One single argument
    if len(pargs) == 1:
        arg = pargs[0]
        # Construct from known classes
        if isinstance( arg, rgb ) or isinstance( arg, hsl ) or isinstance( arg, hsv ):
            result = arg()

        # Check for tuples/lists
        elif( type( arg ) is tuple or type( arg ) is list ):
            larg = len(arg)

            result = list(arg[:3]) + [None] * (3-larg)

        # Check for hex vals as int.
        elif type( arg ) is int:
            # Meaning that we have alpha
            result[2] = arg & 0xFF
            arg = arg >> 8
            result[1] = arg & 0xFF
            arg = arg >> 8
            result[0] = arg & 0xFF

        # Check for hex vals as str.
        elif type( arg ) is str:
            # Check if the values were given as "A,B,C" or "A, B, C"
            if "," in arg:
                tmp = arg[:]
                result[0] = int( tmp[0: tmp.index(",")] )
                tmp = tmp[ tmp.index(",")+1: ]
                result[1] = int( tmp[0: tmp.index(",")] )
                tmp = tmp[ tmp.index(",")+1: ]
                result[2] = int( tmp )
            else:
                # Remove the Hex indicators
                if( arg[0:2] == '0x' or arg[0:2] == '0X'):
                    arg = arg[2:]
                elif( arg[0] == 'x' or arg[0] == 'X' or arg[0] == '#'):
                    arg = arg[1:]

                larg = len(arg)
                # Short hex (CSS version of 3 characters)
                if larg == 3:
                    ints = [ c+c for c in arg ]
                    result[0] = int( ints[0], 16 )
                    result[1] = int( ints[1], 16 )
                    result[2] = int( ints[2], 16 )
                # Regular hex
                elif larg >= 6:
                    result[0] = int( arg[0:2], 16 )
                    result[1] = int( arg[2:4], 16 )
                    result[2] = int( arg[4:6], 16 )
    else:
        lparg = len(pargs)
        result = list(pargs[:3]) + [0] * (3-lparg)

    return result

class _trivalue_array():
    ''' Parent class of a tri-value array object 

    This one is intended for HSL and HSV classes since overrides the mathematic
    operators to increase or decrease the values in the object'''
    
    def __init__(self, *pargs):
        if len(pargs) == 0:
            self._value = [0] * 3
        else:
            self._value = _process_args(*pargs)

    def _0():
        ''' property to refer to element 0 of the array '''
        def fget(self):
            return self._value[0]
        def fset(self, value):
            self._value[0] = value
        return locals()

    def _1():
        ''' property to refer to element 1 of the array '''
        def fget(self):
            return self._value[1]
        def fset(self, value):
            self._value[1] = value
        return locals()

    def _2():
        ''' property to refer to element 2 of the array '''
        def fget(self):
            return self._value[2]
        def fset(self, value):
            self._value[2] = value
        return locals()

    def __call__(self):
        ''' callable to get the vector '''
        return self._value

    def __str__(self):
        ''' string representation for printing '''
        return str(self())

    def __repr__(self):
        ''' representation for command line '''
        output = str(self()) + " "
        output += super(_trivalue_array, self).__repr__()
        return output

    def __add__(self, value):
        ''' this will increase third value'''
        return [ self._value[0], self._value[1], _trivalue_array._cadd(self._value[2], value) ]

    def __radd__(self, value):
        ''' this will increase third value'''
        return self.__add__(value)

    def __iadd__(self, value):
        ''' this will increase third value'''
        self._value[2] = _trivalue_array._cadd(self._value[2], value)
        return self

    def __sub__(self, value):
        ''' This will decrease third value '''
        return [ self._value[0], self._value[1], _trivalue_array._csub(self._value[2], value) ]

    def __rsub__(self, value):
        ''' This will decrease third value '''
        return self.__sub__(value)

    def __isub__(self, value):
        ''' This will decrease third value '''
        self._value[2] = _trivalue_array._csub(self._value[2], value)
        return self

    def __mul__(self, value):
        ''' This will increase saturation '''
        return [ self._value[0], _trivalue_array._cadd(self._value[1], value), self._value[2] ]

    def __rmul__(self, value):
        ''' This will increase saturation '''
        return self.__mul__(value)

    def __imul__(self, value):
        ''' This will increase saturation '''
        self._value[1] = _trivalue_array._cadd(self._value[1], value)
        return self

    def __truediv__(self, value):
        ''' This will decrease saturation '''
        return [ self._value[0], _trivalue_array._csub(self._value[1], value), self._value[2] ]

    def __rtruediv__(self, value):
        ''' This will decrease saturation '''
        return self.__truediv__(value)

    def __itruediv__(self, value):
        ''' This will decrease saturation '''
        self._value[1] = _trivalue_array._csub(self._value[1], value)
        return self

    def __pow__(self, value):
        ''' This will increase hue '''
        return [ _trivalue_array._cadd(self._value[0], value, True), self._value[1], self._value[2] ]

    def __rpow__(self, value):
        ''' This will increase hue '''
        return self.__pow__(value)

    def __ipow__(self, value):
        ''' This will increase hue '''
        self._value[0] = _trivalue_array._cadd(self._value[0], value, True)
        return self

    def __floordiv__(self, value):
        ''' This will decrease hue '''
        return [ _trivalue_array._csub(self._value[0], value, True), self._value[1], self._value[2] ]

    def __rfloordiv__(self, value):
        ''' This will decrease hue '''
        return self.__floordiv__(value)

    def __ifloordiv__(self, value):
        ''' This will decrease hue '''
        self._value[0] = _trivalue_array._csub(self._value[0], value, True)
        return self

    ### EQUALS ###
    def __eq__(self, other):
        ''' Comparison '''
        return self() == other()

    def _cadd(to, value, circle=False):
        ''' closed addition

        Basic function is to add 'value' and 'to' and limit the
        result to 100.

        If circle set to True, the addition limit is done over 360 and 
        will be looped to 360 (using modulus)

        If the value specified is float, it will be taken as 
        a percentage of addition following the same limit rules
        '''

        if not circle and to == 100:
            return to

        if type(value) is int: # We add a number
            to += value

        if type(value) is float:
            factor = 360 if circle else 100
            to += round(factor * value) # We add that %

        if circle and to % 360 >= 0:
            to = to % 360
        elif not circle and to > 100:
            to = 100

        return to

    def _csub(to, value, circle=False):
        ''' closed subtraction

        Basic function is to subtraction 'value' and 'to' and limit
        the result to 0.

        If circle set to True, the subtraction limit is done over 360 and 
        will be looped to 360 (using modulus)

        If the value specified is float, it will be taken as 
        a percentage of subtraction following the same limit rules
        '''
        if not circle and to == 0:
            return to

        if type(value) is int: # We add a number
            to -= value

        if type(value) is float:
            factor = 360 if circle else 100
            to -= round(factor * value) # We add that %

        if circle and to % 360 < 0:
            to = to % 360
        elif not circle and to < 0:
            to = 0

        return to

class rgb():
    ''' base class for rgb color representation and manipulation '''
    def __init__(self, *pargs):
        self.r, self.g, self.b = _process_args(*pargs)

    def __call__(self):
        ''' callable to get the vector '''
        return [self.r, self.g, self.b]

    def __str__(self):
        ''' string representation for printing '''
        return str(self())

    def __repr__(self):
        ''' representation for python interpreter'''
        output = str(self()) + " "
        output += super(rgb, self).__repr__()
        return output

    def __add__(self, other):
        ''' average addition between two colors '''
        return [ (a + b) // 2 for a,b in zip( self(), other() ) ]

    def hsl(self, convert=False):
        ''' conversion from RGB to HSV
        
        If convert is set to True, a new instance of hsl is created and passed
        back as result, otherwise the result is a list 3 values corresponding
        to hue, saturation and light
        '''
        new = None
        ret = hsl.fromrgb(self())
        if convert:
            new = hsl()
            new.h = ret[0]
            new.s = ret[1]
            new.l = ret[2]
        else:
            new = ret
        return new

    def hsv(self, convert=False):
        ''' conversion from RGB to HSV
        
        If convert is set to True, a new instance of hsv is created and passed
        back as result, otherwise the result is a list 3 values corresponding
        to hue, saturation and value
        '''
        new = None
        ret = hsv.fromrgb(self())
        if convert:
            new = hsv()
            new.h = ret[0]
            new.s = ret[1]
            new.v = ret[2]
        else:
            new = ret
        return new

    def cmyk(self):
        ''' conversion from RGB to CMY'''
        return cmy.fromrgb(self())

    def _norm( value ):
        ''' From sRGB defintion, to normalize an input value '''
        result = 0
        if value <= 0.03928:
            result = value / 12.92
        else:
            result = ( (value + 0.055) / 1.055 ) ** 2.4

        return result

    def XYZ(self):
        ''' conversion from RGB to CIE XYZ normalized space '''
        R = rgb._norm( self.r / 255 )
        G = rgb._norm( self.g / 255 )
        B = rgb._norm( self.b / 255 )

        X = R * 0.4124 + G * 0.3576 + B * 0.1805;
        Y = R * 0.2126 + G * 0.7152 + B * 0.0722;
        Z = R * 0.0193 + G * 0.1192 + B * 0.9505;

        return [X,Y,Z]

    def xyz(self):
        ''' conversion from RGB to CIE xyY chromaticity space '''
        xyz = self.XYZ()
        if sum(xyz) == 0:
            x, y, z = [0,0,0]
        else:
            x = round( xyz[0]/sum(xyz), 6 )
            y = round( xyz[1]/sum(xyz), 6 )
            z = round( xyz[2]/sum(xyz), 6 )

        return [x,y,z]

    def wavelength(self):
        # TODO: still pending to calculate this function
        pass

    def hex(self):
        ''' hexadecimal representation of the RGB value '''
        a = self.r
        a = a << 8
        a += self.g
        a = a << 8
        a += self.b
        return a

    def hexs(self):
        ''' hexadecimal string representation of the RGB value '''
        string = hex( self.hex() )
        string += '0' * (6 - len(string[2:]))
        return string

class cmy():
    def fromrgb(rgb):
        R = rgb[0]/255
        G = rgb[1]/255
        B = rgb[2]/255

        K = 1 - max(R,G,B)
        C = ( 1 - R - K ) / ( 1 - K ) if K != 1 else 0
        M = ( 1 - G - K ) / ( 1 - K ) if K != 1 else 0
        Y = ( 1 - B - K ) / ( 1 - K ) if K != 1 else 0
        return [ round(C*100),
                 round(M*100),
                 round(Y*100),
                 round(K*100) ]

class hsl(_trivalue_array):
    ''' Hue Saturation Light class for color manipulation '''
    # Rename the properties using the ones provided by the parent
    # Probably this mechanism is not the most elegant one, but it 
    # helped me to understand properties and inhertance in python 
    h = property(**_trivalue_array._0())
    s = property(**_trivalue_array._1())
    l = property(**_trivalue_array._2())

    def __init__(self, *pargs):
        super(hsl, self).__init__(*pargs)

    def rgb(self):
        ''' convert the HSL object to its RGB representation '''
        return hsl.torgb(self())

    ### CLASS LEVEL METHODS ###
    def torgb(hsl):
        ''' http://www.rapidtables.com/convert/color/hsl-to-rgb.htm '''
        H = hsl[0] / 60
        S = hsl[1] / 100
        L = hsl[2] / 100

        C = (1 - abs(2 * L - 1)) * S
        X = C * ( 1 - abs(H % 2 - 1) )

        RGB = {
                0 : [C,X,0], # 0 <= H < 1
                1 : [X,C,0], # 1 <= H < 2
                2 : [0,C,X], # 2 <= H < 3
                3 : [0,X,C], # 3 <= H < 4
                4 : [X,0,C], # 4 <= H < 5
                5 : [C,0,X], # 5 <= H < 6
              }[ ( hsl[0] % 360) // 60 ]

        m = L - C/2
        return [ round( (RGB[0] + m) * 255 ),
                 round( (RGB[1] + m) * 255 ),
                 round( (RGB[2] + m) * 255 ) ]

    def fromrgb(rgb):
        ''' http://www.rapidtables.com/convert/color/rgb-to-hsl.htm '''
        R = rgb[0] / 255 # norm to [0,1]
        G = rgb[1] / 255 # norm to [0,1]
        B = rgb[2] / 255 # norm to [0,1]

        Imax = max_index(R,G,B)
        Cmax = max(R,G,B)
        Cmin = min(R,G,B)
        delta = Cmax - Cmin

        if delta == 0:
            H = 0
        else:
            H = {
                    0 : 60 * ( (G - B) / delta % 6 ), # Max R
                    1 : 60 * ( (B - R) / delta + 2 ), # Max G
                    2 : 60 * ( (R - G) / delta + 4 )  # Max B
                }[ Imax ]

        L = (Cmax + Cmin) / 2
        S = {
            True  : 0,
            False : delta / (1-abs(2 * L - 1)) if L != 1 and L != 0 else delta
        }[ delta == 0 ]

        return[ round(H), round(S * 100), round(L * 100) ]

class hsv(_trivalue_array):
    ''' Hue Saturation Value class for color manipulation '''
    # Rename the properties using the ones provided by the parent
    # Probably this mechanism is not the most elegant one, but it 
    # helped me to understand properties and inhertance in python 

    h = property(**_trivalue_array._0())
    s = property(**_trivalue_array._1())
    v = property(**_trivalue_array._2())

    def __init__(self, *pargs):
        super(hsv, self).__init__(*pargs)

    def rgb(self):
        return hsv.torgb(self())

    ### CLASS LEVEL METHODS ###
    def torgb(hsv):
        ''' http://www.rapidtables.com/convert/color/hsv-to-rgb.htm '''
        H = hsv[0] / 60
        S = hsv[1] / 100 # normalize to [0,1]
        V = hsv[2] / 100 # normalize to [0,1]

        C = V * S
        X = C * ( 1 - abs(H % 2 - 1) )

        RGB = {
                0 : [C,X,0], # 0 <= H < 1
                1 : [X,C,0], # 1 <= H < 2
                2 : [0,C,X], # 2 <= H < 3
                3 : [0,X,C], # 3 <= H < 4
                4 : [X,0,C], # 4 <= H < 5
                5 : [C,0,X], # 5 <= H < 6
              }[ ( hsv[0] % 360 ) // 60 ]

        m = V - C
        return [ round( (RGB[0] + m) * 255 ),
                 round( (RGB[1] + m) * 255 ),
                 round( (RGB[2] + m) * 255 ) ]

    def fromrgb(rgb):
        ''' http://www.rapidtables.com/convert/color/rgb-to-hsv.htm '''
        R = rgb[0] / 255 # norm to [0,1]
        G = rgb[1] / 255 # norm to [0,1]
        B = rgb[2] / 255 # norm to [0,1]

        Imax = max_index(R,G,B)
        Cmax = max(R,G,B)
        Cmin = min(R,G,B)
        delta = Cmax - Cmin

        if delta == 0:
            H = 0
        else:
            H = {
                    0 : 60 * ( (G - B) / delta % 6 ), # Max R
                    1 : 60 * ( (B - R) / delta + 2 ), # Max G
                    2 : 60 * ( (R - G) / delta + 4 )  # Max B
                }[ Imax ]

        V = Cmax

        S = {
            True  : 0,
            False : delta / Cmax if Cmax != 0 else 1
        }[ Cmax == 0 ]

        return[ round(H), round(S * 100), round(V * 100) ]
