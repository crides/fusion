#!/usr/bin/python3

import math
from solidff import *
import solid

height = 5.3
width = 31.3
length = 36.5
shell = 1.2

def mount():
    hole = 2.1
    thickness = 2
    outer_dia = 5
    offset = 0
    block = q(offset + outer_dia / 2 + 0.1, outer_dia, thickness).y(-outer_dia / 2)
    outer = cy(outer_dia / 2, thickness)
    inner = cy(hole / 2, thickness)
    return (block + outer - inner).y(outer_dia / 2).x(-outer_dia / 2 - offset).c("red")

def body():
    outer = q(width + shell * 2, length + shell * 2, height + shell).y(-shell).x(-shell)
    inner = q(width, length, height)
    return outer - inner

def mask():
    strip_offset = 3
    top_width = 12
    side_width = 9
    # strip = solid.polygon([(width + shell, -shell), (width - top_width, -shell), (0, length + shell), (top_width, length + shell)])
    strip = s(top_width, length + 2*shell).y(-shell).x(width - top_width)
    side_strip = s(width + 2*shell, side_width).x(-shell).y(strip_offset)
    patch = s(strip_offset + shell).x(width - strip_offset).y(-shell)
    return (side_strip + strip + patch).e(20, center=True)

def whole():
    top_offset = 23
    bot_offset = 5
    return body() * mask() \
        + mount().r(90).y(-shell).x(width - bot_offset) \
        + mount().r(-90).y(shell + length).x(top_offset) \
        + mount().x(-shell).y(bot_offset).c("red")

dump(whole, "bat-shell.scad")
