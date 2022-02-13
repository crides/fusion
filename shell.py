from solidff import *
import solid

def imp(f):
    thing = solid.import_(f"gerbers/fusion-{f}.dxf").add_param("$fn", 60)
    return thing.r((0, 180, 0))
switches, screws, bumpons, edge = list(map(imp, ["User_Eco1", "User_Eco2", "User_3", "Edge_Cuts"]))
shells = ((edge - bumpons).e(1.8) - switches.e(1) - screws.e(1.2))
mask = q(150, 150, 3, 'y').x(5)
(shells * mask).dump("shell-left.scad")
(shells * mask.x(-150)).dump("shell-right.scad")
