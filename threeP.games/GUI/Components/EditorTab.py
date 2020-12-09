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
        
            # notebook for editor
        self.__book = wx.aui.AuiNotebook(self)
        self.__shell = wx.py.shell.Shell(self) #size=(700, 200)
        
            # build and set notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__book, 3, wx.EXPAND)
        sizer.Add(self.__shell, 1, wx.EXPAND)
        self.SetSizer(sizer)


# =============================================================================
# Methods for Notebook
# =============================================================================
    def newEditor(self, src=""):
        if src == "":
            self.__book.AddPage(Editor(self.__book, "untitled.py"), "untitled.py")
        else:
            editor = Editor(self.__book, src)
            editor.loadFile(src)
            file = src.split("\\")[-1]
            self.__book.AddPage(editor, file)
        
    
    def loadFile(self, file):
        self.__text.LoadFile(file)
        
        
    def newScript(self, event):
        scriptDialog = wx.TextEntryDialog(None, "Enter a Script Name", caption="New Script", value="")
        with scriptDialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                src = dlg.GetValue() + ".py"
                editor = Editor(self.__book, src)
                self.__book.AddPage(editor, src)
                return editor.saveScript(event)



# =============================================================================
#   Script Editor for Notebook  
# =============================================================================
class Editor(wx.Panel):    
    def __init__(self, parent, path):
        super().__init__(parent)
        
            # editor
        self.__path = path
        self.__editor = wx.py.editwindow.EditWindow(self)
        self.__editor.setDisplayLineNumbers(True)
        
            # save button
        self.__saveBitmap = wx.Bitmap("images\\save_script.png")
        self.__needSaveBitmap = wx.Bitmap("images\\need_save_script.png")
        self.__save = wx.BitmapButton(self, bitmap=self.__saveBitmap)
        self.Bind(wx.EVT_BUTTON, self.saveScript, self.__save)
        self.Bind(wx.stc.EVT_STC_CHANGE, self.needSave)
        
            # build and set editor
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__save, 1)
        sizer.Add(self.__editor, 9, wx.EXPAND)
        self.SetSizer(sizer)
        
    
# =============================================================================
#     Methods for Editor
# =============================================================================
    def loadFile(self, file):
        self.__editor.LoadFile(file)
        self.saveScript(None)
        
        
    def saveScript(self, event):
        directory = interfaceStuff.location + "\\Scripts"
        file = self.__path.split("\\")[-1]
        if isdir(directory):
            with open(directory + "\\" + file, "w", newline="") as toFile:
                for line in range(self.__editor.GetLineCount()):
                    toFile.write(self.__editor.GetLine(line))
                    self.__save.SetBitmap(self.__saveBitmap)
            return True
        else:
            wx.MessageDialog(self, "INVALID DIRECTORY: Please open a project before saving a script").ShowModal()
            return False
        
        
    def needSave(self, event):
        self.__save.SetBitmap(self.__needSaveBitmap)




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