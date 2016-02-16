import random

from kivy.clock import Clock

from kivy.graphics import Color, Rectangle

from kivy.animation import Animation

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty

from kivy.uix.screenmanager import Screen

oimg = Image(source = 'img/ttt_o.png') # 1
ximg = Image(source = 'img/ttt_x.png') # 2
oximg = Image(source = 'img/ttt_ox.png') # 3
xoimg = Image(source = 'img/ttt_xo.png') # 4
boardimg = Image(source = 'img/ttt_board.png')
#loadimg = Image(source ='img/loading.gif', anim_delay=0.04)

phrases = [
            "From there to here, and here to there, funny things are everywhere.",
            "Adults are just outdated children.",
            "Today was good. Today was fun. Tomorrow is another one.",
            "Fun is good.",
            "I like nonsense; it wakes up the brain cells.",
            "I am not a speed reader. I am a speed understander.",
            "The true delight is in the finding out rather than in the knowing.",
            "You're in pretty good shape for the shape you are in.",
            "I do not fear computers. I fear the lack of them."
          ]

def fade(instance, value, duration):
    ''' Generic fading method, uses kivy Animation over opacity property,
    transition until the given value with the given duration'''
    animation = Animation( opacity=value, d=duration )
    animation.start(instance)

def fade_in(instance):
    ''' Wrapper for a fade that will move from whatever the current opacity is 
    to 1 in a quarter of a second'''
    fade(instance, 1, 0.25)

def fade_out(instance):
    ''' Wrapper for a fade that will move from whatever the current opacity is 
    to 0 in a quarter of a second'''
    fade(instance, 0, 0.25)

class ListCheckBox( CheckBox ):
    def __init__(self, index, **kwargs):
        super( ListCheckBox, self ).__init__(**kwargs)
        self.index = index

### LOADING SCREEN ###
# class Loading( Screen ):
#     def __init__(self, **kwargs):
#         super( Loading, self ).__init__( name = 'loading', **kwargs )

#         with self.canvas.before:
#             Color(1,1,1)
#             self. rect = Rectangle( size = self.size, pos = self.pos)

#         self.bind(size = self._update_rect, pos = self._update_rect)
#         self.add_widget( loadimg )

#     def _update_rect( self, instance, value ):
#         self.rect.pos = instance.pos
#         self.rect.size = instance.size

### DASHBOARD CLASSES ###
class _score_board( BoxLayout ):
    _name = "{name}:{score}"

    def __init__(self, **kwargs ):
        super( _score_board, self ).__init__( orientation = "horizontal", **kwargs )
        self.p = {
                   1 : BoxLayout( orientation = "vertical" ), 
                   2 : BoxLayout( orientation = "vertical" )
                 }

        self.add_widget( self.p[1] )
        self.add_widget( self.p[2] )

    def initialize(self, p1, p2):
        self.p[1].clear_widgets()
        self.p[1].add_widget( Label( text = p1.name, font_size = 14, size_hint_y=0.2 ) )
        self.p[1].add_widget( Label( text = str(p1.score), font_size = 28 ) )

        self.p[2].clear_widgets()
        self.p[2].add_widget( Label( text = p2.name, font_size = 14, size_hint_y=0.2 ) )
        self.p[2].add_widget( Label( text = str(p2.score), font_size = 28 ) )

class _control_buttons( BoxLayout ):
    ''' Widget to give the user the option to give up or quit the game '''
    def __init__(self, **kwargs):
        super( _control_buttons,self ).__init__(orientation = "vertical", padding = 10, spacing = 15, **kwargs )

        self.resign = Button( text = "Resign" )
        self.quit = Button( text= "Quit" ) 
        
        self.add_widget( self.resign )
        self.add_widget( self.quit )

class _player_titles( BoxLayout ):
    ''' Widget to show a player's number and which symbol is using to play. 
    It also provides the methods to indicate if it is this player's turn to play'''

    def __init__(self, **kwargs):
        super( _player_titles, self ).__init__( orientation = "horizontal", **kwargs )
        self.current = 1
        
        self.p = {
                   1 : BoxLayout( orientation = "vertical" ), 
                   2 : BoxLayout( orientation = "vertical" )
                 }

        self.add_widget( self.p[1] )
        self.add_widget( self.p[2] )

        self.p[1].opacity = 0.9
        self.p[2].opacity = 0.3

    def initialize(self, p1, p2, current):
        self.p[1].clear_widgets()
        self.p[2].clear_widgets()

        if p1.value == 1:
            self.p[1].add_widget( oimg )
            self.p[2].add_widget( ximg )
        else:
            self.p[1].add_widget( ximg )
            self.p[2].add_widget( oimg )

        self.p[1].add_widget( Label( text=p1.name ) )
        self.p[2].add_widget( Label( text=p2.name ) )

        self.set(current)

    def toggle(self):
        fade( self.p[ self.current ], 0.3, 0.25)
        fade( self.p[ 3-self.current ], 1, 0.25)
        self.current = 3-self.current

    def set(self, player):
        fade( self.p[ 3-player ], 0.3, 0.25 )
        fade( self.p[ player ], 0.9, 0.25 )
        self.current = player

class _dashboard( BoxLayout ):
    quit = BooleanProperty(False)
    resign = BooleanProperty(False)

    def __init__( self, **kwargs ):
        super( _dashboard, self ).__init__( orientation='vertical', padding=10, **kwargs )
        self.size_hint = (.35,1)

        # Player titles
        self.titles = _player_titles()
        #ControlButtons()
        self.buttons = _control_buttons()
        self.buttons.resign.bind( on_press=self._resign )
        self.buttons.quit.bind( on_press=self._quit )
        #ScoreBoard()
        self.scores = _score_board()
        
        self.add_widget( self.titles )
        self.add_widget( self.buttons )
        self.add_widget( self.scores )

    def current(self):
        return self.titles.current

    def initialize(self, p1, p2, current):
        self.titles.initialize(p1,p2, current)
        self.scores.initialize(p1,p2)

    def do_move(self, player):
        self.titles.set(player)

    def do_restart(self, p1, p2, current):
        self.quit = False
        self.resign = False
        self.titles.initialize(p1, p2, current)
        self.scores.initialize(p1, p2)

    def _quit( self, instance ):
        self.quit = True

    def _resign( self, instance ):
        self.resign = True

### GRID CLASSES ###
class _grid_cell( Widget ):
    ''' Instances of this class represent a position in the TicTacToe grid.
    It has the appropriate events to update the image according to the TicTacToe
    core.'''

    click = BooleanProperty(False)
    
    def __init__( self, index, **kwargs ):
        super( _grid_cell, self ).__init__( **kwargs )
        self.index = index
        self.texture = None

    def do_click(self, value):
        self.opacity=0
        self.canvas.clear()

        if value == 1: # meaning that o's are playing
            self.texture = oimg.texture
        else: # meaning that x's are playing
            self.texture = ximg.texture

        with self.canvas:
            self.rect = Rectangle( texture=self.texture, pos=self.pos, size=self.size )
        fade_in(self)

    def do_unclick(self):
        fade_out(self)
        self.canvas.clear()
        self.opacity = 1

    def on_touch_down(self, touch):
        #Let's check that this happened within my boundaries as a widget
        if self.collide_point(*touch.pos):
            self.click = True
            return True

        return super(_grid_cell, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.click = False
        return super(_grid_cell, self).on_touch_up(touch)

class _grid( GridLayout ):
    ''' This is the grid, every time a cell is clicked, the number will be saved here
    for the board to handle the proper things in the game '''

    clicked = NumericProperty(-1)

    def __init__( self, **kwargs ):
        super( _grid, self ).__init__( cols = 3, spacing = 10, size_hint_x = .65, **kwargs )

        with self.canvas.before:
            self.rect = Rectangle( texture = boardimg.texture, 
                                   size = (self.width - 10, self.height - 10), 
                                   pos = self.pos )
        
        self.cells = [ None for i in range(9) ]
        self._populate()

        self.bind( size = self._update_rect, 
                   pos = self._update_rect )

    def do_move( self, position, value ):
        for cell in self.cells:
            if cell.index == position:
                cell.do_click( value )
                return True

        return False

    def do_restart( self ):
        self.clicked = -1
        for cell in self.cells:
            cell.do_unclick()

    def _populate( self ):
        self.clear_widgets()
        for index in range(9):
            self.cells[index] = _grid_cell( index = index )
            self.cells[index].bind( click=self._cell_press )

            self.add_widget( self.cells[index] )

    def _update_rect( self, instance, value ):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _cell_press( self, instance, value ):
        if instance.click is True:
            self.clicked = instance.index

class _img( Widget ):
    def __init__(self, **kwargs):
        super( _img, self ).__init__( **kwargs )
        self.size_hint= (None, None)
        self.size=(72, 72)
        self.texture = None
        self.rect = None

        self.bind( size = self._update_rect,
                   pos = self._update_rect )

    def set(self, value):
        self.canvas.clear()

        if value == 1: # meaning that o's are playing
            self.texture = oimg.texture
        elif value == 2: # meaning that x's are playing
            self.texture = ximg.texture
        elif value == 3: # both
            self.texture = oximg.texture
        elif value == 4:
            self.texture = xoimg.texture

        with self.canvas:
            self.rect = Rectangle( texture=self.texture, pos=self.pos, size=self.size )

    def _update_rect( self, instance, value ):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class _winner_box( BoxLayout ):
    def __init__(self, **kwargs):
        super( _winner_box, self ).__init__( orientation = "vertical", **kwargs )
        self.img = _img( center = self.center )
        self.label = Label(text="Oops", font_size=13)

        self.add_widget(self.img)
        self.add_widget(self.label)

    def set(self, value, text):
        self.clear_widgets()

        self.img.set(value)
        self.label = Label(text=text, font_size=13, text_size=(250, None) )

        self.add_widget(self.img)
        self.add_widget(self.label)

### MAIN GAME BOARD & DASHBOARD ###
class GameBoard( Screen ):
    quit = BooleanProperty(False)

    def __init__(self, **kwargs):
        super( GameBoard, self ).__init__( name = 'board', **kwargs )

        # Here we will receive the game
        self.game = None

        # Create a new grid
        self.grid = _grid()
        # and observe for clicks
        self.grid.bind( clicked=self._next_move )

        # Create the dashboard
        self.dashboard = _dashboard()
        # and observe for events
        self.dashboard.bind( quit = self.do_quit )
        self.dashboard.bind( resign = self.do_resign )

        board_box = BoxLayout( orientation="horizontal", padding=10, spacing=10)
        # The grid of positions
        board_box.add_widget( self.grid )
        # The dashboard
        board_box.add_widget( self.dashboard )

        self.add_widget( board_box )

        # The ending popup
        self.winner = _winner_box()
        self.winner.set(4,"Yay")
        self.endpop = Popup( title="Game Over", content=self.winner, size_hint=(0.6,0.6) )

    def start(self, game = None):
        if game is not None:
            self.game = game

        Clock.schedule_once(self.next, 0.5)

        return True # self.next()

    def next(self, dt, position = None ):
        # We have an error
        if self.game is None: return False
        
        # Let's check if the current player is a PC or not
        t = self.game.players[ self.game.current ].type
        v = self.game.players[ self.game.current ].value

        # If current player is PC
        if t == 1: 
            # This will move automatically the current player to the next one
            p = self.game.next() 
            # print("VOLSKY")
        # If human and we have a position (someone clicked)
        elif position is not None: 
            p = self.game.next( position )
            # print("HOOMAN")
        else:
            # Then verify if the game is over or not
            # print("NOCLICK")
            winner = self.game.board.has_winner()
            spaces = self.game.board.has_space()

            if not spaces or winner is not False:
                # print("END")
                self.end(spaces, winner)

            return True # if no one clicked, we stop

        # If we could play
        if p is not False:
            # First we do the move in the grid
            self.grid.do_move( p, v )
            # Then change the players in the dashboard
            self.dashboard.do_move( self.game.current )
            
            # In five seconds I'm going to attempt playing again
            # in case the next play has to be played by the PC
            Clock.schedule_once(self.next, 0.5)
            return True

        # Then verify if the game is over or not
        # print("NOPLAY")
        winner = self.game.board.has_winner()
        spaces = self.game.board.has_space()

        if not spaces or winner is not False:
            # print("END")
            self.end(spaces, winner)

        return False

    def end(self, spaces, winner):
        value = 4
        # Check for the winner
        if winner is not False:
            value = winner
            for p in self.game.players:
                # Look for whoever has the winning value
                if self.game.players[p].value == winner:
                    text = self.game.players[p].name + " wins!"
                    self.game.players[p].win()
                    break
        else:
            random.shuffle(phrases)
            text = phrases[ 0 ]

        self.winner.set(value, text)
        # Let's pop it up
        self.endpop.open()

        # I pass its own variable to check for the alternation
        self.game.reset( self.game.alternate )
        # Restart the grid
        self.grid.do_restart()
        # Restart the dashboard
        self.dashboard.do_restart(self.game.players[1], self.game.players[2], self.game.current)
        self.start()

    def do_resign(self, instance, value):
        if value is False: return
        
        # Restart the game
        self.game.reset( self.game.alternate )
        # Who was playing?
        print(self.game.current)
        print(self.dashboard.current())
        player = self.game.current
        self.game.players[ 3-player ].win()
        
        # Restart the grid
        self.grid.do_restart()
        # Restart the dashboard
        self.dashboard.do_restart(self.game.players[1], self.game.players[2], self.game.current)
        self.start()

    def do_quit(self, instance, value):
        if value is False: return

        self.do_resign( instance, value )
        self.quit = True

    def _next_move( self, instance, value ):
        if value >= 0:
            self.next( None, position = value )

### MENU SCREEN ###
class _player_figure_selection_box( BoxLayout ):
    def __init__(self, **kwargs):
        super( _player_figure_selection_box, self ).__init__( orientation = "horizontal", **kwargs)
        self.figure = 0 # = o, 1 = x, 2 = x/o (alternate each new game)
        self.fig = [None, None, None]
        self.fig[0] = ListCheckBox( index=0, group="figure", size_hint=(0.1, 1), active=True )
        self.fig[0].bind( active=self._set )
        self.fig[1] = ListCheckBox( index=1, group="figure", size_hint=(0.1, 1) )
        self.fig[1].bind( active=self._set )
        self.fig[2] = ListCheckBox( index=2, group="figure", size_hint=(0.1, 1) )
        self.fig[2].bind( active=self._set )

        self.add_widget( self.fig[0] )
        self.add_widget( Label( text="o") )
        self.add_widget( self.fig[1] )
        self.add_widget( Label( text="x") )
        self.add_widget( self.fig[2] )
        self.add_widget( Label( text="x/o") )

    def _set(self, checkbox, value):
        if value: self.figure = checkbox.index

class _player_name_box( BoxLayout ):
    def __init__(self, name='player', **kwargs):
        super( _player_name_box, self ).__init__( orientation = "horizontal", **kwargs)
        self.textinput = TextInput( text=name, multiline = False, font_size = 12 )
        self.add_widget( Label( text="Name:", size_hint_x=.4, font_size=13 ) )
        self.add_widget( self.textinput )

    def name(self):
        return self.textinput.text

class _player_type_box( BoxLayout ):
    _index = 0

    def __init__(self, **kwargs):
        super( _player_type_box, self ).__init__( orientation = "horizontal", **kwargs)
        self.type = 0 # 0 is Human, 1 is PC

        if 'type' in kwargs:
            self.type = kwargs['type']

        group_name = "type" + str( _player_type_box._index )
        
        human_cb = CheckBox( group=group_name, active=self.type == 0, size_hint=(0.1, 1) )
        human_cb.bind( active = self.set_human )

        pc_cb = CheckBox( group=group_name, active=self.type == 1, size_hint=(0.1, 1) )

        self.add_widget( human_cb )
        self.add_widget( Label( text="Human", font_size=13 ) )
        self.add_widget( pc_cb )
        self.add_widget( Label( text="PC", font_size=13 ) )

        _player_type_box._index += 1

    def set_human(self, checkbox, value):
        if value is True:
            self.type = 0
        else:
            self.type = 1

class Menu( Screen ):
    def __init__(self, **kwargs):
        super( Menu, self ).__init__( name = "menu", **kwargs )

        self.p1_type = _player_type_box( size_hint_y=0.25 )
        self.p1_name = _player_name_box( size_hint_y=0.25, name="Player 1" )
        self.p1_figure = _player_figure_selection_box( size_hint_y=0.3 )
        
        self.p2_type = _player_type_box( size_hint_y=0.25, type=1 )
        self.p2_name = _player_name_box( size_hint_y=0.25, name="Player 2" )

        self.start_btn = Button( text="Start", size_hint_y=0.3 )

        # P1 options (1 list of values)
        p1_box = BoxLayout( orientation = "vertical", padding = 10, spacing = 10 )
        p1_box.add_widget( Label( text="Player 1", size_hint=(1, .25), bold=True ) )
        p1_box.add_widget( self.p1_type )
        p1_box.add_widget( self.p1_name )
        p1_box.add_widget( self.p1_figure )
        p1_box.add_widget( Widget() )

        # P2 options (1 list of values)
        p2_box = BoxLayout( orientation = "vertical", padding = 10, spacing = 10 )
        p2_box.add_widget( Label( text="Player 2", size_hint=(1, .25), bold=True ) )
        p2_box.add_widget( self.p2_type )
        p2_box.add_widget( self.p2_name )
        p2_box.add_widget( Widget() )
        p2_box.add_widget( self.start_btn )
        
        # Menu huge box (2 columns )
        menu_box = BoxLayout( orientation="horizontal", spacing = 10 )
        menu_box.add_widget( p1_box )
        menu_box.add_widget( p2_box )

        self.add_widget( menu_box )
