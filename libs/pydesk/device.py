import os
import uuid
import json

from OCC.Core.Tesselator import ShapeTesselator
from OCC.Extend.TopologyUtils import is_edge, is_wire, discretize_edge, discretize_wire
from OCC.Extend.DataExchange import write_stl_file

class WebRenderLib(RenderLib):
    # render precision setting
    self.shapePrecision = 1 * self.scale
    self.wirePrecision = 1 * self.scale

    def startRender(self):
        self.device = WebDevice(self.hints)

    def renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        color = self.aStyle.getNormedColor()
        self.device.drawLabel(pnt, aText, color)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        color = self.aStyle.getNormedColor()
        transparency = self.aStyle.getNormedTransparency()
        self.device.drawShape(shapeTr, color, transparency)

    def finishRender(self):
        self.device.save()


class WebFastRenderLib(WebRenderLib):
    pass


class StlRenderLibParams:
    def __init__(self, scaleA=1, scaleB=1):
        self.scaleA = scaleA
        self.scaleB = scaleB
        self.scale = scaleB/scaleA
        self.shapePrecision = 1*self.scale
        self.wirePrecision = 1*self.scale


class StlRenderLib(RenderLib):

    def startRender(self):
        self.device = StlDevice(self.hints)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        self.device.drawShape(shapeTr)

    def finishRender(self):
        self.device.save()

class ScreenDevice:
    def __init__(self, hints):
        self.display, self.start_display, add_menu, add_function_to_menu = init_display(
            None, (hints.deviceX, hints.deviceY), True, [128, 128, 128], [128, 128, 128]
        )


class StlDevice:

    def __init__(self, hints):
        self.hints = hints
        self.shapeNum = 1

        print("Stl renderer init")

    def drawPoint(self, pnt, color, size):
        pass

    def drawLabel(self, pnt, text, color):
        pass

    def drawShape(self, shape):
        shape_precision = self.hints.shapePrecision
        if is_edge(shape):
            pass
        elif is_wire(shape):
            pass
        else:  # solid or shell
            print("export shape %s to STL start", str(self.shapeNum).zfill(3))
            shape_hash = "exp_%s_shape" % str(self.shapeNum).zfill(3)
            shape_full_path = os.path.join(self.hints.pathToSave, shape_hash + '.stl')
            write_stl_file(shape, shape_full_path, "ascii", shape_precision / 4, 0.5 / 4)
            print("export shape %s to STL done", str(self.shapeNum).zfill(3))
            self.shapeNum += 1

    def save(self): pass


def jsBool(boolVar):
    if boolVar:
        return 'true'
    else:
        return 'false'


def color_to_hex(rgb_color):
    """ Takes a tuple with 3 floats between 0 and 1.
    Returns a hex. Useful to convert occ colors to web color code
    """
    r, g, b = rgb_color
    if not (0 <= r <= 1. and 0 <= g <= 1. and 0 <= b <= 1.):
        raise AssertionError("rgb values must be between 0.0 and 1.0")
    rh = int(r * 255.)
    gh = int(g * 255.)
    bh = int(b * 255.)
    return "0x%.02x%.02x%.02x" % (rh, gh, bh)


def export_edge_data_to_json(edge_hash, point_set):
    """ Export a set of points to a LineSegment buffer_geometry
    """
    # first build the array of point coordinates
    # edges are built as follows:
    # points_coordinates  =[P0x, P0y, P0z, P1x, P1y, P1z, P2x, P2y, etc.]
    points_coordinates = []
    for point in point_set:
        for coord in point:
            points_coordinates.append(coord)
    # then build the dictionary exported to json
    edges_data = {"metadata": {"version": 4.4,
                               "type": "BufferGeometry",
                               "generator": "pythonocc"},
                # "uuid": edge_hash,
                  "type": "BufferGeometry",
                  "data": {"attributes": {"position": {"itemSize": 3,
                                                       "type": "Float32Array",
                                                       "array": points_coordinates}
                                          }
                           }
                  }
    return json.dumps(edges_data)


class WebDevice:

    def __init__(self, hints):

        self.hints = hints
        self.shapeNum = 1
        self.stringList = []

        print("")
        print("## ThreeJS WebGL renderer")
        print("")

    def drawPoint(self, pnt, color, size):
        self.stringList.append("    zdeskXPoint(%g, %g, %g, %s, %g);\n"
                               % (pnt.X(), pnt.Y(), pnt.Z(), color_to_hex(color), size))

    def drawLabel(self, pnt, text, color):
        self.stringList.append("    zdeskXLabel(%g, %g, %g, '%s', %s);\n"
                               % (pnt.X(), pnt.Y(), pnt.Z(), text, color_to_hex(color)))

    def drawShape(self,
                  shape,
                  color=(0.65, 0.65, 0.7),
                  transparency=0.,
                  line_width=1.,
                  ):
        # if the shape is an edge or a wire, use the related functions
        shininess = 0.9
        specular_color = (0.2, 0.2, 0.2)
        shape_precision = self.hints.shapePrecision
        wire_precision = self.hints.wirePrecision
        if is_edge(shape):
            print("discretize an edge")
            points = discretize_edge(shape, wire_precision)
            edge_hash = "exp_%s_edge" % str(self.shapeNum).zfill(3)
            print("%s, %i segments" % (edge_hash, len(points) - 1))
            self.shapeNum += 1
            str_to_write = export_edge_data_to_json(edge_hash, points)
            edge_full_path = os.path.join(self.hints.pathToSave, edge_hash + '.json')
            with open(edge_full_path, "w") as edge_file:
                edge_file.write(str_to_write)
            # store this edge hash
            self.stringList.append("    zdeskXCurve('%s', %s, %g);\n"
                                   % (edge_hash, color_to_hex(color), line_width))
        elif is_wire(shape):
            print("discretize a wire")
            points = discretize_wire(shape, wire_precision)
            wire_hash = "exp_%s_wire" % str(self.shapeNum).zfill(3)
            print("%s, %i segments" % (wire_hash, len(points) - 1))
            self.shapeNum += 1
            str_to_write = export_edge_data_to_json(wire_hash, points)
            wire_full_path = os.path.join(self.hints.pathToSave, wire_hash + '.json')
            print("Try to save file %s" % wire_full_path)
            with open(wire_full_path, "w") as wire_file:
                wire_file.write(str_to_write)
            print("Save OK")
            print("")
            # store this edge hash
            self.stringList.append("    zdeskXCurve('%s', %s, %g);\n"
                                   % (wire_hash, color_to_hex(color), line_width))
        else:  # solid or shell
            print("tessellate a shape")
            shape_uuid = uuid.uuid4().hex
            shape_hash = "exp_%s_shape" % str(self.shapeNum).zfill(3)
            self.shapeNum += 1
            # tessellate
            tess = ShapeTesselator(shape)
            tess.Compute(compute_edges=False,
                         mesh_quality=shape_precision,
                         parallel=True)
            # export to 3JS
            print("%s, %i triangles" % (shape_hash, tess.ObjGetTriangleCount()))
            shape_full_path = os.path.join(self.hints.pathToSave, shape_hash + '.json')
            print("Try to save file %s" % shape_full_path)
            with open(shape_full_path, 'w') as json_file:
                json_file.write(tess.ExportShapeToThreejsJSONString(shape_uuid))
            print("Save OK")
            print("")
            self.stringList.append("    zdeskXShape('%s', %s, %s, %g, %g);\n"
                                   % (shape_hash, color_to_hex(color), color_to_hex(specular_color), shininess,
                                      1 - transparency))

    def save(self):
        js_filename = os.path.join(self.hints.pathToSave, "slide.js")
        with open(js_filename, "w") as fp:
            fp.write('function loadedSlideGetParam() { \n')
            fp.write('    var param = Object(); \n')
            fp.write('    param.isDesk = %s; \n' % jsBool(self.hints.isDesk))
            fp.write('    param.isAxis = %s; \n' % jsBool(self.hints.isAxis))
            fp.write('    param.isLimits = %s; \n' % jsBool(self.hints.isLimits))
            fp.write('    param.scaleA = %i; \n' % self.hints.scaleA)
            fp.write('    param.scaleB = %i; \n' % self.hints.scaleB)
            fp.write('    param.deskDX = %i; \n' % self.hints.deskDX)
            fp.write('    param.deskDY = %i; \n' % self.hints.deskDY)
            fp.write('    param.deskDZ = %i; \n' % self.hints.deskDZ)
            fp.write('    return param;\n')
            fp.write('}\n')
            fp.write('\n')
            fp.write('function loadedSlideMake(slidePath) { \n')
            fp.write("".join(self.stringList))
            fp.write('}\n')


if __name__ == "__main__":
    pass
