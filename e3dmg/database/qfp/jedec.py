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
# Dimensions from Jedec MS-026D.
#

from e3dmg.generators.qfp import QFPGen

AKA = QFPGen(  # 4x4, pitch 0.65 20pin 1mm height
    D = 6.0,   # overall width
    E = 6.0,   # overall length
    D1 = 4.0,  # body width
    E1 = 4.0,  # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.32,  # pin width
    e = 0.65,  # pin (center-to-center) distance
    npx = 5,   # number of pins along X axis (width)
    npy = 5,   # number of pins along y axis (length)
    epad = None)

ABD = QFPGen(  # 7x7, 0.4 pitch, 64 pins, 1mm height
    D = 9.0,   # overall width
    E = 9.0,   # overall length
    D1 = 7.0,  # body width
    E1 = 7.0,  # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.18,  # pin width
    e = 0.4,   # pin (center-to-center) distance
    npx = 16,  # number of pins along X axis (width)
    npy = 16,  # number of pins along y axis (length)
    epad = None)

AFB = QFPGen(  # 20x20, 0.5 pitch, 144pins, 1mm height
    D = 22.0,  # overall width
    E = 22.0,  # overall length
    D1 = 20.0, # body width
    E1 = 20.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.22,  # pin width
    e = 0.5,   # pin (center-to-center) distance
    npx = 36,  # number of pins along X axis (width)
    npy = 36,  # number of pins along y axis (length)
    epad = None)

ACB = QFPGen(  # 10x10, 0.8 pitch, 44 pins, 1mm height
    D = 12.0,  # overall width
    E = 12.0,  # overall length
    D1 = 10.0, # body width
    E1 = 10.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.37,  # pin width
    e = 0.8,   # pin (center-to-center) distance
    npx = 11,  # number of pins along X axis (width)
    npy = 11,  # number of pins along y axis (length)
    epad = None)

ACC = QFPGen(  # 10x10, 0.65 pitch, 52 pins, 1mm height
    D = 12.0,  # overall width
    E = 12.0,  # overall length
    D1 = 10.0, # body width
    E1 = 10.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.32,  # pin width
    e = 0.65,  # pin (center-to-center) distance
    npx = 13,  # number of pins along X axis (width)
    npy = 13,  # number of pins along y axis (length)
    epad = None)

ACE = QFPGen(  # 10x10, 0.4 pitch, 80 pins, 1mm height
    D = 12.0,  # overall width
    E = 12.0,  # overall length
    D1 = 10.0, # body width
    E1 = 10.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.18,  # pin width
    e = 0.4,   # pin (center-to-center) distance
    npx = 20,  # number of pins along X axis (width)
    npy = 20,  # number of pins along y axis (length)
    epad = None)

ADC = QFPGen(  # 12x12, 0.65 pitch, 64 pins, 1mm height
    D = 14.0,  # overall width
    E = 14.0,  # overall length
    D1 = 12.0, # body width
    E1 = 12.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.32,  # pin width
    e = 0.65,  # pin (center-to-center) distance
    npx = 13,  # number of pins along X axis (width)
    npy = 13,  # number of pins along y axis (length)
    epad = None)

ADD = QFPGen(  # 12x12, 0.5 pitch, 80 pins, 1mm height
    D = 14.0,  # overall width
    E = 14.0,  # overall length
    D1 = 12.0, # body width
    E1 = 12.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.18,  # pin width
    e = 0.5,  # pin (center-to-center) distance
    npx = 20,  # number of pins along X axis (width)
    npy = 20,  # number of pins along y axis (length)
    epad = None)

AEC = QFPGen(  # 14x14, 0.65 pitch, 80 pins, 1mm height
    D = 16.0,  # overall width
    E = 16.0,  # overall length
    D1 = 14.0, # body width
    E1 = 14.0, # body length
    A1 = 0.1,  # body-board seperation
    A2 = 1.0,  # body height
    b = 0.32,  # pin width
    e = 0.65,  # pin (center-to-center) distance
    npx = 20,  # number of pins along X axis (width)
    npy = 20,  # number of pins along y axis (length)
    epad = None)
