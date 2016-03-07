from math import degrees, radians, sqrt, atan2, sin, cos

from kivy.app import App

from kivy.core.window import Window

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout

from kivy.graphics import Rectangle
from kivy.graphics import Color

from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty

class DrawException( Exception ):
    ''' Any error while drawing a mark '''
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return msg

class _mark( Widget ):
    ''' A visual represenation of a point in the screen that can be dragged around '''
    _bgd = Image(source='img/mark.png')
    click = BooleanProperty(False)
    delete = BooleanProperty(False)
    offset = 5

    def __init__(self, index, pos, distance, **kwargs):
        super( _mark, self ).__init__( size=(10,10), pos=pos, size_hint=(None,None), **kwargs )
        self._index = index
        self._distance = distance # or radius to that point
        
        with self.canvas:
            self._rect = Rectangle( texture=_mark._bgd.texture, size=(8,8), pos=(self.x+1, self.y+1) )

        self.bind(pos=self._update_rect)

    # def __str__(self):
    #     return "{index} {d}: {x},{y}".format( index = self._index, d = self.d, x = self.x, y = self.y )

    def d():
        def fget(self):
            return self._distance
        def fset(self, value):
            self._distance = value
        return locals()
    d = property(**d())

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if 'button' in touch.profile and touch.button == 'right':
            #     self.delete = True
            # else:
            self.click = True
            
            return True

        return super(_mark, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.click:
            self.click = False
            return True
        return super(_mark, self).on_touch_up(touch)

    def _update_rect(self, instance, value):
        self._rect.pos = instance.pos

class _colormap( Widget ):
    ''' Generic class for a color map, that allows the drawing of marks on it 
    and has a img background '''
    mouse_pos = ListProperty()
    delete_index = NumericProperty(-1)
    moved_pos = ListProperty()

    def __init__(self, source=None, maximize=False, **kwargs):
        super(_colormap, self).__init__( **kwargs )

        if source is None:
            raise DrawException('source image not provided to create map')

        self._map = Image(source = source)
        self._max = maximize
        self._ind = -1

        self.marks = None

        with self.canvas:
            self.background = Rectangle( texture=self._map.texture, size=self.size, pos=self.pos )
            #self.mark = _mark(index=0, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def mark_index():
        def fget(self):
            return self._ind
        def fset(self, value):
            self._ind = value
        return locals()
    mark_index = property(**mark_index())

    def put_mark(self, x, y, distance=None, index=-1):
        ''' to draw a mark on this map '''
        if self.marks is None:
            self.marks = []

        #print("PUTMARK", self._ind)

        # if no index is specified or when we got an index and is not already in the list
        if ( self._ind == -1 and index == -1 ) or ( index >= len(self.marks) ):
            if y is None:
                y = self.height

            # we create a new map
            self.marks.append( _mark( index=len(self.marks),
                                     pos=( x-_mark.offset+self.x, y-_mark.offset+self.y ),
                                     distance=distance
                                   ) )
            
            self.add_widget( self.marks[-1] )

            self.marks[-1].click = True
            self._ind = self.marks[-1]._index
            
            self.marks[-1].bind( click=self._mark_click, delete=self._mark_delete )
        else:
            
            # let's select which one I have to move
            ind = max(index, self._ind)

            self.marks[ind].d = distance
            self.marks[ind].x = x-_mark.offset+self.x
            if y is not None:
                self.marks[ind].y = y-_mark.offset+self.y

    def on_touch_down(self, touch):
        # Is within my boundaries
        if self.collide_point(*touch.pos):
            # Pass the touch to see if any of the children collides
            super(_colormap, self).on_touch_down(touch)
            # and assign where the click happened
            self.mouse_pos = (touch.x - self.x, touch.y - self.y)
            #grab it to move it
            touch.grab(self)
            return True

        return super(_colormap, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            # if we are dragging a mark
            if touch.grab_current is self and self._ind != -1:
                # then mark the movement to be calculated
                self.mouse_pos = (touch.x - self.x, touch.y - self.y)
                return True            

        return super(_colormap, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.grab_current is self:
                # pass to the children for them to unclick
                super(_colormap, self).on_touch_up(touch)
                # and release the grab
                self.moved_pos = (touch.x - self.x, touch.y - self.y)
                touch.ungrab(self)
                return True

        return super(_colormap, self).on_touch_up(touch)

    def _mark_click(self, instance, value):
        # if we clicked any of the children, set it here
        if value:
            self._ind = instance._index
        else:
            self._ind = -1
            # print(instance._index)

    def _mark_delete(self, instance, value):
        if value:
            self.delete_index = instance._index
            self.delete( self.delete_index )

    def delete(self, index):
        self.remove_widget( self.marks[index] )
        
        del self.marks[index]
        for ind in range(index, len(self.marks)):
            self.marks[ind]._index -= 1

        self.canvas.ask_update()

    def _update_rect(self, instance, value):
        if self._max:
            self.background.pos = instance.pos
            self.background.size = instance.size

        else:
            size = min(instance.width, instance.height) 
            
            x = instance.x + instance.width/2 - size/2
            y = instance.y + instance.height/2 - size/2

            self.background.pos = (x, y)
            self.background.size = (size, size)

class ColorMixer( StackLayout ):
    def __init__(self, **kwargs):
        super(ColorMixer, self).__init__( orientation='tb-lr', padding=10, spacing=10, **kwargs )

        with self.canvas:
            Color(1,1,1)
            self.background = Rectangle(size = self.size, pos = self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.saturation = _colormap(source='img/sat.png', height=190, size_hint=(1,None) )
        self.huevalue = _colormap(source='img/hue_val.png', maximize=True, height=110, size_hint=(1,None) )
        self.add_widget( self.saturation )
        self.add_widget( self.huevalue ) 

        self.saturation.bind( mouse_pos = self.calc_saturation, 
                              moved_pos = self.print_saturation,
                              delete_index=self.del_saturation,
                              size=self._update_data,
                              pos=self._update_data)
        
        self.huevalue.bind( mouse_pos = self.calc_huevalue,
                            moved_pos = self.print_huevalue, 
                            delete_index=self.del_huevalue) 

        # radius of the saturation circle
        self._r = 100
        # center of the saturation circle
        self._h = self.saturation.width/2
        self._k = self.saturation.height/2

    def _saturation(self, value):
        x = value[0]
        y = value[1]

        # Calculate the angle respect x, regardless if we are out of the circle, we have an angle
        theta = degrees( atan2( y-self._k, x-self._h) )
        if theta < 0:
            theta = 360 + theta

        # Calculate the distance from this point to the center of the circle
        radius = sqrt( (x-self._h)**2 + (y-self._k)**2 )
        
        # if the distance is longer than the radius (we are outside the circle)
        if radius <= self._r:
            pass
            # self.saturation.put_mark( x, y, d )
        else:
            X = sqrt( self._r**2 - (y-self._k)**2 ) + self._h

            if x < self._h:
                X = self._h - ( X % self._h )

            # self.saturation.put_mark( X, y, self._r )

            radius = self._r
            x = X
        
        return x, y, theta, radius

    def calc_saturation(self, instance, value):
        x, y, theta, radius = self._saturation(value)
        
        self.saturation.put_mark( x, y, radius )
        
        # convert to local coordinates
        H = theta * self.huevalue.width / 360 

        self.huevalue.put_mark( H, None, index=self.saturation.mark_index )

    def print_saturation(self, instance, value):
        hsv = [0] * 3

        x, y, theta, radius = self._saturation(value)

        hsv[0] = theta
        hsv[1] = radius * 100 / 95

        index = self.saturation.mark_index
        hsv[2] = (self.huevalue.marks[index].y - _mark.offset) * 100 / 110
 
        print("HSV:", hsv)

    def _huevalue(self, value, index):
        h = value[0]
        v = value[1]

        theta = h * 360 / self.huevalue.width

        # if the current index in huevalue, does not exist in
        # saturation (is a new mark)
        if self.saturation.marks is None or index >= len(self.saturation.marks):
            radius = self._r
        else:
            radius = self.saturation.marks[index].d

        return h, v, theta, radius

    def calc_huevalue(self, instance, value):
        index = self.huevalue.mark_index
        h, v, theta, radius = self._huevalue(value, index)
        
        self.huevalue.put_mark(h,v)

        x = self._h + cos(radians(theta)) * radius
        y = self._k + sin(radians(theta)) * radius

        self.saturation.put_mark( x, y, radius, index )

    def print_huevalue(self, instance, value):
        hsv = [0] * 3
        index = self.huevalue.mark_index
        h, v, theta, radius = self._huevalue(value, index)

        hsv[0] = h * 360 / self.huevalue.width
        hsv[1] = radius * 100 / 95
        hsv[2] = v * 100 / 110

        print("HSV:", hsv)

    def del_saturation(self, instance, value):
        self.huevalue.delete(value)

    def del_huevalue(self, instance, value):
        self.saturation.delete(value)

    def _update_rect(self, instance, value):
        self.background.pos = instance.pos
        self.background.size = instance.size

    def _update_data(self, instance, value):
        self._r = instance.height/2
        self._h = instance.width/2
        self._k = instance.height/2

class MainApp(App):
    def build(self):
        Window.size = (350, 330)

        return ColorMixer()

if __name__ == '__main__':
    MainApp().run()