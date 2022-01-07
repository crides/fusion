#!/usr/bin/python3

import math, solid
from solidff import *
from KicadModTree import Pad, Text, Line, Arc, RectLine, Circle
from lib import kicad_fp, m2_hole, half_total_space, washer_outer, nut_outer, nut_outer_safe

ridge_thick = 2
mount_thick = 2
nylon = 1.05
mount_offset = 0
gap = ridge_thick + nylon * 2 + ridge_thick

def top():
    hring = ring(od=washer_outer, id=m2_hole, center=True, hole=True).y(half_total_space)
    stick = hring ** q(nut_outer_safe, mount_thick, ridge_thick).z(-ridge_thick / 2)
    return stick.r(90, 0, 0)

def hinge1():
    hring = ring(od=washer_outer, id=m2_hole, center=True, hole=True).y(half_total_space)
    stick = hring ** q(nut_outer_safe, mount_thick, ridge_thick).z(-ridge_thick / 2)
    stick_sketch = solid.projection(True)(stick)
    top = ring(id=nut_outer, w=ridge_thick / 2, h=10, extra=False, hole=True).z(mount_thick) + ring(id=nut_outer, w=ridge_thick / 2, h=mount_thick)
    bottom = ring(id=m2_hole, od=nut_outer, h=mount_thick, hole=True)
    mask = stick_sketch.e(10).z(-5).r(90, 0, 0)
    return (top.x(nut_outer_safe) + stick.r(90, 0, 0)) * mask + bottom.x(nut_outer_safe)

def hinge2():
    bottom = q(nut_outer_safe, gap - ridge_thick, mount_thick, center="y").c("royalblue") - cy(d=m2_hole, h=mount_thick).x(nut_outer_safe / 2)
    return top().y(-gap / 2) + top().y(gap / 2) + bottom

def hinge1_fp():
    y = (gap + ridge_thick) / 2
    arc_top, arc_bot = (nut_outer_safe, -nut_outer_safe / 2), (nut_outer_safe, nut_outer_safe / 2)
    nut_pos = (nut_outer_safe, 0)
    return [
        RectLine(start=(0, ridge_thick / 2), end=(nut_outer_safe - nut_outer / 2, -ridge_thick / 2), layer='Cmts.User'),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=nut_pos, size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_NPTH),
        Circle(center=nut_pos, radius=nut_outer / 2, layer='Cmts.User'),
        Arc(start=arc_top, center=nut_pos, end=arc_bot, layer='Cmts.User'),
        Line(start=arc_top, end=arc_bot, layer='Cmts.User'),
    ]

def hinge2_fp():
    y = (gap + ridge_thick) / 2
    return [
        RectLine(start=(0, y), end=(nut_outer_safe, -y), layer='Cmts.User'),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=(nut_outer_safe / 2, 0), size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_NPTH),
    ]

dump(hinge1, "hinge1.scad")
dump(hinge2, "hinge2.scad")
kicad_fp("hinge1", hinge1_fp(), dir="fusion")
kicad_fp("hinge2", hinge2_fp(), dir="fusion")
