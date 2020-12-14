##
# @package Blender2GltfBatch
# @ section description Description
# A script to export animated models created in Blender into a folder to be used in threeP.games.\n Running this script will loop through each of the actions associated with a model and create a GLtf (.glb) export named {blender_filename}_{action}.glb.\n
# NOTE: TURN OFF THE VISIBILITY ON ARMATURE AND ALL OTHER OBJECTS (camera and lighting) BEFORE RUNNING

import bpy
from os import makedirs, listdir, remove
from os.path import join, isdir, dirname



## export to this .blend file location
basedir = dirname(bpy.data.filepath)



##
# Loops through all the actions (animation clips) created and exports every frame of the animation into a .png file for a spritesheet, placed in a folder named after the .blend file being exported from.
def blender2png():
        #select the objects in scene (this script was intended for single model files)
    view_layer = bpy.context.view_layer
    bpy.ops.object.select_all(action='SELECT')
    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    
        #loop through every animated action for every object in scene
    for act in bpy.data.actions:
        for obj in selection:
                
                #select the object and toggle through which animation is active
            obj.select_set(True)
            if not obj.parent.animation_data.action:
                pass
            else:
                obj.parent.animation_data.action = act
                view_layer.objects.active = obj
                
                
                    # names for directories and files
                name = bpy.path.clean_name(obj.name)
                gltfFolder = join(basedir, name)
                if not isdir(gltfFolder):
                    makedirs(gltfFolder)
                
                    # render the image as seen by camera set quality and aspect in properties panel
                for frame in range(int(act.frame_range[1])):
                    filepath = join(gltfFolder, name + "_" + act.name + str(frame).zfill(4))
                    bpy.context.scene.render.filepath = filepath
                    bpy.context.scene.frame_set(frame)
                    bpy.ops.render.render(write_still=True)
                    
                obj.select_set(False)


    #run program
if __name__ == "__main__":
    blender2png()



