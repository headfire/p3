
import os
import uuid
import json

from OCC.Core.Tesselator import ShapeTesselator

from OCC.Extend.TopologyUtils import is_edge, is_wire, discretize_edge, discretize_wire
from OCC.Extend.DataExchange import write_stl_file


class StlRenderer:
    
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
  
    def drawShape(self,  shape):
        shape_precision, wire_precision = self.precision 
        if is_edge(shape):
            pass
        elif is_wire(shape):
            pass
        else: #solid or shell
            print("export shape %s to STL start", str(self.shapeNum).zfill(3))
            shape_hash = "exp_%s_shape" % str(self.shapeNum).zfill(3)
            shape_full_path = os.path.join(self._path, shape_hash + '.stl')
            write_stl_file(shape, shape_full_path, "ascii", shape_precision/4, 0.5/4)
            print("export shape %s to STL done", str(self.shapeNum).zfill(3))
            self.shapeNum += 1
         
    

def jsBool(bool):          
  if bool:
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

def export_edgedata_to_json(edge_hash, point_set):
    """ Export a set of points to a LineSegment buffergeometry
    """
    # first build the array of point coordinates
    # edges are built as follows:
    # points_coordinates  =[P0x, P0y, P0z, P1x, P1y, P1z, P2x, P2y, etc.]
    points_coordinates = []
    for point in point_set:
        for coord in point:
            points_coordinates.append(coord)
    # then build the dictionnary exported to json
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


class ThreeJsRenderer:
    
    def __init__(self, decoration, precision, path):
        if not path:
            raise Exception('ThreeJsRenderer need path for exported files')
        self._path = path
        self._js_filename = os.path.join(self._path, "slide.js")
        self.decoration = decoration
        self.precision = precision
        self.shapeNum = 1
        self.stringList = []
        
        print("## threejs %s webgl renderer")
       
    def drawPoint(self, pnt, color, size):
       self.stringList.append("\tzdeskXPoint(%g, %g, %g, %s, %g);\n"
                                        % (pnt.X(), pnt.Y(), pnt.Z(), color_to_hex(color), size))
      
    def drawLabel(self, pnt, text, color):
       self.stringList.append("\tzdeskXLabel(%g, %g, %g, '%s', %s);\n"
                                        % (pnt.X(), pnt.Y(), pnt.Z(), text, color_to_hex(color)))
  
    def drawShape(self,
                     shape,
                     color=(0.65, 0.65, 0.7),
                     transparency=0.,
                     line_width=1.,
                    ):
        # if the shape is an edge or a wire, use the related functions
        shininess=0.9
        specular_color=(0.2, 0.2, 0.2)
        shape_precision, wire_precision = self.precision 
        if is_edge(shape):
            print("discretize an edge")
            pnts = discretize_edge(shape, wire_precision)
            edge_hash = "exp_%s_edge" % str(self.shapeNum).zfill(3)
            self.shapeNum += 1
            str_to_write = export_edgedata_to_json(edge_hash, pnts)
            edge_full_path = os.path.join(self._path, edge_hash + '.json')
            with open(edge_full_path, "w") as edge_file:
                edge_file.write(str_to_write)
            # store this edge hash
            self.stringList.append("\tzdeskXCurve(slidePath+'%s.json', %s, %g);\n"
                                        % (edge_hash, color_to_hex(color), line_width))
            print("%s, %i segments" % (edge_hash ,len(pnts)-1))
        elif is_wire(shape):
            print("discretize a wire")
            pnts = discretize_wire(shape, wire_precision)
            wire_hash = "exp_%s_wire" % str(self.shapeNum).zfill(3)
            self.shapeNum += 1
            str_to_write = export_edgedata_to_json(wire_hash, pnts)
            wire_full_path = os.path.join(self._path, wire_hash + '.json')
            with open(wire_full_path, "w") as wire_file:
                wire_file.write(str_to_write)
            # store this edge hash
            self.stringList.append("\tzdeskXCurve(slidePath+'%s.json', %s, %g);\n"
                                        % (wire_hash, color_to_hex(color), line_width))
            print("%s, %i segments" % (wire_hash ,len(pnts)-1))
        else: #solid or shell
            print("tesselate a shape")
            shape_uuid = uuid.uuid4().hex
            shape_hash = "exp_%s_shape" % str(self.shapeNum).zfill(3)
            self.shapeNum += 1
            # tesselate
            tess = ShapeTesselator(shape)
            tess.Compute(compute_edges=False,
                         mesh_quality=shape_precision,
                         parallel=True)
            # export to 3JS
            shape_full_path = os.path.join(self._path, shape_hash + '.json')
            with open(shape_full_path, 'w') as json_file:
                json_file.write(tess.ExportShapeToThreejsJSONString(shape_uuid))
            self.stringList.append("\tzdeskXShape(slidePath+'%s.json', %s, %s, %g, %g);\n"
                                        % (shape_hash, color_to_hex(color), color_to_hex(specular_color), shininess, 1 - transparency))
            print("%s, %i triangles\n" % (shape_hash, tess.ObjGetTriangleCount()))
       

    def render(self):
        with open(self._js_filename, "w") as fp:
            isDesk, isAxis, scaleA, scaleB, deskDX, deskDY, deskDZ = self.decoration
            fp.write('function loadedSlideGetParam() { \n')
            fp.write('\t var param = Object(); \n')
            fp.write('\t param.isDesk = %s; \n' % jsBool(isDesk) )
            fp.write('\t param.isAxis = %s; \n' % jsBool(isAxis) ) 
            fp.write('\t param.scaleA = %i; \n' % scaleA ) 
            fp.write('\t param.scaleB = %i; \n' % scaleB ) 
            fp.write('\t param.deskDX = %i; \n' % deskDX ) 
            fp.write('\t param.deskDY = %i; \n' % deskDY ) 
            fp.write('\t param.deskDZ = %i; \n' % deskDZ ) 
            fp.write('\t return param;\n') 
            fp.write('}\n')
            fp.write('\n')
            fp.write('function loadedSlideMake(slidePath) { \n')
            fp.write("".join(self.stringList))
            fp.write('}\n')
    
if __name__ == "__main__":
    
     pass