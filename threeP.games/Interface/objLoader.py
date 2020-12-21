# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 18:06:09 2020

@author: Christopher S. Francis
"""


##
# A method to format the faces and diffuse-material from a wavefront(.obj) file into python lists to be used in a wx.glcanvas element
# @param model The .obj file for the model, must be triangulated --convert to stereolithographic(.stl)-- when exporting.
# @param material The .mtl file for the model, currently this only grabs the Kd values
# @return <b>tuple of lists</b> ([[vertex -3d], [textture -2d], [normals -3d]], [red, green, blue])
def loadModel(model, material):
    vertexCoords = []
    textureCoords = []
    normalCoords = []
    
    faces = []
    indices = []
    
    rgb = []
    
    with open(model, "r") as getModel:
        for line in getModel:
            values = line.split()
            if values[0] == 'v':
                vert = []
                for v in values[1:]:
                    vert.append(float(v))
                vertexCoords.append(vert)
            elif values[0] == "vt":
                text = []
                for t in values[1:]:
                    text.append(float(t))
                textureCoords.append(text)
            elif values[0] == "vn":
                norm = []
                for n in values[1:]:
                    norm.append(float(n))
                normalCoords.append(norm)
            elif values[0] == "f":
                for v in values:
                    item = v.split("/")
                    if item != "":
                        faces.append(item)
                    else:
                        faces.append(0)
                        
    with open(material, "r") as getMaterial:
        for line in getMaterial:
            values = line.split()
            if len(values) == 0:
                continue
            if values[0] == "Kd":
                for v in values[1:]:
                    rgb.append(float(v))
                
    
    
    for f in faces:
        if len(f) == 1:
            faces.remove(f)
    
    for f in faces:
        vertex = int(f[0])-1
        #texture = int(f[1]) - 1 ##could be empty string from file???
        normal = int(f[2]) -1
        f[0] = tuple(vertexCoords[vertex])
        f[1] = (0, 0)
        f[2] = tuple(normalCoords[normal])

        
    return faces, rgb

    

    
    
    
if __name__ == "__main__":
    model, color = loadModel("human.obj", "human.mtl")
    print(color)