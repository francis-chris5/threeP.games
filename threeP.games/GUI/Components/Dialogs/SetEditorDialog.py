# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:12:04 2020

@author: Christopher S. Francis
"""


import interfaceStuff
import wx
from os.path import dirname, abspath, isfile
from shutil import copy


# =============================================================================
# Popup dialog with new project options
# =============================================================================
class SetEditorDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetTitle("Set External Editor")
        self.SetSize((400, 370))
        self.__icon = wx.Icon("GUI\\images\\threeP_logo.png")
        self.SetIcon(self.__icon)
        
            # Name Input
        nameLabel = wx.StaticText(self, -1, label="Visible Name of the Editor", pos=(20, 20))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 40))
        
            # Mode Input
        filetypeLabel = wx.StaticText(self, -1, label="Default filetype for this Editor",  pos=(20, 80))
        self.__filetype = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 100))
        
            # Icon Input
        iconLabel = wx.StaticText(self, -1, label="Icon for this editor", pos=(20, 150))
        self.__icon = wx.FilePickerCtrl(self, -1, pos=(10, 170), wildcard="Editor Icon (*.ico,*.png)|*.ico;*.png",style=wx.DIRP_DIR_MUST_EXIST)
        self.__iconLabel = wx.StaticText(self, -1, label="<--- SELECT DIRECTORY --->", pos=(95, 170))
        
            # Location Input
        locationLabel = wx.StaticText(self, -1, label="Location of this Editor's executable application file", pos=(20, 220))
        self.__location = wx.FilePickerCtrl(self, -1, pos=(10, 240), wildcard="Editor (*.exe)|*.exe", style=wx.DIRP_DIR_MUST_EXIST)
        self.__locationLabel = wx.StaticText(self, -1, label="<--- SELECT DIRECTORY --->", pos=(95, 240))
        
            # Clickers
        self.__create = wx.Button(self, wx.ID_OK, label="Set Default Editor", pos=(120, 285))
        self.__cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel", pos=(280, 285))
        
        
            # Dialog Events
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.showLocation, self.__location)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.showIcon, self.__icon)




# =============================================================================
# Methods for New Project Dialog
# =============================================================================
    def showLocation(self, event):
        self.__locationLabel.SetLabel(self.__location.GetPath())
        
    def showIcon(self, event):
        self.__iconLabel.SetLabel(self.__icon.GetPath())
        
    
    
# =============================================================================
#     Getters and Setters
# =============================================================================
    def getName(self):
        return self.__name.GetValue()
    
    def getFiletype(self):
        return self.__filetype.GetValue()
    
    def getIcon(self):
        filepath = self.__icon.GetPath()
        filename = filepath[filepath.rindex("\\") + 1:]
        current = str(dirname(abspath(__file__))).split("\\")
        current.remove("Components")
        current.remove("Dialogs")
        location = ""
        for c in current:
            location += c + "\\"
        if not isfile(location + "\\images\\" + filename):
            copy(filepath, location + "\\images\\" + filename)
        return filename
    
    def getLocation(self):
        return self.__location.GetPath()