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
# Test component models. These models are not even components.
#

from e3dmg.generators.box import BoxGen
from e3dmg import Material

red = (1.,0.,0.)
green = (0.,1.,0.)
blue = (0.,0.,1.)

chrome = Material(diffuseColor = (.3, .3, .3),
                  ambientIntensity = 0.3,
                  specularColor = (.7, .7, .8),
                  shininess = .09)

cube5x5x5 = BoxGen(5,5,5,red)
cube10x10x10 = BoxGen(10,10,10,green)
cube15x15x15 = BoxGen(15,15,15,blue)

chrome_cube = BoxGen(5,5,5,chrome)
