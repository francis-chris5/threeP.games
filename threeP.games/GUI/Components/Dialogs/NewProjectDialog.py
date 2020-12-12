# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:12:04 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
import interfaceStuff
import wx


class NewProjectDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetTitle("New Project")
        self.SetSize((400, 320))
        self.__icon = wx.Icon("images\\threeP_logo.png")
        self.SetIcon(self.__icon)
        
            # Name Input
        nameLabel = wx.StaticText(self, -1, label="Name for the New Project", pos=(20, 20))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 40))
        
            # Mode Input
        modeLabel = wx.StaticText(self, -1, label="Game Mode", pos=(20, 80))
        modeList = ["2D", "3D"]
        self.__mode = wx.RadioBox(self, -1, pos=(10, 100), choices=modeList)
        
            # Location Input
        projectLabel = wx.StaticText(self, -1, label="Location for the New Project", pos=(20, 170))
        self.__location = wx.DirPickerCtrl(self, -1, pos=(10, 190), style=wx.DIRP_DIR_MUST_EXIST)
        self.__directoryLabel = wx.StaticText(self, -1, label="<--- SELECT DIRECTORY --->", pos=(95, 190))
        
            # Clickers
        self.__create = wx.Button(self, -1, label="Create Project", pos=(170, 235))
        self.__cancel = wx.Button(self, -1, label="Cancel", pos=(280, 235))
        
            # Error Message
        self.__error = wx.StaticText(self, -1, label="", size=(90, 120), pos=(250, 30))
        
            # Dialog Events
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.showDirectory, self.__location)
        self.Bind(wx.EVT_BUTTON, self.create, self.__create)
        self.Bind(wx.EVT_BUTTON, self.cancel, self.__cancel)



# =============================================================================
# Methods for New Project Dialog
# =============================================================================
    def showDirectory(self, event):
        self.__directoryLabel.SetLabel(self.__location.GetPath())
        
        
    def cancel(self, event):
        self.Close()
        
        
    def create(self, event):
        isName = False
        isLocation = False
        name = self.__name.GetValue()
        if name != "":
            isName = True
        else:
            self.__error.SetLabel("A name is required for\n a new project.")
        mode = self.__mode.GetSelection() + 2
        location = self.__location.GetPath()
        if location != "":
            isLocation = True
        else:
            self.__error.SetLabel(self.__error.GetLabel() + "\nA location is required\nfor a new project.")
        if isName and isLocation:
            interfaceStuff.newProj(name, mode, location)
            interfaceStuff.updateManifest()
            self.Close()
                
