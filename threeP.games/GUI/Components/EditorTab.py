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


class EditorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.__book = wx.aui.AuiNotebook(self)
        self.__shell = wx.py.shell.Shell(self) #size=(700, 200)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__book, 3, wx.EXPAND)
        sizer.Add(self.__shell, 1, wx.EXPAND)
        self.SetSizer(sizer)


    def newEditor(self, src=""):
        if src == "":
            self.__book.AddPage(Editor(self.__book, "untitled.py"), "untitled.py")
        else:
            editor = Editor(self.__book, src)
            editor.loadFile(src)
            self.__book.AddPage(editor, src)
        
    def loadFile(self, file):
        self.__text.LoadFile(file)
        
        
    def newScript(self, event):
        scriptDialog = wx.TextEntryDialog(None, "Enter a Script Name", caption="New Script", value="")
        with scriptDialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                src = dlg.GetValue() + ".py"
                editor = Editor(self.__book, src)
                self.__book.AddPage(editor, src)




    
class Editor(wx.Panel):    
    def __init__(self, parent, path):
        super().__init__(parent)
        self.__path = path
        self.__editor = wx.py.editwindow.EditWindow(self)
        self.__editor.setDisplayLineNumbers(True)
        self.__save = wx.Button(self, label="Save Script")
        self.Bind(wx.EVT_BUTTON, self.saveScript, self.__save)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__save, 1)
        sizer.Add(self.__editor, 9, wx.EXPAND)
        self.SetSizer(sizer)
        
    def loadFile(self, file):
        self.__editor.LoadFile(file)
        
    def saveScript(self, event):
        directory = interfaceStuff.location + "\\Scripts"
        file = self.__path.split("\\")[-1]
        if isdir(directory):
            with open(directory + "\\" + file, "w", newline="") as toFile:
                for line in range(self.__editor.GetLineCount()):
                    print(self.__editor.GetLine(line))
                    toFile.write(self.__editor.GetLine(line))
        else:
            wx.MessageDialog(self, "INVALID DIRECTORY: Please open a project before saving a script").ShowModal()


class gui(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = EditorTab(self)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    gui(None, -1, "Editor Test")
    app.MainLoop()