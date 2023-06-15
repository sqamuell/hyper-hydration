import math
import os
import random
import subprocess
import sys
import time

import bpy
import numpy as np
from geomdl import BSpline, CPGen, exchange, utilities
from geomdl.visualization import VisPlotly as vis
from matplotlib import cm


def PointsInCircum(r, z, n=15):
    return [
        [np.cos(2 * np.pi / n * x) * r, np.sin(2 * np.pi / n * x) * r, float(z)]
        for x in range(0, n + 1)
    ]


# Initialize vertices of bottle

numLevels = 5
numPtsOnLevel = 6
stepBetweenLevels = 1
radius = 2
offset = 1

# Initialize vertices of bottle

mouthVerticesInner = [PointsInCircum(0.6, 0, numPtsOnLevel)]
topVerticesInner = [
    PointsInCircum(radius, (numLevels + 1) * stepBetweenLevels, numPtsOnLevel)
]

variableVerticesInner = []

# this is what needs to be changed
offsetList = [
    0.011604,
    0.977171,
    0.904748,
    0.969641,
    0.999884,
    0.900495,
    0.973602,
    0.767825,
    0.829448,
    0.086284,
    0.905239,
    0.851182,
    0.986875,
    0.013814,
    0.934239,
    0.978440,
    0.987313,
    0.020059,
    0.940796,
    0.941828,
    0.018459,
    0.043947,
    0.064901,
    0.077804,
    0.960204,
    0.986328,
    0.077025,
    0.934818,
    0.039377,
    0.009958,
]

if len(offsetList) != numLevels * numPtsOnLevel:
    print("Incorrect number of points! Will crash!")
    L = []
    L[0]

indexOffset = 0
for level in range(0 + 1, numLevels + 1):
    nextVertices = PointsInCircum(
        radius + offset, level * stepBetweenLevels, numPtsOnLevel
    )
    for i in range(len(nextVertices) - 1):
        factor = offsetList[indexOffset]
        nextVertices[i][0] *= factor
        nextVertices[i][1] *= factor
        if i == 0:
            nextVertices[-1] = nextVertices[0]
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
    if not firstTriangle:
        mesh_text += "|"
    else:
        firstTriangle = False
    firstVertex = True
    for vertex in triangle:
        if not firstVertex:
            mesh_text += ","
        else:
            firstVertex = False
        mesh_text += str(vertex[0])
        mesh_text += ","
        mesh_text += str(vertex[1])
        mesh_text += ","
        mesh_text += str(vertex[2])

tensor_text = ""
firstFactor = False
for factor in offsetList:
    if not firstFactor:
        tensor_text += ","
    else:
        firstFactor = False
    tensor_text += str(factor)

seconds = time.time()

# mesh_file = open(".\\mesh_data\\mesh_%s.bottle" % str(seconds).replace(".", "_"), "w")
# mesh_file.write(mesh_text)
# mesh_file.close()

path = ".\\mesh_data\\mesh_%s.stl" % str(seconds).replace(".", "_")
thick_filename = "mesh_%s_thick.stl" % str(seconds).replace(".", "_")
logging = "log_%s.txt" % str(seconds).replace(".", "_")

path_thick = ".\\mesh_data\\" + thick_filename
exchange.export_stl(surf, path)
print("mesh generated")

bpy.ops.wm.read_factory_settings()
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="MESH")
bpy.ops.object.delete()

bpy.ops.import_mesh.stl(filepath=path)

obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")

bpy.ops.mesh.remove_doubles()

bpy.ops.object.mode_set(mode="OBJECT")

modifier = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
modifier.thickness = 0.1  # Adjust the thickness as needed

bpy.ops.object.modifier_apply(modifier=modifier.name)

bpy.ops.export_mesh.stl(filepath=path_thick, use_selection=True)

os.remove(path)


command = ["./FluidX3D/bin/FluidX3D.exe", thick_filename]

# Open a file for writing
output_file = open(".\\logs\\" + logging, "w")

# Execute the command and redirect the output to the file
subprocess.run(command, stdout=output_file, stderr=subprocess.PIPE)

# Close the file
output_file.close()
