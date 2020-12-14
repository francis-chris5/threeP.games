# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:13:54 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx
import wx.stc
import wx.py.shell
import wx.py.editor
import wx.py.editwindow
import wx.aui
from os.path import isdir
import interfaceStuff
from Editors.XMLEditor import XMLEditor
from Editors.TextEditor import TextEditor
from Editors.PyEditor import PyEditor
from Editors.PyConsole import PyConsole
from Dialogs.NewScriptDialog import NewScriptDialog
from GameTools import startClass, startTask, startFunction


class EditorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
            # notebook for editor
        self.__book = wx.aui.AuiNotebook(self)
        self.__shell = PyConsole(self)


        
            # build and set notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__book, 3, wx.EXPAND)
        sizer.Add(self.__shell, 1, wx.EXPAND)
        self.SetSizer(sizer)
    
    
    
    
# =============================================================================
#     Getters (and Setters) for Notebook 
# =============================================================================
    def getShell(self):
        return self.__shell

# =============================================================================
# Methods for Notebook
# =============================================================================
    def newEditor(self, src=""):
        if src == "":
            self.__book.AddPage(PyEditor(self.__book, "untitled.py"), "untitled.py")
        elif src[-3:] == ".py":
            editor = PyEditor(self.__book, src)
            editor.loadFile(src)
            file = src.split("\\")[-1]
            self.__book.AddPage(editor, file)
        elif src[-4:] == ".xml":
            editor = XMLEditor(self.__book, src)
            editor.loadFile(src)
            file = src.split("\\")[-1]
            self.__book.AddPage(editor, file)
        elif src[-4:] == ".txt":
            editor = TextEditor(self.__book, src)
            editor.loadFile(src)
            file = src.split("\\")[-1]
            self.__book.AddPage(editor, file)
        
        
    def newScript(self, event):
        nsd = NewScriptDialog(self, -1)
        result = nsd.ShowModal()
        if result == wx.ID_OK:
            script = nsd.create()
            #print(script)
            if script[0] == "Simple/Blank Script":
                if script[1] == "":
                    wx.MessageDialog(self, "A module (a.k.a. filename) is required for a new script, please try again.").ShowModal()
                else:
                    src = interfaceStuff.location + "\\Scripts\\" + script[1] + ".py"
                    editor = PyEditor(self.__book, src)
                    editor.saveFile(event)
                    self.__book.AddPage(editor, src)
                    interfaceStuff.updateManifest()
                    return True
            elif script[0] == "Function/Method":
                if script[1] == "" or script[2] == "":
                    wx.MessageDialog(self, "A module (a.k.a. filename), and a function name are required to generate a function, please try again.").ShowModal()
                else:
                    src = interfaceStuff.location + "\\Scripts"
                    module = startFunction(script[2], script[1], script[4], src)
                    self.newEditor(src + "\\" + script[1] + ".py")
                    interfaceStuff.updateManifest()
                    return True
            elif script[0] == "Panda3d Task":
                if script[1] == "" or script[2] == "":
                    wx.MessageDialog(self, "A module (a.k.a. filename), and a function name are required to generate a function, please try again.").ShowModal()
                else:
                    src = interfaceStuff.location + "\\Scripts"
                    module = startTask(script[2], script[1], src)
                    self.newEditor(src + "\\" + script[1] + ".py")
                    interfaceStuff.updateManifest()
                    return True
            elif script[0] == "Class/Object":
                if script[2] == "":
                    wx.MessageDialog(self, "A name is required to generate a class, please try again.").ShowModal()
                else:
                    src = interfaceStuff.location + "\\Scripts"
                    if len(script[4]) > 1 or script[4][0] != "":
                        module = startClass(script[2], script[2], script[3], script[4], src)
                    else:
                        module = startClass(script[2], script[2], script[3], directory=src)
                    self.newEditor(src + "\\" + script[2] + ".py")
                    interfaceStuff.updateManifest()
                    return True
        else:
            return False


