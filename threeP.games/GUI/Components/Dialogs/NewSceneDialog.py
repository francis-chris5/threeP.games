# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:34:16 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
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
        self.__icon = wx.Icon("images\\new_scene.png")
        self.SetIcon(self.__icon)
        
            # Name Input
        nameLabel = wx.StaticText(self, -1, label="Name for the New Project", pos=(20, 20))
        self.__name = wx.TextCtrl(self, -1, size=(200, 20), pos=(10, 40))
        
            # Object Type
        objectLabel = wx.StaticText(self, -1, label="Game Mode", pos=(20, 80))
        if interfaceStuff.gameMode == 2:
            objectList = ["Prop", "Background", "Player"]
        elif interfaceStuff.gameMode == 3:
            objectList = ["Player"]
        self.__object = wx.RadioBox(self, -1, pos=(10, 100), choices=objectList)
        
        
            # clickers
        self.__create = wx.Button(self, wx.ID_OK, label="Create Script", pos=(170, 235))
        self.__cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel", pos=(280, 235))
        
        
    
# =============================================================================
#     Getters and Settters  
# =============================================================================
    def getName(self):
        return self.__name.GetValue()
    
    
    def getObject(self):
        return self.__object.GetString(self.__object.GetSelection())