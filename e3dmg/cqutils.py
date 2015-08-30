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
# This file contains drawing utilities for cadquery.
#

def crect(wp, rw, rh, cv1, cv):
    """
    Creates a rectangle with chamfered corners.
    wp: workplane object
    rw: rectangle width
    rh: rectangle height
    cv1: chamfer value for 1st corner (lower left)
    cv: chamfer value for other corners
    """
    points = [
        (-rw/2., -rh/2.+cv1),
        (-rw/2., rh/2.-cv),
        (-rw/2.+cv, rh/2.),
        (rw/2.-cv, rh/2.),
        (rw/2., rh/2.-cv),
        (rw/2., -rh/2.+cv),
        (rw/2.-cv, -rh/2.),
        (-rw/2.+cv1, -rh/2.),
        (-rw/2., -rh/2.+cv1)
    ]
    return wp.polyline(points)
