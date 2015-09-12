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

from math import sqrt

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

        self.bt = 1.        # flat part before belt
        self.bd = 0.2       # depth of the belt
        self.bh = 1.        # height of the belt
        self.bf = 0.3       # belt fillet

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

        bt = self.bt      # flat part before belt
        bd = self.bd      # depth of the belt
        bh = self.bh      # height of the belt
        bf = self.bf      # belt fillet

        tc = self.tc      # cut thickness for the bottom
        dc = self.dc    # diameter of the bottom cut
        ts = self.ts      # thickness of the slots at the top in the shape of (+)
        ws = self.ws      # width of the slots

        ef = self.ef      # top and bottom edges fillet

        bpt = 0.1        # bottom plastic thickness (not visual)
        tmt = ts*2       # top metallic part thickness (not visual)

        # TODO: calculate width of the cathode marker bar from the body size
        ciba = 45.  # angle of the cathode identification bar

        # TODO: calculate marker sizes according to the body size
        mmb_h = 2.       # lenght of the (-) marker on the cathode bar
        mmb_w = 0.5      # rough width of the marker

        ef_s2 = ef/sqrt(2)
        ef_x = ef-ef/sqrt(2)

        def bodyp():
            return cq.Workplane("XZ").move(0, bs).\
                   move(0, tc+bpt).\
                   line(dc/2., 0).\
                   line(0, -(tc+bpt)).\
                   line(D/2.-dc/2.-ef, 0).\
                   threePointArc((D/2.-(ef_x), bs+(ef_x)), (D/2., bs+ef)).\
                   line(0, bt).\
                   threePointArc((D/2.-bd, bs+bt+bh/2.), (D/2., bs+bt+bh)).\
                   lineTo(D/2., L+bs-ef).\
                   threePointArc((D/2.-(ef_x), L+bs-(ef_x)), (D/2.-ef, L+bs)).\
                   lineTo(dc/2., L+bs).\
                   line(0, -(tc+tmt)).\
                   line(-dc/2., 0).\
                   close()

        body = bodyp().revolve(360-ciba, (0,0,0), (0,1,0))
        bar = bodyp().revolve(ciba, (0,0,0), (0,1,0))

        # # fillet the belt edges
        BS = cq.selectors.BoxSelector
        # note that edges are selected from their centers
        body = body.edges(BS((-0.5,-0.5, bs+bt-0.01), (0.5, 0.5, bs+bt+bh+0.01))).\
               fillet(bf)
        b_r = D/2.-bd # inner radius of the belt
        bar = bar.edges(BS((b_r/sqrt(2), 0, bs+bt-0.01),(b_r, -b_r/sqrt(2), bs+bt+bh+0.01))).\
              fillet(bf)

        body = body.rotate((0,0,0), (0,0,1), 180-ciba/2)
        bar = bar.rotate((0,0,0), (0,0,1), 180+ciba/2)

        # draw the plastic at the bottom
        bottom = cq.Workplane("XY").workplane(offset=bs+tc).\
                 circle(dc/2).extrude(bpt)

        # draw the metallic part at the top
        top = cq.Workplane("XY").workplane(offset=bs+L-tc-ts).\
             circle(dc/2).extrude(tmt)

        # draw the slots on top in the shape of plus (+)
        top = top.faces(">Z").workplane().move(ws/2,ws/2).\
              line(0,D).line(-ws,0).line(0,-D).\
              line(-D,0).line(0,-ws).line(D,0).\
              line(0,-D).line(ws,0).line(0,D).\
              line(D,0).line(0,ws).close().cutBlind(-ts)

        # draw the (-) marks on the bar
        n = int(L/(2*mmb_h)) # number of (-) marks to draw
        points = []
        first_z = (L-(2*n-1)*mmb_h)/2
        for i in range(n):
            points.append((0, (i+0.25)*2*mmb_h+first_z))
        mmb = cq.Workplane("YZ", (-D/2,0,bs)).pushPoints(points).\
              box(mmb_w, mmb_h, 2).\
              edges("|X").fillet(mmb_w/2.-0.001)

        mmb = mmb.cut(mmb.translate((0,0,0)).cut(bar))
        bar = bar.cut(mmb)

        # draw the leads
        leads = cq.Workplane("XY").workplane(offset=bs+tc).\
                center(-F/2,0).circle(d/2).extrude(-(ll+tc)).\
                center(F,0).circle(d/2).extrude(-(ll+tc+la))

        model = ComponentModel()
        model.addPart(body, self.body_color, "body")
        model.addPart(mmb, self.body_color, "marks")
        model.addPart(top, self.top_color, "top")
        model.addPart(bottom, self.bottom_color, "bottom")
        model.addPart(bar, self.bar_color, "bar")
        model.addPart(leads, self.lead_color, "pins")

        return model
