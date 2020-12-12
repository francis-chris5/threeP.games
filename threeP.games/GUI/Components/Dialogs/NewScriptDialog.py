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
        
        self.__value = ()
        
            # Type of Script to Create Input
        actionLabel = wx.StaticText(self, -1, label="Type of script to create", pos=(20, 70))
        actionList = ["Simple/Blank Script", "Function/Method", "Panda3d Task", "Class/Object"]
        self.__action = wx.RadioBox(self, -1, pos=(10, 30), choices=actionList, style=wx.RA_SPECIFY_ROWS)
        
           # Name Input
        moduleLabel = wx.StaticText(self, -1, label="Module/Script name", pos=(20, 180))
        self.__module = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 200))
        
        nameLabel = wx.StaticText(self, -1, label="Name for the Class, Function, or Task", pos=(280, 70))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(270, 90))
        self.__name.SetEditable(False)
        
        parentLabel = wx.StaticText(self, -1, label="Parent name, only applies to a new class", pos=(280, 110))
        self.__parent = wx.TextCtrl(self, -1, size=(200, 20), pos=(270, 130))
        self.__parent.SetEditable(False)
        
        attributeLabel = wx.StaticText(self, -1, label="Attributes/Parameters, enter a comma delimited list", pos=(280, 150))
        self.__attribute = wx.TextCtrl(self, -1, size=(200, 20), pos=(270, 170))
        self.__attribute.SetEditable(False)
        
        
        
            # Clickers
        self.__create = wx.Button(self, wx.ID_OK, label="Create Script", pos=(170, 235))
        self.__cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel", pos=(280, 235))
        
        
        
            # Events
        self.Bind(wx.EVT_RADIOBOX, self.enterText, self.__action)
        
        
        
        
# =============================================================================
#     Methods for New Script Dialog
# =============================================================================
    def enterText(self, event):
        selection = self.__action.GetString(self.__action.GetSelection())
        if selection == "Simple/Blank Script":
            self.__module.SetEditable(True)
            self.__name.SetEditable(False)
            self.__parent.SetEditable(False)
            self.__attribute.SetEditable(False)
        elif selection == "Function/Method":
            self.__module.SetEditable(True)
            self.__name.SetEditable(True)
            self.__parent.SetEditable(False)
            self.__attribute.SetEditable(True)
        elif selection == "Panda3d Task":
            self.__module.SetEditable(True)
            self.__name.SetEditable(True)
            self.__parent.SetEditable(False)
            self.__attribute.SetEditable(False)
        elif selection == "Class/Object":
            self.__module.SetEditable(False)
            self.__name.SetEditable(True)
            self.__parent.SetEditable(True)
            self.__attribute.SetEditable(True)
            
    
    def create(self):
        action = self.__action.GetSelection()
        module = self.__module.GetValue()
        name = self.__name.GetValue()
        parent = self.__parent.GetValue()
        att = self.__attribute.GetValue()
        attribute = []
        attArray = att.split(",")
        for a in attArray:
            attribute.append(a.strip())
        return (action, module, name, parent, attribute)
            
            
    def cancel(self, event):
        self.Close()
