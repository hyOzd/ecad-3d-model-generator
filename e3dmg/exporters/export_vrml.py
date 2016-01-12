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

def exportVRML(objects, filepath):
    """Export given list of Mesh objects to a VRML file.

    `Mesh` structure is defined in 'export_x3d.py'."""

    with open(filepath, 'w') as f:
        # write the standard VRML header
        f.write("#VRML V2.0 utf8\n\n")

        for obj in objects:
            f.write("Shape { geometry IndexedFaceSet { coordIndex [")

            # write coordinate indexes for each face
            f.write(','.join("%d,%d,%d,-1" % f for f in obj.faces))

            f.write("]") # closes coordIndex

            f.write("coord Coordinate { point [")

            # write coordinate points for each vertex
            f.write(','.join('%.3f,%.3f,%.3f' % (p.x, p.y, p.z) for p in obj.points))

            f.write("]}") # closes Coordinate

            f.write("}\n") # closes IndexedFaceSet

            # TODO: materials
            f.write("appearance Appearance{material Material{diffuseColor %f %f %f}}" % obj.color)

            f.write("}\n") # closes Shape
