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
# This is an example generator. It generates a simple component in the
# shape of a box. Yes, just a box.
#

import cadquery as cq
from e3dmg import ComponentModel, Generator

class BoxGen(Generator):

    def __init__(self, l, w, h, color):
        self.l = l
        self.w = w
        self.h = h
        self.color = color

    def generate(self):
        """Returns a ComponentModel."""
        b = cq.Workplane("XY").box(self.l, self.w, self.h)
        model = ComponentModel()
        model.addPart(b, self.color, "Body")
        return model
