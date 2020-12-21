# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 03:21:17 2020

@author: Christopher S. Francis
"""

import sys
from os import remove, rmdir, execl, listdir
from os.path import join, isfile, isdir, basename, dirname, abspath
sys.path.insert(0, dirname(abspath(__file__)) + "\\Interface")
sys.path.insert(1, dirname(abspath(__file__)) + "\\GUI\\Components")
sys.path.insert(2, dirname(abspath(__file__)) + "\\kernal")
import wx
import webbrowser
import interfaceStuff
from EditorTab import EditorTab
from InspectorTab import InspectorTab
from ProjectTree import ProjectTree
from Dialogs.NewProjectDialog import NewProjectDialog
from Dialogs.NewScriptDialog import NewScriptDialog
from Dialogs.NewSceneDialog import NewSceneDialog
from Dialogs.StdOutDialog import StdOutDialog
from Dialogs.SetEditorDialog import SetEditorDialog



class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
            # project data fields
        self.__projectName = "Test Game"
        self.__gameMode = 2
        self.__location = "C:\\Users\\Chris\\Documents\\delete"
        
            # window settings
        self.__icon = wx.Icon("GUI\\images\\threeP_logo.ico")
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
        self.__mnRunGame = self.__mnRun.Append(wx.Window.NewControlId(), "Run in System", helpString="Generate the game file and run in system console...")
        
            # run menu events
        self.Bind(wx.EVT_MENU, self.runGame, self.__mnRunGame)
        
            # construct asset menu
        self.__mnAssets = wx.Menu()
        self.__mnImportGraphics = self.__mnAssets.Append(wx.Window.NewControlId(), "Import Graphics Folder", helpString="Import a prepared folder of .png or .bam files...")
        self.__mnImportSource = self.__mnAssets.Append(wx.Window.NewControlId(), "Import Graphics/Model Editor File", helpString="Import the editable source file for the graphics")
        
            # asset menu events
        self.Bind(wx.EVT_MENU, self.importGraphics, self.__mnImportGraphics)
        self.Bind(wx.EVT_MENU, self.importSource, self.__mnImportSource)
        
            # construct scene menu
        self.__mnScene = wx.Menu()
        self.__mnNewScene = self.__mnScene.Append(wx.Window.NewControlId(), "New Scene Object", helpString="Creates a new scene object...")
        
            # scene menu events
        self.Bind(wx.EVT_MENU, self.newScene, self.__mnNewScene)
        
            # construct external menu
        self.__mnExternal = wx.Menu()
        self.__mnGraphics2d = self.__mnExternal.Append(wx.Window.NewControlId(), "Open {2d editor not set}", helpString="Opens the selected 2d graphics editing software...")
        self.__mnGraphics3d = self.__mnExternal.Append(wx.Window.NewControlId(), "Open {3d editor not set}" + interfaceStuff.external[3][0], helpString="Opens the selected 3d graphics editing software...")
        if  interfaceStuff.external[2][0] != "nonsense":
            self.__mnGraphics2d.SetItemLabel("Open " + interfaceStuff.external[2][0])
        if  interfaceStuff.external[3][0] != "nonsense":
            self.__mnGraphics3d.SetItemLabel("Open " + interfaceStuff.external[3][0])
            # external menu events
        self.__mnSetEditor2d = self.__mnExternal.Append(wx.Window.NewControlId(), "Set 2d Graphics Editing Software", helpString="Sets a 2d graphics editing software to work with")
        self.__mnSetEditor3d = self.__mnExternal.Append(wx.Window.NewControlId(), "Set 3d Modeling Software", helpString="Sets a 3d graphics editing software to work with")
        self.__mnMakeBam = self.__mnExternal.Append(wx.Window.NewControlId(), "Convert Exported Folder to Bam", helpString="Convert Exported Folder to Bam (hopefully this will be automatic soon)")
        self.Bind(wx.EVT_MENU, self.open2dEditor, self.__mnGraphics2d)
        self.Bind(wx.EVT_MENU, self.open3dEditor, self.__mnGraphics3d)
        self.Bind(wx.EVT_MENU, self.setEditor2d, self.__mnSetEditor2d)
        self.Bind(wx.EVT_MENU, self.setEditor3d, self.__mnSetEditor3d)
        self.Bind(wx.EVT_MENU, self.gltf2bam, self.__mnMakeBam)
        
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
        self.__mnMain.Append(self.__mnScene, "Scene")
        self.__mnMain.Append(self.__mnExternal, "External")
        self.__mnMain.Append(self.__mnHelp, "Help")
        self.SetMenuBar(self.__mnMain)
    
    
    def toolBar(self):
        self.__tlMain = self.CreateToolBar()
        
            # tools
        self.__tlNewProject = self.__tlMain.AddTool(wx.Window.NewControlId(), "New Project", wx.Bitmap("GUI\\images\\new_project.png"), shortHelp="Create a New Project")
        self.__tlOpenProject = self.__tlMain.AddTool(wx.Window.NewControlId(), "Open Project", wx.Bitmap("GUI\\images\\folder_icon.png"), shortHelp="Open an Existing Project")
        self.__tlCloseProject = self.__tlMain.AddTool(wx.Window.NewControlId(), "Close Project", wx.Bitmap("GUI\\images\\close_project.png"), shortHelp="Close the Current Project")
        self.__tlMain.AddSeparator()
        self.__tlNewScript = self.__tlMain.AddTool(wx.Window.NewControlId(), "New Script", wx.Bitmap("GUI\\images\\file_icon.png"), shortHelp="Create a New Python Script")
        self.__tlNewScene = self.__tlMain.AddTool(wx.Window.NewControlId(), "New Scene Object", wx.Bitmap("GUI\\images\\new_scene.png"), shortHelp="Create a New Scene Object")
        self.__tlImportGraphics = self.__tlMain.AddTool(wx.Window.NewControlId(), "Import Graphics Folder", wx.Bitmap("GUI\\images\\graphics_icon.png"), shortHelp="Import an Asset Folder")
        self.__tlImportSource = self.__tlMain.AddTool(wx.Window.NewControlId(), "Imort Graphics/Model Editor Source", wx.Bitmap("GUI\\images\\edit_source.png"), shortHelp="Import a Graphics Source File")
        self.__tlMain.AddSeparator()
        self.__tlRunGame = self.__tlMain.AddTool(wx.Window.NewControlId(), "Run", wx.Bitmap("GUI\\images\\run_button.png"), shortHelp="Run Game in a System Console")
        self.__tlMain.AddSeparator()
        self.__tlHelp = self.__tlMain.AddTool(wx.Window.NewControlId(), "Help", wx.Bitmap("GUI\\images\\help_icon.png"), shortHelp="Quick Access to Python, PyGame, and Panda3d API's")
        
            # tool bar events (that don't have to wait on other components)
        self.Bind(wx.EVT_TOOL, self.CloseCurrentProject, self.__tlCloseProject)
        self.Bind(wx.EVT_TOOL, self.runGame, self.__tlRunGame)
        self.Bind(wx.EVT_TOOL, self.CreateNewProject, self.__tlNewProject)
        self.Bind(wx.EVT_TOOL, self.OpenExistingProject, self.__tlOpenProject)
        self.Bind(wx.EVT_TOOL, self.newScene, self.__tlNewScene)
        self.Bind(wx.EVT_TOOL, self.importGraphics, self.__tlImportGraphics)
        self.Bind(wx.EVT_TOOL, self.importSource, self.__tlImportSource)
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
        self.__trImages = [wx.Icon("GUI\\images\\python_logo.png"), wx.Icon("GUI\\images\\file_icon.png"), wx.Icon("GUI\\images\\folder_icon.png"), wx.Icon("GUI\\images\\manifest_icon.png"), wx.Icon("GUI\\images\\threeP_logo.ico"), wx.Icon("GUI\\images\\graphics_icon.png")]
        self.__trImages.append(wx.Icon("GUI\\images\\" + interfaceStuff.external[3][2])) #3d editor will be index 6
        self.__trImages.append(wx.Icon("GUI\\images\\" + interfaceStuff.external[2][2])) #2d editor will be index 7
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
                interfaceStuff.updateManifest()
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
        # if not isfile(interfaceStuff.location + "\\" + interfaceStuff.projectName + ".py"):
        interfaceStuff.writeGame()
        interfaceStuff.updateManifest()
        self.__trDirectory.loadProject(join(interfaceStuff.location, interfaceStuff.projectName + "_manifest.xml"))
        echo = interfaceStuff.runSystem()
        sod = StdOutDialog(self, echo)
        if sod.ShowModal() == wx.ID_OK:
            self.__tbEditor.newEditor(sod.copyMessage())
            interfaceStuff.updateManifest()
            self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
        
        
    def openFile(self, event):
        filepath = self.__trDirectory.getTree().GetItemText(event.GetItem())
        try:
            start = filepath.index(">") + 1
            filepath = filepath[start:]
            name, extension = interfaceStuff.getFileStuff(filepath)
            if not isdir(filepath) and extension != ".png" and extension != ".glb" and extension != ".bam" and extension != ".ico" and extension != interfaceStuff.external[2][1] and extension != interfaceStuff.external[3][1]:
                result = self.__tbEditor.newEditor(filepath)
                if result == "Scene":
                    self.__tbInspector.openObject(filepath)
            elif extension == ".png" or extension == ".glb" or extension == interfaceStuff.external[2][1] or extension == interfaceStuff.external[3][1]:
                echo = interfaceStuff.systemPreview(filepath)
                sod = StdOutDialog(self, echo)
                if sod.ShowModal() == wx.ID_OK:
                    self.__tbEditor.newEditor(sod.copyMessage())
                    interfaceStuff.updateManifest()
                    self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
            
            elif extension == ".bam":
                wx.MessageDialog(self, "No preview of a Binary-Compressed Sequence Alignment/Map available, see https://samtools.github.io/hts-specs/SAMv1.pdf for details.\nThis file is here because the Panda3D engine uses it, select the associated gltf(.glb) file for a preview of the animated model.").ShowModal()
            elif extension == ".ico":
                wx.MessageDialog(self, "Unable to open .ico file with default system settings, try opening it manually from inside graphics editing software.").ShowModal()
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
        if interfaceStuff.projectName == "":
            wx.MessageDialog(self, "A script cannot be created without a project to save it to.\nPlease open or create a project and try again.").ShowModal()
        else:
            created = self.__tbEditor.newScript(event)
            if created:
                interfaceStuff.updateManifest()
                self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
                
            
    def importGraphics(self, event):
        if interfaceStuff.projectName == "":
            wx.MessageDialog(self, "An asset cannot be imported without a project to import it to.\nPlease open or create a project and try again.").ShowModal()
        else:
            directories = wx.DirDialog(None, "Select the folder to import to " + interfaceStuff.projectName + " Project")
            with directories as dlg:
                isCopied = False
                if dlg.ShowModal() == wx.ID_OK:
                    if interfaceStuff.gameMode == 2 or interfaceStuff.gameMode == 3:
                        isCopied = interfaceStuff.grabAssets(dlg.GetPath())
                    else:
                        isCopied = False
                if isCopied:
                    interfaceStuff.updateManifest()
                    self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
                else:
                    wx.MessageDialog(self, "The selected folder could not be imported, please check the following issues and try again:\nThere is a project open").ShowModal()
    
    
    def importSource(self, event):
        if interfaceStuff.projectName == "":
            wx.MessageDialog(self, "An asset cannot be imported without a project to import it to.\nPlease open or create a project and try again.").ShowModal()
        else:
            directories = wx.FileDialog(None, "Select the folder to import to " + interfaceStuff.projectName + " Project", wildcard="Graphics Source File (*.blend, *.png, *.svg)|*.blend;*.png;*.svg")
            with directories as dlg:
                isCopied = False
                if dlg.ShowModal() == wx.ID_OK:
                    isCopied = interfaceStuff.grabGraphicsSource(dlg.GetPath())
                if isCopied:
                    interfaceStuff.updateManifest()
                    self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
                else:
                    wx.MessageDialog(self, "The selected file could not be imported, please check the following issues and try again:\nThere is a project open...").ShowModal()
                    
    
    def gltf2bam(self, event):
        if interfaceStuff.projectName == "":
            wx.MessageDialog(self, "Assets cannot be converted without a project open, this option is for existing assets only.\nPlease open or create a project and try again.").ShowModal()
        else:
            directories = wx.DirDialog(None, "Select the folder containing the gltf(.glb) files to convert")
            with directories as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    if interfaceStuff.gameMode == 2 or interfaceStuff.gameMode == 3:
                        converts = interfaceStuff.makeBam(dlg.GetPath())
                if converts > 0:
                    interfaceStuff.updateManifest()
                    self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
                else:
                    wx.MessageDialog(self, "None of the files in selected folder could not be converted, please check the following issues and try again:\nThere is a project open\nThere are gltf(.glb) files present in the selected folder").ShowModal()
    
                
    def newScene(self, event):
        if interfaceStuff.projectName == "":
            wx.MessageDialog(self, "An scene object cannot be imported without a project to import it to.\nPlease open or create a project and try again.").ShowModal()
        else:
            scn = NewSceneDialog(self)
            isCopied = False
            if scn.ShowModal() == wx.ID_OK:
                isCopied = interfaceStuff.newSceneObject(scn.getName(), scn.getObject(), scn.getAsset())
                if isCopied:
                    interfaceStuff.updateManifest()
                    self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
                else:
                    wx.MessageDialog(self, "The selected file could not be imported, please check the following issues and try again:\nThere is a project open...").ShowModal()
                    
    
    def setEditor2d(self, event):
        sed = SetEditorDialog(self)
        if sed.ShowModal() == wx.ID_OK:
            config = []
            editor = sed.getName() + "," + sed.getFiletype() + "," + sed.getIcon() + ",\"" + sed.getLocation() + "\"\n"
            with open("threeP.config", "r") as fromConfig:
                for line in fromConfig:
                    config.append(line)
                for c in config:
                    if "editor2d" in c:
                        config.remove(c)
                config.append("editor2d &@" + editor)
            with open("threeP.config", "w") as toConfig:
                for line in config:
                    toConfig.write(line)
            wx.MessageDialog(self, "Please restart threeP.games for these changes to take effect.").ShowModal()
    
    
    def open2dEditor(self, event):
        echo = interfaceStuff.editor2d()
        sod = StdOutDialog(self, echo)
        if sod.ShowModal() == wx.ID_OK:
            self.__tbEditor.newEditor(sod.copyMessage())
            interfaceStuff.updateManifest()
            self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
            
            
    def setEditor3d(self, event):
        sed = SetEditorDialog(self)
        if sed.ShowModal() == wx.ID_OK:
            config = []
            editor = sed.getName() + "," + sed.getFiletype() + "," + sed.getIcon() + ",\"" + sed.getLocation() + "\"\n"
            with open("threeP.config", "r") as fromConfig:
                for line in fromConfig:
                    config.append(line)
                for c in config:
                    if "editor3d" in c:
                        config.remove(c)
                config.append("editor3d &@" + editor)
            with open("threeP.config", "w") as toConfig:
                for line in config:
                    toConfig.write(line)
            wx.MessageDialog(self, "Please restart threeP.games for these changes to take effect.").ShowModal()
    
    
    
    def open3dEditor(self, event):
        echo = interfaceStuff.editor3d()
        sod = StdOutDialog(self, echo)
        if sod.ShowModal() == wx.ID_OK:
            self.__tbEditor.newEditor(sod.copyMessage())
            interfaceStuff.updateManifest()
            self.__trDirectory.loadProject(interfaceStuff.location + "\\" + interfaceStuff.projectName + "_manifest.xml")
            
    
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