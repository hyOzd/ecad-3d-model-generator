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

from e3dmg.generators.dip import DIP300Gen, DIP600Gen
from e3dmg.utils import mm

DIP08 = DIP300Gen(
    D = 9.27,   # package length
    npins = 8  # total number of pins
)
DIP06 = DIP300Gen(7.05, 6)
DIP14 = DIP300Gen(19.05, 14)
DIP16 = DIP300Gen(mm(0.755), 16)
DIP18 = DIP300Gen(mm(0.9), 18)
DIP20 = DIP300Gen(mm(1.03), 20)
DIP22 = DIP300Gen(mm(1.1), 22)
DIP24 = DIP300Gen(mm(1.25), 24)
DIP28 = DIP300Gen(mm(1.4), 28)
DIP22_6 = DIP600Gen(mm(1.1), 22)
DIP24_6 = DIP600Gen(mm(1.25), 24)
DIP28_6 = DIP600Gen(mm(1.4), 28)
DIP32_6 = DIP600Gen(mm(1.63), 32)
DIP40_6 = DIP600Gen(mm(2), 40)
DIP48_6 = DIP600Gen(mm(2.42), 48)
DIP52_6 = DIP600Gen(mm(2.6), 52)
