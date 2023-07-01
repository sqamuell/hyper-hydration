import os

import bpy
import numpy as np
from splipy import curve_factory, surface_factory
from splipy.io.stl import STL


def PointsInCircum(r, z, n=15):
    theta = np.linspace(0, 2 * np.pi, n + 1)[
        :-1
    ]  # Angles evenly spaced around the circle
    x = r * np.cos(theta)  # x-coordinates
    y = r * np.sin(theta)  # y-coordinates
    z = z * np.ones_like(theta)  # z-coordinate (constant)

    points = np.column_stack((x, y, z))  # Combine coordinates into a 2D array
    return np.array(points)


def create_bottle(offsets: np.ndarray, filename: str) -> str:
    temp_file = "../bottles/" + filename + "_pretty" + ".stl"
    output_file = filename + ".stl"

    crvs = [curve_factory.cubic_curve(PointsInCircum(0.3, 0, 6), boundary=4)]
    indexOffset = 0
    for i in range(1, 6):
        points = PointsInCircum(1, i, 6)

        factor = offsets[indexOffset]
        points[i][0] *= factor
        points[i][1] *= factor
        indexOffset += 1

        crv = curve_factory.cubic_curve(points, boundary=4)
        crvs.append(crv)

    crvs.append(curve_factory.cubic_curve(PointsInCircum(1, 6.05, 6), boundary=4))
    # crvs.append(curve_factory.cubic_curve(PointsInCircum(1.5, 10, 6), boundary=4))

    bottle = surface_factory.loft(crvs)

    # Dump result as an stl file which can be viewed in for instance Meshlab
    with STL(temp_file) as myfile:
        myfile.write(
            bottle, n=100
        )  # swap() is to make sure normals are pointing out of the object

    bpy.ops.wm.read_factory_settings()
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.delete()

    bpy.ops.import_mesh.stl(filepath=temp_file)
    bpy.ops.import_mesh.stl(filepath="../cylinder_top.stl")

    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is a mesh
        if obj.type == "MESH":
            # Select the mesh object
            obj.select_set(True)
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=0.01)

    bpy.ops.mesh.normals_make_consistent(inside=False)

    bpy.ops.object.mode_set(mode="OBJECT")

    obj = bpy.context.active_object

    # Enable auto-smooth
    obj.data.use_auto_smooth = True

    # Set the auto-smooth angle (in radians)
    # obj.data.auto_smooth_angle = 0.785398  # 45 degrees

    # Update the mesh to reflect the changes
    obj.data.update()

    modifier = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
    modifier.thickness = 0.1  # Adjust the thickness as needed

    bpy.ops.object.modifier_apply(modifier=modifier.name)

    bpy.ops.export_mesh.stl(filepath="../mesh_data/" + output_file, use_selection=True)

    return output_file
