
##
#@package GameObjects
# A hierarchy of prepared classes to develop games scripted in python using PyGame for 2d games and Panda3d for 3d games.
#
# @mainpage threeP.games
# @section description Summary
# A collection of scripts to ease the task of game development with the Python programming language by interfacing with the PyGame and Panda3D game engines.\n The Graphical User Interface contains tools for project restricted file navigation, Python scripting, and carrying out common tasks in game development.
# @section author Developer
# Christopher S. Francis\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;26 November 2020 to ...

import pygame
from panda3d.core import KeyboardButton
from direct.actor.Actor import Actor
import math
from os import listdir
from os.path import isdir, basename, abspath


##
#The parent class for all of the visible/tangible objects to be used when developing a a 2d game with the PyGame engine.\n
class Stuff2d():

    ##
    #The constructor for Stuff2d
    # @param x the x coordinate of the objects starting positiion
    # @param y the y coordinate of hte objects starting position
    # @param z a value for closer/farther from viewer layering
    # @param h Yaw, rotation around the z axis
    # @param sprite the list of image files as strings to be used for the sprite animations, if only one single image it still must be passed in as a single element list. The design intention when creating this was that all sprite images are placed into a single directory and then retrieved with a list comprehension passed into the constructor. example: sprite=[("images\\sprite\\" + file) for file in listdir("images\\sprite") if isfile(join("images\\sprite", file))].
    def __init__(self, x=0, y=0, z=0, h=0, sprite=[""]):
        self.__x = x
        self.__y = y
        self.__sprite = None
        self.__width = 0
        self.__height = 0
        self.__counter = 0
        
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y
    
    def getZ(self):
        return self.__z

    def getH(self):
        return self.__h

    def getSprite(self):
        return self.__sprite

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height
    
    def getCounter(self):
        return self.__counter

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y
        
    def setZ(self, z):
        self.__z = z

    def setH(self, h):
        self.__h = h

    def setSprite(self, sprite):
        self.__sprite = sprite

    def setWidth(self, width):
        self.__width = width

    def setHeight(self, height):
        self.__height = height
        
    def setCounter(self, counter):
        self.__counter = counter
    
    def loadSprite(self, asset):
        countPng = 0
        a = []
        for item in listdir(asset):
            if item[-4:] == ".png":
                countPng += 1
                a.append(item)
        if countPng == 1:
            return {"still": [asset + "\\" + a[0]]}
        else:
            anim = []
            startAnim = len(basename(asset)) + 1
            animName = ""
            for item in a:
                if item[startAnim:item.rindex(".")-4] != animName:
                    anim.append(item[startAnim:item.rindex(".")-4])
                    animName = item[startAnim:item.rindex(".")-4]
            frames = []
            for name in anim:
                frames.append([])
                
            for item in a:
                for i in range(len(anim)):
                    if item[startAnim:item.rindex(".")-4] == anim[i]:
                        frames[i].append(pygame.image.load(asset + "\\" + item))
            animations = {}
            i = 0
            for key in anim:
                animations[key] = frames[i]
                i += 1
            self.setSprite(animations)
            self.setWidth(self.getSprite()[list(self.getSprite().keys())[0]][0].get_width())
            self.setHeight(self.getSprite()[list(self.getSprite().keys())[0]][0].get_height())

    
    def bounds(self):
        # @todo adjust this for rotation
        return (self.getX(), self.getY(), self.getX() + self.getWidth(), self.getY() + self.getHeight())
    
    ##
    # The calll to render the sprite image in the game, this must be overridden in subclasses, i.e. the actual objects to be used in a game.\n
    # @param game The pygame display surface in the rendering window -object created by line "pygame.display.set_mode((x,y))"
    def render(self, game):
        pass
    
    ##
    # The initialization method for a game object, this must be overridden in subclasses, i.e. the actual objects to be used in a game.\n
    # @returns void
    def start(self):
        pass
    
    ##
    # The actions to be carried out by a game object, this will be called at every frame of the game, this must be overridden in subclasses, i.e. the actual objects to be used in a game.\n
    # @returns void
    def update(self):
        pass
        
        




##
# Various objects for 2d games.\n
# Currently not really different than Stuff2d, just a useful name for inheritance chains
class Prop2d(Stuff2d):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




##
# The object to consolidate background functionality in a single place for working with PyGame 2d game engine.\n
class Background2d(Stuff2d):

    ##
    # The constructor for the Background2d Objects.\n
    # @param bgMode The type of background as a string, options are {"Tile", "Rolling", "Single"}
    def __init__(self, bgMode="Tile", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__bgMode = bgMode

    def getBgMode(self):
        return self.__bgMode

    def setBgMode(self, bgMode):
        self.__bgMode = bgMode
        
        
    ##
    # Method to actually display the background, even if using something other than bgMode = "Tile"\n
    # @param game the pygame display surface in the rendering window -object created by line "pygame.display.set_mode((x,y))"
    def layTiles(self, game, x=0, y=0, frame=0, anim="still"):
        if self.__bgMode == "Tile":
            for i in range(x, x + game.get_width(), self.getWidth()):
                for j in range(y, y + game.get_height(), self.getHeight()):
                    #self.render(game, i, j)
                    game.blit(self.getSprite()[anim][frame], (i, j))


##
# Class for characters, NPC and Mob, in 3d games.
class Character2d(Stuff2d):
    def __init__(self, speed=0, moving=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__speed = speed
        self.__moving = moving
        
    def getSpeed(self):
        return self.__speed
    
    def isMoving(self):
        return self.__moving
    
    def setSpeed(self, speed):
        self.__speed = speed
        
    def setMoving(self, moving):
        self.__moving = moving
        
    ##
    # Method to define movement for this character in the game, must be overridden in subclasses
    # @returns void
    def move(self):
        pass




##
# A class to consolidate all of the player control features for a 2d game.\n
class Control2D():
    
    ##
    # The constructor for 2d control object
    # @param left The left control, default is 'a' key
    # @param down The down control, default is 's' key
    # @param right The right control, default is 'd' key
    # @param up The up control, default is 'w' key

    def __init__(self, left=pygame.K_a, down=pygame.K_s, right=pygame.K_d, up=pygame.K_w):
        self.__left = left
        self.__down = down
        self.__right = right
        self.__up = up

    def getLeft(self):
        return self.__left

    def getDown(self):
        return self.__down

    def getRight(self):
        return self.__right

    def getUp(self):
        return self.__up

    def setLeft(self, left):
        self.__left = left

    def setDown(self, down):
        self.__down = down

    def setRight(self, right):
        self.__right = right

    def setUp(self, up):
        self.__up = up
    
        
    ##
    # Mehtod to dertimine what keys are currently being pressed.\n
    # @param watcher A base.mouseWatcherNode from a Panda3D game which cannot be passed in until runtime
    # @return <b>{bool}</b> A dictionary of boolean values describing the state of each key
    def checkKey(self, event):
        controls = {"left":False, "down":False, "right":False, "up":False}
        if event.key == self.getLeft():
            controls["left"] = True
        if event.key == self.getDown():
            controls["down"] = True
        if event.key == self.getRight():
            controls["right"] = True
        if event.key == self.getUp():
            controls["up"] = True
        return controls
    
 
    
 
    
 


##
# The class for characters in 2d games created with the PyGame engine.\n
class Player2d(Character2d):

    ##
    # The constructor for Characters2D objects
    # @param speed The number of pixels the character will cover during each tick of the clock when moving
    # @param isMoving The boolean to control which animation is playing with regards to walk/run or idle
    def __init__(self, control=Control2D(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__control = control

    
    def getControl(self):
        return self.__control
        
    def setControl(self, control):
        self.__control = control
        
        
    







##
# The parent class for all visible/tangible objects used in 3d games, essentially an expansion of actor, though not a child class, a container with an actor, positions and rotations can go straight in, other stuff probably needs {instance}.getActor() called first.\n
class Stuff3d():
    
    ##
    # The constructor for the 3d game object parent class
    # @param x X-Coordinate
    # @param y Y-Coordinate
    # @param z Z-Coordinate
    # @param h Yaw angle
    # @param p Pitch angle
    # @param r Roll angle
    def __init__(self, x=0, y=0, z=0, h=0, p=0, r=0):
        
        self.__actor = Actor()
        self.__actor.setPos(x, y, z)
        self.__actor.setHpr(h, p, r)
        self.__actor.setScale(1, 1, 1)

    def getX(self):
        return self.__actor.getX()

    def getY(self):
        return self.__actor.getY()

    def getZ(self):
        return self.__actor.getZ()
    
    def getPos(self):
        return self.__actor.getPos()

    def getH(self):
        return self.__actor.getH()

    def getP(self):
        return self.__actor.getP()

    def getR(self):
        return self.__actor.getR()
    
    def getHpr(self):
        return self.__actor.getHpr()

    def getActor(self):
        return self.__actor

    def setX(self, x):
        self.__actor.setX(x)

    def setY(self, y):
        self.__actor.setY(y)

    def setZ(self, z):
        self.__actor.setZ(z)
        
    def setPos(self, x, y, z):
        self.__actor.setPos(x, y, z)

    def setH(self, h):
        self.__actor.setH(h)

    def setP(self, p):
        self.__actor.setP(p)

    def setR(self, r):
        self.__actor.setR(r)
        
    def setHpr(self, h, p, r):
        self.__actor.setHpr(h, p, r)
        
    def setActor(self, actor):
        self.__actor = actor
     
        
    ##
    # All subclasses that will be used need to call this method and pass up a directory of assets, must contain .bam files, if not named as per instructions this method will need overridden with something that passes a dictionary of animated bam files into the setActor() method 
    # NOTE: this must be a relative filepath (for some reason, no absolutes)
    # @param asset The relative filepath to the folder where the .bam files for this object are located at
    # @returns <b>void</b>
    def loadActor(self, asset):
        # convert gltf to bam file here???
        countBams = 0
        a = []
        for item in listdir(asset):
            if item[-4:] == ".bam":
                countBams += 1
                a.append(item)
        if countBams == 1:            
            self.setActor(Actor(asset[asset.find("Assets"):] + "\\" + a[0] , {"Still": asset[asset.find("Assets"):] + "\\" + a[0]}))
        else:
            animations = {}
            startAnim = len(basename(asset)) + 1
            for item in a:
                if item[-4:] == ".bam":
                    animations[item[startAnim:item.rindex(".")]] = asset[asset.find("Assets"):].replace("\\", "\\\\") + "\\" + item
            self.setActor(Actor(asset[asset.find("Assets"):].replace("\\", "\\\\") + "\\" + a[0], animations))
    
    ##
    # The calll to render the sprite image in the game, this must be overridden in subclasses, i.e. the actual objects to be used in a game.\n
    # @param game The pygame display surface in the rendering window -object created by line "pygame.display.set_mode((x,y))"
    def render(self, task):
        pass
    
    ##
    # The initialization method for a game object, this must be overridden in subclasses, i.e. the actual objects to be used in a game.\n
    # @returns void
    def start(self):
        pass
    
    ##
    # The actions to be carried out by a game object, this will be called at every frame of the game, this must be overridden in subclasses, i.e. the actual objects to be used in a game.\n
    # @returns void
    def update(self, task):
        pass




##
# Background objects for 3d games.\n
# Currently not really different than Stuff3d, just a useful name for inheritance chains
class Background3d(Stuff3d):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


##
# Various objects for 3d games.\n
# Currently not really different than Stuff3d, just a useful name for inheritance chains
class Prop3d(Stuff3d):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



##
# Class for characters, NPC and Mob, in 3d games.
class Character3d(Stuff3d):
    def __init__(self, linearSpeed=0, angularSpeed=0, moving=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__linearSpeed = linearSpeed
        self.__angularSpeed = angularSpeed
        self.__moving = moving
        
    def getLinearSpeed(self):
        return self.__linearSpeed
    
    def getAngularSpeed(self):
        return self.__angularSpeed
    
    def isMoving(self):
        return self.__moving
    
    def setLinearSpeed(self, linearSpeed):
        self.__linearSpeed = linearSpeed
    
    def setAngularSpeed(self, angularSpeed):
        self.__angularSpeed = angularSpeed
        
    def setMoving(self, moving):
        self.__moving = moving
        
    ##
    # Method to define movement for this character in the game, must be overridden in subclasses
    # @returns void
    def move(self):
        pass

##
# A class to consolidate all of the player control features for a 3d game.\n
# @param left The left control, default is 'a' key
# @param down The down control, default is 's' key
# @param right The right control, default is 'd' key
# @param up The up control, default is 'w' key
class Control3D():
    def __init__(self, left=KeyboardButton.ascii_key('a'), down=KeyboardButton.ascii_key('s'), right=KeyboardButton.ascii_key('d'), up=KeyboardButton.ascii_key('w')):
        self.__left = left
        self.__down = down
        self.__right = right
        self.__up = up

    def getLeft(self):
        return self.__left

    def getDown(self):
        return self.__down

    def getRight(self):
        return self.__right

    def getUp(self):
        return self.__up

    def setLeft(self, left):
        self.__left = left

    def setDown(self, down):
        self.__down = down

    def setRight(self, right):
        self.__right = right

    def setUp(self, up):
        self.__up = up
    
        
    ##
    # Mehtod to dertimine what keys are currently being pressed.\n
    # @param watcher A base.mouseWatcherNode from a Panda3D game which cannot be passed in until runtime
    # @return <b>{bool}</b> A dictionary of boolean values describing the state of each key
    def checkKey(self, watcher):
        controls = {"left":False, "down":False, "right":False, "up":False}
        keypress = watcher.is_button_down
        if keypress(self.getLeft()):
            controls["left"] = True
        if keypress(self.getDown()):
            controls["down"] = True
        if keypress(self.getRight()):
            controls["right"] = True
        if keypress(self.getUp()):
            controls["up"] = True
        return controls
        


##
# The default non-vehicle player object for third-person 3d games to handle character animations and control.
class Player3d(Character3d):
    ##
    # Constructor for Player3d
    # @param watcher The panda 3d base.mouseWatcherNode for keyboard and mouse events
    # @param control The 3d controller object
    def __init__(self, watcher, control=Control3D(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__watcher = watcher
        self.__control = control
        
    def getWatcher(self):
        return self.__watcher
    
    def getControl(self):
        return self.__control
    def setWatcher(self, watcher):
        self.__watcher = watcher
        
    def setControl(self, control):
        self.__control = control







"""
# Here are a couple methods from earlier testing that may be useful for copy and paste stuff to get started


#### 2d character and rendering ######
    
    ##
    # The method to move the character.\n
    # Currently only handles player movement based off of the WASD keys, but plans will be to add another parameter and a selection structure to handle movement of NPC as well.
    # @param event The key press indicating which direction the player is to move.
    def moveCardinal(self, event):
        direction = self.getControl().checkKey(event)
        if direction["left"]:
            self.setIsMoving(True)
            self.setX(self.getX() - self.getSpeed())
        if direction["down"]:
            self.setIsMoving(True)
            self.setY(self.getY() + self.getSpeed())
        if direction["right"]:
            self.setIsMoving(True)
            self.setX(self.getX() + self.getSpeed())
        if direction["up"]:
            self.setIsMoving(True)
            self.setY(self.getY() - self.getSpeed())



###### 3d Player movement and rendering ######
		
	def moveAngle(self, task):
		turn = 0
		step = 0
		
		#control
		direction = self.getControl().checkKey(self.getWatcher())
		if direction["left"]:
			turn = self.getAngularSpeed()
		if direction["down"]:
			step = self.getLinearSpeed()
		if direction["right"]:
			turn = -self.getAngularSpeed()
		if direction["up"]:
			step = -self.getLinearSpeed()
			
		#animate
		if step != 0 and not self.getIsMoving():
			self.setIsMoving(True)
		if step == 0 and self.getIsMoving():
			self.setIsMoving(False)
			
		#move
		newH = self.getActor().getH() + turn
		self.getActor().setHpr(newH, 0, 0)
		targetAngle = self.getActor().getH() * math.pi/180
		targetX = math.cos(targetAngle + math.pi/4) - math.sin(targetAngle + math.pi/4)
		targetY = math.sin(targetAngle + math.pi/4) + math.cos(targetAngle + math.pi/4)
		newX = self.getActor().getX() + step * targetX
		newY = self.getActor().getY() + step * targetY
		self.getActor().setFluidPos(newX, newY, 0)
		return task.cont
	
	def chooseAnimation(self, task):
		if not self.getIsMoving() and not self.getActor().getAnimControl("Idle").isPlaying():
			self.getActor().loop("Idle")
		elif self.getIsMoving() and not self.getActor().getAnimControl("Walk").isPlaying():
			self.getActor().loop("Walk")
		
		return task.cont
    
    
"""