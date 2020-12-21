# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:34:00 2020

@author: Christopher S. Francis
"""


import wx
from Graphics.GLPanel import GLModel
import interfaceStuff

class InspectorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
            # identification
        nameLabel = wx.StaticText(self, -1, "Name: ", pos=(10, 10))
        self.__name = wx.ComboBox(self, -1, value="", size=(200, 20), pos=(10, 30), choices=["test values", "load a class", "to see instances used"])
        
            # transform
        positionLabel = wx.StaticText(self, -1, "Position", pos=(10, 60))
        self.__x = wx.TextCtrl(self, -1, size=(30, 20), pos=(10, 80))
        self.__y = wx.TextCtrl(self, -1, size=(30, 20), pos=(50, 80))
        self.__y = wx.TextCtrl(self, -1, size=(30, 20), pos=(90, 80))
        rotationLabel = wx.StaticText(self, -1, "Rotation", pos=(10, 110))
        self.__h = wx.TextCtrl(self, -1, size=(30, 20), pos=(10, 130))
        self.__p = wx.TextCtrl(self, -1, size=(30, 20), pos=(50, 130))
        self.__r = wx.TextCtrl(self, -1, size=(30, 20), pos=(90, 130))
        
        
        # collisionArea = wx.StaticText(self, -1, "This Area is for collision stuff, My idea is have object images/animations/bounds preview here and drag out from image and get two comboboxes popup to choose collision and function--any thoughts/suggestions on this", pos=(400, 30), size=(200, 150))
        # scriptingArea = wx.StaticText(self, -1, "This Area is for managing scripts attached to this game object, probably simple combobox selection to start with at least", pos=(400, 220), size=(200, 150))
        # otherArea = wx.StaticText(self, -1, "Obviously this project is a long way from completion enough to even give it a version 1.x, these controls are coming, but for now it all has to be done in the scripting tab", pos=(20, 300), size=(200, 100))
        
        self.__preview = wx.Panel(self, -1, size=(300, 300), pos=(400, 30))
        self.setPreview("GUI\\images\\cube.obj", "GUI\\images\\cube.mtl")
        
    
    
# =============================================================================
#     Getters and Setters
# =============================================================================
    def setPreview(self, obj, mtl):
        self.__model = GLModel(self.__preview, obj, mtl)
        
    def getX(self):
        return self.__x.GetValue()

    def getY(self):
        return self.__y.GetValue()

    def getZ(self):
        return self.__z.GetValue()

    def getH(self):
        return self.__h.GetValue()

    def getP(self):
        return self.__p.GetValue()

    def getR(self):
        return self.__r.GetValue()

    def setX(self, x):
        self.__x.SetValue(x)

    def setY(self, y):
        self.__y.SetValue(y)

    def setZ(self, z):
        self.__z.SetValue(z)

    def setH(self, h):
        self.__h.SetValue(h)

    def setP(self, p):
        self.__p.SetValue(p)

    def setR(self, r):
        self.__r.SetValue(r)
        
    
    
# =============================================================================
#     Methods for Inspector Tab
# =============================================================================
    def openObject(self, filepath):
        pass
        # get the type of thing when a module in Scenes is opened
        # check game script and return a list of instances of that type
        # select an instance from name combo box to see it's properties and preview animations
        # modifications on the GUI then alter those values in the game script