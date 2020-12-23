

##
# @package interfaceStuff
# The methods to interface with the selected game engines, 2d and 3d edting software, and a text editor for scripting to ease the task of constructing a game with PyGame and Panda3D.\n

import sys
from os import makedirs, listdir, system, remove
from os.path import isdir, isfile, join, basename
from shutil import copytree, copy
import subprocess
from xml.sax.saxutils import escape as xml_escape
import xml.etree.ElementTree as ET
from gltf.converter import convert

from GameWriter import GameWriter2d, GameWriter3d
#from GameObjects import Background2d, Player2d, Player3d, Stuff2d
from GameTools import startClass
#import imp


##
# registers saved default values for the MainWindow.py with interface stuff
# @returns <b>void</b>
def loadConfig():
    with open("threeP.config", "r") as fromConfig:
        for line in fromConfig:
            if "editor2d" in line:
                editor = line[line.find("&@")+2:-1].split(",")
                external[2] = tuple(editor)
            if "editor3d" in line:
                editor = line[line.find("&@")+2:-1].split(",")
                external[3] = tuple(editor)
                

## Name for the current working project
projectName = ""

## 2d or 3d mode for the game, must be selected at creation of the project \(no default value assigned\)
gameMode = ""

## The working directory for the project
location = ""


## List of tubles describing the external applications to be used:  [(currently unused -filled with nonsense), (currently unused -filled with nonsense), (2d-editor, file-extension, icon, path), (3d-modeling, file-extension, icon, path)]
external = [("nonsense", ".nonsense", "nonsense.png", "C:\\nonsense"), ("nonsense", ".nonsense", "nonsense.png", "C:\\nonsense"), ("nonsense", ".nonsense", "file_icon.png", "C:\nonsense"), ("nonsense", ".nonsense", "file_icon.png", "C:\nonsense")]
#("Inkscape", ".svg", "inkscape_logo.png", "\"C:\\Inkscape\\bin\\Inkscape.exe\""), ("Blender", ".blend", "blender_logo.png", "\"C:\\Program Files\\Blender Foundation\\Blender 2.82\Blender.exe\"")


# load the default 2d and 3d editor
loadConfig()


#**************  FILE STUFF


##
# Creates a new project at a specified location with a user selected name.\n
# The choice of 2d or 3d game must be entered by the user \(no default setting\).\n
# @param name A name for the game project
# @param mode A selection between a 2d or 3d game 
# @param dir the location the project will be created in 
# @returns <b>void</b>
def newProj(name, mode, direct):
    global projectName, gameMode, location
    projectName = name
    gameMode = mode
    location = join(direct, projectName)
    makedirs(join(location, "Scenes"))
    with open(join(location, "Scenes\\scenes.txt"), "w") as toFile:
        toFile.write("The scenes folder is intended to be used to hold the scripts which\ndefine the various cut-scenes and/or levels of a game.\nThis is where the objects to be used as backgrounds, characters, and\nprops in the game will go (things for the scene was my initial thought\nfor this organization scheme).\n\n\nThis file is included here for to-do lists and notes about the Scenes resources\nsince only new python scripts can be created from within the project.")
    makedirs(join(location, "Assets"))
    with open(join(location, "Assets\\assets.txt"), "w") as toFile:
        toFile.write("The assets folder is intended to serve as the master location to\norganize the multitude of resources needed for a game, such as: images,\nmodels, sound files, etc.\nThe raw data goes here, use the scene folder for creating the objects to be\nused in the game, and the scripts folder for additional controls on those objects.\n\n\nThis file is included here for to-do lists and notes about the Assets resources\nsince only new python scripts can be created from within the project.")
    makedirs(join(location, "Scripts"))
    with open(join(location, "Scripts\\scripts.txt"), "w") as toFile:
        toFile.write("The scripts folder is intended to serve as the master location to\norganize the vast quantity of custom scripts that will be needed to\nassemble a game.\n\n\nThis file is included here for to-do lists and notes about the Scripts resources\nsince only new python scripts can be created from within the project.")
    copytree("GUI\\Project Imports\\ModelBatchExports", location + "\\Scripts\\ModelBatchExports")
    copytree("GUI\\Project Imports\\GameScripts", location + "\\Scripts\\GameScripts")
    copytree("GUI\\Project Imports\\DefaultImages", location + "\\Assets\\DefaultImages")
    filepath = location + "\\Scenes\\GameInstance.py"
    if not isfile(filepath):
        with open(filepath, "w") as newFile:
            newFile.write("imports = []\n")
            newFile.write("inits = []\n")
            newFile.write("mains = []\n")
    updateManifest()



# Retrieves the directory structure of the project as a series of nested lists.\n
# @returns <b>(["directories"["contents"[...]]])
def getDirectoryList(pathList, path):
    for d in listdir(path):
        nextItem = join(path, d)
        pathList.append(d)
        if isdir(nextItem):
            pathList.append(getDirectoryList([], nextItem))
        else:
            return pathList
    return pathList
    



##
# Method to create and rewrite the manifest whenever something that should be in it is changed: files, folders, objects, images, etc. are added to the project.\n
# @returns <b>void</b>
def updateManifest():
    xmlString = directoryToXML(location)
    printXML(join(location, projectName + "_manifest.xml"), xmlString)
    writeTodoList()



##
# A method to parse through the directory structure for the project and reformat it into an xml-string.\n
# Called to make updates to the project manifest.\n
# @param path The directory level to begin marking up the directory structure.
# @returns <b>void</b>
def directoryToXML(path):
    xmlString = "<directory>\n\t<name>%s</name>\n" % xml_escape(basename(path))
    directories = []
    files = []
    for dirs in listdir(path):
        dirPath = join(path, dirs)
        if isdir(dirPath):
            directories.append(dirPath)
        else: 
            files.append(dirPath)
    if files:
        xmlString += "\t\t<files>\n" + "\n".join("\t\t\t<file>\n\t\t\t\t<name>%s</name>\n\t\t\t</file>" % xml_escape(f) for f in files) + "\n\t\t</files>\n\t"
    if directories:
        for d in directories:
            x = directoryToXML(join(path, d))
            xmlString += "\n".join("\t" + line for line in x.split("\n"))
    xmlString += "</directory>\n\n\n"
    return(xmlString)


##
# Method to actually write the xml-string from DirAsXML method to a file along with other pertinent data-fields about the project.\n
# @param filename The name of the file the xml formatted data will be written to.
# @param xml The xml string to write to the file.
# @returns <b>void</b>
def printXML(filename, xml):
    with open(filename, "w") as toFile:
        toFile.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        toFile.write("<MyPyGame>\n")
        toFile.write("\t\t<!-- PROJECT DETAILS -->\n")
        toFile.write("\t<project>" + projectName + "</project>\n")
        toFile.write("\t<mode>" + str(gameMode) + "</mode>\n")
        toFile.write("\t<location>" + location + "</location>\n\n\n")
        toFile.write("\t\t<!-- PROJECT RESOURCES -->\n")
        toFile.write("\t" + xml + "\n\n\n")
        toFile.write("\t\t<!-- PYTHON SCRIPT DEPENDENCIES -->\n")
        toFile.write(dependencyToXML(location) + "\n\n\n")
        toFile.write("</MyPyGame>")
        


##
# A method to parse the data back out of the manifest for the project, i.e. open a project.\n
# @param path The path to and including the *__manifest.xml file
# @returns <b>void</b>
def xmlParseManifest(path):
    global projectName, gameMode, location
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        if child.tag == "project":
            projectName = child.text
        elif child.tag == "mode":
            gameMode = int(child.text)
        elif child.tag == "location":
            location = child.text
  

    
            


##
# A method to check a python script and produce a list of the imported libraries.\n
# @param path The filepath for the python script to be checked
# @returns <b>list</b> 
def checkDependencies(path):
    if path[-3:] != ".py":
        return False
    else:
        dependency = []
        with open(path, "r") as script:
            for line in script:
                if line[0:6] == "import":
                    line = line[7:]
                    dependency.append(line[0:-1])
                elif line[0:4] == "from":
                    line = line[5:]
                    dependency.append(line[0:line.index(" ")])
    return dependency



##
# Checks the project for all the imports in python scripts and returns all of the libraries used in a project to an xml-string.\n
# @ returns <b>str</b> An xml string with library tags nested inside of a dependency tag. 
def dependencyToXML(path):
    xml = ""
    name = ""
    for script in listdir(path):
        dependency = []
        if not isdir(join(path, script)) and script[-3:] == ".py":
            dep = checkDependencies(join(path, script))
            for d in dep:
                dependency.append(d)
        elif isdir(join(path, script)):
            xml += dependencyToXML(join(path, script))
        if len(dependency) > 0:
            xml += "\t<dependencies script=\"" + script + "\">\n"
            for lib in dependency:
                xml += "\t\t<library>" + lib + "</library>\n"
            xml += "\t</dependencies>\n"
    return xml



##
# Check a single file for todo annotations ('\@todo') in comments.\n
# @returns <b>str</b> A string listing the filename and all todo annotations
def checkTodo(filepath):
    stuff = "\n\n" + filepath + "\n"
    with open(filepath, "r") as checkfile:
        number = 0
        for line in checkfile:
            if "@todo" in line:
                stuff += "\t" + str(number) + "\t|\t" + line[line.find("@todo") + 6:]
            number += 1
    if stuff == "\n\n" + filepath + "\n":
        stuff = ""
    return stuff


##
# Checks all files in the project for any todo annotations ('\@todo') in comments
# @returns <b>str</b> String to be written to a file indicating which tasks are listed in which files
def todoList(path):
    tasks = ""
    if isdir(path):
        for item in listdir(path):
            if isfile(path + "\\" + item):
                if item[-3:] == ".py":
                    tasks += checkTodo(path + "\\" + item)
            else:
                tasks += todoList(path + "\\" + item)
    return tasks


##
# Checks the python scripts for todo annotations ('\@todo') in comments and writes it in a textfile to help keep track of all the upcoming tasks.
# @returns <b>void</b>
def writeTodoList():
    tasks = todoList(location)
    if len(tasks) == 0:
        tasks = "\n\nNothing on the todo list\n\nUse @todo annotation in comments to add tasks to this list"
    with open(location + "\\" + "TO-DO.txt", "w") as toFile:        
        toFile.write(tasks)
        
        
"""
##
# A method to import a folder of .png 2d-sprite-sheet images \n
# The folder must be named appropriately in advance and contain only .png files as it will simply copy the entire thing directly over to the Assets folder of the current project.
# @param path The directory where the sprite sheet was originally stored at
# @ returns <b>bool</b> Representing success or failure of the task
def grabSpriteSheet(path):
    allGood = True
    for file in listdir(path):
        if not isfile(join(path,file)) or  file[-4:] != ".png":
            allGood = False
    if allGood:
        if not isdir(location + "\\Assets\\" + path[path.rindex("\\"):]):
            copytree(path, location + "\\Assets\\" + path[path.rindex("\\"):])
            updateManifest()
        return True
    else:
        return False
"""
    
##
# A method to import a folder of image assets.\n
# @param path The directory where the assets were originally stored at
# @ returns <b>bool</b> Representing success or failure of the task
def grabAssets(path):
    destination = location + "\\Assets\\" + basename(path)
    if not isdir(destination):
        copytree(path, destination)
        converts = makeBam(destination)
        updateManifest()
        return True
    elif isdir(destination):
        for item in listdir(path):
            copy(path + "\\" + item, destination)
        converts = makeBam(destination)
        updateManifest()
        return True
    else:
        return False
    
 

"""
##
# A method to import a folder of gltf format (.glb) animated 3d models \n
# The folder must be named appropriately in advance and contain only .glb files which will be copied to an identically named subdirectory of the Assets folder in the current project and generate identically named .bam files to use in Panda3D.\n
# @param path The directory where the gltf (.glb) files were originally located.
# @ returns <b>bool</b> Representing success or failure of the task
def grabModel(path):
    allGood = True
    for file in listdir(path):
        if not isfile(join(path,file)) or  file[-4:] != ".glb":
            allGood = False
    if allGood:
        if not (location + "\\Assets\\") in path:
            destination = location + "\\Assets\\" + path[path.rindex("\\"):]
            copytree(path, destination)
        else:
            destination = path
        for infile in listdir(path):
            outfile = infile[0:-4] + ".bam"
            convert(join(path, infile), join(destination, outfile))
        updateManifest()
        return True
    else:
        return False
"""
    

##
# A method to convert files for animated 3d models in gltf format (.glb)  into .bam files for use in Panda3d\n
# @param path The directory where the gltf (.glb) files were originally located.
# @ returns <b>int</b> Representing number of file conversions
def makeBam(source, destination=""):
    if destination == "":
        destination = source
    counter = 0
    for infile in listdir(source):
        try:
            if infile[-4:] == ".glb":
                outfile = infile[0:-4] + ".bam"
                convert(join(source, infile), join(destination, outfile))
                counter += 1
        except:
            pass
    updateManifest()
    return counter

    
 
    
##
# A method to bring the source files for graphics resources into the project. It checks for the filetype listed with the default editor listed for the project.
# @param path The original location of the graphics source file.
# @returns <b>bool</b> representing the success (True) or failure (False) of the task.
def grabGraphicsSource(path):
    name, extension = getFileStuff(path)
    allGood = True
    if allGood:
        if extension == external[2][1] or extension == external[3][1] or extension == ".png":
            if not (location + "\\Assets\\") in path:
                destination = location + "\\Assets\\" + path[path.rindex("\\"):]
                copy(path, destination)
            updateManifest()
            return True
    else:
        return False
    
    

##
# A method to add a new game object to the scene folder.
# @param name The name for the new object
# @param obj The type of object, either a player or background so far.
# @returns <b>bool</b> indicating the success or failure of the task
def newSceneObject(name, obj, asset):
    rewrite = ["import sys\n", "sys.path.insert(1, \"" + location.replace("\\", "\\\\") + "\")\n"]
    parent = obj + str(gameMode) + "d"
        # creates the game object class
        # rewrites the file with current project as a module source
        # assigns an asset folder to the object
        # adds in args and kwargs for the parent class
    startClass(module=name, name=name, parent=parent, attributes=["Asset"], directory=location + "\\Scenes")
    rewrite.append("from Scripts.GameScripts.GameObjects import " + parent + "\n")
    with open(location + "\\Scenes\\" + name + ".py", "r") as fromFile:
        for line in fromFile:
            if "def __init__" in line:
                line = line.replace("Asset", "Asset=\"" + asset.replace("\\", "\\\\") + "\"")
                line = line[0:-3] + ", *args, **kwargs):\n"
                line += "        super().__init__(*args, **kwargs)\n"
                line += "        #--> This Area for interface usage, best to leave it alone there are already getters and seters for these things\n"
                line += "        #? start inspector read\n"
                line += "        self.setX(0)\n        self.setY(0)\n        self.setZ(0)\n"
                if gameMode == 2:
                    line += "        self.setH(0)\n"
                elif gameMode == 3:
                    line += "        self.setH(0)\n        self.setP(0)\n        self.setR(0)\n"
                line += "        #? end inspector read\n"
                if gameMode == 2:
                    line += "        self.loadSprite(Asset)\n"
                    line += "        #print(\"Animations: \" + str(self.getSprite().keys()))\n"
                    #line += "        print(\"Animations: \" + str(self.getSprite()))\n"
                if gameMode == 3:
                    line += "        self.loadActor(Asset)\n"
                    line += "        #print(\"Animations: \" + str(self.getActor()))\n"
            rewrite.append(line)
    rewrite.append("\n\n        # @todo finish out the class by completeing the start, update, and render methods below, remember to put any new attributes before args and kwargs in the constructor\n\n")
    rewrite.append("\n\n        # @todo If you did not use the Blender export scripts, or store spritesheet/model in the same manner you will need to override (2d) .loadSprite(asset) or (3d) .loadActor(asset) methods as well\n\n")
    rewrite.append("\n\n    def start(self):\n        # @todo define any necessary initialization actions for this object\n        pass")
    if gameMode == 2:
        rewrite.append("\n\n    def update(self):\n        # @todo define actions to be called every frame of the game, remember to call move here\n        pass")
        rewrite.append("\n\n    def render(self, game):\n        # @todo define how this object is to be rendered\n        pass\n")
    elif gameMode == 3:
        rewrite.append("\n\n    def update(self,task):\n        # @todo define actions to be called every frame of the game, remember to call move here\n        return task.cont")
        rewrite.append("\n\n    def render(self, task):\n        # @todo define how this object is to be rendered\n        return task.cont\n")
    rewrite.append("\n\n\n    # @todo Create and import custom scripts to enhance functionality of this game object")
    with open(location + "\\Scenes\\" + name + ".py", "w") as toFile:
        for line in rewrite:
            toFile.write(line)
    return addSceneObject(name, obj)


##
# When a new object is created this adds it to a module containing the strings that will actually be used to manipulate transform data in the interface and written to the game file.
# @param name The name of the game object to add to the list, must be in a .py file with the same name as the game object, i.e. one class per file and names match
# @returns <b>bool</b> Indicating success or failure of the task
def addSceneObject(name, obj=""):
    imports = []
    inits = []
    mains = []
    filepath = location + "\\Scenes\\GameInstance.py"
    if not isfile(filepath):
        with open(filepath, "w") as newFile:
            newFile.write("imports = []\n")
            newFile.write("inits = []\n")
            newFile.write("mains = []\n")
    sys.path.insert(0, location)
    import Scenes.GameInstance
    imports = Scenes.GameInstance.imports
    inits = Scenes.GameInstance.inits
    mains = Scenes.GameInstance.mains
    imports.append("from Scenes." + name + " import " + name)
    if gameMode == 2:
        inits.append("m_" + name + " = " +  name + "()")
        inits.append("m_" + name + ".start()")
        mains.append("m_" + name + ".update()")
        mains.append("m_" + name + ".render(scene)")
    elif gameMode == 3:
        if obj == "Player":
            inits.append("self.m_" + name + " = " +  name + "(watcher=base.mouseWatcherNode)")
        else:
            inits.append("self.m_" + name + " = " +  name + "()")
        inits.append("self.m_" + name + ".start()")
        inits.append("self.m_" + name + ".getActor().reparentTo(self.render)\n")
        mains.append("self.taskMgr.add(self.m_" + name + ".update, \"m_" + name + "_Update\")")
        mains.append("self.taskMgr.add(self.m_" + name + ".render, \"m_" + name + "_Render\")")
    with open(filepath, "w") as toFile:
        toFile.write("imports = ")
        toFile.write(str(imports))
        toFile.write("\n")
        toFile.write("inits = ")
        toFile.write(str(inits))
        toFile.write("\n")
        toFile.write("mains = ")
        toFile.write(str(mains))
        toFile.write("\n")
    sys.modules.pop("Scenes.GameInstance")
    sys.path.pop(0)
    return True



    


##
# Opens non-meaningful-text files with the system defualt for such file types.
# @param filepath The location of the file to be opened. 
# @returns <b>str</b> The sys.stdout echoes from running the subprocess
def systemPreview(filepath):
    command = filepath
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout, result.stderr
    
 
    
##
# A method to take in a filepath and pull out the name and file extension.
# @param filepath The file to extract the name and type data about
# @returns <b>(str, str)</b> The name and then the extension.
def getFileStuff(filepath):
    name = filepath
    try:
        start = name.rindex("\\") + 1
    except:
        start = 0
    name = name[start:]
    dot = name.rindex(".")
    extension = name[dot:]
    return name, extension
    
#************** GRAPHICS STUFF    


##
# Quick start for the chosen 2d graphics editing software, obviously far more useful with the interface linked to a GUI than text based
# @returns <b>str</b> The sys.stdout echoes from running the subprocess
def editor2d():
    command = external[2][3]
    result = subprocess.run(command, capture_output=True)
    return result.stdout, result.stderr


##
# Quick start for the chosen 2d graphics editing software, obviously far more useful with the interface linked to a GUI than text based
# @returns <b>str</b> The sys.stdout echoes from running the subprocess
def editor3d():
    command = external[3][3]
    result = subprocess.run(command, capture_output=True)
    return result.stdout, result.stderr
    
   
#***************  GAME STUFF

##
# A call to the appropriate function of the GameWriter object for the mode set with the project
# @returns <b>void</b>
def writeGame():
    remove(location + "\\Scenes\\GameInstance.py")
    for item in listdir(location + "\\Scenes"):
        if item[-3:] == ".py" and item != "GameInstance.py":
            with open(location + "\\Scenes\\" + item, "r") as checkScript:
                for line in checkScript:
                    if line[:5] == "class":
                        name = line[6: line.index("(")]
                        obj = line[line.index("(")+1:-5]
                        addSceneObject(name, obj)
    sys.path.insert(0, location)
    import Scenes.GameInstance
    imports = Scenes.GameInstance.imports
    inits = Scenes.GameInstance.inits
    mains = Scenes.GameInstance.mains
    if gameMode == 2:
        gw2 = GameWriter2d(projectName, location)
        gw2.directory = location
        gw2.localDirectory(location)
        gw2.importsSection(imports)
        gw2.initializeSection(inits)
        gw2.mainSceneSection(mains)
        gw2.writeGame()
    elif gameMode == 3:
        gw3 = GameWriter3d(projectName, location)
        gw3.directory = location
        gw3.localDirectory(location)
        gw3.importsSection(imports)
        gw3.initializeSection(inits)
        gw3.mainSceneSection(mains)
        gw3.writeGame()
    sys.modules.pop("Scenes.GameInstance")
    sys.path.pop(0)






##
# A method to actually run the game constructed in the project.\n
# Called from a run button on the GUI.\n
# @returns <b>str</b> The sys.stdout echoes from running the subprocess
def runSystem():
    command = "python " + "\"" + location + "\\" + projectName + ".py\""
    result = subprocess.run(command, capture_output=True)
    return result.stdout, result.stderr

    



