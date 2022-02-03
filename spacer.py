#!/usr/bin/python3

import math
from solidff import *
from lib import m2_hole, m2_thread, half_total_space

threaded = False
diameter = 8
thickness = half_total_space - 3.55
insert_wall = (1.25 + (m2_hole - m2_thread) / 2) if threaded else 1
hole_d = m2_thread if threaded else m2_hole
wall = 1
beam = 3

outer_ring = ring(od=diameter, w=wall, h=thickness)
inner_ring = ring(id=hole_d, w=insert_wall, h=thickness)
bar = q((diameter - hole_d - 0.2) / 2, wall, thickness).y(-wall / 2).x(hole_d / 2)
bars = sum(bar.rotate(i * 360 / beam) for i in range(beam))

whole = outer_ring + inner_ring + bars

dump_this(whole, '$fa = 0.1;\n$fs = 0.1;')
