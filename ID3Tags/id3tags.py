import os
import sys
import glob

# to make available all the other code
# the route has to be modified for environment's code

sys.path.append('$CODE_DIR\\_lib')
# sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from shared.misc import _print_data

#From id3.org/id3v2.4.0-frames#line-269
frame_ids = {
  'AENC' : "Audio encryption",
  'APIC' : "Attached picture",
  'ASPI' : "Audio seek point index",
  'COMM' : "Comments",
  'COMR' : "Commercial frame",
  'ENCR' : "Encryption method registration",
  'EQU2' : "Equalisation (2)",
  'ETCO' : "Event timing codes",
  'GEOB' : "General encapsulated object",
  'GRID' : "Group identification registration",
  'LINK' : "Linked information",
  'MCDI' : "Music CD identifier",
  'MLLT' : "MPEG location lookup table",
  'OWNE' : "Ownership frame",
  'PRIV' : "Private frame",
  'PCNT' : "Play counter",
  'POPM' : "Popularimeter",
  'POSS' : "Position synchronisation frame",
  'RBUF' : "Recommended buffer size",
  'RVA2' : "Relative volume adjustment (2)",
  'RVRB' : "Reverb",
  'SEEK' : "Seek frame",
  'SIGN' : "Signature frame",
  'SYLT' : "Synchronised lyric/text",
  'SYTC' : "Synchronised tempo codes",
  'TALB' : "Album/Movie/Show title",
  'TBPM' : "BPM (beats per minute)",
  'TCOM' : "Composer",
  'TCON' : "Content type",
  'TCOP' : "Copyright message",
  'TDEN' : "Encoding time",
  'TDLY' : "Playlist delay",
  'TDOR' : "Original release time",
  'TDRC' : "Recording time",
  'TDRL' : "Release time",
  'TDTG' : "Tagging time",
  'TENC' : "Encoded by",
  'TEXT' : "Lyricist/Text writer",
  'TFLT' : "File type",
  'TIPL' : "Involved people list",
  'TIT1' : "Content group description",
  'TIT2' : "Title/songname/content description",
  'TIT3' : "Subtitle/Description refinement",
  'TKEY' : "Initial key",
  'TLAN' : "Language(s)",
  'TLEN' : "Length",
  'TMCL' : "Musician credits list",
  'TMED' : "Media type",
  'TMOO' : "Mood",
  'TOAL' : "Original album/movie/show title",
  'TOFN' : "Original filename",
  'TOLY' : "Original lyricist(s)/text writer(s)",
  'TOPE' : "Original artist(s)/performer(s)",
  'TOWN' : "File owner/licensee",
  'TPE1' : "Lead performer(s)/Soloist(s)",
  'TPE2' : "Band/orchestra/accompaniment",
  'TPE3' : "Conductor/performer refinement",
  'TPE4' : "Interpreted, remixed, or otherwise modified by",
  'TPOS' : "Part of a set",
  'TPRO' : "Produced notice",
  'TPUB' : "Publisher",
  'TRCK' : "Track number/Position in set",
  'TRSN' : "Internet radio station name",
  'TRSO' : "Internet radio station owner",
  'TSOA' : "Album sort order",
  'TSOP' : "Performer sort order",
  'TSOT' : "Title sort order",
  'TSRC' : "ISRC (international standard recording code)",
  'TSSE' : "Software/Hardware and settings used for encoding",
  'TSST' : "Set subtitle",
  'TXXX' : "User defined text information frame",
  'TYER' : "Year",
  'UFID' : "Unique file identifier",
  'USER' : "Terms of use",
  'USLT' : "Unsynchronised lyric/text transcription",
  'WCOM' : "Commercial information",
  'WCOP' : "Copyright/Legal information",
  'WOAF' : "Official audio file webpage",
  'WOAR' : "Official artist/performer webpage",
  'WOAS' : "Official audio source webpage",
  'WORS' : "Official Internet radio station homepage",
  'WPAY' : "Payment",
  'WPUB' : "Publishers official webpage",
  'WXXX' : "User defined URL link frame"
}

picture_type = {
    0 : "Other",
    1 : "32x32 pixels 'file icon'",
    2 : "Other file icon",
    3 : "Cover (front)",
    4 : "Cover (back)",
    5 : "Leaflet page",
    6 : "Media (e.g. lable side of CD)",
    7 : "Lead artist/lead performer/soloist",
    8 : "Artist/performer",
    9 : "Conductor",
    10 : "Band/Orchestra",
    11 : "Composer",
    12 : "Lyricist/text writer",
    13 : "Recording Location",
    14 : "During recording",
    15 : "During performance",
    16 : "Movie/video screen capture",
    17 : "A bright coloured fish",
    18 : "Illustration",
    19 : "Band/artist logotype",
    20 : "Publisher/Studio logotype"
}

def _decode_synch_safe(data):
    '''From ID3 definition: http://id3.org/id3v2.4.0-structure#line-610
    Synchsafe integers are integers that keep its highest bit (bit 7) zeroed,
    making seven bits out of eight available. Thus a 32 bit synchsafe integer
    can store 28 bits of information.

    Example:
     255 (%11111111) encoded as a 16 bit synchsafe integer is 383
     (%00000001 01111111).'''

    # First, let's clean the empty bits
    cleaned = bytearray(data)
    # _print_data(cleaned)

    for i in range( len(data)-1, 0, -1 ):    
        cleaned[i] |= ( data[i-1] & 0x01 ) << 7

        for j in range(i-1, -1, -1):
            if j>0:
                cleaned[j] |= ( data[j-1] & 0x01 ) << 7
            cleaned[j] >>= 1

    # _print_data(cleaned)

    return cleaned

def _print_tag_info(curfile):
    '''From ID3 specs: http://id3.org/id3v2.4.0-structure#line-100
     +-----------------------------+
     |      Header (10 bytes)      |
     +-----------------------------+
     |       Extended Header       |
     | (variable length, OPTIONAL) |
     +-----------------------------+
     |   Frames (variable length)  |
     +-----------------------------+
     |           Padding           |
     | (variable length, OPTIONAL) |
     +-----------------------------+
     | Footer (10 bytes, OPTIONAL) |
     +-----------------------------+'''
    curfile.seek(0)

    header = curfile.read(10)
    version = "{ID3}v2 {M}.{m}".format( ID3=header[0:3].decode("latin_1"), M=header[3], m=header[4] )
    flags = header[5]
    tagsize = int.from_bytes( _decode_synch_safe( header[6:10] ), byteorder='big')

    print("\n+--- File info\n")
    print("Name:".rjust(10), curfile.name)
    print("Version:".rjust(10), version )
    print("Flags:".rjust(10))
    print("\t- Unsynchronization:", flags&0x80)
    print("\t- Extended:", flags&0x40)
    print("\t- Experimental:", flags&0x20)
    print("Tag size:".rjust(10), tagsize, "\n")

    # If we have an extended header
    if flags&0x40 > 0:
        # not for now ;)
        pass
    
    # Parse the frames
    # While we are in the space of the tagsize
    print("+--- Frames\n")
    
    while curfile.tell() <= tagsize:
        fheader = curfile.read(10)

        # _print_data(fheader)
        
        # This is where the padding starts
        if sum(fheader) == 0: break
        
        fid = "{id}".format(id = fheader[0:4].decode("utf-8") )
        
        # header[3] has the ID3v2 major version used
        # in version 3, the frame size is not synch safe
        if header[3] == 3:
            fsize = int.from_bytes( fheader[4:8],  byteorder='big')
        # in version 4, the frame size is synch safe
        elif header[3] == 4:
            fsize = int.from_bytes( _decode_synch_safe( fheader[4:8] ),  byteorder='big')

        fflags = fheader[8:10]
        fdata = curfile.read(fsize)

        # There are different type of encodings in ID3, indicated in the first 
        # byte of the data: http://id3.org/id3v2.4.0-structure#line-363
        # From python docs: 
        # https://docs.python.org/3/library/codecs.html#standard-encodings

        if fdata[0] >= 0 and fdata[0] <= 3:
            fencoding = {
                # iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1
                0: "latin_1", 
                # U16, utf16
                1: "utf_16",
                # UTF-16BE
                2: "utf_16_be",
                # U8, UTF, utf8
                3: "utf_8"
            }[ fdata[0] ]
        else:
            fencoding = False

        print("Frame:".rjust(10), frame_ids[fid] )
        print("Size:".rjust(10), fsize )
        print("Flags:".rjust(10))

        # Exceptions...
        if fid == 'APIC':
            eomimetype = fdata[1:].index(b'\x00')+1
            
            fmimetype = fdata[1:eomimetype+1].decode("utf-8")
            fpicttype = picture_type[ fdata[eomimetype+1] ]

            fparseddata = "\n"
            fparseddata += "\t - MIME Type: " + fmimetype + "\n"
            fparseddata += "\t - Picture Type: " + fpicttype
        else:
            if fencoding is not False:
                fparseddata = fdata[1:].decode(fencoding)
            else:
                fparseddata = fdata[:fdata.index(b'\x00')].decode("utf-8")
        
        print("Data:".rjust(10), fparseddata, "\n")

def _remove_tag_info(curfile):
    curfile.seek(0)

    header = curfile.read(10)
    tagsize = int.from_bytes( _decode_synch_safe( header[6:10] ), byteorder='big')

    curfile.seek(tagsize, 1)
    data = curfile.read()

    os.write(sys.stdout.fileno(), data)

def _help(argv):
    output = "\nUsage: python {name} file(s) [-i|-d|-r|-h]\n".format(name = argv[0])
    output += "Options:\n"
    output += "\t-i     print tag information of given file(s)\n"
    output += "\t-d     print raw binary data of the given file(s)\n"
    output += "\t-r     remove tag information from given file(s)\n"
    output += "\t-h     print this help"

    print(output)

def _proc_opts(argv):
    result = {'files' : [], 'info' : False, "data": False, 'remove' : False, 'help': False}

    for ind in range(len(argv)):
        # if the shell is not solving the wildcard
        # we will have to handle it here
        if "*." in argv[ind]:
            result['files'] += glob.glob(argv[ind])
        
        # if we have a mp3 single file
        elif "." in argv[ind]:
            result['files'].append( argv[ind] )

        elif "-i" == argv[ind]:
            result['info'] = True

        elif "-d" == argv[ind]:
            result['data'] = True

        elif "-r" == argv[ind]:
            result['remove'] = True

        elif "-h" == argv[ind]:
            result['help'] = True

    return result

if __name__ == '__main__':
    opts = _proc_opts(sys.argv[1:])

    if opts['help']:
        _help(sys.argv)
        sys.exit(0)

    for item in opts['files']:
        with open(item,'rb') as curfile:
            if opts['data']:
                _print_data(curfile.read())
            elif opts['info']:
                _print_tag_info(curfile)
            elif opts['remove']:
                _remove_tag_info(curfile)