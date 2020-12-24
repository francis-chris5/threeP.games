# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:34:00 2020

@author: Christopher S. Francis
"""


import wx
import wx.lib.masked.numctrl
from Graphics.GLPanel import GLModel
import interfaceStuff
from os import listdir
from os.path import isdir, basename


class InspectorTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__reading = False
        self.__transform = {"x": "", "y": "", "z": "", "h": "", "p": "", "r": ""}
        
            # identification
        nameLabel = wx.StaticText(self, -1, "Name: ", pos=(10, 10))
        self.__name = wx.ComboBox(self, -1, value="", size=(200, 20), pos=(10, 30), choices=["no object loaded"])
        
        
            # transform
        positionLabel = wx.StaticText(self, -1, "Position", pos=(10, 60))
        xLabel = wx.StaticText(self, -1, "x", pos=(10, 80))
        self.__x = wx.TextCtrl(self, -1, size=(30, 20), pos=(20, 80))
        yLabel = wx.StaticText(self, -1, "y", pos=(60, 80))
        self.__y = wx.TextCtrl(self, -1, size=(30, 20), pos=(70, 80))
        zLabel = wx.StaticText(self, -1, "z", pos=(110, 80))
        self.__z = wx.TextCtrl(self, -1, size=(30, 20), pos=(120, 80))
        rotationLabel = wx.StaticText(self, -1, "Rotation", pos=(10, 110))
        hLabel = wx.StaticText(self, -1, "h", pos=(10, 130))
        self.__h = wx.TextCtrl(self, -1, size=(30, 20), pos=(20, 130))
        pLabel = wx.StaticText(self, -1, "p", pos=(60, 130))
        self.__p = wx.TextCtrl(self, -1, size=(30, 20), pos=(70, 130))
        rLabel = wx.StaticText(self, -1, "r", pos=(110, 130))
        self.__r = wx.TextCtrl(self, -1, size=(30, 20), pos=(120, 130))
        
        
        
        
        # collisionArea = wx.StaticText(self, -1, "This Area is for collision stuff, My idea is have object images/animations/bounds preview here and drag out from image and get two comboboxes popup to choose collision and function--any thoughts/suggestions on this", pos=(400, 30), size=(200, 150))
        # scriptingArea = wx.StaticText(self, -1, "This Area is for managing scripts attached to this game object, probably simple combobox selection to start with at least", pos=(400, 220), size=(200, 150))
        # otherArea = wx.StaticText(self, -1, "Obviously this project is a long way from completion enough to even give it a version 1.x, these controls are coming, but for now it all has to be done in the scripting tab", pos=(20, 300), size=(200, 100))
        
        self.__previewOptions = wx.ComboBox(self, -1, value="", size=(200, 20), pos=(400, 30), choices=["no object loaded"])
        self.__preview = wx.Panel(self, -1, size=(300, 300), pos=(400, 50))
        
        self.Bind(wx.EVT_COMBOBOX, self.changeImage, self.__previewOptions)
        self.Bind(wx.EVT_COMBOBOX, self.changeSource, self.__name)
        self.Bind(wx.EVT_TEXT, self.changeCoords, self.__x)
        self.Bind(wx.EVT_TEXT, self.changeCoords, self.__y)
        self.Bind(wx.EVT_TEXT, self.changeCoords, self.__z)
        self.Bind(wx.EVT_TEXT, self.changeCoords, self.__h)
        self.Bind(wx.EVT_TEXT, self.changeCoords, self.__p)
        self.Bind(wx.EVT_TEXT, self.changeCoords, self.__r)
        
    
    
# =============================================================================
#     Getters and Setters
# =============================================================================
    def setPreview(self, obj="", mtl=""):
        if interfaceStuff.gameMode == 2:
            png = []
            for item in listdir(obj):
                if item[-4:] == ".png":
                    png.append(item)
            self.__image = wx.StaticBitmap(self.__preview, -1, wx.Bitmap(obj + "\\" + png[0]), pos=(20, 20))
        elif interfaceStuff.gameMode == 3:
            self.__preview.DestroyChildren()
            self.__model = GLModel(self.__preview, obj, mtl)
        
    def getX(self):
        return self.__x.GetValue()

    def getY(self):
        return self.__y.GetValue()

    def getZ(self):
        return self.__z.GetValue()

    def getH(self):
        return self.__h.GetValue()

    def getP(self):
        return self.__p.GetValue()

    def getR(self):
        return self.__r.GetValue()

    def setX(self, x):
        self.__x.SetValue(x)

    def setY(self, y):
        self.__y.SetValue(y)

    def setZ(self, z):
        self.__z.SetValue(z)

    def setH(self, h):
        self.__h.SetValue(h)

    def setP(self, p):
        self.__p.SetValue(p)

    def setR(self, r):
        self.__r.SetValue(r)
        
    def setTransform(self):
        self.setX(self.__transform["x"])
        self.setY(self.__transform["y"])
        self.setZ(self.__transform["z"])
        self.setH(self.__transform["h"])
        if interfaceStuff.gameMode == 3:
            self.setP(self.__transform["p"])
            self.setR(self.__transform["r"])
        
    
    
# =============================================================================
#     Methods for Inspector Tab
# =============================================================================
    
    def clearPreview(self):
        self.__preview.DestroyChildren()
        self.__previewOptions.Set(["no object loaded"])
        self.__name.Set(["no object loaded"])
        
    def clearCoords(self):
        self.setX("")
        self.setY("")
        self.setZ("")
        self.setH("")
        self.setP("")
        self.setR("")
        
        
    def loadProject(self):
        objects = []
        for item in listdir(interfaceStuff.location + "\\Scenes"):
            if item[-3:] == ".py" and item != "GameInstance.py":
                objects.append(item)
        self.__name.Set(objects)
        if interfaceStuff.gameMode == 2:
            self.__p.SetEditable(False)
            self.__r.SetEditable(False)
            self.setPreview(interfaceStuff.location + "\\Assets\\DefaultImages")
        elif interfaceStuff.gameMode == 3:
            self.__p.SetEditable(True)
            self.__r.SetEditable(True)
            self.setPreview("GUI\\images\\cube.obj", "GUI\\images\\cube.mtl")
        
    
    def changeImage(self, event):
        if interfaceStuff.gameMode == 2:
            filepath = interfaceStuff.location + "\\Assets\\" + self.__previewOptions.GetValue()
            self.__image.SetBitmap(wx.Bitmap(filepath))
        elif interfaceStuff.gameMode == 3:
            obj = interfaceStuff.location + "\\Assets\\" + self.__previewOptions.GetValue()
            mtl = obj[:-4] + ".mtl"
            self.setPreview(obj, mtl)
        
    def changeSource(self, event):
        file = self.__name.GetValue()
        reading = False
        with open(interfaceStuff.location + "\\Scenes\\" + file, "r") as fromFile:
            for line in fromFile:
                if "def __init__" in line:
                    source = line[line.find("Asset=") + 7: line.find(", *args")-1].replace("\\\\", "\\")
                if "#? start" in line:
                    reading = True
                if "#? end" in line:
                    reading = False
                if reading:
                    if "setX" in line:
                        self.__transform["x"] = line[line.index("(")+1:line.rindex(")")]
                    elif "setY" in line:
                        self.__transform["y"] = line[line.index("(")+1:line.rindex(")")]
                    elif "setZ" in line:
                        self.__transform["z"] = line[line.index("(")+1:line.rindex(")")]
                    elif "setH" in line:
                        self.__transform["h"] = line[line.index("(")+1:line.rindex(")")]
                    elif "setP" in line:
                        self.__transform["p"] = line[line.index("(")+1:line.rindex(")")]
                    elif "setR" in line:
                        self.__transform["r"] = line[line.index("(")+1:line.rindex(")")]
            self.setTransform()
        if interfaceStuff.gameMode == 2:
            images = []
            for item in listdir(source):
                if item[-4:] == ".png":
                    images.append(basename(source) + "\\" + item)
            self.__previewOptions.Set(images)
        elif interfaceStuff.gameMode == 3:
            obj = []
            for item in listdir(source):
                if item[-4:] == ".obj":
                    obj.append(basename(source) + "\\" + item)
            self.__previewOptions.Set(obj)
            
            
    def changeCoords(self, event):
        try:
            number = float(event.GetString())
            if event.GetId() == self.__x.GetId():
                self.__transform["x"] = str(number)
            elif event.GetId() == self.__y.GetId():
                self.__transform["y"] = str(number)
            elif event.GetId() == self.__z.GetId():
                self.__transform["z"] = str(number)
            elif event.GetId() == self.__h.GetId():
                self.__transform["h"] = str(number)
            elif event.GetId() == self.__p.GetId():
                self.__transform["p"] = str(number)
            elif event.GetId() == self.__r.GetId():
                self.__transform["r"] = str(number)
            # @todo figure out a better time to rewrite file
            self.updateTransform()
        except:
            pass

            
        
    def updateTransform(self):
        lines = []
        file = self.__name.GetValue()
        reading = False
        with open(interfaceStuff.location + "\\Scenes\\" + file, "r") as fromFile:
            for line in fromFile:
                if "#? start" in line:
                    reading = True
                    lines.append(line)
                if "#? end" in line:
                    reading = False
                if reading:
                    if "setX" in line:
                        lines.append("        self.setX(" + str(self.__transform["x"]) + ")\n")
                    elif "setY" in line:
                        lines.append("        self.setY(" + str(self.__transform["y"]) + ")\n")
                    elif "setZ" in line:
                        lines.append("        self.setZ(" + str(self.__transform["z"]) + ")\n")
                    elif "setH" in line:
                        lines.append("        self.setH(" + str(self.__transform["h"]) + ")\n")
                    elif "setP" in line:
                        lines.append("        self.setP(" + str(self.__transform["p"]) + ")\n")
                    elif "setR" in line:
                        lines.append("        self.setR(" + str(self.__transform["r"]) + ")\n")
                else:
                    lines.append(line)
        with open(interfaceStuff.location + "\\Scenes\\" + file, "w") as toFile:
            for line in lines:
                toFile.write(line)
        
    def openObject(self, filepath):
        pass
        # get the type of thing when a module in Scenes is opened
        # check game script and return a list of instances of that type
        # select an instance from name combo box to see it's properties and preview animations
        # modifications on the GUI then alter those values in the game script