from KicadModTree import Footprint, Pad, Text, Line, KicadFileHandler, Arc, Polygon
import math

name = "hinge"
width = 5
height = 8
cu_height = 3

radius = math.sqrt((height**2 * (width/2)**2)/(height**2 + (width/2)**2))
angle = math.asin(radius / height)
left_point = (-math.cos(angle) * radius, math.sin(angle) * radius - height)
right_point = (math.cos(angle) * radius, -math.sin(angle) * radius - height)
cu_left = (-math.sin(angle) * cu_height, -cu_height)
cu_right = (width - math.sin(angle) * cu_height, -cu_height)

fp = Footprint(name)

fp.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.Fab', hide=True))
fp.append(Text(type='value', text=name, at=[1.5, 3], layer='F.Fab', hide=True))

fp.append(Line(start=(0, 0), end=left_point, layer='Edge.Cuts'))
fp.append(Line(start=(width, 0), end=right_point, layer='Edge.Cuts'))
fp.append(Arc(start=right_point, end=left_point, center=(0, -height), layer='Edge.Cuts'))

fp.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=[0, -height], size=[2.1, 2.1], drill=2.1, layers=Pad.LAYERS_THT))
for layers in [Pad.LAYERS_CONNECT_FRONT, Pad.LAYERS_CONNECT_BACK]:
    fp.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=[0, 0], size=[0.000, 0.000],
                  primitives=[Polygon(nodes=[(0, 0), (width, 0), cu_right, cu_left])], layers=layers))

for x in [0.1, 1.8, 3.5]:
    fp.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                  at=[x, -2.2], size=[1, 1], drill=0.5, layers=Pad.LAYERS_THT))
    fp.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                  at=[x + 0.5, -0.8], size=[1, 1], drill=0.5, layers=Pad.LAYERS_THT))

KicadFileHandler(fp).writeFile(f"{name}.kicad_mod")
