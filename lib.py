from KicadModTree import Footprint, Text, KicadFileHandler, Model
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

from KicadModTree import Pad, Line, Arc
def mount_tab_fp(bl, tl, c, tr, br):
    return [
        Line(start=bl, end=tl, layer='Cmts.User'),
        Line(start=tr, end=br, layer='Cmts.User'),
        Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
              at=c, size=(m2_hole, m2_hole), drill=m2_hole, layers=Pad.LAYERS_THT),
        Arc(start=tr, end=tl, center=c, layer='Cmts.User'),
    ]

m2_hole = 2.0
m2_thread = 1.6
half_total_space = 7.5
total_space = half_total_space * 2
washer_outer = 5
nut_outer = 4.5
