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

class Material(object):
    def __init__(self, diffuseColor, ambientIntensity = .2,
                 specularColor = (0,0,0), shininess = .2,
                 emissiveColor = (0,0,0), transparency = 0):
        """Default values are taken from VRML 2.0 specification."""
        self.diffuseColor = diffuseColor
        self.ambientIntensity = ambientIntensity
        self.specularColor = specularColor
        self.shininess = shininess
        self.emissiveColor = emissiveColor
        self.transparency = transparency

class ComponentModel(object):

    def __init__(self):
        # list of tuples: (cqobject, part_color, part_name)
        self.parts = []

    def addPart(self, cqobject, color, name=None):
        """Add a cqobject as part of this ComponentModel."""
        self.parts.append((cqobject, color, name))

    def show(self):
        """Displays the model using cadquery helper functions. These functions
        are provided by cadquery-freecad-module thus you should call
        this method only from FreeCad Cadquery workbench."""
        import Helpers
        for p in self.parts:
            color = (p[1][0]*255, p[1][1]*255, p[1][2]*255, 0)
            Helpers.show(p[0], color)
