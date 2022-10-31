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



class ScreenLib:

    def __init__(self):
        self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display(
            None, (1024, 768), True, [128, 128, 128], [128, 128, 128]
          )

    def _renderShapeObj(self, theShape, color, transparency, materialName):
        ais = AIS_Shape(theShape)
        r,g,b = color
        aisColor =  Quantity_Color(r/100, g/100, b/100, Quantity_TOC_RGB)
        ais.SetColor(aisColor)
        ais.SetTransparency(transparency/100)
        aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(materialName))
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def renderLabel(self, pnt, dLabel ,labelText, color, size):
        pntLabel = gp_Pnt(pnt.X()+dLabel,pnt.Y()+dLabel,pnt.Z()+dLabel)
        print('************',color)
        r,g,b = color 
        self.display.DisplayMessage(pntLabel,
            labelText, size, (r/100, g/100, b/100), False)

    def renderSphere(self, centerPoint, radius, color, transp, material):
        theShape = BRepPrimAPI_MakeSphere(centerPoint, radius).Shape()
        self._renderShapeObj(theShape, color, transp, material)

    def renderSurface(self, surfaceShape, color, transp, material):
        self._renderShapeObj(surfaceShape, color, transp, material)

    def renderCylinder(self, startPoint, endPoint, radius, color, transp, material):
    
        cylVec = gp_Vec(startPoint, endPoint)
        targetDir = gp_Dir(cylVec)
        rotateAngle = gp_Dir(0,0,1).Angle(targetDir)
        if not gp_Dir(0,0,1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0,0,1)
            rotateDir.Cross(targetDir)
        else:    
            rotateDir = gp_Dir(0,1,0)
           
        
        transform = gp_Trsf()
        transform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), rotateDir), rotateAngle)
        transform.SetTranslationPart(gp_Vec(gp_Pnt(0,0,0),startPoint))

        cyl = BRepPrimAPI_MakeCylinder (radius, cylVec.Magnitude()).Shape()
        shape =  BRepBuilderAPI_Transform(cyl, transform).Shape()
        self._renderShapeObj(shape, color, transp, material)

    def renderCone(self, startPoint, endPoint, radius1, radius2, color, transp, material):
    
        cylVec = gp_Vec(startPoint, endPoint)
        targetDir = gp_Dir(cylVec)
        rotateAngle = gp_Dir(0,0,1).Angle(targetDir)
        if not gp_Dir(0,0,1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0,0,1)
            rotateDir.Cross(targetDir)
        else:    
            rotateDir = gp_Dir(0,1,0)
        
        transform = gp_Trsf()
        transform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), rotateDir), rotateAngle)
        transform.SetTranslationPart(gp_Vec(gp_Pnt(0,0,0),startPoint))

        cyl = BRepPrimAPI_MakeCone (radius1, radius2, cylVec.Magnitude()).Shape()
        shape =  BRepBuilderAPI_Transform(cyl, transform).Shape()
        self._renderShapeObj(shape, color, transp, material)
        
    def renderPipe(self, aWire, radius, color, transp, material):
    
        startPoint, tangentDir = getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, radius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire =  BRepBuilderAPI_MakeWire(profileEdge).Wire()
        
        pipeShell = BRepOffsetAPI_MakePipe(aWire, profileWire)
        pipeShape = pipeShell.Shape()
        
        self._renderShapeObj(pipeShape, color, transp, material)
    
    def renderBox(self, firstCornerPoint, secondCornerPoint, color, transp, material):
        x1 = firstCornerPoint.X()
        y1 = firstCornerPoint.Y()
        z1 = firstCornerPoint.Z()
        x2 = secondCornerPoint.X()
        y2 = secondCornerPoint.Y()
        z2 = secondCornerPoint.Z()
        shape = BRepPrimAPI_MakeBox (firstCornerPoint, x2-x1, y2-y1, z2-z1).Shape()
        self._renderShapeObj(shape, color, transp, material)
  
    #todo start -> run
    def start(self):
         self.display.FitAll()
         self.start_display()


class Drawable:
    def __init__(self, geometry):
        self.geometry = geometry
        self.transforms = {}
        self.layerName = 'DefaultLayer'
        self.styleName = 'DefaultStyle'
        
    def transform(transform)
        self.transforms += transform

    def style(styleName)
        self.styleName = styleName
    
    def layer(layerName)
        self.layerName = layerName

class Label(Drawable):
    def render(self, lib):
        pnt, text, size, delta = self.geometry
        lib.renderLabel(pnt, text, size, delta, styleName, layerName)

class Box(Drawable):
    def render(self, lib):
        pnt1, pnt2 = self.geom
        lib.renderBox(pnt1, pnt2, self.styleName, self.layerName)

class Sphere(Drawable):
    def render(self, lib):
        pnt = self.geom
        lib.renderSphere(pnt, r, self.styleName, self.layerName) 

class Cone(Drawable):
    def render(self, lib):
        pnt1, pnt2, r1, r2 = self.geom;
        lib.renderCone(pnt1,pnt2, r1, r2, styleName, layerName)
        
class Tube(Drawable):
    def render(self, lib):
        wire, r = self.geom
        lib.renderTube(wire, r, self.styleName, self.layerName)

class Tor(Drawable):
    def render(self, lib):
        pnt1, pnt2, pnt3, r = self.geom;
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        lib.renderTube(wire, r, self.styleName, self.layerName)

class Surface(Drawable):
    def render(self, lib):
        lib.renderSurface(self.geom, self.styleName, self.layerName)


#************************************************************************
'''
class Points(Drawable):
    def render(self, lib):
        for key in self.geom:
            if self.styler.labelText != None:
                text = self.styler.labelText+str(key)
            else:
                text = self.styler.labelText+str(key)       
            self.styler.labelText = text    
            Point(self.geom[key], self.styler).render(lib)

class Line(Drawable):
    def render(self, lib):
        pnt1,pnt2 = self.geom;
        Cylinder((pnt1, pnt2, self.styler.get('GeomScaledLineWidth')), self.styler).render(lib)

class Vector(Drawable):
    def render(self, lib):
        pnt1, pnt2 = self.geom;


        vCone = gp_Vec(pnt1, pnt2)
        vCone.Normalize()
        vCone.Multiply(10)

        vLine = gp_Vec(gp_Origin(), pnt2)
        vLine.Subtract(vCone)
        
        middlePnt = pnt1.Translated(vLine)
        
        Cylinder((pnt1, middlePnt,self.styler.get('GeomScaledLineWidth')), self.styler).render(lib)
        Cone((middlePnt, pnt2,self.styler.get('GeomScaledLineWidth')*2 , 0), self.styler).render(lib)
         
class Desk(Drawable):
    def render(self, lib):

        originX, originY, originZ = self.styler.originXYZ
        scale = self.styler.scale
        xBox, yBox, zBox = 1500*scale, 1000*scale, 40*scale
        firstCorner = gp_Pnt(-xBox/2-originX, -yBox/2-originY, -zBox-originZ)
        secondCorner = gp_Pnt(xBox/2-originX, yBox/2-originY, -originZ)
        Box((firstCorner, secondCorner),self.styler).render(lib)
        scaleLabelPoint = gp_Pnt( -xBox/2-originX, -yBox/2-originY, zBox/3-originZ)
        lib.renderLabel( scaleLabelPoint, 
                         10 * self.styler.scale, 
                         'A0 M' + self.styler.scaleStr, 
                         self.styler.get('LabelColor'),
                         self.styler.get('LabelScaledSize') )

            
class Axis(Drawable):
    def render(self, lib):
    
            size = 500*self.styler.scale

            step = size/10
            ss = [1,5,10,50,100,500,1000,5000,10000]
            for s in ss:
               if step<s:
                   step=s/5
                   break
  
            Point(gp_Pnt(0,0,0),self.styler).render(lib)
            
            Vector((gp_Pnt(0,0,0),gp_Pnt(size,0,0)), self.styler).render(lib)
            Vector((gp_Pnt(0,0,0),gp_Pnt(0,size,0)), self.styler).render(lib)
            Vector((gp_Pnt(0,0,0),gp_Pnt(0,0,size)), self.styler).render(lib)
            
            Foo(gp_Pnt(size,0,0), self.styler).render(lib)
            Foo(gp_Pnt(0,size,0), self.styler).render(lib)
            Foo(gp_Pnt(0,0,size), self.styler).render(lib)
            
            
            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                Point(gp_Pnt(d,0,0), self.styler).render(lib)
                Point(gp_Pnt(0,d,0), self.styler).render(lib)
                Point(gp_Pnt(0,0,d), self.styler).render(lib)


        #todo label
class Theme:
    def __init__(self):
        
        self.params = dict()

        self.initStyle('', (60,60,60), 50, 3, 'CHROME', (70,70,70) ,30)

        self.initStyle('MainStylePointType', (90,90,10), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initStyle('MainStyleWireType', (10,10,90), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initStyle('MainStyleSurfaceType',(10,10,90), 0, 5,'PLASTIC', (70,70,70) ,30)
     
        self.initStyle('InfoStylePointType', (40,40,40), 50,3,'PLASTIC', (70,70,70) ,30)
        self.initStyle('InfoStyleWireType', (40,40,40), 50, 3,'PLASTIC',  (70,70,70) ,30)
        self.initStyle('InfoStyleSurfaceType', (40,40,40),50, 3,'PLASTIC', (70,70,70) ,30)
      
        self.initStyle('FocusStylePointType', (90,10,10), 0, 5,'PLASTIC', (70,70,70) ,30)
        self.initStyle('FocusStyleWireType', (90,10,10), 0, 3,'PLASTIC', (70,70,70) ,30)
        self.initStyle('FocusStyleSurfaceType', (90,10,10), 50, 3,'PLASTIC', (70,70,70) ,30)


    def getByFullName(self, fullName):
        if fullName in self.params:
            return self.params[fullName]
        else:
            return None

    def get(self, paramName ,layerName, styleName, typeName):
        ret = self.getByFullName(layerName+styleName+typeName+paramName)
        if ret != None:
            return ret
        ret = self.getByFullName(styleName+typeName+paramName)
        if ret != None:
            return ret
        ret = self.getByFullName(typeName+paramName)
        if ret != None:
            return ret
        ret = self.getByFullName(paramName)
        if ret != None:
            return ret
        return None
        

    def initStyle(self, paramNamePrefix, geomColor, geomTransp, geomBoldLevel, geomMaterial, labelColor, labelSize):
        self.params[paramNamePrefix+'GeomColor'] = geomColor
        self.params[paramNamePrefix+'GeomTransparency'] = geomTransp
        self.params[paramNamePrefix+'GeomScaledLineWidth'] = geomBoldLevel
        self.params[paramNamePrefix+'GeomMaterial'] = geomMaterial
        self.params[paramNamePrefix+'LabelColor'] = labelColor
        self.params[paramNamePrefix+'LabelScaledSize'] = labelSize

class Styler:
    def __init__(self, theme):

        self.theme = theme
        self.layerName = 'DefaultLayer'
        self.styleName = 'DefaultStyle'
        self.typeName = 'DefaultType'
        self.hints = {}
        self.labelText = ''

        self.setBounds("1:1", (0,0,0))

    def copy(self):
        copyed = Styler(self.theme)
        copyed.hints = self.hints.copy()
        copyed.layerName = self.layerName
        copyed.styleName = self.styleName
        copyed.typeName = self.typeName
        return copyed

    
    def setBounds(self, scaleStr, originXYZ): 
    
        self.originXYZ = originXYZ
        self.scaleStr = scaleStr
        
        self.originXYZ = originXYZ
        self.scaleStr = scaleStr
        splitted = scaleStr.split(':')
        self.scale = (int(splitted[1])/int(splitted[0]))         


    def setLayer(self, layerName):
        self.layerName = layerName
    
    def setStyle(self, styleName): 
        self.styleName = styleName

    def setDim(self, dimName):
        self.dimName = dimName

    def setHint(self, paramName, paramValue):
        self.hints[paramName] = paramValue
    
    def get(self, paramName):
        if paramName in self.hints:
            ret = self.hints[paramName]
            if ret != None:
                return self.hints[paramName]
        return self.theme.get(paramName,self.layerName, self.styleName, self.typeName)

    def setLabel(self, labelText, labelColor = None, labelScaledSize = None):
        self.labelText = labelText
        self.setHint('LabelColor', labelColor) 
        self.setHint('LabelScaledSize', labelScaledSize) 
        
    def clearLabel(self):
        self.labelText = None
        
    def getLabelText():
        return self.labelText
        
    def isLabel():
        return self.labelText != None
    
    def clearHints():
        self.drawHints = {}
        
    def dump(self):
        return self.layerName+'->'+self.styleName+'->'+self.typeName    
'''
class Scene:

    def __init__(self, globalForGetFunctions, sceneName=None, styles = None):

        if styles != None
            self.styles = styles
        else
            self.styles = {'MainStyle':(50,50,50),0,'CHROME'}
        
        self.sceneName = sceneName
        self.styles = styles
        self.forGetFunctions =  globalForGetFunctions

        self.envs = dict()
        self.cache = dict()
        
        self.last = None
        self.result = None         
        
        '''
        self.setVal('SysPrecisionShape', 0.2)
        self.setVal('SysPrecisionWire', 0.2)
        '''

    def env(self, envName, envDefault):
    
        if self.env = None:
            self.env = {}             
            for param in sys.argv:
               key,sep,val = param.partition('=')
               if val != '':
                 try:
                   self.env[key] = int(val)
                 except ValueError:
                   print('Non int param')          

        if key in self.env:
            return self.env[key]
        else
            return envDefault        

    def render(self, funcName, param1, param2):
'''               
        scriptDir = os.path.dirname(__file__)
        stlRelDir = os.path.join(scriptDir, '..', 'models', slideName)
        stlDir = os.path.abspath(stlRelDir)
        webRelDir = os.path.join(scriptDir, '..','slides', slideName)
        webDir = os.path.abspath(webRelDir)

        renderTarget = self.getVal('RENDER_TARGET')
        
        SysDecors = 'deprecated'
        SysPrecisions = 'deprecated'
        if renderTarget == 'test':
            lib = TestLib(SysDecors, SysPrecisions, webDir, stlDir)
        elif renderTarget == 'screen':
            lib = ScreenLib()
        elif  renderTarget == 'web':
            lib = WebLib(SysDecors, SysPrecisions, webDir)
        elif  renderTarget == 'stl':
            lib = StlLib(SysDecors, SysPrecisions, stlDir)

        print('==> Slide ', slideName)
   '''     
        lib = ScreenLib()
        self.get(funcName, param1, param2)
        self.last.render(lib)
        lib.start()
        
    def getLabel(self, pnt, text, size, delta): 
        self.last = Label(pnt, text, size, delta)

    def getSphere(pnt, r) 
        self.last = Sphere(centerPoint, radius)
        
    def getCone(pnt1, pnt2, r1, r2)    
        self.last = Cone(pnt1, pnt2, r1, r2)
    
    def getBox(pnt1, pnt2)
        self.last = Box(pnt1,pnt2)

    def getWire(wire, radius)
        self.last = Wire(wire, radius)

    def getSurface(surface)
        self.last = Surface(surface)

    def translate(dx, dy, dz)
        self.last.translate(dx, dy, dz)
    
    def rotate(pnt, dir, angle)
        self.last.rotate(pnt, dir, angle)

    def style(styleName)
        self.last.style(styleName)
    
    def layer(styleName)
        self.last.layer(styleName)

    def put(name)
        self.result.add(self.last)
        
    def get(self, objName, param1 = None, param2 = None):
    
        params = ''
        if param1 != None:
          params += str(param1)
        if param2 != None:
          params += ',' + str(param2) 
        cacheKey = 'get' + objName+'('+ params + ')'      
        
        if  cacheKey in self.cache:  
            print('==> Get from cache',cacheKey)         
            self.last = self.cache[cacheKey].copy()
        else:
            self.result = Assembly()
            if param1 == None:
                self.forGetFunctions['get'+objName]()
            elif param2 == None:
                self.forGetFunctions['get'+objName](param1)
            else:
                self.forGetFunctions['get'+objName](param1, param2)
            self.last = self.result
            print('==> Compute', cacheKey)         

if __name__ == '__main__':
    pass

