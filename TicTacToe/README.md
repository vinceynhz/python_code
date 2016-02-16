# Tic Tac Toe

### Contents
1. **tic.py**: core functionality and cli version of the game
2. **tac.py**: helper classes and methods for the graphic version
3. **toe.py**: main code for the graphic tic tac toe

#### Search algorithm
Although initially I wanted to create a tree search strategy and implement alpha-beta pruning for this (which I have done before for a simplified version of chess), after doing some initial [analysis](https://viclab.wordpress.com/2015/10/30/programming-a-tic-tac-toe-part-1-analysis/) I ended up doing just a [weighed calculation](https://viclab.wordpress.com/2015/11/02/programming-a-tic-tac-toe-part-2-coding/) of the possible positions of the whole board.

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

### Graphic version *tac.py*
For the graphic version, I'm using the [Kivy library](https://kivy.org/ "Kivy") for Python, with some tweaks to work with version 3.4, so meaning that it is required to execute the code.

The *tac.py* module contains the following top level widgets:
* *Menu (Screen)*: to configure the players, names and type of a new game
* *GameBoard (Scren)*: the actual tic tac toe game board
* *ListCheckBox (CheckBox)*: extension to add an index attribute
And the following low level widgets according to where they are used:
**Menu Screen**
* *_player_figure_selection_box*: to select which figure the user will play
* *_player_name_box*: to type in user names
* *_player_type_box*: to indicate if a user will be human or computer controlled

**Board Screen**
* *_grid_cell*: a clickable, animated cell
* *_grid*: the 3x3 set of grid cells
* *_img*: the image of the cell
* *_winner_box*: splash screen to show when the game is over
* *_score_board*: exactly that, to show the current score
* *_control_buttons*: to reset, resign or quit a game
* *_player_titles*: to show whose turn is it
* *_dashboard*: the containter for the dashboard

Additionally, it contains some fade actions for Kivy animations, and some global variables for reuse in the modules.

### The tip of the *toe.py*
This last module *toe.py* contains the main executable code for the graphic version of the game. It contains two classes:
* *TicTacToeGame (App)*: which is the main Kivy app
* *GameManager (ScreenManager)*: to control switching between the menu and the actual game

To execute, start kivy in a console:

    $ kivy

Once environment is set, start the application with:

    $ python toe.py

This will bring up the menu:

![TicTacToe - main menu](https://raw.githubusercontent.com/vinceynhz/python_code/master/TicTacToe/img/screen1.png)

From there, you can set up the game and then start, which will bring up the main board:

![TicTacToe - main board](https://raw.githubusercontent.com/vinceynhz/python_code/master/TicTacToe/img/screen2.png)
