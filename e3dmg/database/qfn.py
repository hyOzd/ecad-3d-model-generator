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

# Dimensions are taken from Microchip Packaging Specifications QFN
# section.  Only missing package missing here is 16 Lead QFN FX, which
# has a slightly different lead style.

from e3dmg.generators.qfn import QFNGen, MQFNGen

QFN16_3x3_NG = QFNGen(
    D = 3.0,
    E = 3.0,
    A = 0.90,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 16,
    epad = 1.7
)

QFN16_3x3_MG = QFNGen(
    D = 3.0,
    E = 3.0,
    A = 0.90,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 16,
    epad = 1.1
)

QFN16_4x4_ML = QFNGen(
    D = 4.0,
    E = 4.0,
    A = 0.90,
    A1 = 0.02,
    b = 0.3,
    e = 0.65,
    np = 16,
    epad = 2.65
)

QFN16_4x4_8E = QFNGen(
    D = 4.0,
    E = 4.0,
    A = 0.90,
    A1 = 0.02,
    b = 0.3,
    e = 0.65,
    np = 16,
    epad = 2.05
)

QFN20_4x4_ML = QFNGen(
    D = 4.0,
    E = 4.0,
    A = 0.90,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 20,
    epad = 2.7
)

QFN24_4x4_MJ = QFNGen(
    D = 4.0,
    E = 4.0,
    A = 0.90,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 24,
    epad = 2.7
)

QFN24_4x4_RU = MQFNGen(
    D = 4.0,
    E = 4.0,
    D1 = 3.75,
    E1 = 3.75,
    A = 0.90,
    A1 = 0.02,
    P = 0.42,
    b = 0.25,
    e = 0.5,
    np = 24,
    epad = 2.5
)

QFN24_5x5_LY = QFNGen(
    D = 5.0,
    E = 5.0,
    A = 1,
    A1 = 0.02,
    b = 0.3,
    e = 0.65,
    np = 24,
    epad = 3.25
)

QFN28_5x5_MQ = QFNGen(
    D = 5.0,
    E = 5.0,
    A = 0.9,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 28,
    epad = 3.25
)

QFN28_6x6_ML = QFNGen(
    D = 6.0,
    E = 6.0,
    A = 1,
    A1 = 0.02,
    b = 0.3,
    e = 0.65,
    np = 28,
    epad = 3.7
)

QFN36_6x6_4E = MQFNGen(
    D = 6.0,
    E = 6.0,
    D1 = 5.75,
    E1 = 5.75,
    A = 0.90,
    A1 = 0.02,
    P = 0.42,
    b = 0.25,
    e = 0.5,
    np = 36,
    epad = 3.7
)

QFN40_6x6_RR = MQFNGen(
    D = 6.0,
    E = 6.0,
    D1 = 5.75,
    E1 = 5.75,
    A = 0.90,
    A1 = 0.01,
    P = 0.42,
    b = 0.23,
    e = 0.5,
    np = 40,
    epad = 4.1
)

QFN40_6x6_ML = QFNGen(
    D = 6.0,
    E = 6.0,
    A = 1,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 40,
    epad = 4.65
)

QFN40_6x6_MP = QFNGen(
    D = 5.0,
    E = 5.0,
    A = 0.9,
    A1 = 0.02,
    b = 0.2,
    e = 0.4,
    np = 40,
    epad = 3.5
)

QFN40_6x6_MP_3_7_epad = QFNGen(
    D = 5.0,
    E = 5.0,
    A = 0.9,
    A1 = 0.02,
    b = 0.2,
    e = 0.4,
    np = 40,
    epad = 3.7
)

QFN44_8x8_ML = QFNGen(
    D = 8.0,
    E = 8.0,
    A = 1,
    A1 = 0.02,
    b = 0.3,
    e = 0.65,
    np = 44,
    epad = 6.45
)

QFN48_7x7_5E = MQFNGen(
    D = 7.0,
    E = 7.0,
    D1 = 6.75,
    E1 = 6.75,
    A = 0.90,
    A1 = 0.01,
    P = 0.42,
    b = 0.25,
    e = 0.5,
    np = 48,
    epad = 5.1
)

QFN64_9x9_MR = QFNGen(
    D = 9.0,
    E = 9.0,
    A = 1,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 64,
    epad = 7.15
)

QFN64_9x9_MR_5_4_epad = QFNGen(
    D = 9.0,
    E = 9.0,
    A = 1,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 64,
    epad = 5.4
)

QFN64_9x9_MR_7_7_epad = QFNGen(
    D = 9.0,
    E = 9.0,
    A = 1,
    A1 = 0.02,
    b = 0.25,
    e = 0.5,
    np = 64,
    epad = 7.7
)

QFN64_9x9_RG = QFNGen(
    D = 9.0,
    E = 9.0,
    A = 0.9,
    A1 = 0.02,
    b = 0.20,
    e = 0.5,
    np = 64,
    epad = 4.7
)

QFN72_10x10_5E = MQFNGen(
    D = 10.0,
    E = 10.0,
    D1 = 9.75,
    E1 = 9.75,
    A = 0.90,
    A1 = 0.01,
    P = 0.42,
    b = 0.23,
    e = 0.5,
    np = 72,
    epad = 6
)
