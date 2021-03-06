# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:46:52 2020

@author: Christopher S. Francis
"""

import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
import wx
import wx.glcanvas
from OpenGL.GL import *
from objLoader import loadModel


class GLBase(wx.glcanvas.GLCanvas):
    def __init__(self, parent):
        super().__init__(parent, -1)
        self.__initialize = False
        self.__context = wx.glcanvas.GLContext(self)
        
            # mouse positions for rotating
        self.__x = 30
        self.__y = 30
        self.__previousX = 30
        self.__previousY = 30
        
        self.__left = -0.3
        self.__top = 0.5
        self.__spread = 0.6
        
        #self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        #self.SetTransparent(True)
        
            # event hanlers for canvas
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.onGrab)
        self.Bind(wx.EVT_MIDDLE_UP, self.onRelease)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onZoom)
        self.Bind(wx.EVT_MOTION, self.onRotate)
        
        
    
# =============================================================================
#     Getters and Setters
# =============================================================================
    def getX(self):
        return self.__x
    
    def getPreviousX(self):
        return self.__previousX
    
    def getY(self):
        return self.__y
    
    def getPreviousY(self):
        return self.__previousY
    
    def getSize(self):
        return self.__size
    
    def getLeft(self):
        return self.__left
    
    def getTop(self):
        return self.__top
    
    def getSpread(self):
        return self.__spread
    
    def setX(self, x):
        self.__x = x
        
    def setPreviousX(self, x):
        self.__previousX = x
        
    def setY(self, y):
        self.__y = y
    
    def setPreviousY(self, y):
        self.__previousY = y
        
    def setSize(self, size):
        self.__size = size
        
    def setLeft(self, left):
        self.__left = left
        
    def setTop(self, top):
        self.__top = top
        
    def setSpread(self, spread):
        self.__spread = spread
        
    
    
# =============================================================================
#     Methods for the class
# =============================================================================
    # def onSize(self, event):
    #     wx.CallAfter(self.setViewport)
    #     event.Skip()
        
    def setViewport(self):
        size = self.GetClientSize()
        self.SetCurrent(self.__context)
        glViewport(0, 0, size.GetWidth(), size.GetHeight())
        
        
    def onPaint(self, event):
        deviceContext = wx.PaintDC(self)
        self.SetCurrent(self.__context)
        if not self.__initialize:
            self.initGL()
            self.__initialize = True
        self.onDraw()
        
        # sort of abstract, the children will use this
    def onDraw(self):
        pass
        
    
    # @todo put in the mouse events
        # middle - rotate
        # left and right will generate code
    def onGrab(self, event):
        self.CaptureMouse()
        x, y = event.GetPosition()
        self.setX(x)
        self.setPreviousX(x)
        self.setY(y)
        self.setPreviousY(y)
        
    def onRelease(self, event):
        self.ReleaseMouse()
        
    
    def onZoom(self, event):
        # @todo right numbers but my thought on where to put them was incorrect
        delta = event.GetWheelRotation() / 1000
        self.setSpread(self.getSpread() + delta)
    
    def onRotate(self, event):
        if event.Dragging() and event.MiddleIsDown():
            self.setPreviousX(self.getX())
            self.setPreviousY(self.getY())
            x, y = event.GetPosition()
            self.setX(x)
            self.setY(y)
            self.Refresh(False)
        elif event.Dragging() and event.RightIsDown():
            # @todo right numbers but my thought on where to put them was incorrect
            l, t = event.GetPosition()
            l /= 1000
            t /= 1000
            self.setLeft(l - self.getLeft())
            self.setTop(t - self.getTop())
    
    

# =============================================================================
# The model to display
# =============================================================================
class GLModel(GLBase):
    def __init__(self, parent, obj, mtl, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetSize(300, 300)
        self.__obj = obj
        self.__mtl = mtl
        self.__model, self.__material = loadModel(self.__obj, self.__mtl)
        
      
    def initGL(self):
        
        glMatrixMode(GL_PROJECTION)
        glFrustum(self.getLeft(), self.getLeft() + self.getSpread(), self.getTop() - self.getSpread(), self.getTop(), 1.0, 8.0)
        
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0, 0, -5)
        
        glRotatef(self.getY(), 1.0, 0.0, 0.0)
        glRotatef(self.getX(), 0.0, 1.0, 0.0)
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
    def onDraw(self, obj="", mtl=""):
        if obj != "" and mtl != "":
            self.__obj = obj
            self.__mtl = mtl
            self.__model, self.__material = loadModel(self.__obj, self.__mtl)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glBegin(GL_TRIANGLES)
        #model, material = loadModel("human.obj", "human.mtl")
        for f in self.__model:
            glColor3f(self.__material[0], self.__material[1], self.__material[2])
            glNormal3f(f[2][0], f[2][1], f[2][2])
            glVertex3f(f[0][0], f[0][1], f[0][2])
        glEnd()
        
        
        width, height = self.GetSize()
        scaleX = 180.0 / width
        scaleY = 180.0 / height

        glRotatef( (self.getY() - self.getPreviousY()) * scaleY, 1, 0.0, 0.0)
        glRotatef( (self.getX() - self.getPreviousX()) * scaleX, 0.0, 1.0, 0.0)
        
        
        self.SwapBuffers()
        
        
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, -1, "GLPanel Test")
    gl = GLModel(frame, "C:\\Users\\Chris\\Documents\\delete\\testing\\Assets\\Human\\Human_walk.obj", "C:\\Users\\Chris\\Documents\\delete\\testing\\Assets\\Human\\Human_walk.mtl")
    frame.SetSize(gl.GetSize())
    frame.Show()
    app.MainLoop()
        