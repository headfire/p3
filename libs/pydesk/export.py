import os
import uuid
import json

from render import RenderLib

from OCC.Core.Tesselator import ShapeTesselator
from OCC.Extend.TopologyUtils import is_edge, is_wire, discretize_wire
from OCC.Extend.DataExchange import write_stl_file
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Pnt


def _jsBool(boolVar):
    if boolVar:
        return 'true'
    else:
        return 'false'


def _colorToHex(rgb_color):
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


def _export_edge_data_to_json(edge_hash, point_set):
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


class ExportLib(RenderLib):

    def __init__(self, scaleAB, pathToExport):
        super().__init__(scaleAB)
        self.pathToExport = pathToExport
        self.precision = self.scale

    def initPrecisionUp(self, factor_1_10):
        self.precision /= factor_1_10,

    def initPrecisionDown(self, factor_1_10):
        self.precision *= factor_1_10,


class StlExportLib(ExportLib):
    def __init__(self, scaleAB, pathToExport):
        super().__init__(scaleAB, pathToExport)

    def outStart(self):
        print()
        print('***** StlRenderLib start ******')
        print()

    def outFinish(self):
        print()
        print('***** StlRenderLib finish ******')
        print()

    def outShape(self, shape):
        fileName = self.renderName + '.stl'
        fullFileName = os.path.join(self.pathToExport, fileName)
        print('Start export shape to %s' % fileName)
        write_stl_file(shape, fullFileName, 'ascii', self.precision / 4, 0.5 / 4)
        print("Finish export")

    # this render not enable export to STL
    def renderWire(self, wire): pass
    def renderPoint(self, pnt): pass
    def renderArrow(self, pnt1, pnt2): pass
    def renderCircle(self, pnt1, pnt2, pnt3): pass
    def renderLabel(self, pnt, text): pass
    def renderLine(self, pnt1, pnt2): pass
    def renderDecor(self): pass

'''
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
                               % (pnt.X(), pnt.Y(), pnt.Z(), _color_to_hex(color), size))

    def drawLabel(self, pnt, text, color):
        self.stringList.append("    zdeskXLabel(%g, %g, %g, '%s', %s);\n"
                               % (pnt.X(), pnt.Y(), pnt.Z(), text, _color_to_hex(color)))

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
'''
class WebOutExportLib(ExportLib):
    def __init__(self, scaleAB, pathToExport):
        super().__init__(scaleAB, pathToExport)
        self.stringList = []

    def outShape(self, shape, material, color, transparency):

        specular_color = color
        shininess = 1
        print("tessellate a shape")
        shape_uuid = uuid.uuid4().hex
        shape_hash = "exp_%s_shape" % str(self.shapeNum).zfill(3)
        self.shapeNum += 1
        # tessellate
        tess = ShapeTesselator(shape)
        tess.Compute(compute_edges=False,
                     mesh_quality=self.shapePrecision,
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
                                  1 - transparency, material))

    def outLabel(self, text):
        self.stringList.append("    zdeskXLabel(%g, %g, %g, '%s', %s);\n"
           % (pnt.X(), pnt.Y(), pnt.Z(), text, _colorToHex(self.styleColor)))


class WebSmartExportLib(WebOutExportLib):
    def __init__(self, scaleAB, pathToExport):
        super().__init__(scaleAB, pathToExport)

    def basePrim(self, prim):pass
    def baseWire(self, wire): pass
    def baseLabel(self, text): pass
    def baseShape(self, shape): pass


class WebSuperSmartExportLib(WebSmartExportLib):
    def __init__(self, scaleAB, pathToExport):
        super().__init__(scaleAB, pathToExport)

    def renderPoint(self, pnt):
        self.brashForPoint()
        self.sizeForPoint()
        self.stringList.append("    zdeskXPoint(%g, %g, %g, %s, %g);\n"
                               % (pnt.X(), pnt.Y(), pnt.Z(), _colorToHex(self.styleColor), self.pointRadius*2))

    def exportLabel(self, pnt, text, color):
        self.stringList.append("    zdeskXLabel(%g, %g, %g, '%s', %s);\n"
                               % (pnt.X(), pnt.Y(), pnt.Z(), text, _colorToHex(color)))

    def exportShape(self,  shape, material, color, transparency):
        # if the shape is an edge or a wire, use the related functions
        shininess = 0.9
        specular_color = (0.2, 0.2, 0.2)
        shape_precision = self.hints.shapePrecision
        wire_precision = self.hints.wirePrecision

    def baseWire(self, wire):
        fileName = self.renderName + '.json'
        fullFileName = os.path.join(self.pathToExport, fileName)
        print('Export wire to ' + fileName)
        points = discretize_wire(wire, self.precision)
        print("%i segments" % (len(points) - 1))
        strToWrite = _exportWireToJson(fileName, points)
        print("Try to save file %s" % wire_full_path)
        with open(wire_full_path, "w") as wire_file:
            wire_file.write(str_to_write)
        print("Save OK")
        print("ExportFinish")
        print("")
        # store this edge hash
        self.stringList.append("    zdeskXCurve('%s', %s, %g);\n"
                               % (wire_hash, color_to_hex(color), lineRadius*2, material, transparency))


    def exportFinish(self):
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
