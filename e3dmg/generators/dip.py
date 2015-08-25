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

import cadquery as cq
from e3dmg import ComponentModel, Generator
from math import tan, radians, sqrt
from e3dmg.utils import mm

class DIPGen(Generator):

    def __init__(self, D, E1, E, A1, A2, b1, b, e, npins):
        self.D = D    # package length
        self.E1 = E1  # package width
        self.E = E    # package shoulder-to-shoulder width
        self.A1 = A1  # package board seperation
        self.A2 = A2  # package height
        self.b1 = b1  # pin width
        self.b = b    # pin width
        self.e = e    # pin center to center distance (pitch)
        self.npins = npins  # number of pins

        # common dimensions

        self.L = 3.3         # tip to seating plane
        self.c = 0.254       # lead thickness

        self.fp_r = 0.8      # first pin indicator radius
        self.fp_d = 0.2      # first pin indicator depth
        self.fp_t = 0.4      # first pin indicator distance from edge
        self.ef = 0.05       # fillet of edges

        self.ti_r = 0.75     # top indicator radius
        self.ti_d = 0.5      # top indicator depth

        self.the = 12.0      # body angle in degrees
        self.tb_s = 0.15     # top part of body is that much smaller

        self.case_color = (0.1, 0.1, 0.1)
        self.pins_color = (0.9, 0.9, 0.9)

    def generate(self):
        # extract parameters to local namespace
        D = self.D
        E1 = self.E1
        E = self.E
        A1 = self.A1
        A2 = self.A2
        b1 = self.b1
        b = self.b
        e = self.e
        npins = self.npins
        L = self.L
        c = self.c
        fp_r = self.fp_r
        fp_d = self.fp_d
        fp_t = self.fp_t
        ef = self.ef
        ti_r = self.ti_r
        ti_d = self.ti_d
        the = self.the
        tb_s = self.tb_s

        # calculated dimensions

        A = A1 + A2

        A2_t = (A2-c)/2.# body top part height
        A2_b = A2_t     # body bottom part height
        D_b = D-2*tan(radians(the))*A2_b # bottom length
        E1_b = E1-2*tan(radians(the))*A2_b # bottom width
        D_t1 = D-tb_s # top part bottom length
        E1_t1 = E1-tb_s # top part bottom width
        D_t2 = D_t1-2*tan(radians(the))*A2_t # top part upper length
        E1_t2 = E1_t1-2*tan(radians(the))*A2_t # top part upper width

        # start drawing with case
        case = cq.Workplane(cq.Plane.XY()).workplane(offset=A1).rect(D_b, E1_b). \
               workplane(offset=A2_b).rect(D, E1).workplane(offset=c).rect(D,E1). \
               rect(D_t1,E1_t1).workplane(offset=A2_t).rect(D_t2,E1_t2). \
               loft(ruled=True)

        # draw top indicator
        case = case.faces(">Z").center(D_b/2., 0).hole(ti_r*2, ti_d)

        # draw 1st pin (side pin shape)
        x = e*(npins/4.-0.5) # center x position of first pin
        ty = (A2+c)/2.+A1 # top point (max z) of pin

        # draw the side part of the pin
        pin = cq.Workplane("XZ", (x, E/2., 0)).\
              moveTo(+b/2., ty).line(0, -(L+ty-b)).line(-b/4.,-b).line(-b/2.,0).\
              line(-b/4.,b).line(0,L-b).line(-(b1-b)/2.,0).line(0,ty).close().extrude(c)

        # draw the top part of the pin
        pin = pin.faces(">Z").workplane().center(-(b1+b)/4.,c/2.).\
              rect((b1+b)/2.,-E/2.,centered=False).extrude(-c)

        # fillet the corners
        def fillet_corner(pina):
            BS = cq.selectors.BoxSelector
            return pina.edges(BS((1000, E/2.-c-0.001, ty-c-0.001), (-1000, E/2.-c+0.001, ty-c+0.001))).\
                fillet(c/2.).\
                edges(BS((1000, E/2.-0.001, ty-0.001), (-1000, E/2.+0.001, ty+0.001))).\
                fillet(1.5*c)

        pin = fillet_corner(pin)

        # draw the 2nd pin (regular pin shape)
        x = e*(npins/4.-0.5-1) # center x position of 2nd pin
        pin2 = cq.Workplane("XZ", (x, E/2., 0)).\
               moveTo(b1/2., ty).line(0, -ty).line(-(b1-b)/2.,0).line(0,-L+b).\
               line(-b/4.,-b).line(-b/2.,0).line(-b/4.,b).line(0,L-b).\
               line(-(b1-b)/2.,0).line(0,ty).\
               close().extrude(c)

        # draw the top part of the pin
        pin2 = pin2.faces(">Z").workplane().center(0,-E/4.).rect(b1,-E/2.).extrude(-c)
        pin2 = fillet_corner(pin2)

        # create other pins (except last one)
        pins = [pin, pin2]
        for i in range(2,npins/2-1):
            pin_i = pin2.translate((-e*(i-1),0,0))
            pins.append(pin_i)

        # create last pin (mirrored 1st pin)
        x = -e*(npins/4.-0.5)
        pinl = cq.Workplane("XZ", (x, E/2., 0)).\
               moveTo(-b/2., ty).line(0, -(L+ty-b)).line(b/4.,-b).line(b/2.,0).\
               line(b/4.,b).line(0,L-b).line((b1-b)/2.,0).line(0,ty).close().\
               extrude(c).\
               faces(">Z").workplane().center(-(b1+b)/4.,c/2.).\
               rect((b1+b)/2.,-E/2.,centered=False).extrude(-c)
        pinl = fillet_corner(pinl)

        pins.append(pinl)

        def union_all(objects):
            o = objects[0]
            for i in range(1,len(objects)):
                o = o.union(objects[i])
            return o

        # union all pins
        pins = union_all(pins)

        # create other side of the pins (mirror would be better but there
        # is no solid mirror API)
        pins = pins.union(pins.rotate((0,0,0), (0,0,1), 180))

        # finishing touches
        BS = cq.selectors.BoxSelector
        case = case.edges(BS((D_t2/2.+0.1, E1_t2/2., 0), (D/2.+0.1, E1/2.+0.1, A2))).fillet(ef)
        case = case.edges(BS((-D_t2/2., E1_t2/2., 0), (-D/2.-0.1, E1/2.+0.1, A2))).fillet(ef)
        case = case.edges(BS((-D_t2/2., -E1_t2/2., 0), (-D/2.-0.1, -E1/2.-0.1, A2))).fillet(ef)
        case = case.edges(BS((D_t2/2., -E1_t2/2., 0), (D/2.+0.1, -E1/2.-0.1, A2))).fillet(ef)
        case = case.edges(BS((D/2.,E1/2.,A-ti_d-0.001), (-D/2.,-E1/2.,A+0.1))).fillet(ef)

        # add first pin indicator
        case = case.faces(">Z").workplane().center(D_t2/2.-fp_r-fp_t,E1_t2/2.-fp_r-fp_t).\
               hole(fp_r*2, fp_d)

        # extract pins from the case
        case = case.cut(pins)

        model = ComponentModel()
        model.addPart(case, self.case_color, "body")
        model.addPart(pins, self.pins_color, "pins")
        return model

class DIP300Gen(DIPGen):
    """A sub-generator for 300mil wide DIP packages"""
    def __init__(self, D, npins):
        DIPGen.__init__(
            self,
            D = D,         # package length
            E1 = 6.35,     # package width
            E = 7.874,     # shoulder to shoulder width (includes pins)
            A1 = 0.38,     # base to seating plane
            A2 = 3.3,      # package height
            b1 = 1.524,    # upper lead width
            b = 0.457,     # lower lead width
            e = 2.54,      # pin to pin distance
            npins = npins  # total number of pins
        )

class DIP600Gen(DIPGen):
    """A sub-generator for 600mil wide DIP packages"""
    def __init__(self, D, npins):
        DIPGen.__init__(
            self,
            D = D,          # package length
            E1 = mm(0.53),  # package width
            E = mm(0.61),   # shoulder to shoulder width (includes pins)
            A1 = 0.38,      # base to seating plane
            A2 = 3.3,       # package height
            b1 = 1.524,     # upper lead width
            b = 0.457,      # lower lead width
            e = 2.54,       # pin to pin distance
            npins = npins   # total number of pins
        )
