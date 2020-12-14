# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:19:41 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx
import interfaceStuff
from datetime import datetime


class StdOutDialog(wx.Dialog):
    def __init__(self, parent, result=""):
        super().__init__(parent)
        self.SetTitle("sys.stdout")
        self.SetSize((600, 320))
        self.__icon = wx.Icon("images\\threep_logo.png")
        self.SetIcon(self.__icon)
        
        self.__result = list(result)
        if self.__result[0] == b"":
            self.__result[0] = b"No messages on sys.stdout from this process"
        if self.__result[1] == b"":
            self.__result[1] = b"No messages on sys.stderr from this process"
        
            # good feedback
        self.__stdout = wx.StaticText(self, -1, label=self.__result[0].decode('ascii'), size=(280, 200), pos=(20, 20), style=wx.ST_NO_AUTORESIZE)
        self.__stdout.SetForegroundColour((50, 168, 82))
        self.__stdout.Wrap(260)
        
            # bad feedback
        self.__stderr = wx.StaticText(self, -1, label=self.__result[1].decode('ascii'), size=(280, 200), pos=(300, 20), style=wx.ST_NO_AUTORESIZE)
        self.__stderr.SetForegroundColour((237, 57, 40))
        self.__stderr.Wrap(260)
        
            
        
            
            # Clickers
        self.__copy = wx.Button(self, wx.ID_OK, label="Copy", pos=(170, 235))
        self.__cancel = wx.Button(self, wx.ID_CANCEL, label="Close", pos=(280, 235))
        
        
        
        
    def copyMessage(self):
        filepath = interfaceStuff.location + "\\" + "STDOUT and STDERR Log.txt"
        with open(filepath, "w") as toFile:
            toFile.write("LOGGED AT: " + str(datetime.now()) + "\n\n")
            toFile.write("\t\t--sys.stdout--\n")
            toFile.write(self.__stdout.GetLabel() + "\n\n")
            toFile.write("\t\t--sys.stderr--\n")
            toFile.write(self.__stderr.GetLabel() + "\n")
        return filepath
        
        
        