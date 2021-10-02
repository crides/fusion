#!/usr/bin/python3

import math
from solidff import *
from lib import m2_thread, half_total_space

diameter = 9.8
thickness = half_total_space - 3.55
insert_wall = 1.5
wall = 1
beam = 3

outer_ring = ring(od=diameter, w=wall, h=thickness)
inner_ring = ring(id=m2_thread, w=insert_wall, h=thickness)
bar = q((diameter - m2_thread - 0.2) / 2, wall, thickness).y(-wall / 2).x(m2_thread / 2)
bars = sum(bar.rotate(i * 360 / beam) for i in range(beam))

whole = outer_ring + inner_ring + bars

dump(whole, "spacer.scad", '$fa = 0.1;\n$fs = 0.1;')
