

##
# @package interfaceStuff
# The methods to interface with the selected game engines, 2d and 3d edting software, and a text editor for scripting to ease the task of constructing a game with PyGame and Panda3D.\n


from os import makedirs, listdir, system
from os.path import isdir, isfile, join, basename
from shutil import copytree
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
        toFile.write("The scenes folder is intended to be used to hold the scripts which\ndefine the various cut-scenes and/or levels of a game.\n")
    makedirs(join(location, "Assets"))
    with open(join(location, "Assets\\assets.txt"), "w") as toFile:
        toFile.write("The assets folder is intended to serve as the master location to\norganize the multitude of resources needed for a game, such as: images,\nmodels, sound files, etc.\n")
    makedirs(join(location, "Scripts"))
    with open(join(location, "Scripts\\scripts.txt"), "w") as toFile:
        toFile.write("The scripts folder is intended to serve as the master location to\norganize the vast quantity of custom scripts that will be needed to\nassemble a game.\n")
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
        toFile.write(dependencyToXML() + "\n\n\n")
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


def dependencyToXML():
    dependency = []
    for script in listdir(location):
        if not isdir(script) and script[-3:] == ".py":
            print("Checking: " + str((script)))
            dep = checkDependencies(location + "\\" + script)
            for d in dep:
                dependency.append(d)
    for script in listdir(location + "\\Scripts"):
        if not isdir(script) and script[-3:] == ".py":
            print("Checking: " + str((script)))
            dep = checkDependencies(location + "\\Scripts\\" + script)
            for d in dep:
                dependency.append(d)
    xml = "\t<dependencies>\n"
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
        destination = location + "\\Assets\\" + path[path.rindex("\\"):]
        copytree(path, destination)
        for infile in listdir(path):
            outfile = infile[0:-4] + ".bam"
            convert(join(path, infile), join(destination, outfile))
        updateManifest()
        return True
    else:
        return False



def systemPreview(file):
    command = "\"" + file + "\""
    system(command)
    
#************** GRAPHICS STUFF    



def editor2d():
    openInkscape = "C:\\Program Files\\Inkscape\\bin\\Inkscape.exe"
    subprocess.call(openInkscape, shell=True)
    



def editor3d():
    openBlender = "C:\\Program Files\\Blender Foundation\\Blender 2.82\Blender.exe"
    subprocess.call(openBlender, shell=True)
    
    
#*************** SCRIPTING STUFF



def scriptEditor():
    openTextEditor = "C:\\Program Files\\Notepad++\\notepad++.exe"
    subprocess.call(openTextEditor, shell=True)
    
    
    
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
def runGame():
    command = "python " + "\"" + location + "\\" + projectName + ".py\""
    system(command)



