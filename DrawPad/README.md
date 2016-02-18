# Draw Pad

Have you played [Nitrome's Magic Touch](http://www.nitrome.com/games/magictouch/)? 

While playing the game I started thinking how to program something like that after doing [some analysis](https://viclab.wordpress.com/2015/12/29/input-normalization-for-pattern-recognition/) I gathered some ideas about the neccessary processing to the input in order to normalize it for a neural network.

This component is the result of coding some of those ideas.

### Contents
1. **drawpad.py**, gui application result of the [analysis](https://viclab.wordpress.com/2015/12/29/input-normalization-for-pattern-recognition/)

### Graphic Application
For the graphic version, I'm using the [Kivy library](https://kivy.org/ "Kivy") for Python, with some tweaks to work with version 3.4, so meaning that it is required to execute the code.

The *draw.py* module contains the following top-level widgets and components:
* *DrawPad (App)*, main Kivy application
* *Pad (Widget)*, this represents the widget in which the user can draw a line
* *Scaled (Widget)*, this one shows the scaled input to a smaller square matrix, regardless the original shape of the drawing

To execute, start kivy in a console:

    $ kivy

Once environment is set, start the application with:

    $ python drawpad.py

This will bring up the app, you can draw on the left panel, when the click is raised the app will do the processing and will show the results on the right panel:

![Drawpad - Screen 1](https://raw.githubusercontent.com/vinceynhz/python_code/master/DrawPad/img/screen1.png)

![Drawpad - Screen 2](https://raw.githubusercontent.com/vinceynhz/python_code/master/DrawPad/img/screen2.png)