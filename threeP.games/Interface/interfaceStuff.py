

##
# @package interfaceStuff
# The methods to interface with the selected game engines, 2d and 3d edting software, and a text editor for scripting to ease the task of constructing a game with PyGame and Panda3D.\n


from os import makedirs, listdir, system
from os.path import isdir, isfile, join, basename
from shutil import copytree, copy
import subprocess
from xml.sax.saxutils import escape as xml_escape
import xml.etree.ElementTree as ET
from gltf.converter import convert

from GameWriter import GameWriter2d, GameWriter3d

## Name for the current working project
projectName = ""

## 2d or 3d mode for the game, must be selected at creation of the project \(no default value assigned\)
gameMode = ""

## The working directory for the project
location = ""


## List of tubles describing the external applications to be used:  [(currently unused -filled with nonsense), (currently unused -filled with nonsense), (2d-editor, file-extension, icon, path), (3d-modeling, file-extension, icon, path)]
external = [("nonsense", ".nonsense", "nonsense.png", "C:\\nonsense"), ("nonsense", ".nonsense", "nonsense.png", "C:\\nonsense"), ("Inkscape", ".svg", "inkscape_logo.png", "\"C:\\Inkscape\\bin\\Inkscape.exe\""), ("Blender", ".blend", "blender_logo.png", "\"C:\\Program Files\\Blender Foundation\\Blender 2.82\Blender.exe\"")]



#**************  FILE STUFF


##
# Creates a new project at a specified location with a user selected name.\n
# The choice of 2d or 3d game must be entered by the user \(no default setting\).\n
# @param name A name for the game project
# @param mode A selection between a 2d or 3d game 
# @param dir the location the project will be created in 
# @return <b>void</b>
def newProj(name, mode, direct):
    global projectName, gameMode, location
    projectName = name
    gameMode = mode
    location = join(direct, projectName)
    makedirs(join(location, "Scenes"))
    with open(join(location, "Scenes\\scenes.txt"), "w") as toFile:
        toFile.write("The scenes folder is intended to be used to hold the scripts which\ndefine the various cut-scenes and/or levels of a game.\n\n\nThis file is included here for to-do lists and notes about the Scenes resources\nsince only new python scripts can be created from within the project.")
    makedirs(join(location, "Assets"))
    with open(join(location, "Assets\\assets.txt"), "w") as toFile:
        toFile.write("The assets folder is intended to serve as the master location to\norganize the multitude of resources needed for a game, such as: images,\nmodels, sound files, etc.\n\n\nThis file is included here for to-do lists and notes about the Assets resources\nsince only new python scripts can be created from within the project.")
    makedirs(join(location, "Scripts"))
    with open(join(location, "Scripts\\scripts.txt"), "w") as toFile:
        toFile.write("The scripts folder is intended to serve as the master location to\norganize the vast quantity of custom scripts that will be needed to\nassemble a game.\n\n\nThis file is included here for to-do lists and notes about the Scripts resources\nsince only new python scripts can be created from within the project.")
    copytree("images\\ModelBatchExports", location + "\\Scripts\\ModelBatchExports")
    updateManifest()



# Retrieves the directory structure of the project as a series of nested lists.\n
# @return <b>(["directories"["contents"[...]]])
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
def updateManifest():
    xmlString = directoryToXML(location)
    printXML(join(location, projectName + "_manifest.xml"), xmlString)



##
# A method to parse through the directory structure for the project and reformat it into an xml-string.\n
# Called to make updates to the project manifest.\n
# @param path The directory level to begin marking up the directory structure.
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
# @return <b>list</b> 
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
# @ return <b>str</b> An xml string with library tags nested inside of a dependency tag. 
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
# A method to import a folder of .png 2d-sprite-sheet images \n
# The folder must be named appropriately in advance and contain only .png files as it will simply copy the entire thing directly over to the Assets folder of the current project.
# @param path The directory where the sprite sheet was originally stored at
# @ return <b>bool</b> Representing success or failure of the task
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
 


##
# A method to import a folder of gltf format (.glb) animated 3d models \n
# The folder must be named appropriately in advance and contain only .glb files which will be copied to an identically named subdirectory of the Assets folder in the current project and generate identically named .bam files to use in Panda3D.\n
# @param path The directory where the gltf (.glb) files were originally located.
# @ return <b>bool</b> Representing success or failure of the task
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
    
 
    
##
# A method to bring the source files for graphics resources into the project. It checks for the filetype listed with the default editor listed for the project.
# @param path The original location of the graphics source file.
# @return <b>bool</b> representing the success (True) or failure (False) of the task.
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
# Opens non-meaningful-text files with the system defualt for such file types.
# @param filepath The location of the file to be opened. 
def systemPreview(filepath):
    command = "\"" + filepath + "\""
    result = subprocess.getoutput(command)
    return result
    
 
    
##
# A method to take in a filepath and pull out the name and file extension.
# @param filepath The file to extract the name and type data about
# @return <b>(str, str)</b> The name and then the extension.
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
# @return <b>sys.stdout</b>
def editor2d():
    openEditor = external[2][3]
    result = subprocess.getoutput(openEditor)
    return result


##
# Quick start for the chosen 2d graphics editing software, obviously far more useful with the interface linked to a GUI than text based
# @return <b>sys.stdout</b>
def editor3d():
    openBlender = external[3][3]
    result = subprocess.getoutput(openBlender)
    return result
    
   
#***************  GAME STUFF

##
# A call to the appropriate function of the GameWriter object for the mode set with the project
# @return <b>void</b>
def writeGame():
    if gameMode == 2:
        print(projectName, location)
        gw2 = GameWriter2d(projectName, location)
        gw2.directory = location
        gw2.writeGame()
    elif gameMode == 3:
        gw3 = GameWriter3d(projectName, location)
        gw3.directory = location
        gw3.writeGame()



##
# A method to actually run the game constructed in the project.\n
# Called from a run button on the GUI.\n
def runSystem():
    command = "python " + "\"" + location + "\\" + projectName + ".py\""
    #system(command)
    ###subprocess.call(command, shell=True)
    result = subprocess.getoutput(command)
    return result

    



