# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:34:00 2020

@author: Christopher S. Francis
"""

import wx

class InspectorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        nameLabel = wx.StaticText(self, -1, "Name: ", pos=(10, 10))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 30))
        positionLabel = wx.StaticText(self, -1, "Position", pos=(10, 60))
        self.__x = wx.TextCtrl(self, -1, size=(30, 20), pos=(10, 80))
        self.__y = wx.TextCtrl(self, -1, size=(30, 20), pos=(50, 80))
        self.__y = wx.TextCtrl(self, -1, size=(30, 20), pos=(90, 80))
        rotationLabel = wx.StaticText(self, -1, "Rotation", pos=(10, 110))
        self.__h = wx.TextCtrl(self, -1, size=(30, 20), pos=(10, 130))
        self.__p = wx.TextCtrl(self, -1, size=(30, 20), pos=(50, 130))
        self.__r = wx.TextCtrl(self, -1, size=(30, 20), pos=(90, 130))
        
        
        collisionArea = wx.StaticText(self, -1, "This Area is for collision stuff, My idea is have object images/animations/bounds preview here and drag out from image and get two comboboxes popup to choose collision and function--any thoughts/suggestions on this", pos=(400, 30), size=(200, 150))
        scriptingArea = wx.StaticText(self, -1, "This Area is for managing scripts attached to this game object, probably simple combobox selection to start with at least", pos=(400, 220), size=(200, 150))
        otherArea = wx.StaticText(self, -1, "Obviously this project is a long way from completion enough to even give it a version 1.x, these controls are coming, but for now it all has to be done in the scripting tab", pos=(20, 300), size=(200, 100))
        
    def getText(self):
        return self.__name
    
    def setText(self, text):
        self.__name = text



class gui(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = InspectorTab(self)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    gui(None, -1, "Inspector Test", size=(700, 450))
    app.MainLoop()