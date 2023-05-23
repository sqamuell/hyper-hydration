import numpy as np
from geomdl import BSpline
from geomdl import utilities
from geomdl import exchange
from geomdl.visualization import VisPlotly as vis
from geomdl import CPGen
from matplotlib import cm
import random
import sys
import time

def PointsInCircum(r,z,n=15):
    return [[np.cos(2*np.pi/n*x)*r,np.sin(2*np.pi/n*x)*r, float(z)] for x in range(0,n)]


#Initialize vertices of bottle

numLevels = 5
numPtsOnLevel = 6
stepBetweenLevels = 1
radius = 2
offset = 1

#Initialize vertices of bottle

mouthVerticesInner = [PointsInCircum(2 ,0,numPtsOnLevel)]
topVerticesInner = [PointsInCircum(radius,(numLevels + 1) * stepBetweenLevels,numPtsOnLevel)]

variableVerticesInner = []

#this is what needs to be changed
offsetList = [
    \
    0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5
    \
    ]
 
if len(offsetList) != numLevels * numPtsOnLevel:
    print("Incorrect number of points! Will crash!")
    L = []
    L[0]

indexOffset = 0
for level in range(0 + 1, numLevels + 1):
    nextVertices = PointsInCircum(radius + offset,level * stepBetweenLevels,numPtsOnLevel)
    for i in range(len(nextVertices) - 1):
        factor = offsetList[indexOffset]
        nextVertices[i][0] *= factor
        nextVertices[i][1] *= factor
        if (i == 0): nextVertices[-1] = nextVertices[0]
        indexOffset += 1
    variableVerticesInner += [nextVertices]

allVerticesInner = mouthVerticesInner + variableVerticesInner + topVerticesInner

print("Successfully generated points and a unique tensor!")

# Create a BSpline surface instance
surf = BSpline.Surface()

# Set degrees
surf.degree_u = 3
surf.degree_v = 3

# Get the control points from the generated grid
surf.ctrlpts2d = allVerticesInner

# Set knot vectors
surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, surf.ctrlpts_size_u)
surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, surf.ctrlpts_size_v)

# Set sample size
surf.sample_size = 100

# Set visualization component
# surf.vis = vis.VisSurface(ctrlpts=True, legend=False)
# print("Generating visualization, please wait...")

# Plot the surface
# surf.render(colormap=cm.terrain)

mesh_text = ""
firstTriangle = True
for triangle in surf.faces:
    if not firstTriangle: mesh_text += "|"
    else: firstTriangle = False
    firstVertex = True
    for vertex in triangle:
        if not firstVertex: mesh_text += ","
        else: firstVertex = False
        mesh_text += str(vertex[0])
        mesh_text += ","
        mesh_text += str(vertex[1])
        mesh_text += ","
        mesh_text += str(vertex[2])

tensor_text = ""
firstFactor = False
for factor in offsetList:
    if not firstFactor: tensor_text += ","
    else: firstFactor = False
    tensor_text += str(factor)

seconds = time.time()

mesh_file = open(".\\mesh_data\\mesh_%s.text" % seconds, "w")
mesh_file.write(mesh_text)
mesh_file.close()
print("mesh generated")