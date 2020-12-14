

##
# @package GameWriter
# The objects to actually write the Python script for a 2d or 3d game once it has been assembled with the interface.\n

from os.path import join, isdir

##
# An object to write the full 2d game python script
class GameWriter2d:
    
    ##
    # The standard initialize method for a python class
    # @param title The name for the game, the only required argument in the object
    # @param directory The location the python script will be written to
    # @param sceneWidth The pixel width of a 2d scene with a default value of 768
    # @param sceneHeight The pixel height of a 2d scene with a default value of 512
    # @param framesPerSecond The number of frames per second the game will run at
    def __init__(self, title, directory = "", sceneWidth = 768, sceneHeight = 512, framesPerSecond = 60):
        self.imports = ["import pygame"]
        self.initialize = ["pygame.init()", "clock = pygame.time.Clock()"]
        self.mainLoop = ["playing = True", "while playing:", "    for event in pygame.event.get():", "        if event.type == pygame.QUIT:", "            playing = False", "    # @todo handle the events here"]
        self.shutDown = ["pygame.quit()"]
        self.title = title
        self.directory = directory
        self.framesPerSecond = framesPerSecond
        self.sceneWidth = sceneWidth
        self.sceneHeight = sceneHeight
        
        self.initializeSection()
        self.mainLoopSection()
        
    
    ##
    # Method to include the local project directory as an import source for modules to be used in the game.\n
    # @param path The directory path where local python modules will be found at
    def localDirectory(self, path):
        self.imports.insert(0, "import sys")
        self.imports.insert(1, "sys.path.insert(1, \"" + path.replace("\\", "\\\\") + "\")")
        self.imports.append("\n# @todo import required modules here, --The game will check project resources so 'import Scripts.MyModule' for example\n\n")
        
    
    ##
    # Method to fill up the writable list with lines related to initializing a 2d game
    # @return <b>void</b>
    def initializeSection(self, items=[]):
        self.initialize.append("scene = pygame.display.set_mode((" + str(self.sceneWidth) + ", " + str(self.sceneHeight) + "))")
        self.initialize.append("pygame.display.set_caption(\"" + self.title + "\")")
        self.initialize.append("\n\n# @todo initialize custom game objects here\n\n")
        
        
    ##
    # Method to fill up the writable list with lines related to the main loop section of a 2d game
    # @return <b>void</b>
    def mainLoopSection(self, items=[]):
        self.mainLoop.insert(len(self.mainLoop), "\n\n    # @todo manipulate the game objects here\n")
        self.mainLoop.insert(len(self.mainLoop), "    pygame.display.flip()")
        self.mainLoop.insert(len(self.mainLoop), "    clock.tick(" + str(self.framesPerSecond) + ")")
        
    
    ##
    # Method to write the python script for a 2d game once the writable lists have all been filled appropriately
    # @return <b>void</b>
    def writeGame(self):
        path = join(self.directory, self.title + ".py")
        with open(path, mode="w") as toFile:
            for line in self.imports:
                toFile.write(line + "\n")
            toFile.write("\n\n\n")
            
            for line in self.initialize:
                toFile.write(line + "\n")
            toFile.write("\n\n\n")
            
            for line in self.mainLoop:
                toFile.write(line + "\n")
            toFile.write("\n")
            
            for line in self.shutDown:
                toFile.write(line + "\n")
            toFile.write("\n\n\n")
            

            
        



##
# An object to write the full 3d game python script
class GameWriter3d:

    ##
    # The standard initialize method for a python class
    # @param title The name for the game, the only required argument for the object
    # @param directory The location the python script will be written to
    def __init__(self, title, directory = ""):
        self.imports = ["from direct.showbase.ShowBase import ShowBase", "from panda3d.core import AmbientLight"]
        self.mainScene = ["class Scene(ShowBase):", "    def __init__(self):", "        super().__init__()\n"]
        self.runGame = ["    game = Scene()", "    try:", "        game.run()", "    except:", "        base.destroy()"]
        self.title = title
        self.directory = directory
        
        self.mainSceneSection()
    
    
    ##
    # Method to include the local project directory as an import source for modules to be used in the game.\n
    # @param path The directory path where local python modules will be found at
    def localDirectory(self, path):
        self.imports.insert(0, "import sys")
        self.imports.insert(1, "sys.path.insert(1, \"" + path.replace("\\", "\\\\") + "\")")
        self.imports.append("\n# @todo import required modules here, --The game will check project resources so 'import Scripts.MyModule' for example\n\n")
     
        
    def mainSceneSection(self, items=[]):
        self.mainScene.append("        # @todo replace and/or adjust default camera")
        self.mainScene.append("        self.cam.setPos(15, -7, 4)")
        self.mainScene.append("        self.cam.lookAt(0, 0, 0)\n")
        self.mainScene.append("        # @todo replace and/or adjust the default lighting")
        self.mainScene.append("        self.light = AmbientLight('alight')")
        self.mainScene.append("        self.light.setColor( (0.8, 0.8, 0.8, 1) )")
        self.mainScene.append("        attachLight = self.render.attachNewNode(self.light)")
        self.mainScene.append("        self.render.setLight(attachLight)\n\n")
        self.mainScene.append("        # @todo Insert custom models and actors for the scene here\n")
         
         
    ##
    # Method to write the python script for a 3d game once the writable lists have all been filled appropriately
    # @return <b>void</b>
    def writeGame(self):
        path = join(self.directory, self.title + ".py")
        with open(path, mode="w") as toFile:
            for line in self.imports:
                toFile.write(line + "\n")
            toFile.write("\n\n\n")
            
            for line in self.mainScene:
                toFile.write(line + "\n")
            toFile.write("\n\n\n")
            
            toFile.write("if __name__ == \"__main__\":\n")
            for line in self.runGame:
                toFile.write(line + "\n")


