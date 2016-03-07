import sys
import getopt
import json

# to make available all the other code
# the route has to be modified for environment's code

sys.path.append('$CODE_DIR\\_lib')
# sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from colors.colorlib import Color

_xml_signature = '<?xml version="1.0" encoding="UTF-8"?>\n'
_xml_simple_style = '<?xml-stylesheet type="text/xsl" href="web/layout.xslt"?>\n'
_xml_detailed_style = '<?xml-stylesheet type="text/xsl" href="web/detailed_layout.xslt"?>\n'

_xml_header = '<ColorPalette name="{name}" url="{url}">\n'
_xml_header_nourl = '<ColorPalette name="{name}">\n'
_xml_palette_header = '<Palette name="{name}" url="{url}">\n'
_xml_palette_trailer = '</Palette>\n'

_xml_swatches_header = '<Swatches id="{id}">\n'
_xml_swatches_trailer = '</Swatches>\n'

_xml_trailer = '</ColorPalette>\n'

class swatches():
    ''' Class to create color swatches from json data '''
    def __init__(self, data = None):
        self._url = None
        self._data = data
        self._next = 0

    def parse(self, url):
        ''' take a json file and parse it into a dictionary

        The data can be a simple palette (with multiple colors), or a set
        of palettes '''
        self._url = url
        with open( self._url ) as _file:
            self._data = json.load(_file)

        if self._data is None:
            raise Exception("Error reading " + self._url)

        self._next = 0

    def reload(self):
        ''' reload the file from disk '''
        if self._url is None: return

        with open( self._url ) as _file:
            self._data = json.load(_file)

        if self._data is None:
            raise Exception("Error reading " + self._url)

        self._next = 0

    def get(self, index=None):
        ''' retrieve a color or palette by index '''
        result = None
        # if this is a simple palette
        if 'colors' in self._data:
            if index is None:
                result = self._data['colors']
            else:
                result = self._data['colors'][index % len(self._data['colors'])]

        # if this is a compound palette
        elif 'palettes' in self._data:
            if index is not None:
                result = swatches( self._data['palettes'][index] )

        return result

    def next(self):
        ''' to iterate through the data '''
        result = None
        # If this is a simple palette
        if 'colors' in self._data:
            result = self._data['colors'][self._next]
            self._next = (self._next + 1) % len(self._data['colors'])
        # If this is a compound palette
        elif 'palettes' in self._data:
            result = swatches( self._data['palettes'][self._next] )
            self._next = (self._next + 1) % len(self._data['palettes'])

        return result

    def rewind(self):
        ''' restart the iterator '''
        self._next = 0

    def count(self):
        ''' get the number of palettes or the number of colors 
        if a single palette '''
        result = None
        # If this is a simple palette
        if 'colors' in self._data:
            result = len(self._data['colors'])

        # If this is a compound palette
        elif 'palettes' in self._data:
            result = len(self._data['palettes'])

        return result

    def name(self):
        ''' get the name of the palette (if any) '''
        if 'name' in self._data:
            return self._data['name']
        return None

    def url(self):
        ''' get the url of the palette (if any) '''
        if 'url' in self._data:
            return self._data['url']
        return None

    def ismultiple(self):
        ''' to verify if this swatch has multiple palettes or not '''
        return 'palettes' in self._data

    def xml(self):
        ''' to create an xml file with each palette shown '''
        output = _xml_signature
        output += _xml_simple_style
        output += _xml_header.format( name=self.name(), url=self.url() )

        if 'colors' in self._data:
            output += _xml_palette_header.format( name=self.name(), url=self.url() )
            output += Color.xml( None, self.get() )
            output += _xml_palette_trailer

        elif 'palettes' in self._data:
            for i in range(self.count()):
                tmp = self.get(i)
                output += _xml_palette_header.format( name=tmp.name(), url=tmp.url() )
                output += Color.xml( None, tmp.get() )
                output += _xml_palette_trailer

        output += _xml_trailer
        return output

    def detail_xml(self):
        ''' to create a detailed xml based on a single palette, creating an
        analysis of each color '''

        if 'palettes' in self._data: return None

        output = _xml_signature
        output += _xml_detailed_style

        output += _xml_header.format( name=self.name(), url=self.url() )

        # First the palette itself:
        output += _xml_palette_header.format( name=self.name(), url=self.url() )
        output += Color.xml( None, self.get() )
        output += _xml_palette_trailer

        # Then for each color
        for i in range(self.count()):
            col = Color( self.get(i) )
            output += _xml_swatches_header.format( id = col.hexs() )
            output += col.xml('circle')
            output += col.xml('complement')
            output += col.xml('split')
            output += col.xml('triad')
            output += col.xml('tetrad')
            output += col.xml('blend')
            output += col.xml('tint', 10, 5)
            output += col.xml('shade', 10, 5)
            output += col.xml('saturate', 10, 5)
            output += col.xml('desaturate', 10, 5)
            output += _xml_swatches_trailer

        output += _xml_trailer

        return output

def _help( exit = 0 ):
    print("\n Usage:")
    print("\tcolor.py -h")
    print("\tcolor.py -s <source_file> [-n <palette_num> -d]")
    print("\tcolor.py -c <color> -o <operation> [args]")
    print("\n Options:")
    print("\t-h               : Print this help")
    print("\t-s <source_file> : JSON file to parse")
    print("\t-n <palette_num> : [optional] Number of palette from the input file to analyze.")
    print("\t-d               : [optional] Along with -n will print the detailed view in XML.")
    print("\t-c <color>       : color in any of these forms:")
    print("\t                    - r,g,b | \"r, g, b\"")
    print("\t                   where r,g & b are between 0 and 255")
    print("\t                    - 0xRRGGBB | #RRGGBB ")
    print("\t                   where R,G & B are hex values between 0x00 and 0xFF")
    print("\t-o <operation>   : operation to perform to the given color.")
    print("\t                   It can be any of the following: ")
    print("\t                    - tint -v value [-t times]")
    print("\t                    - shade -v value [-t times]")
    print("\t                    - saturate [-v value] [-t times]")
    print("\t                    - desaturate [-v value] [-t times]")
    print("\t                    - spin -v angle [-t times]")
    print("\t                    - triad")
    print("\t                    - tetrad [-v S|R] ")
    print("\t                    - blend")
    print("\t                    - circle")
    print("\t                    - complement")
    print("\t                    - split")
    print("\t                    - analogous")

    sys.exit( exit )

def _main(argv):
    sourcefile = None
    palettenum = None
    color = None
    operation = None
    value = None
    times = None
    detailed = False

    # if no arguments given, print help
    if len(argv) == 0:
        _help(2)

    try:
        # parse the parameters
        opts, args = getopt.getopt(argv, "hs:n:c:o:v:t:d")
    except getopt.GetoptError as e:
        print(e)
        _help(2)

    for opt, val in opts:
        if opt == "-h":
            _help()

        elif opt in "-s":
            sourcefile = val

        elif opt == "-n":
            palettenum = int(val)

        elif opt == "-c":
            color = val

        elif opt == "-o":
            operation = val

        elif opt == "-v":
            # tetrad is the only one that accept a character as value
            if operation is not None and operation == "tetrad":
                value = val
            elif '.' in val:
                value = float(val)
            else:
                value = int(val)

        elif opt == "-t":
            times = int(val)

        elif opt == "-d":
            detailed = True

    # if source file is indicated
    if sourcefile is not None and sourcefile != "":
        # get and parse the data
        data = swatches()
        data.parse( sourcefile )
        output = None

        # if palette num given and is positive number
        if palettenum is not None and palettenum >= 0:
            # create detail view for the palette
            if detailed:
                output = data.get(palettenum).detail_xml()
            # create simple view for the palette
            else:
                output = data.get(palettenum).xml()
        else:
            output = data.xml()

        print(output[:-1])

    # if a single color was given
    elif color is not None:
        c = Color(color)
        output = None
        # in the case of a detail, create each transformation as a palette in
        # a simple view
        if detailed:
            output = _xml_signature
            output += _xml_simple_style
            output += _xml_header_nourl.format(name='Combinations of ' + c.hexs())
            output += c.xml('circle', detailed=True)
            output += c.xml('complement', detailed=True)
            output += c.xml('split', detailed=True)
            output += c.xml('triad', detailed=True)
            output += c.xml('tetrad', detailed=True)
            output += c.xml('blend', detailed=True)
            output += c.xml('tint', 10, 5, detailed=True)
            output += c.xml('shade', 10, 5, detailed=True)
            output += c.xml('saturate', 10, 5, detailed=True)
            output += c.xml('desaturate', 10, 5, detailed=True)
            output += _xml_trailer
        # if an operation was given
        elif operation is not None:
            if value is not None and times is not None:
                output = c.xml(operation, value, times)
            elif value is not None:
                output = c.xml(operation, value)
            elif times is not None:
                output = c.xml(operation, times=times)
            else:
                output = c.xml(operation)
        else:
            output = c.xml()
        
        print(output[:-1])
    else:
        _help(1)

    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        _main( sys.argv[1:] )