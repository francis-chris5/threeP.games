# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 05:02:00 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx
import wx.stc
from os.path import isdir
import interfaceStuff
from Editors.PyCompleter import PyCompleter
import Editors.myWords as myWords


# =============================================================================
# PARENT EDITOR CLASSS FOR EDITOR TAB
# =============================================================================
class TextEditor(wx.Panel):
    def __init__(self, parent, path):
        super().__init__(parent)
        
            # editor
        self.__path = path
        self.__stcEditor = wx.stc.StyledTextCtrl(self, -1)
        
            # save button
        self.__picSave = wx.Bitmap("images\\save_script.png")
        self.__picNeedSave = wx.Bitmap("images\\need_save_script.png")
        self.__btnSave = wx.BitmapButton(self, bitmap=self.__picSave)
        
            # color the keywords/symbols
        self.__clrBase = "#434343"
        self.__clrPrimary = "#237ba1"
        self.__clrAccent = "#eb9178"
        self.__clrComment = "#c590e0"
        self.__clrString = "#77ad68"
        self.setFont()
        self.lineNumbering()
        self.baseStyle()
        
            # event binding for editors
        self.Bind(wx.EVT_BUTTON, self.saveFile, self.__btnSave)
        self.Bind(wx.stc.EVT_STC_CHANGE, self.needSave)
        
            # build and set editor
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__btnSave, 1)
        sizer.Add(self.getEditor(), 9, wx.EXPAND)
        self.SetSizer(sizer)
        
    
# =============================================================================
#     Getters and Setters
# =============================================================================
    def getPath(self):
        return self.__path
    
    def getEditor(self):
        return self.__stcEditor
    
    def getBaseColor(self):
        return self.__clrBase
    
    def getPrimaryColor(self):
        return self.__clrPrimary
    
    def getAccentColor(self):
        return self.__clrAccent
    
    def getStringColor(self):
        return self.__clrString
    
    def getCommentColor(self):
        return self.__clrComment
    
    def setBaseColor(self, color):
        self.__clrBase = color
    
    def setPrimaryColor(self, color):
        self.__clrPrimary = color
        
    def setAccentColor(self, color):
        self.__clrAccent = color
        
    def setStringColor(self, color):
        self.__clrString = color
        
    def setCommentColor(self, color):
        self.__clrComment = color

    
    
# =============================================================================
#     Load and Save Methods for Editors
# =============================================================================
    def loadFile(self, file):
        self.getEditor().LoadFile(file)
        self.saveFile(None)
        
        
    def saveFile(self, event):
        file = self.getPath()[self.getPath().rindex("\\")+1:]
        path = self.getPath()[:self.getPath().rindex("\\")]
        if isdir(path):
            if file != interfaceStuff.projectName + "_manifest.xml":
                with open(path + "\\" + file, "w", newline="") as toFile:
                    for line in range(self.getEditor().GetLineCount()):
                        toFile.write(self.getEditor().GetLine(line))
                        self.__btnSave.SetBitmap(self.__picSave)
            else:
                wx.MessageDialog(self, "The manifest is an automtically generated critical file, altering it could destroy the project so it cannot be saved here.").ShowModal()
            return True
        else:
            return False
        
        
    def needSave(self, event):
        self.__btnSave.SetBitmap(self.__picNeedSave)
        
        
    

    
    
    
# =============================================================================
#     Styling Methods for Editors
# =============================================================================
    def lineNumbering(self):
            #symbols
        self.getEditor().SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL) 
        self.getEditor().SetMarginWidth(0, 6)
        
            #folding
        self.getEditor().SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.getEditor().SetMarginWidth(1, 6)
        
            #numbers
        self.getEditor().SetMarginType(2, wx.stc.STC_MARGIN_NUMBER)
        self.getEditor().SetMarginWidth(2, 25)
        
            #not sure yet, probably some symbol though
                # error/warning  or TODO symbol
        self.getEditor().SetMarginType(3, wx.stc.STC_MARGIN_SYMBOL)
        self.getEditor().SetMarginWidth(3, 6)
        
        self.getEditor().SetMarginType(4, wx.stc.STC_MARGIN_SYMBOL)
        self.getEditor().SetMarginWidth(4, 6)
        
    
    def setFont(self):
        self.__font = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.getEditor().face = self.__font.GetFaceName()
        self.getEditor().size = self.__font.GetPointSize()
        
        
    def getFaces(self):
        return dict(font=self.getEditor().face, size=self.getEditor().size)
    
    
    def baseStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:" + self.getBaseColor() + ", " + fonts
        self.getEditor().StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
