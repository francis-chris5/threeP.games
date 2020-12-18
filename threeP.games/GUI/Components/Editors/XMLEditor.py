# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 06:09:57 2020

@author: Christopher S. Francis
"""

import wx.stc
from Editors.TextEditor import TextEditor



# =============================================================================
# EDITOR FOR XML FILES
# =============================================================================
class XMLEditor(TextEditor):
    def __init__(self, parent, path):
        super().__init__(parent, path)
        self.setStyle()
        
    def setStyle(self):
        faces = self.getFaces()
        fonts = "face: %(font)s,size:%(size)d" % faces
        default = "fore:" + self.getBaseColor() + ", " + fonts
        self.getEditor().StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default)
        
        self.getEditor().SetLexer(wx.stc.STC_LEX_XML)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_XMLSTART, "fore:" + self.getAccentColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_XMLEND, "fore:" + self.getAccentColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_TAG, "fore:" + self.getPrimaryColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_TAGUNKNOWN, "fore:" + self.getPrimaryColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:" + self.getAccentColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:" + self.getAccentColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:" + self.getStringColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:" + self.getStringColor() + "," + fonts)
        self.getEditor().StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:" + self.getCommentColor() + "," + fonts)
