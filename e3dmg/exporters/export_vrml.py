# -*- coding: utf-8 -*-
#
# Copyright © 2015 Hasan Yavuz Özderya
#
# This file is part of ecad-3d-model-generator.
#
# ecad-3d-model-generator is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# ecad-3d-model-generator is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ecad-3d-model-generator.  If not, see
# <http://www.gnu.org/licenses/>.
#
# This is an exporter script for exporting cadquery objects as STEP
# models. It uses FreeCADs gui library. Note that this library
# initalizes FreeCAD's mainwindow thus enables some GUI
# functionality. This may have some unknown (yet) side effects.
#

#
# This is a script to export FreeCAD objects as VRML files.
#
# FreeCAD already supports pretty good VRML export. This script on the
# other hand will produce a slightly more dense output thus smaller
# file size. Main factor is the lack of indentation and new lines.
#

from e3dmg import Material

def meshToVRML(mesh):
    """Returns the VRML Shape node representation of a `Mesh`"""
    s = "Shape { geometry IndexedFaceSet { coordIndex ["
    # write coordinate indexes for each face
    s += ','.join("%d,%d,%d,-1" % f for f in mesh.faces)
    s += "]" # closes coordIndex
    s += "coord Coordinate { point ["
    # write coordinate points for each vertex
    s += ','.join('%.3f %.3f %.3f' % (p.x, p.y, p.z) for p in mesh.points)
    s += "]}" # closes Coordinate
    s += "}\n" # closes IndexedFaceSet

    if isinstance(mesh.color, Material):
        material = "diffuseColor %f %f %f\n" % mesh.color.diffuseColor + \
                   "ambientIntensity %f\n" % mesh.color.ambientIntensity + \
                   "specularColor %f %f %f\n" % mesh.color.specularColor + \
                   "shininess %f\n" % mesh.color.shininess + \
                   "emissiveColor %f %f %f\n" % mesh.color.emissiveColor + \
                   "transparency %f\n" % mesh.color.transparency
        s += "appearance Appearance{material Material{%s}}" % material
    else:
        print(mesh.color)
        s += "appearance Appearance{material Material{diffuseColor %f %f %f}}" % mesh.color

    s += "}\n" # closes Shape

    return s

def shapeToMesh(shape, color, scale=None):
    from export_x3d import Mesh
    mesh_data = shape.tessellate(1)
    points = mesh_data[0]
    if scale != None:
        points = map(lambda p: p*scale, points)
    return Mesh(points = points,
                faces = mesh_data[1],
                color = color)

def exportVRML(objects, filepath):
    """Export given list of Mesh objects to a VRML file.

    `Mesh` structure is defined in 'export_x3d.py'."""

    with open(filepath, 'w') as f:
        # write the standard VRML header
        f.write("#VRML V2.0 utf8\n\n")

        for obj in objects:
            f.write(meshToVRML(obj))

def exportVRML2(objects, filepath):
    """This is an EXPERIMENTAL exporter. Unlike above one, this one can
    export fused multi color FreeCAD shapes, but it also relies on
    FreeCADGui module. Output isn't good either (each face exported as
    a different shape).
    """

    with open(filepath, 'w') as f:
        # write the standard VRML header
        f.write("#VRML V2.0 utf8\n\n")

        for obj in objects:
            # does object have different colored faces?
            if len(obj.ViewObject.DiffuseColor) > 1:
                for i, face in enumerate(obj.Shape.Faces):
                    f.write(meshToVRML(shapeToMesh(face, obj.ViewObject.DiffuseColor[i][0:3])))
            else:
                raise NotImplemented("Use other exporter :P")
