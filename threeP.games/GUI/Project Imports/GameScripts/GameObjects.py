
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

##
#The parent class for all of the custom objects to be used when developing a a 2d game with the PyGame engine.\n
class Stuff2d():

    ##
    #The constructor for Stuff2d
    #@param x the x coordinate of the objects starting positiion
    #@param y the y coordinate of hte objects starting position
    #@param sprite the list of image files as strings to be used for the sprite animations, if only one single image it still must be passed in as a single element list. The design intention when creating this was that all sprite images are placed into a single directory and then retrieved with a list comprehension passed into the constructor. example: sprite=[("images\\sprite\\" + file) for file in listdir("images\\sprite") if isfile(join("images\\sprite", file))].
    def __init__(self, x=0, y=0, sprite=["images\\empty.svg"]):
        self.__x = x
        self.__y = y
        self.__sprite = self.loadSpriteSheet(sprite)
        self.__width = self.__sprite[0].get_width()
        self.__height = self.__sprite[0].get_height() 
        
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getSprite(self):
        return self.__sprite

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    ##
    # Replaces the list of sprites for the object.\n
    # @param sprite Must be a list of filenames as strings, if only a single image, pass it in as a single element list.
    def setSprite(self, sprite):
        self.__sprite = self.loadSpriteSheet(sprite)

    def setWidth(self, width):
        self.__width = width

    def setHeight(self, height):
        self.__height = height
        
    def loadSpriteSheet(self, sprite):
        spriteSheet = []
        for s in sprite:
            spriteSheet.append(pygame.image.load(s))
        self.setWidth(spriteSheet[0].get_width())
        self.setHeight(spriteSheet[0].get_height())
        return spriteSheet
        
        
    ##
    # The method to render an object on the scene using the PyGame blit (block transfer) method, to be called every pass of the main loop in the game.\n
    # @param game The pygame display surface in the rendering window -object created by line "pygame.display.set_mode((x,y))"
    # @param x The x coordinate of where to render the object at
    # @param y The y coordinate of where to render the object at
    # @param frame The frame of the sprite animation to render, design intentions are for this parameter to be filled with a ternary operator checking a global counter, example: for idle/walk animations with 20 frames each (counter%20, counter%20+20)[character.getIsMoving()]
    def render(self, game, x, y, frame=0):
        if len(self.__sprite) == 1:
            game.blit(self.__sprite[0], (x, y))
        else: 
            game.blit(self.__sprite[frame], (x, y))
        
    def bounds(self):
        print("bounds method coming soon")
        
    def addScript(self):
        print("add script coming soon")




##
# The object to consolidate background functionality in a single place for working with PyGame 2d game engine.\n
class Background2d(Stuff2d):

    ##
    # The constructor for the Background2d Objects.\n
    # @param bgMode The type of background as a string, options are {"Tile", "Rolling", "Single"}
    def __init__(self, x=0, y=0, sprite=["images\\empty.svg"], bgMode="Tile"):
        super().__init__(x, y, sprite)
        self.__bgMode = bgMode

    def getBgMode(self):
        return self.__bgMode

    def setBgMode(self, bgMode):
        self.__bgMode = bgMode
        
        
    ##
    # Method to actually display the background, even if using something other than bgMode = "Tile"\n
    # @param game the pygame display surface in the rendering window -object created by line "pygame.display.set_mode((x,y))"
    def layTiles(self, game):
        if self.__bgMode == "Tile":
            for i in range(0, game.get_width(), self.getWidth()):
                for j in range(0, game.get_height(), self.getHeight()):
                    self.render(game, i, j)




##
# The class for characters in 2d games created with the PyGame engine.\n
class Player2d(Stuff2d):

    ##
    # The constructor for Characters2D objects
    # @param speed The number of pixels the character will cover during each tick of the clock when moving
    # @param isMoving The boolean to control which animation is playing with regards to walk/run or idle
    def __init__(self, x=0, y=0, sprite=["images\\empty.svg"], speed=0, isMoving=False):
        super().__init__(x, y, sprite)
        self.__speed = speed
        self.__isMoving = isMoving

    def getSpeed(self):
        return self.__speed

    def getIsMoving(self):
        return self.__isMoving

    def setSpeed(self, speed):
        self.__speed = speed

    def setIsMoving(self, isMoving):
        self.__isMoving = isMoving
        
        
    ##
    # The method to move the character.\n
    # Currently only handles player movement based off of the WASD keys, but plans will be to add another parameter and a selection structure to handle movement of NPC as well.
    # @param event The key press indicating which direction the player is to move.
    def move(self, event):
        if event.key == pygame.K_a:
            self.setIsMoving(True)
            self.setX(self.getX() - self.getSpeed())
        if event.key == pygame.K_s:
            self.setIsMoving(True)
            self.setY(self.getY() + self.getSpeed())
        if event.key == pygame.K_d:
            self.setIsMoving(True)
            self.setX(self.getX() + self.getSpeed())
        if event.key == pygame.K_w:
            self.setIsMoving(True)
            self.setY(self.getY() - self.getSpeed())




##
# A class to consolidate all of the player control features for a game.\n
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
# @param watcher
# @param actor
# @param control
# @param isMoving
# @param linearSpeed
# @param angularSpeed
class Player3d():
	def __init__(self, watcher, actor, control=Control3D(), isMoving=False, linearSpeed=0.05, angularSpeed=3):
		self.__watcher = watcher
		self.__actor = actor
		self.__control = control
		self.__isMoving = isMoving
		self.__linearSpeed = linearSpeed
		self.__angularSpeed = angularSpeed

	def getWatcher(self):
		return self.__watcher

	def getActor(self):
		return self.__actor

	def getControl(self):
		return self.__control

	def getIsMoving(self):
		return self.__isMoving

	def getLinearSpeed(self):
		return self.__linearSpeed

	def getAngularSpeed(self):
		return self.__angularSpeed

	def setWatcher(self, watcher):
		self.__watcher = watcher

	def setActor(self, actor):
		self.__actor = actor

	def setControl(self, control):
		self.__control = control

	def setIsMoving(self, isMoving):
		self.__isMoving = isMoving

	def setLinearSpeed(self, linearSpeed):
		self.__linearSpeed = linearSpeed

	def setAngularSpeed(self, angularSpeed):
		self.__angularSpeed = angularSpeed
		
	def move(self, task):
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