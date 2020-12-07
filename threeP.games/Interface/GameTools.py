# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:07:27 2020

@author: Christopher S. Francis
"""


##
# @package GameTools
# A collection of methods to make it easier to add scripting functionality to custom game objects

from os import path, makedirs

##
# A method to create the start for a python class structure with getters and setters for all the attributes.\n
# @param module The python module (a.k.a. file) to write the object to, it writes in append mode so it will not delete objects and methods already in the module.
# @param name The name for this class
# @param parent The class the new class will inherit from if applicable
# @param attributes[] A list of strings representing all the desired attributes for the class. Each element in this list will be added to the __init__ constructor and have a getter and setter method generated.
# @param directory The directory to write the objects to, will be created if it does not already exist
def startClass(module="myModule", name="myClass", parent="", attributes=[], directory=""):
    if not path.exists(directory) and directory != "":
        makedirs(directory)
    if directory[-2:] != "\\":
        directory = directory + "\\"
    with open(directory + module + ".py", mode="a") as createClass:
        createClass.write("\n")
        createClass.write("\n")
        createClass.write("\n")
        createClass.write("class " + name + "(" + parent + "):\n")
        createClass.write("    def __init__(self")
        if len(attributes) == 0:
            createClass.write("):\n")
            if parent != "":
                createClass.write("        super().__init__()\n")
            else:
                createClass.write("        pass")
        else:
            createClass.write(", ") 
        for att in attributes:
            if att != attributes[-1]:
                createClass.write(att + ", ") 
            else:
                createClass.write(att + "):\n")
        
        for att in attributes:
            createClass.write("        self.__" + att + " = " + att + "\n")
        
        for att in attributes:
            createClass.write("\n")
            first = att[0]
            createClass.write("    def get" + att.replace(first, first.upper(), 1) + "(self):\n")
            createClass.write("        return self.__" + att + "\n")
            
        for att in attributes:
            createClass.write("\n")
            first = att[0]
            createClass.write("    def set" + att.replace(first, first.upper(), 1) + "(self, " + att + "):\n")
            createClass.write("        self.__" + att + " = " + att +"\n")
        
        
##
# A method to generate a set up a new task and add it to the task manager in the Panda3D engine.\n
# Currently this is only set up to work if there is only one single class per file or a module of non-class methods to import
# @param name A name for the task to be added to the Panda3D task manager
# @param module The module (a.k.a. python file) to add the task into, if omitted it will be added directly to the main game object
# @param directory The directory to write the objects to, will be created if it does not already exist
def startTask(name, module="", directory=""):
    if module == "":
        # @todo: If no module name entered add directly to the child of ShowBase in the current project
        pass
    else:
        if not path.exists(directory) and directory != "":
            makedirs(directory)
        if directory[-2:] != "\\":
            directory = directory + "\\"
        containsObjects = False
        if path.exists(directory + "\\" + module+".py"):
            with open(directory + "\\" + module + ".py", mode="r") as checkScript:
                for line in checkScript:
                    if "class" in line:
                        containsObjects = True
            if containsObjects:
                with open(directory + "\\" + module + ".py", mode="a") as addTask:
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("    def " + name + "(self, task):")
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("        return task.cont")
            else:
                with open(directory + "\\" + module + ".py", mode="a") as addTask:
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("def " + name + "(task):")
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("    return task.cont")
                    addTask.write("\n")
        else:
            with open(directory + "\\" + module + ".py", mode="a") as addTask:
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("def " + name + "(task):")
                    addTask.write("\n")
                    addTask.write("\n")
                    addTask.write("    return task.cont")
                    addTask.write("\n")
    


##
# A method to generate the method header and attach it to an object or module.\n
# Currently this is only set up to work if there is only one single class per file or a module of non-class methods to import
# @param name A name for the function to be added to an object for either a 2d or 3d game
# @param module The module (a.k.a. python file) to add the function into, if omitted it will be added directly to the module containing the main game object
# @param parameters A list of strings representing the parameters that will be needed for the method
def startFunction(name, module="", parameters=[], directory=""):
    if module == "":
        # @todo: If no module name entered add directly to the main module of the 2d or 3d game in the current project
        pass
    else:
        if not path.exists(directory) and directory != "":
            makedirs(directory)
        if directory[-2:] != "\\":
            directory = directory + "\\"
        containsObjects = False
        if path.exists(directory + module+".py"):
            with open(directory + module + ".py", mode="r") as checkScript:
                for line in checkScript:
                    if "class" in line:
                        containsObjects = True
            if containsObjects:
                with open(directory + module + ".py", mode="a") as addFunc:
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("    def " + name + "(self")
                    if len(parameters) == 0:
                        addFunc.write("):")
                    else:
                        addFunc.write(", ")
                    for p in parameters:
                        if p != parameters[-1]:
                            addFunc.write(p + ", ")
                        else:
                            addFunc.write(p + "):")
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("        return #enter the return or delete this line")
                    addFunc.write("\n")
            else:
                with open(directory + module + ".py", mode="a") as addFunc:
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("def " + name + "(")
                    if len(parameters) == 0:
                        addFunc.write("):")
                    for p in parameters:
                        if p != parameters[-1]:
                            addFunc.write(p + ", ")
                        else:
                            addFunc.write(p + "):")
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("    return #enter the return or delete this line")
                    addFunc.write("\n")
        else:
            with open(directory + module + ".py", mode="a") as addFunc:
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("def " + name + "(")
                    if len(parameters) == 0:
                        addFunc.write("):")
                    for p in parameters:
                        if p != parameters[-1]:
                            addFunc.write(p + ", ")
                        else:
                            addFunc.write(p + "):")
                    addFunc.write("\n")
                    addFunc.write("\n")
                    addFunc.write("    return #enter the return or delete this line")
                    addFunc.write("\n")
    