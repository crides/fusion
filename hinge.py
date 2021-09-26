#!/usr/bin/python3

import math, solid
from solidff import *
from KicadModTree import Footprint, Pad, Text, Line, KicadFileHandler, Arc, Polygon, Model

ridge_thick = 2
mount_thick = 2
height = 8.1
thread = 2.1
outer_dia = 5
nylon = 1.05
mount_offset = 0
gap = ridge_thick + nylon * 2 + ridge_thick

def top():
    slant = solid.hull()(cy(outer_dia / 2, ridge_thick, center=True).y(height), q(outer_dia, 0.1, ridge_thick).z(-ridge_thick / 2))
    holed = slant - cy(thread / 2, ridge_thick, center=True).y(height)
    stick = holed + q(outer_dia, mount_thick, ridge_thick).z(-ridge_thick / 2)
    return stick.r(90, 0, 0)

def mount():
    block = q(outer_dia, mount_offset + outer_dia / 2, mount_thick)
    outer = cy(outer_dia / 2, mount_thick).x(outer_dia / 2).y(mount_offset + outer_dia / 2)
    inner = cy(thread / 2, mount_thick).x(outer_dia / 2).y(mount_offset + outer_dia / 2)
    return (block + outer - inner).c("salmon")

def hinge1():
    bottom = mount().y(ridge_thick / 2) + mount().m(0, 1, 0).y(-ridge_thick / 2)
    return top() + bottom

def hinge2():
    side = mount().y((gap + ridge_thick) / 2) + mount().m(0, 1, 0).y(-(gap + ridge_thick) / 2)
    bottom = side + q(outer_dia, gap - ridge_thick, mount_thick).y(-(gap - ridge_thick) / 2).c("royalblue")
    return top().y(-gap / 2) + top().y(gap / 2) + bottom

def hinge_mount(dist):
    left_top = (0, -dist)
    left_bot = (0, dist)
    right_top = (outer_dia, -dist)
    right_bot = (outer_dia, dist)
    center_top = (outer_dia / 2, -dist)
    center_bot = (outer_dia / 2, dist)
    return [
        Line(start=left_bot, end=left_top, layer='Cmts.User'),
        Line(start=right_bot, end=right_top, layer='Cmts.User'),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=center_top, size=(2.1, 2.1), drill=2.1, layers=Pad.LAYERS_THT),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=center_bot, size=(2.1, 2.1), drill=2.1, layers=Pad.LAYERS_THT),
        Arc(start=right_top, end=left_top, center=center_top, layer='Cmts.User'),
        Arc(start=left_bot, end=right_bot, center=center_bot, layer='Cmts.User'),
    ]

def kicad_fp(name: str, entities, fp_typ="through_hole", dir=None):
    fp = Footprint(name)
    fp.setAttribute(fp_typ)
    prelude = [
        Text(type='reference', text='REF**', at=[0, -3], layer='F.Fab', hide=True),
        Text(type='value', text=name, at=[1.5, 3], layer='F.Fab', hide=True),
        Model(filename=f"${{KIPRJMOD}}/{name}.wrl")
    ]
    fp.extend(prelude + entities)
    dir = "" if dir == None else f"{dir}.pretty/"
    KicadFileHandler(fp).writeFile(f"{dir}{name}.kicad_mod")

dump(hinge1, "hinge1.scad")
dump(hinge2, "hinge2.scad")
kicad_fp("hinge1", hinge_mount((ridge_thick + outer_dia) / 2), dir="fusion")
kicad_fp("hinge2", hinge_mount((gap + ridge_thick + outer_dia) / 2), dir="fusion")
