#!/usr/bin/python3

import math
from solidff import *
from KicadModTree import Pad, Text, Line, Arc, Polygon, RectLine, Circle
from lib import kicad_fp, mount_tab_fp, m2_hole, nut_outer

height = 6.5
width = 31.3
length = 36.5
shell = 1.2

thickness = 2
offset = 0
def mount(magnet=False):
    block = q(offset + nut_outer / 2, nut_outer, thickness).y(-nut_outer / 2)
    hring = ring(od=nut_outer, id=m2_hole, h=thickness, hole=True)
    m = block + hring
    if magnet:
        m += ring(id=m2_hole, w=1, h=height+shell, hole=True) + cy(r=4, h=thickness).z(height+shell - thickness)
    return m.y(nut_outer / 2).x(-nut_outer / 2 - offset).c("red")

def body():
    outer = q(width + shell * 2, length + shell * 2, height + shell).y(-shell).x(-shell)
    inner = q(width, length, height)
    return outer - inner

def mask():
    strip_offset = 3
    top_width = 12
    side_width = 9
    strip = s(top_width, length + 2*shell).y(-shell).x(width - top_width)
    side_strip = s(width + 2*shell, side_width).x(-shell).y(strip_offset)
    patch = s(strip_offset + shell).x(width - strip_offset).y(-shell)
    return (side_strip + strip + patch).e(20, center=True)

top_offset = 26
bot_offset = 5
def whole():
    left_mount = mount()
    return body() * mask() \
        + mount().r(90).y(-shell).x(width - bot_offset) \
        + mount().r(-90).y(shell + length).x(top_offset) \
        + mount(True).x(-shell).y(bot_offset).c("salmon")

def fp():
    left = lambda x, y: (-shell + x, -bot_offset + y)
    bot = lambda x, y: (width - bot_offset + x, shell + y)
    top = lambda x, y: (top_offset + x, -shell - length + y)
    return [
        RectLine(start=(0, 0), end=(width, -length), layer='Cmts.User'),
        RectLine(start=(-shell, shell), end=(width + shell, -length - shell), layer='Cmts.User'),
        Circle(center=left(-nut_outer/2-offset,-nut_outer/2), radius=4, layer='Cmts.User'),
    ] \
        + mount_tab_fp(left(0,0), left(-nut_outer/2-offset,0), left(-nut_outer/2-offset,-nut_outer/2), left(-nut_outer/2-offset,-nut_outer), left(0,-nut_outer)) \
        + mount_tab_fp(top(0,0), top(0,-nut_outer/2-offset), top(nut_outer/2,-nut_outer/2-offset), top(nut_outer,-nut_outer/2-offset), top(nut_outer,0)) \
        + mount_tab_fp(bot(0,0), bot(0,nut_outer/2+offset), bot(-nut_outer/2,nut_outer/2+offset), bot(-nut_outer,nut_outer/2+offset), bot(-nut_outer,0))


kicad_fp("bat-shell", fp(), dir="fusion")
dump_this(whole, '$fa = 0.5;\n$fs = 0.1;')
