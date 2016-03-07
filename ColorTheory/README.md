# Color Theory

### Contents
1. **color.py**: command line functionality to parse json files and create xml output of color and palette analysis
2. **colorpicker.py**: graphical interface for a color picker based on hsv
3. **ColourMatching.py**: graphical plots for the CIE color matching functions RGB and XYZ
4. **data**
  1. **top.json**: JSON file that contains the top 10 palettes from [ColourLovers](http://www.colourlovers.com/palettes/most-loved/all-time/meta)
5. **output**
  1. **0xFF0000.xml**: simple XML view of all the possible transformations of color 0xFF0000
  2. **0xFE6543.xml**: simple XML view of all the possible transformations of color 0xFE6543 
  3. **GiantGoldfish.xml**: detailed XML view for the palette namde GiantGoldFish from the JSON file in data
  4. **Top.xml**: simple XML view of all the palettes in JSON file in data
  5. **web**
    1. **layout.xslt**: to transform a XML file created with color.py into an HTML version of it for visualization
    2. **detailed_layout.xslt**: to transform an XML file created with color.py into an HTML version of it for visualization
    3. **css**
      1. **theme.css**: theme used in the HTML result of the XSL transformation
    4. **js**
      1. **bootstrap.min.js**: bootstrap visual library, used for tooltip creation in detailed views
      2. **maps.js**: javascript that parses the HTML info and draws into canvases the marks over an HSV and Chromaticity maps

### Color Transformations
The contents in this module correspond to my studies and analysis on Color Theory and the initial step into the analysis of Color Harmony. On the color transformations, these code contains the implementation of my analysis on the color wheel and the basic functions of color harmony. For the details on the calculation of the color circle, I'm working on a paper, pending to add reference.

### Command line *color.py*
This module serves as a command for the console to perform operations on json data containing palettes and colors or passing colors as well and create transformations from them.

To use, simply type on a command line console:

    $ python color.py -h

This will show the help with all the possible options and combinations. 

**Details of a single color**
To get the possible representations of a single color, type in:

    $ python color.py -c **rrr**,**ggg**,**bbb**

Where rrr is the red component, ggg is the green component, and bbb is the blue component of the color; these three parameters take values from 0 to 255. This will show the XML swatch of a single color and the hex, hsl, hsv, cmyk and xyz chromaticity representations:

    $ python color.py -c 192,168,227

    <Swatch name="Self">
    <Color value="192, 168, 227" hex="0xc0a8e3" hsl="264, 51, 77" hsv="264, 26, 89" cmyk="15, 26, 0, 11" xyz="0.286638, 0.25
    8624, 0.454738" />
    </Swatch>

Alternative options to pass a color exist including hexadecimal, use -h to see them.

**Apply transformation to a color**
To apply one of the possible transformations, type in:

    $ python color.py -c **rrr**,**ggg**,**bbb** -o **operation**

The operation name may allow two parameters, value and times; the value is used in transformations that require an amount or variation for its calculation while times indicate how many times the operation will be applied to the color

**Get data from a json file**
To use a json file as a source

    $ python color.py -s **source_file**

This will open the file and get the xml representation of its contents, either a multiple palette or a single one. There is an example of a json file under the data folder

### XML Output of *color.py*
The results of the execution of color.py command, can be saved to XML files under the *output* folder, this will allow a web browser to use the XSLT under *web* folder to convert the data in the XML into a web application for analysis.

There are some examples provided in the output folder. The 0xFF0000.xml file is an analysis of the color red, GiantGoldfish is a color palette taken from ColourLovers and so on.

Depending on the execution of the command, the XMLs can call for a *simple layout* ot a *detailed layout*.

**Simple Layout**
This will take each swatch or palette and will display each color, it's multiple representations and will create a HSV map indicating the position of each color, along with the CIE xy chromaticity diagram of all the colors in the palette; an XML using the simple layout can contain any number of palettes or swatches:

![XML Output - Simple Layout](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/screen5.png)

**Detailed Layout**
An XML using the detailed layout contains a single parent palette and a detailed view of the color circle and harmony formulas for each color in it. 

When loaded, the palette will be shown on the top-left side of the screen and the HSV and Chromaticity diagrams under it. 

The right side of the screen will show the harmonic formulas for a selected color. Click on any color on the main palette to see the harmonic combinations of that particular color. By hovering the mouse on any color on the detailed view, a tooltip will show displaying the RGB, HSV, HSL and HEX values of it.

![XML Output - Detailed Layout](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/screen6.png)

The detailed view uses bootstrap and jquery to show the tooltip. The rest of CSS and JS files I developed specifically for these displays.

### Graphic Color Picker *colorpicker.py*
For the graphic application, I'm using the [Kivy library](https://kivy.org/ "Kivy") for Python, with some tweaks to work with version 3.4, so meaning that it is required to execute the code.

When executed, this module shows a color picker widget or color selector in the HSV space.

The colorpicker module contains the following top level widgets:
* *_mark (Widget)*: represents a visible mark in the screen
* *_colormap (Widget)*: generic class that shows a map in which marks can be drawn and dragged around

Additionally, it contains the following classes:
* *ColorMixer (StackLayout)*: which composes two maps, one for the hue-saturation selection and one for the hue-value selection. It contains also the methods in charge of linking the behaviour between marks on the two maps, and mouse coordinate conversion to HSV values.
* *MainApp (App)*: the actual kivy application

To execute, start kivy in a console:

    $ kivy

Once environment is set, start the application with:

    $ python colorpicker.py

This will bring up the Color Picker widget:
 
![ColorPicker - main app](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/screen1.png)

From there you can add marks by clicking on any of the two maps. When a mark is created on one map, automatiacally one is aded to the other map. For instance, if a mark is added to the hue-saturation space, automatically one will be added to the hue-value space with the same hue and value set to 100 by default.

![ColorPicker - adding marks](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/screen2.png)

Marks existing on the screen can be clicked and dragged around, which will automatically move the corresponding mark on the other map. 

![ColorPicker - dragging marks](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/screen3.gif)

Finally, when a mark is moved or created, it's corresponding HSV value is printed out to the console:

![ColorPicker - HSV value](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/screen4.gif)

### Color Matching Functions *ColourMatching.py*
This module uses [VPython](http://vpython.org/) to create the plots. The information used to create the plots was published by the [CIE](http://www.cie.co.at/) (Commission International d l'Eclairage) on the *CIE 15: Technical Report: Colorimetry, 3rd edition*

This module plots out the CIE RGB and XYZ colour matching functions using the data provided by the CIE in the Colorimetry technical documentation. I used this module to create the graphics for the paper on RGB transformations I am working on.

The module contains two methods:
* *rgb_colormatching()*
* *XYZ_colormatching()*

It can be executed from console as:

    $ python -i ColourMatching.py

Once the python interpreter has loaded the module, the plots can be created by calling the functions as follows:

    >>> rgb_colormatching()
    >>> XYZ_colormatching()