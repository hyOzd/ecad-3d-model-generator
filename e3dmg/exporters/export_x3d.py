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
# This is a script to export FreeCAD objects as X3D files.
#

import FreeCAD
import xml.etree.ElementTree as et
import os
from collections import namedtuple
from e3dmg import Material

# points: [Vector, Vector, ...]
# faces: [(pi, pi, pi), ], pi: point index
# color: (Red, Green, Blue), values range from 0 to 1.0
Mesh = namedtuple('Mesh', ['points', 'faces', 'color'])

def getShapeNode(vertices, faces, color=None):
    """Returns a <Shape> node for given mesh data.
    vertices: list of vertice coordinates as `Vector` type
    faces: list of tuple of vertice indexes ex: (1, 2, 3)
    color: tuple in the form of (R, G, B) or `componentmodel.Material`"""

    shapeNode = et.Element('Shape')
    faceNode = et.SubElement(shapeNode, 'IndexedFaceSet')
    faceNode.set('coordIndex', ' '.join(["%d %d %d -1" % face for face in faces]))
    coordinateNode = et.SubElement(faceNode, 'Coordinate')
    coordinateNode.set('point',
        ' '.join(["%f %f %f" % (p.x, p.y, p.z) for p in vertices]))

    if color != None:
        if isinstance(color, Material):
            appearanceNode = et.SubElement(shapeNode, 'Appearance')
            materialNode = et.SubElement(appearanceNode, 'Material')
            materialNode.set('diffuseColor', "%f %f %f" % color.diffuseColor)
            materialNode.set('ambientIntensity', "%f" % color.ambientIntensity)
            materialNode.set('specularColor', "%f %f %f" % color.specularColor)
            materialNode.set('shininess', "%f" % color.shininess)
            materialNode.set('emissiveColor', "%f %f %f" % color.emissiveColor)
            materialNode.set('transparency', "%f" % color.transparency)
        else: # tuple of (R, G, B) expected
            appearanceNode = et.SubElement(shapeNode, 'Appearance')
            materialNode = et.SubElement(appearanceNode, 'Material')
            materialNode.set('diffuseColor', "%f %f %f" % color)

    return shapeNode

def exportX3D(objects, filepath):
    """Export given list of Mesh objects to a X3D file."""

    fileNode = et.Element('X3D')
    fileNode.set('profile', 'Interchange')
    fileNode.set('version', '3.3')
    sceneNode = et.SubElement(fileNode, 'Scene')

    for o in objects:
        shapeNode = getShapeNode(o.points, o.faces, o.color)
        sceneNode.append(shapeNode)

    with open(filepath, "w") as f:
        f.write(et.tostring(fileNode))
