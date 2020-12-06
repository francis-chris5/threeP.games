# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:34:00 2020

@author: Christopher S. Francis
"""

import wx
import wx.py.shell
import code

class Console(wx.Panel):
	def __init__(self, parent):
		super().__init__(parent)
		
		shell = wx.py.shell.Shell(self, size=(700, 450))
		
	def getText(self):
		return self.__name
	
	def setText(self, text):
		self.__name = text



class gui(wx.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		c = Console(self)
		self.Show()
		
if __name__ == "__main__":
	app = wx.App()
	gui(None, -1, "Tree Test")
	app.MainLoop()