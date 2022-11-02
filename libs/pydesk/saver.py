import os
import uuid
import json

from OCC.Core.Tesselator import ShapeTesselator

from OCC.Extend.TopologyUtils import is_edge, is_wire, discretize_edge, discretize_wire
from OCC.Extend.DataExchange import write_stl_file


class StlSaverLib:

    def __init__(self, precision, path):
        if not path:
            raise Exception('StlRenderer need path for exported files')
        self._path = path
        self.precision = precision
        self.shapeNum = 1

        print("Stl renderer init")

    def drawPoint(self, pnt, color, size):
        pass

    def drawLabel(self, pnt, text, color):
        pass

    def drawShape(self, shape):
        shape_precision, wire_precision = self.precision
        if is_edge(shape):
            pass
        elif is_wire(shape):
            pass
        else:  # solid or shell
            print("export shape %s to STL start", str(self.shapeNum).zfill(3))
            shape_hash = "exp_%s_shape" % str(self.shapeNum).zfill(3)
            shape_full_path = os.path.join(self._path, shape_hash + '.stl')
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
                  "uuid": edge_hash,
                  "type": "BufferGeometry",
                  "data": {"attributes": {"position": {"itemSize": 3,
                                                       "type": "Float32Array",
                                                       "array": points_coordinates}
                                          }
                           }
                  }
    return json.dumps(edges_data)


class WebSaverLib:

    def __init__(self, decoration, precision, path):

        self._path = path
        self._js_filename = os.path.join(self._path, "slide.js")
        self.decoration = decoration
        self.precision = precision
        self.shapeNum = 1
        self.stringList = []

        print("")
        print("## ThreeJS WebGL renderer")
        print("")

    def drawPoint(self, pnt, color, size):
        self.stringList.append("\t zdeskXPoint(%g, %g, %g, %s, %g);\n"
                               % (pnt.X(), pnt.Y(), pnt.Z(), color_to_hex(color), size))

    def drawLabel(self, pnt, text, color):
        self.stringList.append("\t zdeskXLabel(%g, %g, %g, '%s', %s);\n"
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
        shape_precision, wire_precision = self.precision
        if is_edge(shape):
            print("discretize an edge")
            points = discretize_edge(shape, wire_precision)
            edge_hash = "exp_%s_edge" % str(self.shapeNum).zfill(3)
            print("%s, %i segments" % (edge_hash, len(points) - 1))
            self.shapeNum += 1
            str_to_write = export_edge_data_to_json(edge_hash, points)
            edge_full_path = os.path.join(self._path, edge_hash + '.json')
            with open(edge_full_path, "w") as edge_file:
                edge_file.write(str_to_write)
            # store this edge hash
            self.stringList.append("\t zdeskXCurve('%s', %s, %g);\n"
                                   % (edge_hash, color_to_hex(color), line_width))
        elif is_wire(shape):
            print("discretize a wire")
            points = discretize_wire(shape, wire_precision)
            wire_hash = "exp_%s_wire" % str(self.shapeNum).zfill(3)
            print("%s, %i segments" % (wire_hash, len(points) - 1))
            self.shapeNum += 1
            str_to_write = export_edge_data_to_json(wire_hash, points)
            wire_full_path = os.path.join(self._path, wire_hash + '.json')
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
            shape_full_path = os.path.join(self._path, shape_hash + '.json')
            print("Try to save file %s" % shape_full_path)
            with open(shape_full_path, 'w') as json_file:
                json_file.write(tess.ExportShapeToThreejsJSONString(shape_uuid))
            print("Save OK")
            print("")
            self.stringList.append("    zdeskXShape('%s', %s, %s, %g, %g);\n"
                                   % (shape_hash, color_to_hex(color), color_to_hex(specular_color), shininess,
                                      1 - transparency))

    def save(self):
        with open(self._js_filename, "w") as fp:
            isDesk, isAxis, scaleA, scaleB, deskDX, deskDY, deskDZ = self.decoration
            fp.write('function loadedSlideGetParam() { \n')
            fp.write('    var param = Object(); \n')
            fp.write('    param.isDesk = %s; \n' % jsBool(isDesk))
            fp.write('    param.isAxis = %s; \n' % jsBool(isAxis))
            fp.write('    param.scaleA = %i; \n' % scaleA)
            fp.write('    param.scaleB = %i; \n' % scaleB)
            fp.write('    param.deskDX = %i; \n' % deskDX)
            fp.write('    param.deskDY = %i; \n' % deskDY)
            fp.write('    param.deskDZ = %i; \n' % deskDZ)
            fp.write('    return param;\n')
            fp.write('}\n')
            fp.write('\n')
            fp.write('function loadedSlideMake(slidePath) { \n')
            fp.write("".join(self.stringList))
            fp.write('}\n')


if __name__ == "__main__":
    pass
