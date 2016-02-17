# Cellular Automata

### Contents
1. **automaton.py**: Conway's game of life rules
2. **life.py**: Graphic Interface for the conway's game of life

### Some background
Long time ago in a galaxy far, far away, while having a conversation with my Software Engineering teacher, he mention about Conway's Game of Life, he explained the rules of it.

I never gave it a deeper thought but I kept wondering about its nature, its history and pretty much what is it about it that makes it relevant?

Until now that I studied some of the math involved in a cellular automata and readed some of the history behind it by Von Neuman, the implementation resulted really fun.

### *automaton.py* module
This module contains methods with Conway's Game of Life rules, to calculate births and deaths from generation to generation. 

I am using some sort of sparse array idea (a Python list, with lists nested inside for the coordinates) to analyze which coordinates can live, which ones are added and which ones will be deleted.

The following methods are defined:
* *survivors*, this one gets the count of immediate neighbours to a given cell (considered as the center) and if the number of them is 2 or 3 the cell is added to the "output" 
* *births*, this one is tricky since it considers the extended neighborhood and possible combinations of them.
* *addnodup*, union operation for groups and sets
* *count_neighbourhoods*, it calculates the number of valid neighbours in the extended neighbourhoods by exploiting comprehensions and a list of predefined coeficients to add or subtract to the coordinates
* *newborns*, if for a given cell, there are 2 neighbors surrounding, then a new cell is added

### *life.py* module
For the graphic version, I'm using the [Kivy library](https://kivy.org/ "Kivy") for Python, with some tweaks to work with version 3.4, so meaning that it is required to execute the code.

This is the graphical interface for the Game of Life, it allows to create patterns by clicking on the canvas, you can resize it and go generation by generation or let it evolve automatically using the controls at the bottom

![Cellular Automata - Conway's Game of Life](https://raw.githubusercontent.com/vinceynhz/python_code/master/CellularAutomata/img/screenshot2.png)


