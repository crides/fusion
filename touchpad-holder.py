#!/usr/bin/python3

import math
from solidff import *
from KicadModTree import Pad, Text, Line, Arc, Polygon, RectLine
from lib import kicad_fp, mount_tab_fp, total_space, nut_outer

wall = 1.5
base_thick = 2
m2_hole = 2.0
tab_thick = 1.8
tab_width = 10 #9.5
touchpad_width = 8
touchpad_corner = 1
top_thick = 1.2
top_tab_width = 5
top_tab_corner = 2
holder_thick = 1.5

holder_total_thick = holder_thick + tab_thick + top_thick
rotation = 45
holder_rotated_thick = math.cos(math.radians(rotation)) * holder_total_thick \
    + math.sin(math.radians(rotation)) * touchpad_width / 2 #tab_width / 2
base_space = total_space - holder_rotated_thick
hole_offset = 3 + nut_outer/2
left_dist = (touchpad_width/2 + top_tab_width) * math.cos(math.radians(rotation)) - wall

PCB_width = 7
PCB_thick = 3
FPC_width = 5
FPC_offset = 0.5
FPC_thick = 1
FPC_hole_len = 3

def center_rect(l, r, t, b):
    return s(r - l, t - b).x(l).y(b)

def holder():
    bot = s(tab_width, True).e(holder_thick)
    fpc_hole_sketch = s(wall + PCB_width, PCB_thick) + s(wall + FPC_hole_len, FPC_width)
    fpc_hole = fpc_hole_sketch.t(-wall - tab_width / 2, - (tab_width / 2 - FPC_offset)).e(holder_thick + FPC_thick)
    horiz = s(tab_width, wall, True)
    offset = wall / 2 + tab_width / 2
    walls = horiz.y(offset) + horiz.y(-offset) + s(wall, tab_width + 2*wall, True).x(-offset)
    walls = walls.e(holder_thick + tab_thick)
    tab_outer_full = s(top_tab_width*2 + touchpad_width - 2*top_tab_corner, True).o(r=top_tab_corner)
    right_offset = touchpad_width / 2 - 0.5
    tab_outer = center_rect(-20, right_offset, 20, -20) * tab_outer_full
    tab_inner = s(touchpad_width - 2*touchpad_corner, True).o(r=touchpad_corner)
    tab = tab_outer - tab_inner
    upper_hole = s(20, True).e(20).h()
    holder = bot + walls + tab.e(top_thick).z(holder_thick + tab_thick) - fpc_hole + upper_hole.z(holder_total_thick)
    return holder.r(0, -rotation, 0).x(math.sin(math.radians(rotation)) * holder_total_thick)

def base():
    forw_dist = 15
    comp_thick = 3.5

    def mount_tab():
        sketch = center_rect(-nut_outer/2, nut_outer/2, 0, -nut_outer/2) + c(nut_outer/2) - c(m2_hole/2)
        return sketch.e(base_thick).c("darkgreen")

    fillet_corner = ((s(wall * 2, True) - c(wall)) * s(wall)).e(wall).x(-wall).r(90, 0, 0).z(-wall)

    back_mount = mount_tab().y(-tab_width/2 + nut_outer/2).x(hole_offset)
    back_wall = center_rect(-left_dist, nut_outer/2 + hole_offset, -tab_width/2, -tab_width/2-wall).e(total_space)

    top_center_wall = center_rect(hole_offset - nut_outer/2, hole_offset + nut_outer/2, tab_width/2 + wall, tab_width/2).e(total_space)
    top_left_wall = center_rect(-left_dist, hole_offset - nut_outer/2, tab_width/2 + wall, tab_width/2).e(total_space - comp_thick).z(comp_thick)
    forw_mount = mount_tab().x(hole_offset).y(nut_outer/2 + wall + tab_width/2)

    left_wall = center_rect(-left_dist - wall, -left_dist, tab_width/2 + wall, -tab_width/2 - wall).e(total_space - comp_thick).z(comp_thick)

    comp_hole = q(hole_offset - nut_outer / 2 + left_dist, tab_width + wall, comp_thick).t(-left_dist - wall, -tab_width/2).h()

    walls = top_center_wall + top_left_wall + back_wall + left_wall + \
        fillet_corner.t(-left_dist, -tab_width/2, comp_thick) + \
        fillet_corner.t(hole_offset - nut_outer/2, tab_width/2 + wall, comp_thick)

    return walls + forw_mount + back_mount + comp_hole

def whole():
    return holder().z(base_space).c("royalblue") + base()

def footprint():
    n = nut_outer
    hn = n / 2
    w = wall
    t = tab_width
    ht = t / 2
    ho = hole_offset
    ld = left_dist
    mount_tab = lambda x, y: mount_tab_fp((x-hn,-y+hn), (x-hn,-y), (x,-y), (x+hn,-y), (x+hn,-y+hn))
    return [
        *mount_tab(ho, hn-ht), *mount_tab(ho, hn+w+ht),
        Polygon(nodes=[(-ld-w,-ht-w), (ho+hn,-ht-w), (ho+hn,-ht), (-ld,-ht), 
                       (-ld,ht), (hn+ho,ht), (hn+ho,ht+w), (-ld-w,ht+w)],
                layer='Cmts.User'),
    ]

dump(whole, "touchpad-holder.scad")
kicad_fp("touchpad-holder", footprint(), dir="fusion")
