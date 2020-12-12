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
        scriptDialog = wx.TextEntryDialog(None, "Enter a Script Name", caption="New Script", value="")
        with scriptDialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                src = interfaceStuff.location + "\\Scripts\\" + dlg.GetValue() + ".py"
                editor = PyEditor(self.__book, src)
                self.__book.AddPage(editor, src)
                return editor.saveFile(event)




# =============================================================================
# Open a Testing Window for Editor Notebook
# =============================================================================
class gui(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = EditorTab(self)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    gui(None, -1, "Editor Test")
    app.MainLoop()