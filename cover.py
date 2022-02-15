import cadquery as cq

imp = lambda f: cq.importers.importDXF(f"gerbers/fusion-{f}.dxf", tol=1e-3).wires()

res = (
    imp("Edge_Cuts").toPending().extrude(-1.8)
    .faces("<Z").fillet(1.5)
    .cut(imp("User_Eco1").toPending().extrude(-1))
    .cut(imp("User_Eco2").toPending().extrude(-1.2))
    .cut(imp("User_3").toPending().extrude(-1.8))
    # .add(imp("User_3")).toPending().cutThruAll()
)
cq.exporters.export(res, "cover.stl")
cq.Assembly(res, color=cq.Color("gray")).save("cover.step")
