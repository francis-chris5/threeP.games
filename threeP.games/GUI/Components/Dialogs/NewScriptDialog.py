# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:20:57 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
import interfaceStuff
import wx


class NewScriptDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetTitle("New Python Script")
        self.SetSize((600, 320))
        self.__icon = wx.Icon("images\\python_logo.png")
        self.SetIcon(self.__icon)
        
                   # Name Input
        moduleLabel = wx.StaticText(self, -1, label="Module/Script name", pos=(20, 10))
        self.__module = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 30))
        
        nameLabel = wx.StaticText(self, -1, label="Name for the Class, Function, or Task", pos=(280, 70))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(270, 90))
        
        parentLabel = wx.StaticText(self, -1, label="Parent name, only applies to a new class", pos=(280, 110))
        self.__parent = wx.TextCtrl(self, -1, size=(200, 20), pos=(270, 130))
        
        attributeLabel = wx.StaticText(self, -1, label="Attributes/Parameters, enter a comma delimited list", pos=(280, 150))
        self.__attribute = wx.TextCtrl(self, -1, size=(200, 20), pos=(270, 170))
        
            # Mode Input
        actionLabel = wx.StaticText(self, -1, label="Type of script to create", pos=(20, 70))
        actionList = ["Simple/Blank Script", "Function/Method", "Panda3d Task", "Class/Object"]
        self.__action = wx.RadioBox(self, -1, pos=(10, 90), choices=actionList, style=wx.RA_SPECIFY_ROWS)
        
        
            # Clickers
        self.__create = wx.Button(self, -1, label="Create Script", pos=(170, 235))
        self.__cancel = wx.Button(self, -1, label="Cancel", pos=(280, 235))
        
            # Error Message
        #self.__error = wx.StaticText(self, -1, label="", size=(90, 120), pos=(250, 30))
        
        
# =============================================================================
#         @todo
#   change event on radio box determines which boxes are grayed out
#       basic: all out
#       class: all on
#       function: name and parameters on, parent off
#       task: name on, parent and parameters off
#
#
#   generate the appropriate code (GameObjects.py), save all scripts to scripts folder, return true/false for success/failure 
# =============================================================================
