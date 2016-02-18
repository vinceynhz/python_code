import sys
# to make available all the other code
# the route has to be modified for environment's code

sys.path.append('$CODE_DIR\\_lib')
# sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from shared import misc

from kivy.app import App

from kivy.core.window import Window

from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Point
from kivy.graphics import Fbo
from kivy.graphics import Rectangle

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ListProperty

class Scaled(Widget):
    def __init__(self, **kwargs):
        super(Scaled, self).__init__(**kwargs)

        self.elements = []
        self.pointsize = 5 # this multiplies by two according to kivy docs

        with self.canvas:
            self._fbo = Fbo(size=self.size)
            self._rect = Rectangle( texture=self._fbo.texture )

        with self._fbo:
            Color(1,1,1)
            self._fborect = Rectangle(size=self._fbo.size)
            Color(0,0,1)
            self._points = Point( pointsize = self.pointsize )

        self._fbo.add_reload_observer(self._clear_fbo)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def drawpoint(self, x, y):
        self.elements.append([x,y])
        self._points.add_point( x, y )

    def draw(self,matrix):
        self._points.points = []
        self._clear_fbo()

        for point in matrix:
            x = int( point[0] * ( self.pointsize * 2 ) + self.pointsize )
            y = int( point[1] * ( self.pointsize * 2 ) + self.pointsize )
            self.drawpoint( x,y )

    # RELOADING THE BUFFER AT ANY CHANGE
    def _clear_fbo(self, fbo = None):
        ''' This will reload the framebufferer either by the call of the
        observer or by the deletion of a point'''
        if fbo is None:
            fbo = self._fbo

        fbo.bind()
        fbo.clear_buffer()
        fbo.add( Color(1,1,1) )
        fbo.add( self._fborect )
        fbo.add( Color(0,0,1) )
        fbo.add( self._points )
        fbo.release()

    def _update_rect(self, instance, value):
        self._fbo.size = instance.size
        self._fborect.size = instance.size
        self._rect.size = instance.size
        self._rect.pos = instance.pos
        self._rect.texture = self._fbo.texture

class Pad(Widget):
    scaled = ListProperty()
    def __init__(self, **kwargs):
        super(Pad, self).__init__(**kwargs)

        # Which elements exist in the grid in the normalized coordinates
        self.elements = []
        self.oldxy = None

        with self.canvas:
            self._fbo = Fbo(size=self.size)
            self._rect = Rectangle( texture=self._fbo.texture )

        with self._fbo:
            Color(1,1,1)
            self._fborect = Rectangle(size=self._fbo.size)
            Color(1,0,0)

        self._fbo.add_reload_observer(self._clear_fbo)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # let's hold the mouse
            touch.grab(self)

            self.elements = []
            self._clear_fbo()

            x = round(touch.x - self.x)
            y = round(touch.y - self.y)

            # and keep the position
            self.oldxy = [x,y]
            return True

        return super(Pad, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):

            x = round(touch.x - self.x)
            y = round(touch.y - self.y)

            self.drawline([x,y])
            # and keep the position
            self.oldxy = [x,y]
            return True

        return super(Pad, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            # print('elements', self.elements)

            # try:
            with misc.timeit() as t:
                self.reducematrix()
            # finally:
            print('Matrix reduction and redraw')

            self.oldxy = None
            return True

        return super(Pad, self).on_touch_up(touch)

    def drawline(self, newxy):
        if newxy not in self.elements:
            self.elements.append(newxy)
            with self._fbo:
                Line( points=self.oldxy + newxy, width=1 )

    def reducematrix(self):
        self.matrix = []
        minx = None
        maxx = None
        miny = None
        maxy = None

        with misc.timeit() as t:
            for i in range( len(self.elements)-1 ): # all but last
                # take the current
                origin = self.elements[i]
                # and the next
                point = self.elements[i+1]

                # and get all pixels in between
                points = misc.allpoints(origin, point)

                for p in points:
                    if p not in self.matrix:

                        if minx is None or p[0] < minx:
                            minx = p[0]
                        if maxx is None or p[0] > maxx:
                            maxx = p[0]
                        if miny is None or p[1] < miny:
                            miny = p[1]
                        if maxy is None or p[1] > maxy:
                            maxy = p[1]

                        self.matrix.append(p)
        print('- Calc all points')

        # ajust to the minimum coord
        for p in self.matrix:
            p[0] = p[0] - minx
            p[1] = p[1] - miny

        # print('matrix', self.matrix)
        if maxx is not None:
            size = max(maxx - minx, maxy - miny)
            # print('  minx', minx, 'miny', miny, 'maxx', maxx, 'maxy', maxy, 'size', size)
        else:
            size = self.width

        with misc.timeit() as t:
            self.scaled = misc.scalematrix(self.matrix, (size,size), (15,15))
        # finally:
        print('- Scale matrix')
        # print('scaled', self.scaled)

    # RELOADING THE BUFFER AT ANY CHANGE
    def _clear_fbo(self, fbo = None):
        ''' This will reload the framebufferer either by the call of the
        observer or by the deletion of a point'''
        if fbo is None:
            fbo = self._fbo

        fbo.bind()
        fbo.clear_buffer()
        fbo.add( Color(1,1,1) )
        fbo.add( self._fborect )
        fbo.add( Color(1,0,0) )
        fbo.release()

    def _update_rect(self, instance, value):
        self._fbo.size = instance.size
        self._fborect.size = instance.size
        self._rect.size = instance.size
        self._rect.pos = instance.pos
        self._rect.texture = self._fbo.texture

class DrawPad(App):
    def build( self ):
        Window.size = (400,200)
        box = BoxLayout(orientation = 'horizontal', padding=10, spacing=10)
        self.pad = Pad(size_hint=(None,None), size=(180,180) )
        self.scaled = Scaled(size_hint=(None,None), size=(180,180) )
        box.add_widget( self.pad )
        box.add_widget( self.scaled )

        self.pad.bind(scaled = self.drawscaled)
        return box

    def drawscaled(self, instance, value):
        self.scaled.draw(self.pad.scaled)

if __name__ == '__main__':
    DrawPad().run()
