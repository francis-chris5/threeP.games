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



# =============================================================================
# EDITOR FOR PYTHON SCRIPTS
# =============================================================================
class PyEditor(TextEditor):
    def __init__(self, parent, path):
        super().__init__(parent, path)
        self.setStyle()
    
    
    def setStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:" + self.getBaseColor() + ", " + fonts
        self.getEditor().StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
        
        self.getEditor().SetLexer(wx.stc.STC_LEX_PYTHON)
        kwlist = u" ".join(myWords.python)
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
