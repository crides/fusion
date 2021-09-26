#!/usr/bin/python3

import math
from solidff import *

diameter = 9.8
thickness = 8.1 - 3.55
insert_wall = 1.5
wall = 1
thread_dia = 2.1
hole_dia = 3.15
beam = 3

outer_ring = ring(r1=diameter / 2, r2=diameter / 2 - wall, h=thickness)
inner_ring = ring(r1=hole_dia / 2 + insert_wall, r2=hole_dia / 2, h=thickness)
nothread_ring = ring(r1=hole_dia / 2, r2=thread_dia / 2, h=thickness - 4)
bar = q((diameter - hole_dia - 0.2) / 2, wall, thickness).back(wall / 2).right(hole_dia / 2)
bars = sum(bar.rotate(i * 360 / beam) for i in range(beam))

whole = ((outer_ring + inner_ring + bars) + nothread_ring)

dump(whole, "spacer.scad", '$fa = 0.1;\n$fs = 0.1;')
