#  ![threeP_logo](https://user-images.githubusercontent.com/50467171/101322789-9938f100-3835-11eb-8039-757b020a1da2.png) threeP.games

An interface and graphical-interface to package game development projects written in Python with the PyGame and Panda3D engines.

<h2>Introduciton</h2>

So I've grown weary of scripting my games in C#, I hope to replace quizzes in classes that I teach with educational video games, which means a steady flow of dinky things better than radio buttons and check boxes on a webpage styled to look like paper needs to flow out, and I would prefer to script these games in Python. The game engines PyGame and Panda3D were selected for 2d and 3d games respectively, but a graphical user interface I liked for them could not be found. So, making my own.


This is the very early stages of a work in progress. Currently the packaging for the resources is about all that has been migrated from plan to code, but there is a <a href="https://www.youtube.com/playlist?list=PLBA4kDe4kZOo_WFbTgha65ItMjBETfl5y">YouTube tutorial playlist</a> that accompanies its development, so I wanted to get it shared on here quickly. Here's the video that goes over the parts ready at the initial (couple) commit(s) here: https://youtu.be/Acjpz2xwbfs.


wxPython was selected for putting together the Graphical User Interface due to the ease of embedding scripting tools with the wx.py.editor and wx.py.shell libraries, and many many other reasons... These python scripting tools are about the only things working so far, in default format mind you, along with setting up the project directories and a couple new/save/open features. 

<h2>Instructions</h2>

The run button writes the game, though it currently is only in the initial state: open engine and start main loop for both 2d and 3d, then runs it in a system console subprocess --not the embedded console, so open it with the exec(open(FILEPATH).run()) method in embedded console to get error messages. 

Scripts can only be saved to the "Scripts" folder in a project so each tab in the editor has a save button but no browse feature, and only scripts in the current project can be opened, do so by double clicking on the directory tree.

So at this point, basically just the directory structure set up...

Script documentation generated with doxygen available at: https://francis-chris5.github.io/threeP.games/html/index.html




![threeP_screenshot](https://user-images.githubusercontent.com/50467171/101573848-88f45380-39a6-11eb-8ef8-70a1826eceb9.jpg)




I forgot to list all the dependencies as I was making this at first, the full list will be coming, but I know that in addition to the core Python API I at least used:

<blockquote>
      
      https://www.pygame.org/wiki/GettingStarted (engine used for 2d games)
      https://www.panda3d.org/ (engine used for 3d games)
      https://docs.panda3d.org/1.10/python/tools/model-export/converting-from-blender (I chose second link: https://github.com/Moguri/panda3d-gltf)
      https://www.wxpython.org/pages/downloads/ (graphical user interface package used)
      https://inkscape.org/ (interface has method to open this)
      https://www.blender.org/ (interface has method to open this)
      
   </blockquote>
  
  
  Very excited about this project so updates will be coming along very shortly...

