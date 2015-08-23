#!/usr/bin/python
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

import os
import FreeCAD, FreeCADGui
import cadquery as cq

def makeFCObject(doc, cqobject, color=None):
    """Creates an Object in document tree.
    `doc` : FreeCAD document object
    `cqobject` : cadquery object
    `color` : color RGB tuple
    """
    o = doc.addObject("Part::Feature", "Box")
    o.Shape = cqobject.toFreecad()
    if color: o.ViewObject.ShapeColor = color
    return o

def exportx3d(objects, filename):
    from export_x3d import exportX3D, objectToMesh, Mesh

    def shapeToMesh(shape, color):
        mesh_data = shape.tessellate(1)
        return Mesh(points = mesh_data[0],
                    faces = mesh_data[1],
                    color = color)

    meshes = []
    for o in objects:
        meshes.append(shapeToMesh(o[0].toFreecad(), o[1]))

    exportX3D(meshes, filename)

def export(ftype, componentModel, filename, fuse=False):
    """ Exports given ComponentModel object using FreeCAD.

    `ftype` : one of "STEP", "VRML", "FREECAD", "X3D"
    `componentModel` : a ComponentModel instance
    `filename` : name of the file, extension is important
    `fuse` : fuse objects together before export (preserves color)

    X3D exporter doesn't support `fuse` parameter.
    """
    # objects = []
    # for p in componentModel.parts:
    #     objects.append((p[0], p[1]))

    objects = componentModel.parts
    # TODO: raise Exception, if there are no objects to export!

    if len(objects) == 1: # can't fuse if there is only 1 object
        fuse = False

    # export to X3D, continue for other exporters (VRML, FREECAD, STEP)
    if ftype == "X3D":
        if fuse: print("X3D exporter can't do fuse, ignoring.")
        exportx3d(objects, filename)
        return

    # init FreeCADGui
    try:
        import ImportGui
    except ImportError:
        FreeCADGui.showMainWindow()
        FreeCADGui.getMainWindow().hide() # prevent splash of main window
        import ImportGui # must be after `showMainWindow`

    # make sure RefineShape=False
    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/Boolean")
    usersRSOption = pg.GetBool("RefineModel") # will be restored, we promise
    pg.SetBool("RefineModel", False)

    # create a FreeCAD document
    doc = FreeCAD.newDocument()

    # create objects
    fcobjects = [makeFCObject(doc, co[0], co[1]) for co in objects]

    if fuse:
        fuseobj = doc.addObject("Part::MultiFuse","Fusion")
        fuseobj.Shapes = fcobjects
        doc.recompute()
        exportObjects = [fuseobj]
    else:
        exportObjects = fcobjects

    doc.recompute()

    if ftype == "STEP":
        ImportGui.export(exportObjects, filename)
    elif ftype == "VRML":
        # workaround for not exporting unselected objects (v0.16)
        # http://www.freecadweb.org/tracker/view.php?id=2221
        FreeCADGui.Selection.clearSelection()
        for o in exportObjects: FreeCADGui.Selection.addSelection(o)
        # TODO: ensure the filename ends with .wrl
        FreeCADGui.export(exportObjects, filename)
    elif ftype == "FREECAD":
        # TODO: export only the exportObjects by moving to a new
        #       document or deleting other objects
        doc.saveAs(filename)
    else:
        raise Exception("Unknown export file type!")

    # restore RefineShape option
    pg.SetBool("RefineModel", usersRSOption)
