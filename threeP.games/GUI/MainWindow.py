# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 03:21:17 2020

@author: Christopher S. Francis
"""

import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx
from os.path import join, isfile
import interfaceStuff
from EditorTab import EditorTab
from InspectorTab import InspectorTab
from ProjectTree import ProjectTree
from NewProjectDialog import NewProjectDialog


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__projectName = "Test Game"
        self.__gameMode = 2
        self.__location = "C:\\Users\\Chris\\Documents\\delete"
        
        self.__icon = wx.Icon("images\\threeP_logo.ico")
        self.SetIcon(self.__icon)
        self.SetSize((1100, 600))
        
        self.mainMenu()
        self.toolBar()
        self.mainContent()
        self.CreateStatusBar(3, 0, id=wx.Window.NewControlId())
        
        #self.Maximize(True)
        self.Show()
        
        
    def getProjectName(self):
        return self.__projectName

    def getGameMode(self):
        return self.__gameMode

    def getLocation(self):
        return self.__location

    def setProjectName(self, projectName):
        self.__projectName = projectName

    def setGameMode(self, gameMode):
        self.__gameMode = gameMode

    def setLocation(self, location):
        self.__location = location

        
        
    def mainMenu(self):
        self.mnMain = wx.MenuBar()
        self.mnFile = wx.Menu()
        self.mnNewProject = self.mnFile.Append(wx.Window.NewControlId(), "New Project", helpString="Create a new project...")
        self.Bind(wx.EVT_MENU, self.CreateNewProject, self.mnNewProject)
        self.mnOpenProject = self.mnFile.Append(wx.Window.NewControlId(), "Open Project", helpString="Open an existing project...")
        self.Bind(wx.EVT_MENU, self.OpenExistingProject, self.mnOpenProject)
        
        self.mnFile.AppendSeparator()
        
        self.mnNewScript = self.mnFile.Append(wx.Window.NewControlId(), "New Script", helpString="Create a new script in the Script Editor Tab...")
        
        self.mnFile.AppendSeparator()
        
        self.mnClose = self.mnFile.Append(wx.Window.NewControlId(), "Close Project", helpString="Close the current project...")
        self.Bind(wx.EVT_MENU, self.CloseCurrentProject, self.mnClose)
        
        
        self.mnMain.Append(self.mnFile, "File")
        self.SetMenuBar(self.mnMain)
    
    
    def toolBar(self):
        tbTools = self.CreateToolBar()
        self.ToolBar = tbTools
        runButton = tbTools.AddTool(wx.Window.NewControlId(), "Run", wx.Bitmap("images\\run_button.png"))
        self.Bind(wx.EVT_TOOL, self.runGame, runButton)
        tbTools.Realize()

    def mainContent(self):
            #tab panes
        nbMainContent = wx.Notebook(self)
        self.tbEditor = EditorTab(nbMainContent)
        self.tbInspector = InspectorTab(nbMainContent)
        nbMainContent.AddPage(self.tbEditor, "Script Editor")
        nbMainContent.AddPage(self.tbInspector, "Inspector")
        self.Bind(wx.EVT_MENU, self.tbEditor.newScript, self.mnNewScript)
        
            #directory tree
        #self.trDirectory = wx.GenericDirCtrl(self, wx.Window.NewControlId(), size=(300, 1500))
        #self.trDirectory.SetPath(self.getLocation())
        self.trDirectory = ProjectTree(self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.openFile, self.trDirectory.getTree())
        vBox = wx.BoxSizer(wx.HORIZONTAL)
        vBox.Add(self.trDirectory, 1, wx.EXPAND)
        vBox.Add(nbMainContent, 4, wx.EXPAND)
        self.SetSizer(vBox)
        
        
        
        
    def CreateNewProject(self, event):
        npd = NewProjectDialog(self, -1)
        npd.ShowModal()
        path = join(interfaceStuff.location, interfaceStuff.projectName + "_manifest.xml")
        if isfile(path):
            self.trDirectory.loadProject(path)
                    
    def OpenExistingProject(self, event):
        fileDialog = wx.FileDialog(None, "Select the Manifest for Project", wildcard="XML Project Manifest (*.xml)|*.xml")
        with fileDialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                manifest = dlg.GetPath()
                interfaceStuff.xmlParseManifest(manifest)
                self.trDirectory.loadProject(manifest)
                
    def CloseCurrentProject(self, event):
        interfaceStuff.updateManifest()
        interfaceStuff.projectName = ""
        interfaceStuff.gameMode = ""
        interfaceStuff.location = ""
        self.trDirectory.clearTree()

    
    def runGame(self, event):
        interfaceStuff.writeGame()
        interfaceStuff.updateManifest()
        self.trDirectory.loadProject(join(interfaceStuff.location, interfaceStuff.projectName + "_manifest.xml"))
        interfaceStuff.runGame()
        
        
        
    def openFile(self, event):
        file = self.trDirectory.getTree().GetItemText(event.GetItem())
        start = file.index(">") + 1
        file = file[start:]
        self.tbEditor.newEditor(file)
        """
        if file[file.index("."):] == ".py":
            self.tbEditor.setStyle("python")
        elif file[file.index("."):] == ".xml" or file[file.index("."):] == ".svg":
            self.tbEditor.setStyle("xml")
        else:
            self.tbEditor.setStyle("base")
        """



if __name__ == "__main__":
    app = wx.App()
    MainWindow(None, 1, title="threeP.games")
    app.MainLoop()