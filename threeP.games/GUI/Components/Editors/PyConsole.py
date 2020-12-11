# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 06:46:30 2020

@author: Christopher S. Francis
"""


import wx
import wx.py.shell
import Editors.myWords as myWords


# =============================================================================
# Python Shell Console for Notebook
# =============================================================================
class PyConsole(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
            # console shell
        self.__shell = wx.py.shell.Shell(self)
        self.__clearIcon = wx.Bitmap("images\\clear_icon.png")
        self.__clear = wx.BitmapButton(self, bitmap=self.__clearIcon)
        

            # color the keywords/symbols
        self.__clrBase = "#434343"
        self.__clrPrimary = "#237ba1"
        self.__clrAccent = "#eb9178"
        self.__clrComment = "#c590e0"
        self.__clrString = "#77ad68"
        self.setFont()
        self.setStyle()
        
            # bindings
        self.Bind(wx.EVT_BUTTON, self.clear, self.__clear)

        
        toolSizer = wx.BoxSizer(wx.VERTICAL)
        toolSizer.Add(self.__clear)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.__shell, wx.EXPAND)
        sizer.Add(toolSizer)
        self.SetSizer(sizer)




# =============================================================================
#     Getters and Setters
# =============================================================================
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
# Methods for PyConsole
# =============================================================================
    def clear(self, event):
        self.__shell.clear()
        self.__shell.prompt()
        
        
        
    def setFont(self):
        self.__font = wx.Font(10, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.__shell.face = self.__font.GetFaceName()
        self.__shell.size = self.__font.GetPointSize()
        
        
    def getFaces(self):
        return dict(font=self.__shell.face, size=self.__shell.size)
    
        
    def setStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:" + self.getBaseColor() + ", " + fonts
        self.__shell.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
        
        self.__shell.SetLexer(wx.stc.STC_LEX_PYTHON)
        kwlist = u" ".join(myWords.python)
        self.__shell.SetKeyWords(0, kwlist)
        self.__shell.StyleSetSpec(wx.stc.STC_P_DEFAULT, default)
        self.__shell.StyleSetSpec(wx.stc.STC_P_WORD, "fore:" + self.getPrimaryColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_NUMBER, default)
        self.__shell.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:" + self.getAccentColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:" + self.getAccentColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_OPERATOR, default)
        self.__shell.StyleSetSpec(wx.stc.STC_P_STRING, "fore:" + self.getStringColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:" + self.getStringColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:" + self.getStringColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:" + self.getStringColor() + "," + fonts)
        self.__shell.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:" + self.getCommentColor() + "," + fonts)

