# -*- coding: utf-8 -*-
#
# Copyright © 2015 Maurice https://launchpad.net/~easyw
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
# A generator for QFN style components. Based on;
# https://github.com/easyw/kicad-3d-models-in-freecad/blob/master/cadquery/FCAD_script_generator/make_qfn_export_fc.py
#

import cadquery as cq
from e3dmg import ComponentModel, Generator
from e3dmg.cqutils import crect
from math import tan, radians

class QFNGen(Generator):

    def __init__(self, D, E, A, A1, b, e, npx, npy, epad,
                 flanged=False, D1=None, E1=None, the=None, P=None):
        self.D = D        # body overall length
        self.E = E        # body overall width
        self.A = A        # overall height
        self.A1 = A1      # body-board separation
        self.b = b        # pin width
        self.e = e        # pin (center to center) distance, pitch
        self.npx = npx    # number of pins along X axis (width)
        self.npy = npy    # number of pins along Y axis (length)
        self.epad = epad  # exposed pad, `None` or `(length D2, width E2)`

        self.A3 = 0.2     # terminal thickness (pin height on the side)
        self.L = 0.35     # pin length (at the bottom of the package)
        self.ef = 0.03    # fillet of the edges
        self.fp_r = 0.2   # first pin indicator radius
        self.fp_d = 0.05  # first pin indicator depth
        self.fp_t = 0.2   # first pin indicator distance from edge
        self.ecc = 0.2    # epad fpi corner chamfer

        # parameters specific to molded case type
        self.flanged = flanged # case type flanged (molded) or standard (saw cut)
        self.D1 = D1      # molded top length
        self.E1 = E1      # molded top width
        self.the = the    # mold draft angle
        self.P = P        # corner chamfer

        self.case_color = (0.1, 0.1, 0.1)
        self.pins_color = (0.9, 0.9, 0.9)

    def generate(self):
        D = self.D
        E = self.E
        A = self.A
        A1 = self.A1
        b = self.b
        e = self.e
        npx = self.npx
        npy = self.npy

        A3 = self.A3
        L = self.L
        ef = self.ef
        fp_r = self.fp_r
        fp_d = self.fp_d
        fp_t = self.fp_t
        ecc = self.ecc

        if self.epad:
            D2 = self.epad[0]
            E2 = self.epad[1]

        if self.flanged:
            D1 = self.D1
            E1 = self.E1
            the = self.the
            P = self.P

        # calculated dimensions
        A2 = A - A1

        # draw the case
        cw = D-A1*2
        cl = E-A1*2
        if not self.flanged: # standard simple box style case
            case = cq.Workplane("XY").workplane(offset=A1). \
                   box(cw, cl, A2, centered=(True,True,False)) # margin (A1) to see fused pins
            case = case.edges("|Z").fillet(ef)
            case = case.faces(">Z").fillet(ef)
            # draw first pin indicator
            fp_x = -(cw/2)+fp_t+fp_r
            fp_y = -(cl/2)+fp_t+fp_r
            case = case.faces(">Z").workplane().center(fp_x, fp_y).hole(fp_r*2, fp_d)
        else: # molded case type
            D1_t = D1-2*tan(radians(the))*(A-A3)
            E1_t = E1-2*tan(radians(the))*(A-A3)
            case = cq.Workplane("XY").workplane(offset=A1)
            case = crect(case, cw, cl, P, P)
            case = case.extrude(A3-A1)
            case = case.faces(">Z").workplane()
            case = crect(case, D1, E1, P*0.8, P*0.8).\
                   workplane(offset=A-A3)
            case = crect(case, D1_t, E1_t, P*0.6, P*0.6).\
                   loft(ruled=True)

            # fillet the bottom vertical edges
            case = case.edges("|Z").fillet(ef)

            # fillet top and side faces of the top molded part
            BS = cq.selectors.BoxSelector
            case = case.edges(BS((-D1/2, -E1/2, A3+0.001), (D1/2, E1/2, A+0.001))).fillet(ef)

            # draw first pin indicator
            fp_x = -(D1_t/2)+fp_t+fp_r
            fp_y = -(E1_t/2)+fp_t+fp_r
            case = case.faces(">Z").workplane().center(fp_x, fp_y).hole(fp_r*2, fp_d)

        # draw pins
        bpin = cq.Workplane("XY").\
                moveTo(b, 0). \
                lineTo(b, L-b/2). \
                threePointArc((b/2,L),(0, L-b/2)). \
                lineTo(0, 0). \
                close().extrude(A3).translate((b/2,E/2,0)). \
                rotate((b/2,E/2,0), (0,0,1), 180)

        pins = []

        # create top and bottom side pins
        first_pos = -(npx-1)*e/2
        for i in range(npx):
            pin = bpin.translate((first_pos+i*e, 0, 0))
            pins.append(pin)
            pin = bpin.translate((first_pos+i*e, 0, 0)).\
                  rotate((0,0,0), (0,0,1), 180)
            pins.append(pin)

        # create right and left side pins
        for i in range(npy):
            pin = bpin.translate((first_pos+i*e, (D-E)/2, 0)).\
                  rotate((0,0,0), (0,0,1), 90)
            pins.append(pin)
            pin = bpin.translate((first_pos+i*e, (D-E)/2, 0)).\
                  rotate((0,0,0), (0,0,1), 270)
            pins.append(pin)

        # draw exposed pad
        if self.epad:
            #pins.append(cq.Workplane("XY").box(D2, E2, A1+A1/10).translate((0,0,A1+A1/10)))
            epad = cq.Workplane("XY"). \
                   moveTo(-D2/2+ecc, -E2/2). \
                   lineTo(D2/2, -E2/2). \
                   lineTo(D2/2, E2/2). \
                   lineTo(-D2/2, E2/2). \
                   lineTo(-D2/2, -E2/2+ecc). \
                   close().extrude(A1)
            pins.append(epad)

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
