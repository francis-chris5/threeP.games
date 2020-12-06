# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:13:54 2020

@author: Christopher S. Francis
"""
import wx
import wx.stc
import wx.py.shell
import wx.py.editwindow
import re
import keyword
import myWords

class EditorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.__text = wx.stc.StyledTextCtrl(self, -1) #size=(750, 450)
        self.__text.setDisplayLineNumbers(True)
        self.__shell = wx.py.shell.Shell(self) #size=(700, 200)

        self.setFont()
        self.lineNumbering()
        self.setStyle("python")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__text, 3, wx.EXPAND)
        sizer.Add(self.__shell, 1, wx.EXPAND)
        self.SetSizer(sizer)

        
    def setStyle(self, language):
        if language == "python":
            self.pythonStyle()
        elif language == "xml":
            self.xmlStyle()
        else:
            self.baseStyle()
        
        
    def lineNumbering(self):
        #symbols
        self.__text.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL) 
        self.__text.SetMarginWidth(0, 6)
        
        #folding
        self.__text.SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.__text.SetMarginWidth(1, 6)
        
        #numbers
        self.__text.SetMarginType(2, wx.stc.STC_MARGIN_NUMBER)
        self.__text.SetMarginWidth(2, 25)
        
        #not sure yet, probably some symbol though
        self.__text.SetMarginType(3, wx.stc.STC_MARGIN_SYMBOL)
        self.__text.SetMarginWidth(3, 6)
        
        self.__text.SetMarginType(4, wx.stc.STC_MARGIN_SYMBOL)
        self.__text.SetMarginWidth(4, 6)
        
        
    def setFont(self):
        self.__font = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.__text.face = self.__font.GetFaceName()
        self.__text.size = self.__font.GetPointSize()
        
    def getFaces(self):
        return dict(font=self.__text.face, size=self.__text.size)
    
    
    def baseStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:#434343, " + fonts
        self.__text.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
    
    def pythonStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:#434343, " + fonts
        self.__text.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
        
        self.__text.SetLexer(wx.stc.STC_LEX_PYTHON)
        kwlist = u" ".join(myWords.python)
        self.__text.SetKeyWords(0, kwlist)
        self.__text.StyleSetSpec(wx.stc.STC_P_DEFAULT, default)
        self.__text.StyleSetSpec(wx.stc.STC_P_WORD, "fore:#eb9178," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:#a86f32," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#237ba1," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#237ba1," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_OPERATOR, default)
        self.__text.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#77ad68," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#77ad68," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#77ad68," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#77ad68," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#c590e0," + fonts)
        #self.__text.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:#ad2626," + fonts)
        
    
    
    def xmlStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:#434343, " + fonts
        self.__text.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
        
        self.__text.SetLexer(wx.stc.STC_LEX_XML)
        kwlist = u" ".join(myWords.xml)
        self.__text.SetKeyWords(0, kwlist)
        self.__text.StyleSetSpec(wx.stc.STC_H_XMLSTART, "fore:#eb9178," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_XMLEND, "fore:#eb9178," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_TAG, "fore:#237ba1," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_TAGUNKNOWN, "fore:#237ba1," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:#eb9178," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:#eb9178," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:#77ad68," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:#77ad68," + fonts)
        self.__text.StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:#c590e0," + fonts)



    def loadFile(self, file):
        self.__text.LoadFile(file)
        
        
        


class gui(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = EditorTab(self)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    gui(None, -1, "Editor Test")
    app.MainLoop()