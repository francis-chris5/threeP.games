# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 03:21:17 2020

@author: Christopher S. Francis
"""

import sys
sys.path.insert(1, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\Interface")
sys.path.insert(2, "C:\\Users\\Chris\\Documents\\game dev in python\\threeP.games\\GUI\\Components")
import wx
import webbrowser
from os import remove, rmdir
from os.path import join, isfile, isdir
import interfaceStuff
from EditorTab import EditorTab
from InspectorTab import InspectorTab
from ProjectTree import ProjectTree
from NewProjectDialog import NewProjectDialog


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
            # project data fields
        self.__projectName = "Test Game"
        self.__gameMode = 2
        self.__location = "C:\\Users\\Chris\\Documents\\delete"
        
            # window settings
        self.__icon = wx.Icon("images\\threeP_logo.ico")
        self.SetIcon(self.__icon)
        self.SetSize((1100, 600))
        
            # window components
        self.mainMenu()
        self.toolBar()
        self.mainContent()
        self.CreateStatusBar(3, 0, id=wx.Window.NewControlId())
        
            #launch window
        #self.Maximize(True)
        self.Show()
        
    
    
        # getters and setters for project data
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


# =============================================================================
#     Window Components
# =============================================================================
    def mainMenu(self):
        self.__mnMain = wx.MenuBar()
        
            # construct file menu
        self.__mnFile = wx.Menu()
        self.__mnNewProject = self.__mnFile.Append(wx.Window.NewControlId(), "New Project", helpString="Create a new project...")
        self.__mnOpenProject = self.__mnFile.Append(wx.Window.NewControlId(), "Open Project", helpString="Open an existing project...")
        self.__mnFile.AppendSeparator()
        self.__mnNewScript = self.__mnFile.Append(wx.Window.NewControlId(), "New Script", helpString="Create a new script in the Script Editor Tab...")
        self.__mnFile.AppendSeparator()
        self.__mnClose = self.__mnFile.Append(wx.Window.NewControlId(), "Close Project", helpString="Close the current project...")
        self.__mnExit = self.__mnFile.Append(wx.Window.NewControlId(), "Exit", helpString="Exit this application...")
        
            #file menu events
        self.Bind(wx.EVT_MENU, self.CreateNewProject, self.__mnNewProject)
        self.Bind(wx.EVT_MENU, self.OpenExistingProject, self.__mnOpenProject)
        self.Bind(wx.EVT_MENU, self.CloseCurrentProject, self.__mnClose)
        self.Bind(wx.EVT_MENU, self.exitApp, self.__mnExit)
        
            # construct run menu
        self.__mnRun = wx.Menu()
        self.__mnRunSystem = self.__mnRun.Append(wx.Window.NewControlId(), "Run in System", helpString="Generate the game file and run...")
        
            # run menu events
        self.Bind(wx.EVT_MENU, self.runGame, self.__mnRunSystem)
        
            # construct asset menu
        self.__mnAssets = wx.Menu()
        self.__mnImportGraphics = self.__mnAssets.Append(wx.Window.NewControlId(), "Import Graphics Folder", helpString="Import a prepared folder of .png or .bam files...")
        
            # asset menu events
        self.Bind(wx.EVT_MENU, self.importGraphics, self.__mnImportGraphics)
        
            # construct help menu
        self.__mnHelp = wx.Menu()
        self.__mnPythonHelp = self.__mnHelp.Append(wx.Window.NewControlId(), "Python", helpString="Links to the official Python API Documentation Site...")
        self.__mnPanda3DHelp = self.__mnHelp.Append(wx.Window.NewControlId(), "Panda3D", helpString="Links to the official Panda3D API Documentation Site...")
        self.__mnPyGameHelp = self.__mnHelp.Append(wx.Window.NewControlId(), "PyGame", helpString="Links to the official PyGame API Documentation Site...")
        
            # help menu events
        self.Bind(wx.EVT_MENU, self.pythonHelp, self.__mnPythonHelp)
        self.Bind(wx.EVT_MENU, self.panda3DHelp, self.__mnPanda3DHelp)
        self.Bind(wx.EVT_MENU, self.pyGameHelp, self.__mnPyGameHelp)
        
            # build and set menu        
        self.__mnMain.Append(self.__mnFile, "File")
        self.__mnMain.Append(self.__mnRun, "Run")
        self.__mnMain.Append(self.__mnAssets, "Assets")
        self.__mnMain.Append(self.__mnHelp, "Help")
        self.SetMenuBar(self.__mnMain)
    
    
    def toolBar(self):
        self.__tlMain = self.CreateToolBar()
        
            # tools
        self.__tlNewProject = self.__tlMain.AddTool(wx.Window.NewControlId(), "New Project", wx.Bitmap("images\\new_project.png"))
        self.__tlOpenProject = self.__tlMain.AddTool(wx.Window.NewControlId(), "Open Project", wx.Bitmap("images\\open_project.png"))
        self.__tlCloseProject = self.__tlMain.AddTool(wx.Window.NewControlId(), "Close Project", wx.Bitmap("images\\close_project.png"))
        self.__tlMain.AddSeparator()
        self.__tlNewScript = self.__tlMain.AddTool(wx.Window.NewControlId(), "New Script", wx.Bitmap("images\\new_script.png"))
        self.__tlImportGraphics = self.__tlMain.AddTool(wx.Window.NewControlId(), "Import Graphics Folder", wx.Bitmap("images\\graphics_icon.png"))
        self.__tlMain.AddSeparator()
        self.__tlRunSystem = self.__tlMain.AddTool(wx.Window.NewControlId(), "Run", wx.Bitmap("images\\run_button.png"))
        self.__tlMain.AddSeparator()
        self.__tlHelp = self.__tlMain.AddTool(wx.Window.NewControlId(), "Help", wx.Bitmap("images\\help_icon.png"))
        
            # tool bar events (that don't have to wait on other components)
        self.Bind(wx.EVT_TOOL, self.CloseCurrentProject, self.__tlCloseProject)
        self.Bind(wx.EVT_TOOL, self.runGame, self.__tlRunSystem)
        self.Bind(wx.EVT_TOOL, self.CreateNewProject, self.__tlNewProject)
        self.Bind(wx.EVT_TOOL, self.OpenExistingProject, self.__tlOpenProject)
        self.Bind(wx.EVT_TOOL, self.importGraphics, self.__tlImportGraphics)
        self.Bind(wx.EVT_TOOL, self.tlHelp, self.__tlHelp)
        
            # build and set menu
        self.__tlMain.Realize()

    def mainContent(self):
            # tab panes
        self.__nbMainContent = wx.Notebook(self)

        self.__tbEditor = EditorTab(self.__nbMainContent)
        self.__tbInspector = InspectorTab(self.__nbMainContent)
        self.__nbMainContent.AddPage(self.__tbEditor, "Script Editor")
        self.__nbMainContent.AddPage(self.__tbInspector, "Inspector")
        
            # directory tree
        self.__trImages = [wx.Icon("images\\python_logo.png"), wx.Icon("images\\new_script.png"), wx.Icon("images\\open_project.png"), wx.Icon("images\\manifest_icon.png"), wx.Icon("images\\threeP_logo.ico"), wx.Icon("images\\graphics_icon.png")]
        self.__trDirectory = ProjectTree(self, self.__trImages)
        
            # main content events
        self.Bind(wx.EVT_MENU, self.newScript, self.__mnNewScript)
        self.Bind(wx.EVT_TOOL, self.newScript, self.__tlNewScript)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.openFile, self.__trDirectory.getTree())
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.removeFile, self.__trDirectory.getTree())
        
            # build and set main content
        vBox = wx.BoxSizer(wx.HORIZONTAL)
        vBox.Add(self.__trDirectory, 1, wx.EXPAND)
        vBox.Add(self.__nbMainContent, 4, wx.EXPAND)
        self.SetSizer(vBox)
        
        
        
# =============================================================================
#     Main Window Operations
# =============================================================================
    def CreateNewProject(self, event):
        npd = NewProjectDialog(self, -1)
        npd.ShowModal()
        path = join(interfaceStuff.location, interfaceStuff.projectName + "_manifest.xml")
        if isfile(path):
            self.__trDirectory.loadProject(path)
            self.SetTitle("threeP.games:        " + interfaceStuff.location)
    
    
    def OpenExistingProject(self, event):
        fileDialog = wx.FileDialog(None, "Select the Manifest for Project", wildcard="XML Project Manifest (*.xml)|*.xml")
        with fileDialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                manifest = dlg.GetPath()
                interfaceStuff.xmlParseManifest(manifest)
                self.__trDirectory.loadProject(manifest)
                self.SetTitle("threeP.games:        " + interfaceStuff.location)
         
                
    def CloseCurrentProject(self, event):
        interfaceStuff.updateManifest()
        interfaceStuff.projectName = ""
        interfaceStuff.gameMode = ""
        interfaceStuff.location = ""
        self.__trDirectory.clearTree()
        self.SetTitle("threeP.games")
        
        
    def exitApp(self, event):
        self.Close()

    
    def runGame(self, event):
        interfaceStuff.writeGame()
        interfaceStuff.updateManifest()
        self.__trDirectory.loadProject(join(interfaceStuff.location, interfaceStuff.projectName + "_manifest.xml"))
        interfaceStuff.runGame()
        
        
    def openFile(self, event):
        file = self.__trDirectory.getTree().GetItemText(event.GetItem())
        try:
            start = file.index(">") + 1
            file = file[start:]
            if not isdir(file) and file[-4:] != ".png" and file[-4:] != ".bam":
                self.__tbEditor.newEditor(file)
        except ValueError:
            branch = self.__trDirectory.getTree().GetSelection()
            if self.__trDirectory.getTree().IsExpanded(branch):
                self.__trDirectory.getTree().Collapse(branch)
            else:
                self.__trDirectory.getTree().Expand(branch)
        
        
        
    def removeFile(self, event):
        sure = wx.MessageDialog(self, message="Are you sure you want to permenantly delete this item?", caption="Remove Script From Project", style=wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL)
        if sure.ShowModal() == wx.ID_YES:
            try:
                file = self.__trDirectory.getTree().GetItemText(event.GetItem())
                start = file.index(">") + 1
                file = file[start:]
                if not isdir(file):
                    remove(file)
            except ValueError:
                branch = self.__trDirectory.getTree().GetItemText(event.GetItem())
                if branch == interfaceStuff.projectName or branch == "Assets" or branch == "Scenes" or branch == "Scripts":
                    wx.MessageDialog(self, "A core directory in the project cannot be removed.").ShowModal()
                else:
                    wx.MessageDialog(self, "This feature currently is not working, please delete from the normal file controls on your system for the time being. Sorry for any inconvenience.").ShowModal()
            interfaceStuff.updateManifest()
            self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")


    def newScript(self, event):
        created = self.__tbEditor.newScript(event)
        if created:
            interfaceStuff.updateManifest()
            self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
            
            
    def importGraphics(self, event):
        directories = wx.DirDialog(None, "Select the folder to import to " + interfaceStuff.projectName + " Project")
        with directories as dlg:
            isCopied = False
            if dlg.ShowModal() == wx.ID_OK:
                if interfaceStuff.gameMode == 2:
                    isCopied = interfaceStuff.grabSpriteSheetOrModel(dlg.GetPath(), ".png")
                elif interfaceStuff.gameMode == 3:
                    isCopied = interfaceStuff.grabSpriteSheetOrModel(dlg.GetPath(), ".bam")
                else:
                    isCopied = False
            if isCopied:
                self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
            else:
                wx.MessageDialog(self, "The selected folder could not be imported, please check the following issues and try again:\nThere is a project open\nThe folder contians only the apporpriate image type for this project (2d:.png, 3d: .bam)").ShowModal()
                
    
    def tlHelp(self, event):
        self.pyGameHelp(event)
        self.pythonHelp(event)
        self.panda3DHelp(event)
        
        
    def pythonHelp(self, event):
        webbrowser.open_new_tab("https://docs.python.org/3/library/index.html")
    
    
    def panda3DHelp(self, event):
        webbrowser.open_new_tab("https://docs.panda3d.org/1.10/python/reference/")
    
    
    def pyGameHelp(self, event):
        webbrowser.open_new_tab("https://www.pygame.org/docs/")





# =============================================================================
# Open Main Window
# =============================================================================
if __name__ == "__main__":
    app = wx.App()
    MainWindow(None, 1, title="threeP.games")
    app.MainLoop()