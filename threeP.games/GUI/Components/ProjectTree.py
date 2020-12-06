# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:12:04 2020

@author: Christopher S. Francis
"""
import wx
import xml.etree.ElementTree as ET

class ProjectTree(wx.Panel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.__tree = wx.TreeCtrl(self, -1) #size=(200, 500)
		#self.loadProject("C:\\Users\\Chris\\Documents\\delete\\example\\example_manifest.xml")
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.__tree, 1, wx.EXPAND)
		self.SetSizer(sizer)
		
		
	def loadProject(self, path):
		self.__tree.DeleteAllItems()
		tree = ET.parse(path)
		root = tree.getroot()
		for child in root:
			if child.tag == "project":
				treeRoot = self.__tree.AddRoot(child.text)
			else:
				self.parseDirectory(treeRoot, child)
		self.__tree.ExpandAll()

			
	def parseDirectory(self, root, directory):
		for item in directory:
			if item.tag == "directory":
				branch = self.__tree.AppendItem(root, item.find("name").text)
				self.parseDirectory(branch, item)
			if item.tag == "files":
				self.parseDirectory(root, item)
			if  item.tag == "file":
				name = item.find("name").text
				try:
					start = name.rindex("\\") + 1
				except:
					start = 0
				name = name[start:]
				branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text)
				#branch = self.__tree.AppendItem(root, item.find("name").text)
	
	
	def getTree(self):
		return self.__tree





class gui(wx.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		p = ProjectTree(self)
		self.Show()
		
if __name__ == "__main__":
	app = wx.App()
	gui(None, -1, "Tree Test")
	app.MainLoop()