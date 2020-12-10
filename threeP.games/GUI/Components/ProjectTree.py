# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:12:04 2020

@author: Christopher S. Francis
"""


import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx
from os.path import dirname
import xml.etree.ElementTree as ET
import interfaceStuff


class ProjectTree(wx.Panel):
    def __init__(self, parent, images = [], *args, **kwargs):
        super().__init__(parent)
        
            # tree
        self.__tree = wx.TreeCtrl(self, -1)
        
            #images for tree items
        self.__images = wx.ImageList(16, 16)
        for img in images:
            self.__images.Add(img)
        self.__tree.AssignImageList(self.__images)
        
            # build and set tree
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__tree, 1, wx.EXPAND)
        self.SetSizer(sizer)
        

        
# =============================================================================
#  Tree Methods       
# =============================================================================
    def loadProject(self, path):
        self.__tree.DeleteAllItems()
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            if child.tag == "project":
                treeRoot = self.__tree.AddRoot(child.text, 4)
            else:
                self.parseDirectory(treeRoot, child)
        self.__tree.ExpandAll()

            
    def parseDirectory(self, root, directory):
        for item in directory:
            if item.tag == "directory":
                branch = self.__tree.AppendItem(root, item.find("name").text, 2)
                self.parseDirectory(branch, item)
            if item.tag == "files":
                self.parseDirectory(root, item)
            if  item.tag == "file":
                name, extension = interfaceStuff.getFileStuff(item.find("name").text)
                if extension == ".py":
                    branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 0)
                elif extension == ".xml":
                    if name[-12:] == "manifest.xml":
                        branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 3)
                    else:
                        branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 1)
                elif extension == ".png" or extension == ".glb":
                    branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 5)
                elif extension == interfaceStuff.external[3][1]:
                    branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 6)
                elif extension == interfaceStuff.external[2][1]:
                    branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 7)
                else:
                    branch = self.__tree.AppendItem(root, name + "   --->"  + item.find("name").text, 1)
                
    
    def getTree(self):
        return self.__tree
    
    
    def clearTree(self):
        self.__tree.DeleteAllItems()




# =============================================================================
# Open a Testing Window for Tree
# =============================================================================
class gui(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = ProjectTree(self)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    gui(None, -1, "Tree Test")
    app.MainLoop()