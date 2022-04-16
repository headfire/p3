from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_XOY, gp_YOZ, gp_Trsf, gp_DX,gp_Ax1, gp_Origin
from OCC.Core.Geom import Geom_Axis2Placement, Geom_CartesianPoint, Geom_Point
from OCC.Core.AIS import AIS_Point, AIS_Trihedron, AIS_Shape, AIS_Line
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe, BRepOffsetAPI_MakePipeShell
from OCC.Core.TopoDS import TopoDS_Edge

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone

from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.GC import  GC_MakeCircle
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import BRepTools_WireExplorer

from _threejs import ThreeJsRenderer, StlRenderer

import os

import sys

import json

DEFAULT_STYLE = (50,50,50),0,'CHROME'

POINT_TYPES = [ 'POINT', 'PLUS', 'STAR', 'X',  'O', 'O_POINT', 'O_PLUS', 'O_STAR',  'O_X',
  'RING1', 'RING2', 'RING3', 'BALL' ]

LINE_TYPES = { 'EMPTY':-1, 'SOLID':0, 'DASH':1, 'DOT':2, 'DOTDASH':3 }

MATERIAL_TYPES = [ 'BRASS', 'BRONZE', 'COPPER', 'GOLD',  'PEWTER', 'PLASTER', 'PLASTIC',
  'SILVER',  'STEEL', 'STONE', 'SHINY_PLASTIC', 'SATIN',  'METALIZED', 'NEON_GNC',
  'CHROME', 'ALUMINIUM', 'OBSIDIAN', 'NEON_PHC', 'JADE, CHARCOAL',  'WATER, GLASS',
  'DIAMOND', 'DEFAULT' ]

SHAPE_TYPES = ['COMPOUND', 'COMPSOLID', 'SOLID', 'SHELL',
  'FACE', 'WIRE', 'EDGE', 'VERTEX', 'SHAPE']

TOPO_TYPES = ['TopAbs_COMPOUND', 'TopAbs_COMPSOLID', 'TopAbs_SOLID', 'TopAbs_SHELL',
                      'TopAbs_FACE', 'TopAbs_WIRE', 'TopAbs_EDGE', 'TopAbs_VERTEX', 'TopAbs_SHAPE']

class Env:
    def __init__(self):
        self.envs = {}             
        for param in sys.argv:
           key,sep,val = param.partition('=')
           if val != '':
             try:
               self.envs[key] = int(val)
             except ValueError:
               print('Non int param')          
        
    def env(self, envName, envDefault):
        if key in self.envs:
            return self.envs[key]
        else:
            return envDefault        



def objToStr(obj) :
    ret = dict()
    ret['CLASS'] = str(obj.__class__.__name__)
    if isinstance(obj,gp_Pnt):
       ret['x,y,z'] = '(' + str(obj.X()) + ',' + str(obj.Y()) + ',' + str(obj.Z()) + ')'
    elif isinstance(obj, AIS_Point):
        ret['Component().Pnt()'] = obj.Component().Pnt()
    elif isinstance(obj, AIS_Line):
        pass
    elif isinstance(obj, Geom_Point):
        ret['Pnt()'] = obj.Pnt()
    elif isinstance(obj, AIS_Shape):
        ret['Shape()']  = obj.Shape()
    elif isinstance(obj, TopoDS_Shape):
        ret['Type'] = SHAPE_TYPES[obj.ShapeType()]
        exp = TopExp_Explorer(obj, TopAbs_EDGE)
        i = 0
        while (exp.More()):
           ret['Edge-'+str(i)] = exp.Current().__class__.__name__
           i += 1
           exp.Next()
        exp = TopExp_Explorer(obj, TopAbs_VERTEX)
        i = 0
        while (exp.More()):
           ret['Vertex-'+str(i)] = exp.Current().__class__.__name__
           i += 1
           exp.Next()
    #todo QuantityColor
    elif hasattr(obj,'__dict__'):
       return vars(obj)
    else:
        ret['class'] = ' Unknown structure '
    return ret

def dumpObj(obj):
  print(json.dumps(obj, default=lambda obj: objToStr(obj), indent=5))

def n(val, default):
   if val == None:
       return default
   return val


'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''



class TestLib:

    def __init__(self):
        print('Test lib: init()')

    def start(self):
        print('Test lib: start()')

    def drawPoint(self, pnt, style):
        print('Test lib: drawPoint()')


    def drawLabel(self, pnt, text, style):
        print('Test lib: drawLabel()')

    def drawShape(self, shape, style):
        print('Test lib: drawShape()')


class StlLib:

    def __init__(self, decoration, precision, path):
       print('Stl lib: init()')
       self.stl = StlRenderer(precision, path)

    def start(self):
        print('Stl lib: start()')

    def drawPoint(self, pnt, style):
        print('Stl lib: drawPoint()')

    def drawLabel(self, pnt, text, style):
        print('Stl lib: drawLabel()')

    def drawShape(self, shape, style):
        print('Stl lib: drawShape()')
        self.stl.drawShape(shape)



class WebLib:

    def __init__(self, decoration, precision, path):
        print('Web lib: init()')
        self.web = ThreeJsRenderer(decoration, precision, path)

    def start(self):
        print('Web lib: start()')
        self.web.render()

    def drawPoint(self, pnt, style):
        print('Web lib: drawPoint()')
        self.web.drawPoint(pnt, style['color'], style['pointSize'])

    def drawLabel(self, pnt, text, style):
        print('Web lib: drawLabel()')
        self.web.drawLabel(pnt, text, style['color'])

    def drawShape(self, shape, style):
        print('Web lib: drawShape()')
        self.web.drawShape(shape, style['color'], style['tran'] ,style['lineWidth'])


def getWireStartPointAndTangentDir(aWire):
    ex = BRepTools_WireExplorer(aWire)
    edge = ex.Current()
    vertex = ex.CurrentVertex()
    v = getVectorTangentToCurveAtPoint(edge, 0)
    return BRep_Tool.Pnt(vertex), gp_Dir(v)

def getVectorTangentToCurveAtPoint(aEdge, uRatio):
  aCurve, aFP, aLP = BRep_Tool.Curve(aEdge)
  aP = aFP + (aLP - aFP) * uRatio
  v1 = gp_Vec()
  p1 = gp_Pnt()
  aCurve.D1(aP,p1,v1)
  return v1;


class ScreenRenderer:

    def __init__(self):
        self.styles = None  
        self.display = None
  
    def getStyle(self, styleName): 
        if self.styles != None:
            if styleName in self.styles:
                return self.styles[styleName]
        return DEFAULT_STYLE
        
    def render(self, drawable, styles):
        self.display, start_display, add_menu,  add_function_to_menu  = init_display(
            None, (700, 500), True, [128, 128, 128], [128, 128, 128]
          )
 
        self.styles = styles
        drawable.render(self)
        self.styles = None

        self.display.FitAll()
        start_display()

    def renderShapeObj(self, shape, transforms, styleName):
        color, transparency, materialName = self.getStyle(styleName)
        trsf = gp_Trsf()
        for tr in transforms:
            trsf *= tr.getTrsf()
        shape =  BRepBuilderAPI_Transform(shape, trsf).Shape()
        ais = AIS_Shape(shape)
        r,g,b = color
        aisColor =  Quantity_Color(r/256, g/256, b/256, Quantity_TOC_RGB)
        ais.SetColor(aisColor)
        ais.SetTransparency(transparency/100)
        aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(materialName))
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def renderLabel(self, geometry, transforms, styleName, layerName):
        pnt, text, size = geometry
        color, transparency, materialName = self.getStyle(styleName)
        r, g, b =  color
        trsf = gp_Trsf()
        for tr in transforms:
            trsf *= tr.getTrsf()
        pntTrans = pnt.Transformed(trsf)    
        self.display.DisplayMessage(pntTrans, text, size, (r/256, g/256, b/256), False)

    def renderBox(self, geometry, transforms, styleName, layerName):
        xSize, ySize, zSize = geometry 
        shape = BRepPrimAPI_MakeBox (xSize, ySize, zSize).Shape()
        self.renderShapeObj(shape, transforms, styleName)
        
    def renderSphere(self, geometry, transforms, styleName, layerName):
        pnt, r = geometry
        shape = BRepPrimAPI_MakeSphere(pnt, r).Shape()
        self.renderShapeObj(shape, transforms,styleName)

    def renderCone(self, geometry, transforms, styleName, layerName):
        r1, r2, h = geometry
        shape = BRepPrimAPI_MakeCone (r1, r2, h).Shape()
        self.renderShapeObj(shape, transforms,styleName)

    def renderCylinder(self, geometry, transforms, styleName, layerName):
        r, h = geometry 
        shape = BRepPrimAPI_MakeCylinder (r, h).Shape()
        self.renderShapeObj(shape, transforms,styleName)

    def renderTube(self, geometry, transforms, styleName, layerName):
        aWire, radius = geometry
        startPoint, tangentDir = getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, radius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire =  BRepBuilderAPI_MakeWire(profileEdge).Wire()
        
        pipeShell = BRepOffsetAPI_MakePipe(aWire, profileWire)
        pipeShape = pipeShell.Shape()
        
        self.renderShapeObj(pipeShape, transforms, styleName)

    def renderSurface(self, geometry, styleName, layerName):
        surfaceShape = geometry
        self.renderShapeObj(surfaceShape, transforms, styleName)

#************************************************************

class Transform():
    def __init__(self, geometry):
        self.geometry = geometry
    def getTrsf():
        pass

class Rotate(Transform):
    def getTrsf(self): 
        pnt, direct, angle = self.geometry    
        trsf = gp_Trsf()
        trsf.SetRotation(pnt, direct, angle)
        return rtsf

    
class Translate(Transform):
    def getTrsf(self):
        dx, dy, dz = self.geometry    
        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(dx, dy, dz))
        return trsf
 
class Scale(Transform):
    def getTrsf(self):    
        kx, ky, kz = self.geometry    
        trsf = gp_Trsf()
        trsf.SetScale(kx, ky, kz)
        return trsf

class FromPointToPoint(Transform):
       
    def getTrsf(self):    
        pnt1, pnt2 = self.geometry        
        dirVec = gp_Vec(pnt1, pnt2)
        targetDir = gp_Dir(dirVec)
        
        rotateAngle = gp_Dir(0,0,1).Angle(targetDir)
        if not gp_Dir(0,0,1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0,0,1)
            rotateDir.Cross(targetDir)
        else:    
            rotateDir = gp_Dir(0,1,0)
        
        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(gp_Pnt(0,0,0), rotateDir), rotateAngle)
        trsf.SetTranslationPart(gp_Vec(gp_Pnt(0,0,0), pnt1))

        return trsf

#************************************************************
 
class Drawable:
    def __init__(self, geometry):
    
        self.geometry = geometry
        self.transforms = []
        self.layerName = None
        self.styleName = None
        self.childs = {}
        self.childsCnt = 0


    def add(self, drawable, name = None):
        if name == None:
            name = 'Child'+str(self.childsCnt)
        self.childs[name] = drawable
        self.childsCnt += 1
        
    def dump(self, prefix = ''):
        print(prefix+self.__class__.__name__)
        for key in self.childs:
            self.childs[key].dump(prefix+'['+key+']')
        
    def copy(self):
        copyed = self.__class__(geometry)     
        copyed.geometry = self.geometry
        copyed.transforms = self.transforms.copy()
        copyed.layerName = self.layerName
        copyed.styleName = self.styleName
        for key in self.childs:
            copyed.childs[key] = self.childs[key].copy() 
        return copyed;
    
    def addTransform(self, transform):
        self.transforms.append(transform)
        for key in self.childs:
            self.childs[key].addTransform(transform)
            
    def translate(self, dx,dy,dz):
        self.addTransform(Translate((dx,dy,dz)))

    def scale(self, kx,ky,kz):
        self.addTransform(Scale((kx,ky,kz)))

    def rotate(self, pnt, dir, angle):
        self.addTransform(Rotate((pnt, dir, angle)))
        
    def fromPointToPoint(self, pnt1, pnt2):
        self.addTransform(FromPointToPoint((pnt1, pnt2)))


    def setStyle(self, styleName):
        if self.styleName == None:
            self.styleName = styleName
        for key in self.childs:
            self.childs[key].setStyle(styleName)
            
    def setLayer(self, layerName):
        if self.layerName == None:
            self.layerName = layerName
        self.layerName = layerName
        for key in self.childs:
            self.childs[key].setLayer(layerName)

    def render(self, lib):
        self.renderSelf(lib)
        for key in self.childs:
            self.childs[key].render(lib)

    def renderSelf(self, lib):
        pass
    

class Hook(Drawable):
    #pnt = self.geometry
    pass

class Label(Drawable):
    def renderSelf(self, lib):
        lib.renderLabel(self.geometry, self.transforms, self.styleName, self.layerName)
 
class Box(Drawable):
    def renderSelf(self, lib):
        lib.renderBox(self.geometry, self.transforms, self.styleName, self.layerName)

class Sphere(Drawable):
    def renderSelf(self, lib):
        lib.renderSphere(self.geometry, self.transforms, self.styleName, self.layerName) 

class Cone(Drawable):
    def renderSelf(self, lib):
        lib.renderCone(self.geometry, self.transforms,  self.styleName, self.layerName)

class Cylinder(Drawable):
    def renderSelf(self, lib):
        lib.renderCylinder(self.geometry, self.transforms, self.styleName, self.layerName)
        
class Tube(Drawable):
    def renderSelf(self, lib):
        lib.renderTube(self.geometry, self.transforms, self.styleName,  self.layerName)

class Tor(Drawable):
    def renderSelf(self, lib):
        pnt1, pnt2, pnt3, r = self.geometry
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        lib.renderTube((wire, r), self.transforms, self.styleName,  self.layerName)

class Surface(Drawable):
    def renderSelf(self, lib):
        lib.renderSurface(self.geometry,  self.transforms, self.styleName, self.layerName)

#************************************************************


class StandartLib:

    def getGroup(self):
        return Drawable(None)

    def getFoo(self):
        return Drawable(None)

    def getContainer(self, customData):
        return Drawable((customData))
        
    def getHook(self, pnt) :
        return Drawable(pnt)

    def getLabel(self, pnt, text, size ): 
        return Label((pnt, text, size))

    def getBox(self, xSize, ySyze, zSize):
        return Box((xSize, ySyze, zSize))

    def getSphere(self, pnt, r) :
        return Sphere((pnt, r))
        
    def getCone(self, r1, r2, h):    
        return Cone((r1, r2, h))

    def getCylinder(self, r, h):    
        return Cylinder((r, h))

    def getTube(self, wire, radius):
        return Tube((wire, radius))

    def getSurface(self, surface):
        return Surface(surface)

