#!/usr/bin/python3

import math
from solidff import *
from KicadModTree import Pad, Text, Line, Arc, Polygon, RectLine
from lib import kicad_fp, m2_hole, half_total_space, washer_outer, nut_outer

ridge_thick = 2
mount_thick = 2
nylon = 1.05
mount_offset = 0
gap = ridge_thick + nylon * 2 + ridge_thick

def top():
    hring = ring(od=washer_outer, id=m2_hole, center=True, hole=True).y(half_total_space)
    stick = hull(hring, q(nut_outer, mount_thick, ridge_thick).z(-ridge_thick / 2))
    return stick.r(90, 0, 0)

def mount():
    block = q(nut_outer, mount_offset + nut_outer / 2, mount_thick)
    hring = ring(od=nut_outer, id=m2_hole, h=mount_thick, hole=True).x(nut_outer / 2).y(mount_offset + nut_outer / 2)
    return (block + hring).c("salmon")

def hinge1():
    bottom = mount().y(ridge_thick / 2) + mount().m(0, 1, 0).y(-ridge_thick / 2)
    return top() + bottom

def hinge2():
    side = mount().y((gap + ridge_thick) / 2) + mount().m(0, 1, 0).y(-(gap + ridge_thick) / 2)
    bottom = side + q(nut_outer, gap - ridge_thick, mount_thick).y(-(gap - ridge_thick) / 2).c("royalblue")
    return top().y(-gap / 2) + top().y(gap / 2) + bottom

def hinge_mount(dist):
    left_top = (0, -dist)
    left_bot = (0, dist)
    right_top = (nut_outer, -dist)
    right_bot = (nut_outer, dist)
    center_top = (nut_outer / 2, -dist)
    center_bot = (nut_outer / 2, dist)
    return [
        Line(start=left_bot, end=left_top, layer='Cmts.User'),
        Line(start=right_bot, end=right_top, layer='Cmts.User'),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=center_top, size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_NPTH),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=center_bot, size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_NPTH),
        Arc(start=right_top, end=left_top, center=center_top, layer='Cmts.User'),
        Arc(start=left_bot, end=right_bot, center=center_bot, layer='Cmts.User'),
    ]

dump(hinge1, "hinge1.scad")
dump(hinge2, "hinge2.scad")
kicad_fp("hinge1", hinge_mount((ridge_thick + nut_outer) / 2), dir="fusion")
kicad_fp("hinge2", hinge_mount((gap + ridge_thick + nut_outer) / 2), dir="fusion")
