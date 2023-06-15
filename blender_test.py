import bpy
import numpy as np
import random

#pip install fake-bpy-module-2.93
# or pip install fake-bpy-module-latest
#conda install -c kitsune.one python-blender

#safe script changes in blender via 'alt + s'


#Helper Functions
#from https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle
def PointsInCircum(r,z,n=15):
    return [[np.cos(2*np.pi/n*x)*r,np.sin(2*np.pi/n*x)*r, float(z)] for x in range(0,n+1)]


#Initialize vertices of bottle
height = 30
radius = 10

#the mouth
mouthVertices= [PointsInCircum(3,-1)]
topVertices= [PointsInCircum(radius,height)]

variableVertices = []
for level in range(height):
    nextVertices = PointsInCircum(radius,level)
    # n = nextVertices[0]
    # nextVertices.append(n)
    for i in range(len(nextVertices) - 1):
        factor = random.random()
        nextVertices[i][0] *= factor
        nextVertices[i][1] *= factor
        if (i == 0):
            nextVertices[-1][0] *= factor
            nextVertices[-1][1] *= factor


    variableVertices += [nextVertices]

allVertices = mouthVertices + variableVertices + topVertices


bpy.ops.mesh.convex_hull(delete_unused=True, use_existing_faces=True, make_holes=False, join_triangles=True, face_threshold=0.698132, shape_threshold=0.698132, uvs=False, vcols=False, seam=False, sharp=False, materials=False)