# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 06:09:57 2020

@author: Christopher S. Francis
"""

import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx.stc
from Editors.TextEditor import TextEditor
import Editors.myWords as myWords
from Editors.PyCompleter import PyCompleter



# =============================================================================
# EDITOR FOR PYTHON SCRIPTS
# =============================================================================
class PyEditor(TextEditor):
    def __init__(self, parent, path):
        super().__init__(parent, path)
        
        self.__lastSpace = 0
        self.__words = myWords.python
        
        self.getEditor().SetUseTabs(False)
        self.getEditor().SetTabWidth(4)
        self.setStyle()

        self.Bind(wx.stc.EVT_STC_CHARADDED, self.auto)
    
    
    def setStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:" + self.getBaseColor() + ", " + fonts
        self.getEditor().StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
        
        self.getEditor().SetLexer(wx.stc.STC_LEX_PYTHON)
        kwlist = u" ".join(self.__words)
        self.getEditor().SetKeyWords(0, kwlist)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_DEFAULT, default)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_WORD, "fore:" + self.getPrimaryColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_NUMBER, default)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:" + self.getAccentColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:" + self.getAccentColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_OPERATOR, default)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_STRING, "fore:" + self.getStringColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:" + self.getStringColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:" + self.getStringColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:" + self.getStringColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:" + self.getCommentColor() + "," + fonts)
        
    def getWords(self):
        string = ""
        py = myWords.python
        self.__words.sort()
        for words in myWords.python:
            string += words + "?1 "
        return string
    
    def checkWords(self):
        # @todo get the lexer to update colors on my class, variables, and methods
        for line in range(self.getEditor().GetLineCount()):
            content = self.getEditor().GetLine(line)
            if "def" in content:
                df = content.find("def")
                ln = content.index(":")
                functionName = content[df + 4:ln]
                if not functionName in self.__words:
                    self.__words.append(functionName)
            elif "class" in content:
                cs = content.find("class")
                ln = content.index(":")
                className = content[cs + 6:ln]
                if not className in self.__words:
                    self.__words.append(className)
            elif "=" in content and not "==" in content and not "!=" in content and not ">=" in content and not "<=" in content:
                variable = content[0:content.index("=")].strip()
                if not variable in self.__words:
                    self.__words.append(variable)
                    
    
    def auto(self, event):
            # @todo figure out how to detect backspace and subtract from matching letters
        if event.GetKey() != 32 and event.GetKey() != 10 and event.GetKey() != 13:
            self.__lastSpace += 1
        else:
            if event.GetKey() == 10:
                self.checkWords()
            self.__lastSpace = 0
        self.getEditor().AutoCompShow(self.__lastSpace, self.getWords())
        

    