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

    def _renderShapeObj(self, theShape, color100, transp100, materialName):
        ais = AIS_Shape(theShape)
        r,g,b = color100
        aisColor =  Quantity_Color(r/100, g/100, b/100, Quantity_TOC_RGB)
        ais.SetColor(aisColor)
        ais.SetTransparency(transp100/100)
        aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(materialName))
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def renderLabel(self, pnt, dLabel ,labelText, color, size):
        pntLabel = gp_Pnt(pnt.X()+dLabel,pnt.Y()+dLabel,pnt.Z()+dLabel)
        r,g,b = color 
        self.display.DisplayMessage(pntLabel,
            labelText, size, (r/100, g/100, b/100), False)

    def renderSphere(self, centerPoint, radius, quality, color, transp, material):
        theShape = BRepPrimAPI_MakeSphere(centerPoint, radius).Shape()
        self._renderShapeObj(theShape, color, transp, material)

    def renderSurface(self, surfaceShape, quality, color, transp, material):
        self._renderShapeObj(surfaceShape, color, transp, material)

    def renderCylinder(self, startPoint, endPoint, radius, quality, color, transp, material):
    
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

    def renderCone(self, startPoint, endPoint, radius1, radius2, quality, color, transp, material):
    
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
        
    def renderPipe(self, aWire, radius, quality, color, transp, material):
    
        startPoint, tangentDir = getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, radius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire =  BRepBuilderAPI_MakeWire(profileEdge).Wire()
        
        pipeShell = BRepOffsetAPI_MakePipe(aWire, profileWire)
        pipeShape = pipeShell.Shape()
        
        self._renderShapeObj(pipeShape, color, transp, material)
    
    def renderBox(self, firstCornerPoint, secondCornerPoint, quality, color, transp, material):
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
    def __init__(self, geom, styler):
        self.geom = geom
        self.styler = styler.copy()

class Foo(Drawable):
    def render(self, lib):
        if self.labelText != None:
            lib.renderLabel(self.geom, 10 * self.styler.scale, self.labelText, 
                   self.styler.get('LabelColor',(60,60,60)), 
                   self.styler.get('LabelSize'),20)

class Cylinder(Drawable):
    def render(self, lib):
        pnt1, pnt2, r = self.geom;
        lib.renderCylinder(pnt1,pnt2, r, 
            self.styler.get('GeomColor',(60,60,60)), 
            self.styler.get('GeomTransp',0), 
            self.styler.get('GeomMaterial','PLASTIC'))

class Cone(Drawable):
    def render(self, lib):
        pnt1, pnt2, r1, r2 = self.geom;
        lib.renderCone(pnt1,pnt2, r1, r2, 
            self.styler.get('GeomColor'), 
            self.styler.get('GeomTransparency'), 
            self.styler.get('GeomMaterial'))

class Point(Drawable):
    def render(self, lib):
        center = self.geom
        lib.renderSphere(center, 
            self.styler.get('GeomScaledLineWidth')*2,
            self.styler.get('GeomColor'), 
            self.styler.get('GeomTransparency'), 
            self.styler.get('GeomMaterial'))
        Foo(center, self.labelText, self.styler).render(lib)
        
class Wire(Drawable):
    def render(self, lib):
        lib.renderPipe(self.geom, 
            self.styler.get('GeomScaledLineWidth'), 
            self.styler.get('GeomColor'), 
            self.styler.get('GeomTransparency'), 
            self.styler.get('GeomMaterial'))

class Circle(Drawable):
    def render(self, lib):
        pnt1,pnt2,pnt3 = self.geom;
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        lib.drawShape(edge, self.styler.getDrawSetting('Wire'))

class Surface(Drawable):
    def render(self, lib):
        lib.renderSurface(self.geom, 
            self.styler.get('GeomColor'), 
            self.styler.get('GeomTransparency'), 
            self.styler.get('GeomMaterial'))

class Box(Drawable):
    def render(self, lib):
        firstCorner, secondCorner = self.geom
        lib.renderBox(firstCorner, secondCorner, 
            self.styler.get('GeomColor'), 
            self.styler.get('GeomTransparency'), 
            self.styler.get('GeomMaterial'))

#************************************************************************

class Points(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        for key in self.geom:
            if self.labelText != None:
                text = self.labelText+str(key)
            else:
                text = self.labelText+str(key)       
            Point(self.geom[key], text, self.styler).render(lib)

class Line(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Wire')
        pnt1,pnt2 = self.geom;
        Cylinder((pnt1, pnt2, setting['GeomBoldLevel']*self.boldFactor),'',self.styler).render(lib)
        #todo label

class Vector(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Wire')
        pnt1, pnt2 = self.geom;


        vCone = gp_Vec(pnt1, pnt2)
        vCone.Normalize()
        vCone.Multiply(10)

        vLine = gp_Vec(gp_Origin(), pnt2)
        vLine.Subtract(vCone)
        
        middlePnt = pnt1.Translated(vLine)
        
        Cylinder((pnt1, middlePnt, setting['GeomBoldLevel']*self.boldFactor), '',self.styler).render(lib)
        Cone((middlePnt, pnt2, setting['GeomBoldLevel']*self.boldFactor*3, 0), '',self.styler).render(lib)
        #todo label
         
class Desk(Drawable):
    def render(self, lib):

        setting = self.styler.getDrawSetting('Surface')
        
        originX, originY, originZ = self.styler.originXYZ
        scale = self.styler.scale
        xBox, yBox, zBox = 1500*scale, 1000*scale, 40*scale
        firstCorner = gp_Pnt(-xBox/2-originX, -yBox/2-originY, -zBox-originZ)
        secondCorner = gp_Pnt(xBox/2-originX, yBox/2-originY, -originZ)
        Box((firstCorner, secondCorner),'',self.styler).render(lib)
        scaleLabelPoint = gp_Pnt( -xBox/2-originX, -yBox/2-originY, zBox/3-originZ)
        lib.renderLabel( scaleLabelPoint, 10 * self.styler.scale, 'A0 M' + self.styler.scaleStr, setting['LabelColor'], setting['LabelSize'] )

            
class Axis(Drawable):
    def render(self, lib):
    
            setting = self.styler.getDrawSetting('Surface')
            size = 500*self.styler.scale

            step = size/10
            ss = [1,5,10,50,100,500,1000,5000,10000]
            for s in ss:
               if step<s:
                   step=s/5
                   break

            #lib.renderTrihedron(size, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])
  
            Point(gp_Pnt(0,0,0),'',self.styler).render(lib)
            
            Vector((gp_Pnt(0,0,0),gp_Pnt(size,0,0)),'',self.styler).render(lib)
            Vector((gp_Pnt(0,0,0),gp_Pnt(0,size,0)),'',self.styler).render(lib)
            Vector((gp_Pnt(0,0,0),gp_Pnt(0,0,size)),'',self.styler).render(lib)
            
            Foo(gp_Pnt(size,0,0),'X', self.styler).render(lib)
            Foo(gp_Pnt(0,size,0),'Y', self.styler).render(lib)
            Foo(gp_Pnt(0,0,size),'Z', self.styler).render(lib)
            
            
            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                Point(gp_Pnt(d,0,0),'',self.styler).render(lib)
                Point(gp_Pnt(0,d,0),'',self.styler).render(lib)
                Point(gp_Pnt(0,0,d),'',self.styler).render(lib)


        #todo label

class Theme:
    def __init__(self):
        
        self.params = dict()

        self.initStyle('MainStylePointType', (90,90,10), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initStyle('MainStyleWireType', (10,10,90), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initStyle('MainStyleSurfaceType',(10,10,90), 0, 5,'PLASTIC', (70,70,70) ,30)
     
        self.initStyle('InfoStylePointType', (40,40,40), 50,3,'PLASTIC', (70,70,70) ,30)
        self.initStyle('InfoStyleWireType', (40,40,40), 50, 3,'PLASTIC',  (70,70,70) ,30)
        self.initStyle('InfoStyleSurfaceType', (40,40,40),50, 3,'PLASTIC', (70,70,70) ,30)
      
        self.initStyle('FocusStylePointType', (90,10,10), 0, 5,'PLASTIC', (70,70,70) ,30)
        self.initStyle('FocusStyleWireType', (90,10,10), 0, 3,'PLASTIC', (70,70,70) ,30)
        self.initStyle('FocusStyleSurfaceType', (90,10,10), 50, 3,'PLASTIC', (70,70,70) ,30)

        self.initStyle('', (60,60,60), 50, 3, 'CHROME', (70,70,70) ,30)

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
        self.params[paramNamePrefix+'GeomLineScaledSize'] = geomBoldLevel
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
        return self.layer+'->'+self.style+'->'+self.dim    

class Scene:

    def __init__(self, globalForGetFunctions):

        self.drawables = []
        self.drawHints = { }
        self.drawStyle = 'Main'
        self.drawLabelText = None
        
        self.vals = dict()
        self.cache = dict()
        self.forGetFunctions =  globalForGetFunctions

        self.setValsFromCLI()
        
        self.styler = Styler(Theme()) 
        self.theme = Theme()
        
        '''
        self.setVal('SysPrecisionShape', 0.2)
        self.setVal('SysPrecisionWire', 0.2)
        '''
        
    def setValsFromCLI(self):
        for param in sys.argv:
           key,sep,val = param.partition('=')
           if val != '':
             try:
               self.setVal(key, int(val))
             except ValueError:
               print('Non int param')          

    def initRenderLib(self):
    
        slideName = self.getVal('SLIDE_NAME') + str(self.getVal('SLIDE_NUM')) + "_test"
        
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
            
        return lib        
   
    def setVal(self, valKey, val):
        if valKey not in self.vals:
            self.vals[valKey] = val

    def getVal(self, valKey):
        return self.vals[valKey]

    def putToRender(self, drawable):
        self.drawables.append(drawable)

    def render(self):
        self.setVal('RENDER_TARGET', 'screen')
        
        self.setVal('SCENE_SCALE', '1:1')
        self.setVal('SCENE_IS_DESK', True)
        self.setVal('SCENE_IS_AXIS', True)
        self.setVal('SCENE_ORIGIN', (0,0,0))

        self.setVal('SLIDE_NUM', 0)
        self.setVal('SLIDE_NAME', 'noname')

        self.styler.setBounds(self.getVal('SCENE_SCALE'), self.getVal('SCENE_ORIGIN'))
        
        self.styler.setStyle('Info')

        if self.getVal('SCENE_IS_DESK'):
            self.putToRender( Desk(None, self.styler) )         
        if self.getVal('SCENE_IS_AXIS'):
            self.putToRender( Axis(None, self.styler) )         

        lib = self.initRenderLib()
        print('==> Slide', self.getVal('SLIDE_NAME'), self.getVal('SLIDE_NUM'))
        
        for drawable in self.drawables:
            print('==> Render', drawable.__class__.__name__, drawable.geom)
            drawable.render(lib)

        lib.start()

    def style(self, style, color = None, transp = None): 
        self.drawStyle = style
        self.drawHints['GeomColor'] = color
        self.drawHints['GeomTransp'] = transp
        
    def label(self, labelText, labelColor = None, labelSize = None): 
        self.styler.setLabel(labelText, labelColor, labelSize)

    def draw(self, geomName, param1 = None, param2 = None):
    
        geom =  self.get(geomName, param1, param2)
        
        if geomName.endswith('Point'):
            self.styler.setDim('PointDim')
            drawable = Point(geom, self.styler)
        elif geomName.endswith('Points'):
            self.styler.setDim('PointDim')
            drawable = Points(geom, self.styler)
        elif geomName.endswith('Line'):
            self.styler.setDim('LineDim')
            drawable = Line(geom, self.styler)
        elif geomName.endswith('Wire'):
            self.styler.setDim('LineDim')
            drawable = Wire(geom, self.styler)
            self.styler.setDim('SurfaceDim')
        elif geomName.endswith('Surface'):
            drawable = Surface(geom, self.styler)
        else:    
            self.styler.setDim('PointDim')
            drawable = Foo(geom, self.styler)
            
        self.putToRender(drawable)
        print('==> PutToRender', drawable.__class__.__name__, self.styler.dump)
        
        self.styler.clearLabel()

        
    def getCacheKey(self, objName, param1, param2):
        params = ''
        if param1 != None:
          params += str(param1)
        if param2 != None:
          params += ',' + str(param2) 
        return 'get' + objName+'('+ params + ')'      
        
    def get(self, objName, param1 = None, param2 = None):
        cacheKey = self.getCacheKey(objName, param1, param2)
        if  cacheKey in self.cache:  
            print('==> Get from cache',cacheKey)         
            return self.cache[cacheKey]
        else:
            if param1 == None:
                obj = self.forGetFunctions['get'+objName]()
            elif param2 == None:
                obj = self.forGetFunctions['get'+objName](param1)
            else:
                obj = self.forGetFunctions['get'+objName](param1, param2)

            print('==> Compute', cacheKey)         
            self.cache[cacheKey] = obj
            return obj       

if __name__ == '__main__':
    pass

