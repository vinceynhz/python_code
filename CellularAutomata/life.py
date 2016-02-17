# from random import randint

# Fancy and cool conway's game rules
import automaton

from kivy.app import App
from kivy.core.window import Window

from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Fbo, Color, Point, Rectangle

from kivy.properties import NumericProperty

class Grid( Widget ):
    point_size = NumericProperty(10)
    
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        # Which elements exist in the grid in the normalized coordinates
        self.elements = []
        # If active, it can't be modified
        self.active = False
        
        # To the canvas, we add the FrameBufferObject and the rect to show it
        with self.canvas:
            self.fbo = Fbo(size=self.size)
            self.rect = Rectangle(texture=self.fbo.texture)
            # Color(1,0,0)
            # self.rect = Rectangle(size = self.size, pos = self.pos)

        # To the FrameBufferObject I set the color and add the point list
        with self.fbo:
            Color(1,1,1)
            self.points = Point( pointsize=self.point_size )

        # add some observers to the fbo, changes for the point_size (grid 
        # resizing) and widget resizing
        self.fbo.add_reload_observer(self._populate_fbo)
        self.bind( point_size = self._reshape )
        self.bind( size = self._update_rect, pos = self._update_rect )

    def on_touch_down(self, touch):
        ''' Handle adding/removing points when the grid is not active'''
        if not self.active and self.collide_point(*touch.pos):
            # Move to a 0,0 from where the widget starts
            x = touch.x - self.x
            y = touch.y - self.y
            self.add_point( [x,y] )

            return True

        return super(Grid, self).on_touch_down(touch)

    def normalize(self, coords):
        ''' normalization of coordinates, it will transform any given point in 
        the widget to its corresponding normalized coords '''
        # TODO: Create a picture to describe what are the normalized coordinates
        if type(coords) is tuple:
            coords = list(coords)

        if type(coords) is list:
            for ind in range(len(coords)):
                coords[ind] = int( coords[ind] // ( self.points.pointsize * 2 ) )
            return coords
        else:
            return int( coords // ( self.points.pointsize * 2 ) )

    def adjust(self, coords):
        ''' adjustment of a normalized coordinate to the real coordinate using
        the current point size as a guide '''
        if type(coords) is tuple:
            coords = list(coords)

        if type(coords) is list:
            for ind in range(len(coords)):
                coords[ind] = int( coords[ind] * ( self.points.pointsize * 2 ) + self.points.pointsize )
            return coords
        else:
            return int( coords * ( self.points.pointsize * 2 ) + self.points.pointsize )

    def add_point(self, point, redraw=True):
        ''' method to add a point to the grid if it doesn't exist
        if it's there, remove it'''
        point = self.normalize(point)
        
        if point in self.elements:
            where = self.elements.index( point )

            # Steal the reference to the vector of points
            points = self.points.points
            self.points.points = []
            # Clean the desired point
            del(points[where*2])
            del(points[where*2])

            # Reassign the property for the context to know (kivy weird things)
            self.points.points = points

            # Remove from the historical
            del(self.elements[where])

            # Redraw if asked for
            if redraw:
                self._populate_fbo(self.fbo)
        else:
            # add the normalized coords to the element list
            # it has to be copied because the adjust method will modify
            # the elements in points
            self.elements.append(point[:])
            # add the point to the visible points using the adjusted coordinates
            # the * leading self.adjust is to unpack the resulting array
            self.points.add_point( *self.adjust(point) )

        # print(self.elements)

    def next(self, instance):
        if len(self.elements) == 0: return
        
        # calculate the survivors
        nextgen = automaton.survivors(self.elements)
        # print(nextgen)
        # calculate any possible newborns
        nextgen += automaton.births(self.elements)
        # print(nextgen)

        # replace the current elements
        self.elements = nextgen
        # The vector comes with minivectors within, which is fine for the 
        # list of elements but doesn't work for the adjustment of points in
        # the screen
        nextgen = [ i for cell in nextgen for i in cell ]
        # adjust the elements to the actual coordinates
        nextgen = self.adjust( nextgen )
        # assign the vector back
        self.points.points = nextgen
        # redraw
        self._populate_fbo()

    def clear(self, instance):
        self.elements = []
        self.points.points = []
        self._populate_fbo()

    # RELOADING THE BUFFER AT ANY CHANGE
    def _populate_fbo(self, fbo = None):
        ''' This will reload the framebufferer either by the call of the 
        observer or by the deletion of a point'''
        if fbo is None:
            fbo = self.fbo

        fbo.bind()
        fbo.clear_buffer()
        fbo.add(self.points)
        fbo.release()

    def _reshape(self, instance, value):
        # There are no elements
        if len(self.elements) == 0:
            # We just update the points to be drawn
            self.points.pointsize = self.point_size
        # If we do have elements
        else:
            # steal the reference to the vector
            points = self.points.points
            self.points.points = []

            # normalize using current value
            points = self.normalize( points )
            # reassing the value
            self.points.pointsize = self.point_size
            # adjust using new value
            points = self.adjust( points )

            # assign the vector back
            self.points.points = points
            # redraw
            self._populate_fbo()

    # REDRAWING THE FBO AND THE
    def _update_rect( self, instance, value ):
        self.fbo.size = instance.size
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        self.rect.texture = self.fbo.texture

class Controls(BoxLayout):
    def __init__(self, **kwargs):
        super(Controls, self).__init__(orientation = 'horizontal', spacing=20, **kwargs)
        self.next = Button(text="Next")
        self.clear = Button(text="Clear")
        self.change = Button(text="Change")
        self.start = Button(text="Start")
        self.stop = Button(text="Stop")
        self.generation = Label(text="0")
        self.pointsize = TextInput(text="10", multiline = False, font_size = 12)

        self.add_widget( self.next )
        self.add_widget( self.clear )
        self.add_widget( Label(text="Point Size") )
        self.add_widget( self.pointsize )
        self.add_widget( self.change )
        self.add_widget( self.start )
        self.add_widget( self.stop )
        self.add_widget( self.generation )
        # self.add_widget( Widget(size_hint=(None,None), width=Window.width/2, height=Window.height/2) )

class MyApp( App ):
    def build(self):
        Window.size = (750, 600)
        whole = BoxLayout(orientation='vertical', margin=10, spacing=10)
        self.grid = Grid( size_hint=(1 ,0.95) )
        self.controls = Controls( size_hint=(1,0.05) )
        self.counter = 0

        whole.add_widget( self.grid )
        whole.add_widget( self.controls )

        self.controls.next.bind(on_press=self.grid.next)
        self.controls.clear.bind(on_press=self.grid.clear)
        self.controls.change.bind(on_press=self.change)
        self.controls.start.bind(on_press=self.start)
        self.controls.stop.bind(on_press=self.halt)

        return whole

    def change(self, instance):
        try:
            self.grid.point_size = int(self.controls.pointsize.text)
        except Exception as e:
            print(e)

    def start(self, instance):
        self.grid.active = True
        self.counter = 0
        Clock.schedule_interval(self.autocallback, 0.1)

    def autocallback(self, dt):
        self.counter += 1
        self.controls.generation.text = str(self.counter)
        self.grid.next(None)

    def halt(self, instance):
        Clock.unschedule(self.autocallback)
        self.grid.active = False
        # print(self.grid.elements)

if __name__ == '__main__':
    MyApp().run()
    pass