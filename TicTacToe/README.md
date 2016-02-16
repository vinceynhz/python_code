# Tic Tac Toe

### Contents
1. **tic.py**: core functionality and cli version of the game
2. **tac.py**: helper classes and methods for the graphic version
3. **toe.py**: main code for the graphic tic tac toe

### Command line version *tic.py*
The *tic.py* module contains three classes: *Board*, *Player* and *Game*. This classes are wired to the graphical interface but they provide standalone functionality to have a game based in the python interpreter.

To start a game just import the library to the interpreter:
    
    $ python -i tic.py

And create a new instance of the Game class:

    >>> game = Game()

This will setup some defaults, for instance Player 1 (which is the user) will be set to play o's while Player 2 (which is the computer) is x's. 

About the board, the tic tac toe board is divided and numbered as follows:

     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8

So to play, you just have to call the *next()* method from the Game class passing the position you want to play:

    >>> game.next(3)

And to show the board, you can print it out directly:

    >>> print(game.board)

The *Player* class allows two types of players: 
* **Human**: the game will expect a position to be played
* **Computer**: the game will calculate the next position regardless a position

#### Search algorithm
Although initially I wanted to create a tree search strategy and implement alpha-beta pruning for this (which I have done before for a simplified version of chess), after doing some initial [analysis](https://viclab.wordpress.com/2015/10/30/programming-a-tic-tac-toe-part-1-analysis/) I ended up doing just a [weighed calculation](https://viclab.wordpress.com/2015/11/02/programming-a-tic-tac-toe-part-2-coding/) of the possible positions of the whole board.

### Graphic version *tac.py*
For the graphic version, I'm using the [Kivy library](https://kivy.org/ "Kivy") for Python, with some tweaks to work with version 3.4