# ID3 Tags

### Contents
1. **id3tags.py**: module to show tag information of an mp3 file
2. **sample.mp3**: exactly that, a sample mp3: Polka in G - Henry Reed (1999)

### About...
For a while now I have had knowledge of the tagging system in mp3, with the boom of personal music players and mp3 being the most common format for that, the tagging system became really useful. This code was for me to learn the binary composition of the tagging system and to keep a good practice regarding protocol parsing from raw data. 

### The *id3tags.py* module
This module is the one that decodes and prints out the information in the ID3 tags. It contains the following methods:

* *_print_tag_info*: to parse the header information and each one of the frames in the file
* *_remove_tag_info*: to precisesly that, remove the ID3 tag header and all of the frames from the file
* *_decode_synch_safe*: ID3 has a particular way to encode integer values to avoid problems with little endian, big endian, these module follows the definition of the algorithm to decode an synchsafe integer value.
* *_proc_opts*: to process command line options
* *_help*: to print usage information and command line options

It additionally contains a couple of dictionaries with the possible frame IDs defined by ID3 and the possible types of covers a file can have.

To execute, froma command line:

    $ python id3tags.py sample.mp3 -i

This will print the header and frame information in sample.mp3 file
