# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:34:16 2020

@author: Christopher S. Francis
"""


import interfaceStuff
import wx


# =============================================================================
# Popup dialog with new scene item options
# =============================================================================
class NewSceneDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetTitle("New Scene Object")
        self.SetSize((600, 320))
        self.__icon = wx.Icon("GUI\\images\\new_scene.png")
        self.SetIcon(self.__icon)
        
            # Name Input
        nameLabel = wx.StaticText(self, -1, label="Name for the New Project", pos=(20, 20))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 40))
        
            # Object Type
        objectLabel = wx.StaticText(self, -1, label="Game Object Type", pos=(20, 80))
        if interfaceStuff.gameMode == 2:
            objectList = ["Player"] # "Prop", "Background", 
        elif interfaceStuff.gameMode == 3:
            objectList = ["Player"]
        self.__object = wx.RadioBox(self, -1, pos=(10, 100), choices=objectList)
        
        
            # Asset Input
        assetLabel = wx.StaticText(self, -1, label="Asset Folder To Link This Game Object To", pos=(20, 160))
        self.__asset = wx.DirPickerCtrl(self, -1, pos=(10, 180), style=wx.DIRP_DIR_MUST_EXIST)
        self.__assetLocation = wx.StaticText(self, -1, label="<--- SELECT DIRECTORY --->", pos=(95, 180))
        
        
            # clickers
        self.__create = wx.Button(self, wx.ID_OK, label="Add Object", pos=(170, 235))
        self.__cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel", pos=(280, 235))
        
            # events
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.showLocation, self.__asset)
        
        
    
# =============================================================================
#     Getters and Settters  
# =============================================================================
    def getName(self):
        return self.__name.GetValue()
    
    
    def getObject(self):
        return self.__object.GetString(self.__object.GetSelection())
    
    def getAsset(self):
        return self.__asset.GetPath()
    
    
    
    
# =============================================================================
#     Methods for NewSceneDialog
# =============================================================================
    def showLocation(self, event):
        self.__assetLocation.SetLabel(self.__asset.GetPath())