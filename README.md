#  ![threeP_logo](https://user-images.githubusercontent.com/50467171/101322789-9938f100-3835-11eb-8039-757b020a1da2.png) threeP.games

An interface and graphical-interface to package game development projects written in Python with the PyGame and Panda3D engines.

<h2>Introduciton</h2>

So I've grown weary of scripting my games in C#, I hope to replace quizzes in classes that I teach with educational video games, which means a steady flow of dinky things better than radio buttons and check boxes on a webpage styled to look like paper needs to flow out, and I would prefer to script these games in Python. The game engines PyGame and Panda3D were selected for 2d and 3d games respectively, but a graphical user interface I liked for them could not be found. So, making my own.


This is the very early stages of a work in progress. Currently the packaging for the resources is about all that has been migrated from plan to code, but there is a <a href="https://www.youtube.com/playlist?list=PLBA4kDe4kZOo_WFbTgha65ItMjBETfl5y">YouTube tutorial playlist</a> that accompanies its development, so I wanted to get it shared on here quickly. Here's the video that goes over the parts ready at the initial (couple) commit(s) here: https://youtu.be/Acjpz2xwbfs.


wxPython was selected for putting together the Graphical User Interface due to the ease of embedding scripting tools with the wx.py.editor and wx.py.shell libraries, and many many other reasons... These python scripting tools are about the only things working so far, in default format mind you, along with setting up the project directories and a couple new/save/open features. 

![threep_screenshot_main](https://user-images.githubusercontent.com/50467171/102130540-fa0c8e80-3e1e-11eb-9f7a-861b46b2b963.jpg)

As I began development of the inspector tab it quickly became apparent that my orignal plan, to use GLtf format with PyOpenGL, was going to require some complex code and a little trickery. Falling back to a simpler plan B uses wavefront (.obj and .mtl) format for the object previews, which also happens to be the standard format for 3d games in PyGame, so a future version (once the original is completed and working) may switch to include a choice of engines rather than simply PyGame for 2d and Panda3d for 3d (2d in panda is easy -just ignore the z-axis except for front/back issues).

<h2>Instructions</h2>

<h4>Create Project</h4>

The create new project functions will provide a dialog box where a name, mode (2d or 3d), and directory must be selected. This cannot be changed via GUI, and it is HIGHLY RECOMMENDED to simply create a new project and copy over the parts that were not automatically generated if major changes to any of these three main properties are required.

![threep_screenshot_newProject](https://user-images.githubusercontent.com/50467171/102130539-f973f800-3e1e-11eb-88f7-cd7e4ee68790.jpg)

![threep_screenshot_newProjectGenerated](https://user-images.githubusercontent.com/50467171/102130543-faa52500-3e1e-11eb-89c4-94f4f3a8a3c6.jpg)

<h4>Open Project</h4>

The open project function will bring up a standard file browser dialog box restricted to .xml files, select the {project-name}_manifest.xml file to open the project.

<h4>Run Game</h4>

The run button writes the game script if it doesn't already exist, though it currently is only in the initial state: open engine and start main loop for both 2d and 3d, then runs it in a system console subprocess --not the embedded Python console, that is intended only for small tests (single line or block) while composing the scripts. Messages, errors and confirmations and anything else that may come to sys.stdout are delivered via message dialog after completeion of the program. Messages delivered to sys.stdout or sys.stderr can be copied to a text file in the project, however, copying new error messages will overwrite what is already in the file.

![threep_screenshot_stderr](https://user-images.githubusercontent.com/50467171/102130548-faa52500-3e1e-11eb-97e2-cca776116e2e.jpg)

![threep_screenshot_stdout](https://user-images.githubusercontent.com/50467171/102130549-faa52500-3e1e-11eb-961e-35105be5b3f9.jpg)

![threep_screenshot_errLog](https://user-images.githubusercontent.com/50467171/102130990-8a4ad380-3e1f-11eb-9d86-e52aa0a211eb.jpg)

Since this runs in a system console, not a python interpreter, it is necessary that the computer can run python scripts in a system console, check by opening your console, such as command prompt or powershell on windows, type python and hit enter. If that is an unrecognized command you will need to set an environment variable to python --here are videos I made for a recent class I taught showing how: <a href="https://www.youtube.com/watch?v=COuSOim_JHg&list=PLBA4kDe4kZOrASKhq43mnJ9INP7snu7BZ&index=1">Windows</a> (about 14 minutes in) or <a href="https://www.youtube.com/watch?v=Cy0eVMAuA2w&list=PLBA4kDe4kZOrASKhq43mnJ9INP7snu7BZ&index=2">Apache Server</a>, or obviously you could just search google for 'set environment variables.'


<h4>Scripting</h4>

Scripts can only be saved to the "Scripts" folder in a project so each tab in the editor has a save button but no browse feature, and only scripts in the current project can be opened, do so by double clicking on the directory tree. Also note that a new script can only be created when there is a project open. The python script editor uses the official python recommendation of four(4) spaces for indenting --this will match idle and should be what most IDE's do, but files started in many regular text editors could result in a mix-tab-spaces issue. XML files can be viewed and edited in the editor, but changes to the {projectName}_manifest.xml cannot be saved. Text files can also be viewed, edited and saved, just that creating is for python scripts alone, the project will be created with a text file in each of the three main folders to serve todo-list and notes functions.

![threep_screenshot_newScript2d](https://user-images.githubusercontent.com/50467171/102130536-f973f800-3e1e-11eb-8f08-f3233f44791f.jpg)

![threep_screenshot_newScript3d](https://user-images.githubusercontent.com/50467171/102130538-f973f800-3e1e-11eb-850d-4a01401067a6.jpg)

The autocomplete functionality, while still very crude, will at least show the key terms for python along with any variables, methods, and classes created in the current python script.

![threep_screenshot_autocomplete](https://user-images.githubusercontent.com/50467171/102130844-5c658f00-3e1f-11eb-9bd9-86dde93444b5.jpg)

<h4>Import Assets</h4>

There are two ways to import assets into the project, by folder and by source. To import a folder simply click the import assets button (see picture below) and navigate to and select the folder to import. To import by source (the preferred and intended method), see paragraphs below the pictures.

![threep_screenshot_importSource](https://user-images.githubusercontent.com/50467171/102575046-462a2e00-40c0-11eb-9649-0db829305a9d.jpg)
![threep_screenshot_importAssets](https://user-images.githubusercontent.com/50467171/102575047-46c2c480-40c0-11eb-9418-8e9473f6c208.jpg)

Direct integration, at least from blender which contains its own python API can be a bit problematic if the blender python version does not exactly match the native python environment, so there are export scripts included (hopefully more coming for other major 3d modeling softwares: MEL and Zscript for example), load them into the animated model in blender, then just hit run to get the folder to import into the threeP.games project. 

The blender2gltf.py script exports one 3d model for each animation named model_{action}.glb which will need to be converted to a .bam copy when imported into the threeP.games project (at this time there is an option in the "External" menu to do this, automation should be coming soon), and the blender2png.py script exports a .png file for every keyframe of the animation from the viewpoint of the active camera in the scene named model_{action}####.png (so it will work whether it is a 2d or 3d animated model). Both export scripts give the folder the same name as the blender file the model is saved in and place it in the same directory as the blender file. Selecting a gltf(.glb) or .png graphics file from the directory tree will open it in the system default for viewing such a file.

<h4>External Editors</h4>

Loadng the source graphics file rather than exports requires a default 2d graphics editor or 3d modeling software to be set. Once a default is set the external applications can be opened for new file creation directly from the GUI through the "External" options in the main menu. Double clicking on a source graphics file in the directory tree (once a default editor is set) will open with one of these editors externally as a subprocess, so the threeP.games user interface will be unresponsive until the external editor is closed any sys.stdout messages will be presented in a message dialog once the external editor is closed and the threeP.games graphical user interface is returned to.

To set a default external editor select "External" in the main menu and then choose the appropriate option for 2d or 3d. The dialog box pictured below will appear, fill in the form for a name to refer to it by in buttons on this GUI, the primary type of file you wish to open with this editor, a .ico or .png file for the icon associated with this editor (do not leave this blank, choose any image if you don't have the actual icon), and select the location for the actual .exe application. To replace a default external editor simply follow these steps to overwrite it, to completely remove it delete the appropriate line from the threeP.config file.

![threep_screenshot_editor1](https://user-images.githubusercontent.com/50467171/102166349-e2063080-3e59-11eb-94aa-4711d50d53d6.jpg)

![threep_screenshot_editor](https://user-images.githubusercontent.com/50467171/102163179-a28b1480-3e58-11eb-88ec-31396fbeeb3c.jpg)

<h4>Scene Objcets</h4>

The "Scenes" folder is for the objects that will actually be placed into the game. Selecting the "New Scene Object" tool or menu option will bring up a dialog to choose from the short list of objects that are ready so far: 2d backgrounds, 2d props, 2d player, 3d player. More options will be coming soon. Along with the type of game object to insert, give it a name and chooose the folder containing the image assets: all sprite-sheet files for 2d and all bam files for 3d in a single folder, do not organize into subfolders, a dictionary to refer to the various animations will be generated from the given files.

![threep_screenshot_newScene](https://user-images.githubusercontent.com/50467171/102130534-f8db6180-3e1e-11eb-84c4-e0b1a5800270.jpg)

A file will be generated for the scene object which will need customization to the start() and update() methods. The start() method will be called one time when the object is initialized, and the update() method will be called at every frame of the game. It is highly recommended to put all customizations here, as other locations may be overwritten as files are (re)generated.

There is also a file named GameInstance which contains the strings that will actually be written to the final game script. It is HIGHLY recommended not to mess with this file, as the entire project depends upon the order this file is generated, and errors here may result in the entire project needing redone.

<h4>TODO List</h4>

There is a ToDo list text file at the top level of the project, simply place the annotaion "@todo" IN A COMMENT to add items on the ToDo-List text file. The generated files all come with some @todo items in them at this point.

<h4>Help</h4>

The help features link directly to the official API documentation pages for Python, PyGame, and Panda3D.

![threep_screenshot_help](https://user-images.githubusercontent.com/50467171/102130530-f8db6180-3e1e-11eb-93eb-cc31bed72ed3.jpg)

<h4>Deleting an unused resource/script</h4>

To remove a file from the project, right-click on it in the directory tree and confirm the choice.

<h2>In Conclusion...</h2>

So at this point, basically just the directory structure set up...

Script documentation generated with doxygen available at: https://francis-chris5.github.io/threeP.games/html/index.html

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

