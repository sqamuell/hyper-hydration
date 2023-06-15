import bpy
import numpy as np
from mathutils import Vector

bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="MESH")
bpy.ops.object.delete()

z = 5


def makePrimitiveCircle(objName, v, r, f, loc, rot, layers=[0]):
    bpy.ops.mesh.primitive_circle_add(
        vertices=v,
        radius=r,
        fill_type=f,
        enter_editmode=False,
        location=loc,
        rotation=rot,
    )
    ob = bpy.context.active_object
    ob.name = objName
    ob.show_name = True
    me = ob.data
    me.name = objName + "Mesh"
    return ob


def PointsInCircum(r, z, n=15):
    return [
        [np.cos(2 * np.pi / n * x) * r, np.sin(2 * np.pi / n * x) * r, float(z)]
        for x in range(0, n + 1)
    ]


offsetList = [
    0.011604,
    0.977171,
    0.904748,
    0.086284,
    0.969641,
    0.999884,
    0.086284,
    0.900495,
    0.973602,
    0.767825,
    0.829448,
    0.077025,
    0.086284,
    0.086284,
    0.905239,
    0.086284,
    0.851182,
    0.986875,
    0.077025,
    0.013814,
    0.934239,
    0.086284,
    0.978440,
    0.987313,
    0.999884,
    0.086284,
    0.020059,
    0.940796,
    0.941828,
    0.018459,
    0.043947,
    0.064901,
    0.2323,
    0.077804,
    0.960204,
    0.077025,
    0.986328,
    0.077025,
    0.934818,
    0.039377,
    0.009958,
]


def moveVertex(point, factor):
    # Move the point by the factor from its location to the center (0,0,0)
    # and then move it back by the same factor
    point[0] += factor * (0 - point[0])
    point[1] += factor * (0 - point[1])
    # point[2] += factor * (0 - point[2])
    return point


bpy.ops.surface.primitive_nurbs_surface_cylinder_add(enter_editmode=True)
# bpy.ops.object.select_all(action="DESELECT")

surface = bpy.context.active_object
for pointIndex in range(0, len(surface.data.splines[0].points) - 8):
    surface.data.splines[0].points[pointIndex].select = False

myVec = Vector((0.0, 0.0, 2.0))
for _i in range(0, z - 2):
    bpy.ops.curve.extrude_move(TRANSFORM_OT_translate={"value": myVec})

print(surface.data.splines[0].points[0].co)

# bpy.ops.transform.translate(value=(, , 0))

for pointIndex in range(0, len(surface.data.splines[0].points)):
    parameter = offsetList[pointIndex]

    surface.data.splines[0].points[pointIndex].co[0] = parameter * (
        0 - surface.data.splines[0].points[pointIndex].co[0]
    )
    surface.data.splines[0].points[pointIndex].co[1] = parameter * (
        0 - surface.data.splines[0].points[pointIndex].co[1]
    )

bpy.ops.object.editmode_toggle()

# scale z axis by .5
bpy.ops.transform.resize(value=(1, 1, 0.5))
bpy.ops.transform.translate(value=(0, 0, 0.5))

# parameter_index = 0
# for z in range(5):
#     points = PointsInCircum(1, z, 6)

#     bpy.ops.curve.primitive_nurbs_curve_add(enter_editmode=False, align="WORLD")
#     curve = bpy.context.active_object

#     bpy.ops.object.editmode_toggle()
#     bpy.ops.curve.delete(type="VERT")

#     for index in range(1, len(points)):
#         parameter = offsetList[parameter_index]

#         bpy.ops.curve.vertex_add(location=moveVertex(points[index], parameter))

#         parameter_index += 1

#     bpy.ops.curve.cyclic_toggle()
#     bpy.ops.object.editmode_toggle()

# bpy.ops.object.select_by_type(type="CURVE")
# bpy.ops.object.convert(target="MESH")

# bpy.ops.object.select_by_type(type="MESH")
# bpy.ops.object.join()

# bpy.ops.object.editmode_toggle()
# bpy.ops.mesh.select_all(action="SELECT")

# # bridge edge loops
# bpy.ops.mesh.bridge_edge_loops()
# bpy.ops.mesh.remove_doubles()

# bpy.ops.object.editmode_toggle()

# bpy.ops.object.shade_smooth(use_auto_smooth=True)
# bpy.ops.object.modifier_add(type="SOLIDIFY")
# bpy.context.object.modifiers["Solidify"].thickness = 0.05
