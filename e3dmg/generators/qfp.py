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
# A generator for QFP style components. It is based on Jedec
# MS-026D.
#

import cadquery as cq
from e3dmg import ComponentModel, Generator
from math import tan, radians, sqrt

class QFPGen(Generator):

    def __init__(self, D, E, D1, E1, A1, A2, b, e, npx, npy, epad):
        self.D = D          # overall width
        self.E = E          # overall length
        self.D1 = D1        # body width
        self.E1 = E1        # body length
        self.A1 = A1        # body-board seperation
        self.A2 = A2        # body height
        self.b = b          # pin width
        self.e = e          # pin (center-to-center) distance
        self.npx = npx      # number of pins along X axis (width)
        self.npy = npy      # number of pins along y axis (length)
        self.epad = epad    # exposed pad, None or the dimensions as tuple: (width, length)

        # common dimensions from MS-026D
        self.the = 12.0      # body angle in degrees
        self.tb_s = 0.15     # top part of body is that much smaller

        self.c = 0.1         # pin thickness, body center part height
        self.R1 = 0.1        # pin upper corner, inner radius
        self.R2 = 0.1        # pin lower corner, inner radius
        self.S = 0.2         # pin top flat part length (excluding corner arc)

        # other common dimensions
        self.fp_r = 0.5      # first pin indicator radius
        self.fp_d = 0.2      # first pin indicator distance from edge
        self.fp_z = 0.1      # first pin indicator depth
        self.ef = 0.05       # fillet of edges
        self.max_cc1 = 1     # maximum size for 1st pin corner chamfer

        self.case_color = (0.1, 0.1, 0.1)
        self.pins_color = (0.9, 0.9, 0.9)

    def generate(self):
        """Returns a ComponentModel."""
        # prepare parameters for easier access
        D = self.D
        E = self.E
        D1 = self.D1
        E1 = self.E1
        A1 = self.A1
        A2 = self.A2
        b = self.b
        e = self.e
        npx = self.npx
        npy = self.npy
        epad = self.epad

        the = self.the
        tb_s = self.tb_s

        c = self.c
        R1 = self.R1
        R2 = self.R2
        S = self.S

        fp_r = self.fp_r
        fp_d = self.fp_d
        fp_z = self.fp_z
        ef = self.ef
        max_cc1 = self.max_cc1

        if self.epad:
            D2 = self.epad[0]
            E2 = self.epad[1]

        # calculated dimensions for body
        A = A1 + A2
        A2_t = (A2-c)/2 # body top part height
        A2_b = A2_t     # body bottom part height
        D1_b = D1-2*tan(radians(the))*A2_b # bottom width
        E1_b = E1-2*tan(radians(the))*A2_b # bottom length
        D1_t1 = D1-tb_s # top part bottom width
        E1_t1 = E1-tb_s # top part bottom length
        D1_t2 = D1_t1-2*tan(radians(the))*A2_t # top part upper width
        E1_t2 = E1_t1-2*tan(radians(the))*A2_t # top part upper length

        # calculate chamfers
        totpinwidthx = (npx-1)*e+b # total width of all pins on the X side
        totpinwidthy = (npy-1)*e+b # total width of all pins on the Y side

        cc1 = min((D1-totpinwidthx)/2., (E1-totpinwidthy)/2.) - 0.5*tb_s
        cc1 = min(cc1, max_cc1)
        cc = cc1/2.

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

        # start drawing with case model
        case = cq.Workplane(cq.Plane.XY()).workplane(offset=A1)
        case = crect(case, D1_b, E1_b, cc1-(D1-D1_b)/4., cc-(D1-D1_b)/4.)  # bottom edges
        case = case.pushPoints([(0,0)]).workplane(offset=A2_b)
        case = crect(case, D1, E1, cc1, cc)     # center (lower) outer edges
        case = case.pushPoints([(0,0)]).workplane(offset=c)
        case = crect(case, D1,E1,cc1, cc)       # center (upper) outer edges
        case = crect(case, D1_t1,E1_t1, cc1-(D1-D1_t1)/4., cc-(D1-D1_t1)/4.) # center (upper) inner edges
        case = case.pushPoints([(0,0)]).workplane(offset=A2_t)
        cc1_t = cc1-(D1-D1_t2)/4. # this one is defined because we use it later
        case = crect(case, D1_t2,E1_t2, cc1_t, cc-(D1-D1_t2)/4.) # top edges
        case = case.loft(ruled=True).faces(">Z").fillet(ef)

        # first pin indicator is created with a spherical pocket
        sphere_r = (fp_r*fp_r/2 + fp_z*fp_z) / (2*fp_z)
        sphere_z = A + sphere_r * 2 - fp_z - sphere_r
        sphere_x = -D1_t2/2.+cc1_t/2.+(fp_d+fp_r)/sqrt(2)
        sphere_y = -E1_t2/2.+cc1_t/2.+(fp_d+fp_r)/sqrt(2)
        sphere = cq.Workplane("XY", (sphere_x, sphere_y, sphere_z)). \
                 sphere(sphere_r)
        case = case.cut(sphere)

        # calculated dimensions for pin
        R1_o = R1+c # pin upper corner, outer radius
        R2_o = R2+c # pin lower corner, outer radius
        L = (D-D1)/2.-R1-R2-S

        # Create a pin object at the center of top side.
        bpin = cq.Workplane("YZ", (0,E1/2,0)). \
               moveTo(-tb_s, A1+A2_b). \
               line(S+tb_s, 0). \
               threePointArc((S+R1/sqrt(2), A1+A2_b-R1*(1-1/sqrt(2))),
                             (S+R1, A1+A2_b-R1)). \
               line(0, -(A1+A2_b-R1-R2_o)). \
               threePointArc((S+R1+R2_o*(1-1/sqrt(2)), R2_o*(1-1/sqrt(2))),
                             (S+R1+R2_o, 0)). \
               line(L-R2_o, 0). \
               line(0, c). \
               line(-(L-R2_o), 0). \
               threePointArc((S+R1+R2_o-R2/sqrt(2), c+R2*(1-1/sqrt(2))),
                             (S+R1+R2_o-R1, c+R2)). \
               lineTo(S+R1+c, A1+A2_b-R1). \
               threePointArc((S+R1_o/sqrt(2), A1+A2_b+c-R1_o*(1-1/sqrt(2))),
                             (S, A1+A2_b+c)). \
               line(-S-tb_s, 0).close().extrude(b).translate((-b/2,0,0))

        pins = []
        # create top, bottom side pins
        first_pos = -(npx-1)*e/2
        for i in range(npx):
            pin = bpin.translate((first_pos+i*e, 0, 0))
            pins.append(pin)
            pin = bpin.translate((first_pos+i*e, 0, 0)).\
                  rotate((0,0,0), (0,0,1), 180)
            pins.append(pin)

        # create right, left side pins
        first_pos = -(npy-1)*e/2
        for i in range(npy):
            pin = bpin.translate((first_pos+i*e, (D1-E1)/2, 0)).\
                  rotate((0,0,0), (0,0,1), 90)
            pins.append(pin)
            pin = bpin.translate((first_pos+i*e, (D1-E1)/2, 0)).\
                  rotate((0,0,0), (0,0,1), 270)
            pins.append(pin)

        # create exposed thermal pad if requested
        if self.epad:
            pins.append(cq.Workplane("XY").box(D2, E2, A1).translate((0,0,A1/2)))

        # merge all pins to a single object
        merged_pins = pins[0]
        for p in pins[1:]:
            merged_pins = merged_pins.union(p)
        pins = merged_pins

        # extract pins from case
        case = case.cut(pins)

        model = ComponentModel()
        model.addPart(case, self.case_color, "body")
        model.addPart(pins, self.pins_color, "pins")

        return model
