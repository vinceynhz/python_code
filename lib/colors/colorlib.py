import sys

# to make available all the other code
# the route has to be modified for environment's code

sys.path.append('$CODE_DIR\\_lib')
# sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from shared import vector
from colors.spaces import rgb, hsl, hsv

### Helper variables ###
_rgb_str = 'RGB'
_cmy_str = 'CMY'

_xml_swatch_header = '<Swatch name="{name}">\n'
_xml_swatch_trailer = '</Swatch>\n'

_xml_palette_header = '<Palette name="{name}">\n'
_xml_palette_trailer = '</Palette>\n'

_xml_color = '<Color value="{value}" hex="{hex}" hsl="{hsl}" hsv="{hsv}" cmyk="{cmyk}" xyz="{xyz}" />\n'

def _in_range(value, min, max):
    """ find if value is within the boundaries of min and max """
    return value >= min and value <= max

def _avg( a, b ):
    """ find the integer average of two values """
    return ( a + b ) // 2

def _add_color(name, circle, color):
    ret = 1

    if name in _rgb_str:
        # m(inor)   minor component
        # M(ajor)   major component
        # r(ed)     which component from the original color should be put in the
        #           red of the resultant
        # g(reen)   which component from the original color should be put in the
        #           green of the resultant
        # b(lue)    which component from the original color should be put in the
        #           blue of the resultant
        inds = {      #m  M  r  g  b
                'R' : [1, 2, 0, 2, 1],
                'G' : [0, 2, 2, 1, 0],
                'B' : [0, 1, 1, 0, 2]
        }[name]

        # If minor greater than the major
        if color[ inds[0] ] >= color[ inds[1] ]:
            circle[ name + '1' ] = color
            circle[ name + '2' ] = [ color[ inds[2] ], color[ inds[3] ], color[ inds[4] ] ]
        else:
            circle[ name + '2' ] = color
            circle[ name + '1' ] = [ color[ inds[2] ], color[ inds[3] ], color[ inds[4] ] ]
            ret = 2

    elif name in _cmy_str:
        circle[ name ] = color

    return ret

def _rotate_color(source, target, color):
    direction = {
        'RG' : "z",  'RB' : "iy",
        'GR' : "iz", 'GB' : "x",
        'BR' : "y",  'BG' : "ix",
        'CM' : "iz", 'CY' : "y",
        'MC' : "z",  'MY' : "ix",
        'YC' : "iy", 'YM' : "x"
    }[ source + target ]

    new = vector.rotate( color, direction, 90 )
    return vector.clean( new )

def _get_color(name, circle, val = 1):
    new = {
         'R' : [ _avg( circle['Y'][0], circle['M'][0] ),
                 min( circle['Y'][1], circle['M'][1] ),
                 min( circle['Y'][2], circle['M'][2] ) ],

         'G' : [ min( circle['Y'][0], circle['C'][0] ),
                 _avg( circle['Y'][1], circle['C'][1] ),
                 min( circle['Y'][2], circle['C'][2] ) ],

         'B' : [ min( circle['C'][0], circle['M'][0] ),
                 min( circle['C'][1], circle['M'][1] ),
                 _avg( circle['C'][2], circle['M'][2] ) ],

         'C' : [ _avg( circle['G' + str(val)][0], circle['B' + str(val)][0] ),
                 circle['G' + str(val)][1],
                 circle['B' + str(val)][2] ],

         'M' : [ circle['R' + str(val)][0],
                 _avg( circle['R' + str(val)][1], circle['B' + str(val)][1] ),
                 circle['B' + str(val)][2] ],

         'Y' : [ circle['R' + str(val)][0],
                 circle['G' + str(val)][1],
                 _avg( circle['R' + str(val)][2], circle['G' + str(val)][2] ) ]
    }[name]

    return new

class Color(rgb):
    def __init__(self, *pargs):
        self._identity = None
        self._circle = None

        lparg = len(pargs)
        if lparg == 1 and isinstance(pargs[0], rgb):
            # If it is already a rgb, we just save it
            super(Color, self).__init__(pargs[0])
        elif lparg == 1 and ( isinstance(pargs[0], hsl) or
                              isinstance(pargs[0], hsv) ):
            super(Color, self).__init__(pargs[0].rgb())
        else:
            super(Color, self).__init__(*pargs)

    ### SETTERS FOR CHAINING (NOT TATUM) ###
    def R(self, value):
        self.r = value
        return self

    def G(self, value):
        self.g = value
        return self

    def B(self, value):
        self.b = value
        return self

    ### TRANSFORMATIONS ###
    def tint(self, value, times=1):
        '''
        Tint is the mixture of a color with white, which increases lightness...

        from Wikipedia: https://en.wikipedia.org/wiki/Tints_and_shades
        '''
        _hsl = self.hsl(True)
        _result = []

        for i in range(times):
            _hsl += value
            _result.append( _hsl.rgb() )

        return _result[0] if len(_result) == 1 else _result

    def shade(self, value, times=1):
        '''
        shade is the mixture of a color with black, which reduces lightness

        from Wikipedia: https://en.wikipedia.org/wiki/Tints_and_shades
        '''
        _hsl = self.hsl(True)
        _result = []

        for i in range(times):
            _hsl -= value
            _result.append( _hsl.rgb() )

        return _result[0] if len(_result) == 1 else _result

    def saturate(self, value=10, times=1):
        # To increase saturation
        _hsv = self.hsv(True)
        _result = []

        for i in range(times):
            _hsv *= value
            _result.append( _hsv.rgb() )

        return _result[0] if len(_result) == 1 else _result

    def desaturate(self, value=10, times=1):
        # To decrease saturation
        _hsv = self.hsv(True)
        _result = []

        for i in range(times):
            _hsv /= value
            _result.append( _hsv.rgb() )

        return _result[0] if len(_result) == 1 else _result

    def spin(self, angle, times=2):
        # To change the hue of a color
        ''' Rotate the color using its hue '''
        _hsl = self.hsl(True)
        _result = []

        _result.append( self() )
        for i in range(times-1):
            _hsl **= angle
            _result.append( _hsl.rgb() )

        return _result[0] if len(_result) == 1 else _result

    def triad(self):
        # Calculate triad harmonic set
        return self.spin(120, 3)

    def tetrad(self, kind='S'):
        # Calculate tetrad harmonic set, either rectangular or squared
        if kind == 'S':
            return self.spin(90, 4)
        elif kind == 'R':
            _hsl = self.hsl(True)
            _result = []
            # Starting point
            _result.append( self() )
            # +60
            _hsl **= 60
            _result.append( _hsl.rgb() )
            # +120
            _hsl **= 120
            _result.append( _hsl.rgb() )
            # +60
            _hsl **= 60
            _result.append( _hsl.rgb() )
            return _result

    def complement(self):
        # Calculate the complementary color
        return self.spin(180,2)

    def split(self):
        # Calculate the split harmonic set
        _hsl = self.hsl(True)
        _result = []

        _result.append( self() )

        _hsl **= 150
        _result.append( _hsl.rgb() )

        _hsl **= 60
        _result.append( _hsl.rgb() )

        return _result

    def analogous(self):
        # Calculate the analogous colors
        _hsl = self.hsl(True)
        _result = []

        _hsl //= 60
        _result.append( _hsl.rgb() )
        for i in range(4):
            _hsl **= 30
            _result.append( _hsl.rgb() )

        return _result

    def blend(self):
        # Give a nice blend on hues of this color
        _hsl = self.hsl(True)
        _result = []

        _result.append( self() )
        for i in range(4):
            _hsl **= 15
            _result.append( _hsl.rgb() )

        return _result

    def circle(self, force=False):
        # To calculate the circle based on the vectorial space of RGB. 
        # TODO: Add reference to paper about this
        if self._circle is not None and not force:
            return self._circle

        base = ''
        # copy of the rgb
        rgb = self()
        # create a dict to contain all the colors in the circle
        circle = { k : [ 0 for i in range(3) ] for k in [ a + str(b) for b in (1,2) for a in _rgb_str ] + list(_cmy_str) }
        # normalize the rgb values from 0 - 255, to 0 - 1
        percents = [ i/255 for i in rgb ]

        # The first thing, is to verify, which type of color is this
        # get the index of the dominant color
        dominant = vector.max_index(rgb)

        # REDS
        if dominant == 0: # Meaning this color is primarily red
            # YELLOW
            # If the green component is within the range 10% of the red,
            # from the left is a yellow
            if _in_range( percents[1], percents[0]-0.1, percents[0] ):
                base = 'Y'
            # MAGENTA
            # If the blue component is within the range 10% of the red,
            # from the left is a magenta
            elif _in_range( percents[2], percents[0]-0.1, percents[0] ):
                base = 'M'
            # RED
            else:
                base = 'R'

        # GREENS
        elif dominant == 1: # Meaning this color is primarily green
            # YELLOW
            # If the red component is within the range 10% of the green,
            # from the left is a yellow
            if _in_range( percents[0], percents[1]-0.1, percents[1] ):
                base = 'Y'

            # CYAN
            # If the blue component is within the range 10% of the green,
            # from the left is a cyan
            elif _in_range( percents[2], percents[1]-0.1, percents[1] ):
                base = 'C'

            # GREEN
            else:
                base = 'G'

        # BLUES
        elif dominant == 2: # Meaning this color is primarily blue
            # MAGENTA
            # If th red component is within the range 10% of the blue,
            # from the left is a magenta
            if _in_range( percents[0], percents[2]-0.1, percents[2] ):
                base = 'M'

            # CYAN
            # If the green component is within the range 10% of the blue,
            # from the left is a cyan
            elif _in_range( percents[1], percents[2]-0.1, percents[2] ):
                base = 'C'

            else:
                base = 'B'

        self._identity = base

        if base in _rgb_str:
            if base == 'R':
                val = _add_color( 'R', circle, rgb )

                green = _rotate_color('R', 'G', rgb)
                _add_color( 'G', circle, green )

                blue = _rotate_color('R', 'B', rgb)
                _add_color( 'B', circle, blue )
            elif base == 'G':
                val = _add_color( 'G', circle, rgb )

                red = _rotate_color('G', 'R', rgb)
                _add_color( 'R', circle, red )

                blue = _rotate_color('G', 'B', rgb)
                _add_color( 'B', circle, blue )
            elif base =='B':
                val = _add_color( 'B', circle, rgb )

                green = _rotate_color('B', 'G', rgb)
                _add_color( 'G', circle, green )

                red = _rotate_color('B', 'R', rgb)
                _add_color( 'R', circle, red )

            self._identity += str(val)

            yellow = _get_color('Y', circle, val)
            _add_color( 'Y', circle, yellow )

            cyan = _get_color('C', circle, val)
            _add_color( 'C', circle, cyan )

            magenta = _get_color('M', circle, val)
            _add_color( 'M', circle, magenta )

        elif base in _cmy_str:
            if base == 'C':
                _add_color( 'C', circle, rgb )

                yellow = _rotate_color('C', 'Y', rgb)
                _add_color( 'Y', circle, yellow )

                magenta = _rotate_color('C', 'M', rgb)
                _add_color( 'M', circle, magenta )
            elif base == 'Y':
                _add_color( 'Y', circle, rgb )

                cyan = _rotate_color('Y', 'C', rgb)
                _add_color( 'C', circle, cyan )

                magenta = _rotate_color('Y', 'M', rgb)
                _add_color( 'M', circle, magenta )
            elif base == 'M':
                _add_color( 'M', circle, rgb )

                cyan = _rotate_color('M', 'C', rgb)
                _add_color( 'C', circle, cyan )

                yellow = _rotate_color('M', 'Y', rgb)
                _add_color( 'Y', circle, yellow )

            red = _get_color('R', circle)
            _add_color( 'R', circle, red )

            green = _get_color('G', circle)
            _add_color( 'G', circle, green )

            blue = _get_color('B', circle)
            _add_color( 'B', circle, blue )

        result = []
        result.append(circle['R1'])
        result.append(circle['Y'])
        result.append(circle['G1'])
        if circle['G1'] != circle['G2']:
            result.append(circle['G2'])
        result.append(circle['C'])
        result.append(circle['B2'])
        if circle['B1'] != circle['B2']:
            result.append(circle['B1'])
        result.append(circle['M'])
        if circle['R1'] != circle['R2']:
            result.append(circle['R2'])

        self._circle = result
        return result

    def identify(self):
        # To know or calculate the identity of the color, [TODO: reference to paper]
        if self._identity is None:
            self._circle = self.circle(True)

        return self._identity

    def xml(self=None, name="self", *pargs, **kwargs):
        ''' Intention is to transform an input array into a nice XML
        To consider, all values will be taken as if RGB and are processed as such '''
        if self is None:
            array = name
            output = ""
        else:
            array = {
                'self' : self,
                'tint' : self.tint,
                'shade' : self.shade,
                'saturate' : self.saturate,
                'desaturate' : self.desaturate,
                'spin' : self.spin,
                'triad' : self.triad,
                'tetrad' : self.tetrad,
                'blend' : self.blend,
                'circle' : self.circle,
                'complement' : self.complement,
                'split' : self.split,
                'analogous' : self.analogous
            # }[name](*pargs, **kwargs)
            }[name](*pargs)

            if 'detailed' in kwargs and kwargs['detailed']:
                output = _xml_palette_header.format(name=name.capitalize())
            else:
                output = _xml_swatch_header.format(name=name.capitalize())

        # Check if we have a list of lists
        if type(array[0]) is list or type(array[0]) is str:
        #if len(array) > 3: # we have more than 3 elements to create a color
            for e in array:
                color = rgb(e)
                output += _xml_color.format( value = color.__str__()[1:-1],
                                             hex=color.hexs(),
                                             hsl=str(color.hsl())[1:-1],
                                             hsv=str(color.hsv())[1:-1],
                                             cmyk = str(color.cmyk())[1:-1],
                                             xyz = str(color.xyz())[1:-1]
                                         )
        else:
            color = rgb(array)
            output += _xml_color.format( value = color.__str__()[1:-1],
                                         hex=color.hexs(),
                                         hsl=str(color.hsl())[1:-1],
                                         hsv=str(color.hsv())[1:-1],
                                         cmyk = str(color.cmyk())[1:-1],
                                         xyz = str(color.xyz())[1:-1]
                                     )

        if self is not None:
            # if detailed:
            if 'detailed' in kwargs and kwargs['detailed']:
                output += _xml_palette_trailer
            else:
                output += _xml_swatch_trailer
            # output += _xml_swatch_trailer

        return output

