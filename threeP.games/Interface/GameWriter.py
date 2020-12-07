

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
        self.mainLoop = ["playing = True", "while playing:", "    for event in pygame.event.get():", "        if event.type == pygame.QUIT:", "            playing = False"]
        self.shutDown = ["pygame.quit()"]
        self.title = title
        self.directory = directory
        self.framesPerSecond = framesPerSecond
        self.sceneWidth = sceneWidth
        self.sceneHeight = sceneHeight
        
    
    
    ##
    # Method to fill up the writable list with lines related to initializing a 2d game
    # @return <b>void</b>
    def initializeSection(self):
        self.initialize.append("scene = pygame.display.set_mode((" + str(self.sceneWidth) + ", " + str(self.sceneHeight) + "))")
        self.initialize.append("pygame.display.set_caption(\"" + self.title + "\")")
        
        
        
    ##
    # Method to fill up the writable list with lines related to the main loop section of a 2d game
    # @return <b>void</b>
    def mainLoopSection(self):
        self.mainLoop.append("    pygame.display.flip()")
        self.mainLoop.append("    clock.tick(" + str(self.framesPerSecond) + ")")
        
    
    ##
    # Method to write the python script for a 2d game once the writable lists have all been filled appropriately
    # @return <b>void</b>
    def writeGame(self):
        self.initializeSection()
        self.mainLoopSection()
        path = join(self.directory, self.title + ".py")
        with open(path, mode="w") as toFile:
            for line in self.imports:
                toFile.write(line + "\n")
            for line in self.initialize:
                toFile.write(line + "\n")
            for line in self.mainLoop:
                toFile.write(line + "\n")
            for line in self.shutDown:
                toFile.write(line + "\n")
        



##
# An object to write the full 3d game python script
class GameWriter3d:

    ##
    # The standard initialize method for a python class
    # @param title The name for the game, the only required argument for the object
    # @param directory The location the python script will be written to
    def __init__(self, title, directory = ""):
        self.imports = ["from direct.showbase.ShowBase import ShowBase"]
        self.mainScene = ["class Scene(ShowBase):", "    def __init__(self):", "        super().__init__()"]
        self.runGame = ["game = Scene()", "game.run()"]
        self.title = title
        self.directory = directory
        
    
    ##
    # Method to write the python script for a 3d game once the writable lists have all been filled appropriately
    # @return <b>void</b>
    def writeGame(self):
        path = join(self.directory, self.title + ".py")
        with open(path, mode="w") as toFile:
            for line in self.imports:
                toFile.write(line + "\n")
            for line in self.mainScene:
                toFile.write(line + "\n")
            for line in self.runGame:
                toFile.write(line + "\n")
                
        
        
        
        
        
#gw = GameWriter3d("Test Game 2")
#gw.WriteGame()
        
        
        
        
        
        
        
        
        