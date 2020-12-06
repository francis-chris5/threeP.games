# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:13:54 2020

@author: Christopher S. Francis
"""
import wx
import wx.stc
import wx.py.shell
import wx.py.editor
import wx.py.editwindow
import wx.aui
import re
import keyword
import myWords

class EditorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        #self.__book = wx.py.editor.EditorNotebook(self)
        self.__book = wx.aui.AuiNotebook(self)
        self.newEditor()
        self.__shell = wx.py.shell.Shell(self) #size=(700, 200)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__book, 3, wx.EXPAND)
        sizer.Add(self.__shell, 1, wx.EXPAND)
        self.SetSizer(sizer)


    def newEditor(self, src=""):
        if src == "":
            self.__book.AddPage(Editor(self.__book), "untitled.py")
        else:
            editor = Editor(self.__book)
            editor.loadFile(src)
            self.__book.AddPage(editor, src)
        
    def loadFile(self, file):
        self.__text.LoadFile(file)



    
class Editor(wx.Panel):    
    def __init__(self, parent):
        super().__init__(parent)
        self.__editor = wx.py.editwindow.EditWindow(self)
        self.__editor.setDisplayLineNumbers(True)
        sizer = wx.BoxSizer()
        sizer.Add(self.__editor, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
    def loadFile(self, file):
        self.__editor.LoadFile(file)


class gui(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = EditorTab(self)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    gui(None, -1, "Editor Test")
    app.MainLoop()