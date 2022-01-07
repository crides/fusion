#!/usr/bin/python3

import math
from solidff import *
from KicadModTree import Pad, Text, Line, Circle, Polygon, RectLine
from lib import kicad_fp, mount_tab_fp, total_space, nut_outer, m2_hole

tol = 0.5
tp_tall = 5.5 + tol
tp_dia = 23.2 + 2 * tol
tp_boss_dia = 0.8
tp_boss_thick = 0.8
tp_overlay_thick = 0.2
tp_fpc_wide = 9 + tol
tp_fpc_off = 17.4 - tp_dia / 2 + tol
tp_chip_thick = 2.2
thick = 1
base_thick = 2

boss = c(d=tp_boss_dia).x(tp_dia / 2).e(tp_boss_thick)
bosses = (boss.r(30) + boss.r(60) + boss.r(-135)).z(tp_tall - tp_boss_thick - tp_overlay_thick)
top_ring = ring(h=thick, od=tp_dia, w=1).z(tp_tall - tp_boss_thick - tp_overlay_thick - thick)
outer_shell = ring(h=tp_tall, id=tp_dia, w=thick)
cutout = q(100, tp_fpc_wide, 2, center='y').r(180)

mount_off = (tp_dia / 2 - thick - nut_outer / 2) / math.sqrt(2)
mount = (s(10).o(r=nut_outer / 2) - c(d=m2_hole)).t(mount_off, mount_off).e(base_thick).r(45)
mounts = mount + mount.r(180)
mounts *= cy(d=tp_dia, h=10)
whole = outer_shell + bosses + top_ring + mounts - cutout

def footprint():
    mount_off = tp_dia / 2 - thick - nut_outer / 2
    return [
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=(0, mount_off), size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_NPTH),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=(0, -mount_off), size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_NPTH),
        Circle(center=(0, 0), radius=tp_dia / 2, layer='Cmts.User'),
        Circle(center=(0, 0), radius=tp_dia / 2 + thick, layer='Cmts.User'),
    ]

whole.dump_this('$fa = 0.5;\n$fs = 0.1;')
kicad_fp("touchpad-holder", footprint(), dir="fusion")
