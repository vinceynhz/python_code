from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen

from tic import Game, Player    # TicTacToe core classes and methods
from tac import Menu, GameBoard # TicTacToe gui helpers

class GameManager( ScreenManager ):
    def __init__(self, **kwargs):
        super( GameManager, self ).__init__( transition=FadeTransition(), **kwargs )
        self.game = None
        self.p1 = None
        self.p2 = None

        self.menu = Menu()
        self.menu.start_btn.bind( on_press = self.start )

        self.game_board = GameBoard()
        self.game_board.bind( quit = self.quit )
        
        self.add_widget( self.menu )
        self.add_widget( self.game_board )
        #self.add_widget( Loading() )

    def start(self, instance):
        # Then setup the screen

        p1_figure = self.menu.p1_figure.figure

        self.p1 = Player(
                    name = self.menu.p1_name.name(),
                    type = self.menu.p1_type.type
                   )

        self.p2 = Player(
                    name = self.menu.p2_name.name(),
                    type = self.menu.p2_type.type
                   )

        # We setup the game
        self.game = Game( p1 = self.p1, p2 = self.p2 )

        if p1_figure == 2: # Meaning that we have to alternate
            self.game.alternate = True
            self.p1.value = 1
            self.p2.value = 2
        else:
            self.p1.value = p1_figure + 1
            self.p2.value = 2 - p1_figure
        
        #Let's start the dashboard values
        self.game_board.dashboard.initialize(self.p1, self.p2, self.game.current)
        
        # Then setup the screen
        self.current = "board"
        # Then we start the game ;)
        self.game_board.start( self.game )

    def quit(self, instance, value):
        self.game_board.quit = False
        self.current = "menu"

class TicTacToeGame( App ):
    icon = 'img/avatar_leaf.png'
    title = 'Vic Tac Toe'
    
    def build(self):
        Window.size = (450, 300)
        return GameManager()

if __name__ == '__main__':
    TicTacToeGame().run()