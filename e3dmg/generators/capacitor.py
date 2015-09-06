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

class RadialGen(Generator):
    """Radial capacitor generator."""

    def __init__(self, L, D, d, F, ll=4., la=1., bs=1.,
                 body_color=(0.797, 0.234, 0.234)):

        self.L = L     # overall height of the body
        self.D = D     # body diameter
        self.d = d     # lead diameter
        self.F = F     # lead separation (center to center)
        self.ll = ll   # lead length
        self.la = la   # extra lead length of the anode

        self.bs = bs   # board separation

        self.br = 0.7       # radius of the belt hollow
        self.bx = 0.5       # center of the belt (sideways from the body)
        self.bd = 1.5       # center of the belt (from the bottom of the body)
        self.bf = 0.6       # belt fillet

        self.tc = 0.2       # cut thickness for the bottom&top
        self.dc = D*0.7     # diameter of the bottom&top cut
        self.ts = 0.1       # thickness of the slots at the top in the shape of (+)
        self.ws = 0.1       # width of the slots

        self.ef = 0.2       # top and bottom edges fillet

        self.body_color = body_color
        self.bottom_color = (0.156, 0.156, 0.156)
        self.top_color = (0.859, 0.859, 0.859)
        self.bar_color = (0.781, 0.781, 0.781)
        self.lead_color = (0.938, 0.938, 0.938)

    def generate(self):
        L = self.L     # overall height of the body
        D = self.D     # body diameter
        d = self.d     # lead diameter
        F = self.F     # lead separation (center to center)
        ll = self.ll   # lead length
        la = self.la   # extra lead length of the anode

        bs = self.bs     # board separation

        br = self.br      # radius of the belt hollow
        bx = self.bx      # center of the belt (sideways from the body)
        bd = self.bd      # center of the belt (from the bottom of the body)
        bf = self.bf      # belt fillet

        tc = self.tc      # cut thickness for the bottom
        dc = self.dc    # diameter of the bottom cut
        ts = self.ts      # thickness of the slots at the top in the shape of (+)
        ws = self.ws      # width of the slots

        ef = self.ef      # top and bottom edges fillet

        bpt = 0.1        # bottom plastic thickness (not visual)
        tmt = ts*2       # top metallic part thickness (not visual)

        # TODO: calculate width of the cathode marker bar from the body size
        ciba = 45  # angle of the cathode identification bar

        # TODO: calculate marker sizes according to the body size
        mmb_h = 2.       # lenght of the (-) marker on the cathode bar
        mmb_w = 0.5      # rough width of the marker

        # draw the radial body
        body = cq.Workplane("XY").workplane(offset=bs).\
               circle(D/2).extrude(L).\
               faces(">Z").fillet(ef)

        # draw and cut the belt
        belt = cq.Workplane("XZ").center(D/2+bx,bs+bd).circle(br).\
               center(-D/2-bx,0).revolve()
        body = body.cut(belt)

        # fillet the belt edges
        BS = cq.selectors.BoxSelector
        # note that edges are selected from their centers
        body = body.edges(BS((-0.1,-0.1, bs+0.1), (0.1, 0.1, bs+bd+br))).\
            fillet(bf)

        # fillet the bottom of the body
        body = body.faces("<Z").fillet(ef)

        # cut the bottom of the body
        body = body.faces("<Z").workplane().hole(dc, tc+bpt)

        # draw the plastic at the bottom
        bottom = cq.Workplane("XY").workplane(offset=bs+tc).\
                 circle(dc/2).extrude(bpt)

        # cut the top
        body = body.faces(">Z").workplane().hole(dc, tc+tmt)

        # draw the metallic part at the top
        top = cq.Workplane("XY").workplane(offset=bs+L-tc-ts).\
             circle(dc/2).extrude(tmt)

        # draw the slots on top in the shape of plus (+)
        top = top.faces(">Z").workplane().move(ws/2,ws/2).\
              line(0,D).line(-ws,0).line(0,-D).\
              line(-D,0).line(0,-ws).line(D,0).\
              line(0,-D).line(ws,0).line(0,D).\
              line(D,0).line(0,ws).close().cutBlind(-ts)

        # draw the cathode identification bar
        bar = cq.Workplane("XY").line(-D, 0).line(0,D).close().extrude(bs+L)
        bar = bar.cut(bar.translate((0,0,0)).cut(body)) # translate is used for copying
        # rotate so that it aligns with cathode pin
        bar = bar.rotate((0,0,0),(0,0,1),45/2.)

        # draw the (-) marks on the bar
        n = int(L/(2*mmb_h)) # number of (-) marks to draw
        points = []
        first_z = (L-(2*n-1)*mmb_h)/2
        for i in range(n):
            points.append((0, (i+0.25)*2*mmb_h+first_z))
        mmb = cq.Workplane("YZ", (-D/2,0,bs)).pushPoints(points).\
              box(mmb_w, mmb_h, 2).\
              edges("|X").fillet(mmb_w/2.-0.001)

        bar = bar.cut(mmb)
        body = body.cut(bar)

        # draw the leads
        leads = cq.Workplane("XY").workplane(offset=bs+tc).\
                center(-F/2,0).circle(d/2).extrude(-(ll+tc)).\
                center(F,0).circle(d/2).extrude(-(ll+tc+la))

        model = ComponentModel()
        model.addPart(body, self.body_color, "body")
        model.addPart(top, self.top_color, "top")
        model.addPart(bottom, self.bottom_color, "bottom")
        model.addPart(bar, self.bar_color, "bar")
        model.addPart(leads, self.lead_color, "pins")

        return model
