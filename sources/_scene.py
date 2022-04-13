from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_XOY, gp_YOZ, gp_Trsf, gp_DX,gp_Ax1
from OCC.Core.Geom import Geom_Axis2Placement, Geom_CartesianPoint, Geom_Point
from OCC.Core.AIS import AIS_Point, AIS_Trihedron, AIS_Shape, AIS_Line
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe, BRepOffsetAPI_MakePipeShell
from OCC.Core.TopoDS import TopoDS_Edge

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder

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
        rotateDir = gp_Dir(0,0,1)
        rotateDir.Cross(targetDir)
        
        transform = gp_Trsf()
        transform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), rotateDir), rotateAngle)
        transform.SetTranslationPart(gp_Vec(gp_Pnt(0,0,0),startPoint))

        cyl = BRepPrimAPI_MakeCylinder (radius, cylVec.Magnitude()).Shape()
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

    def renderTrihedron(self, size, color, transp100, materialName):
    
        pnt = gp_Pnt(0,0,0)
        dir1 = gp_Dir(gp_Vec(0,0,1))
        dir2 = gp_Dir(gp_Vec(1,0,0))
        geomAxis = Geom_Axis2Placement(pnt, dir1, dir2)

        ais = AIS_Trihedron(geomAxis)
        ais.SetSize(size)
        
        r,g,b = color
        aisColor =  Quantity_Color(r/100, g/100, b/100, Quantity_TOC_RGB)
        ais.SetColor(aisColor)
        ais.SetArrowColor(aisColor)
        ais.SetTextColor(aisColor)
        ais.SetTransparency(transp100/100)
        aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(materialName))
        ais.SetMaterial(aspect)

        self.display.Context.Display(ais, False)
  
    #todo start -> run
    def start(self):
         self.display.FitAll()
         self.start_display()


class Drawable:
    def __init__(self, geom, labelText, styler):
        self.geom = geom
        self.styler = styler
        self.labelText = labelText
        if self.labelText == None:
            self.labelText = ''
        self.boldFactor=0.2

class Foo(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        lib.drawLabel(self.geom, self.labelText, setting)

class Cylinder(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Wire')
        pnt1, pnt2, r = self.geom;
        lib.renderCylinder(pnt1,pnt2, r, 2/10, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])
        #todo label

class Point(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        center = self.geom
        lib.renderSphere(center, setting['GeomBoldLevel']*self.boldFactor*2, 2/10, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])
        if setting['LabelIsRender']:
            lib.renderLabel(self.geom, 10 * self.styler.scale, self.labelText, setting['LabelColor'], setting['LabelSize'])
        
        
class Wire(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Wire')
        lib.renderPipe(self.geom, setting['GeomBoldLevel']*self.boldFactor, 2/10,setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])
        #todo label

class Circle(Drawable):
    def render(self, lib):
        pnt1,pnt2,pnt3 = self.geom;
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        lib.drawShape(edge, self.styler.getDrawSetting('Wire'))
        #todo label

class Surface(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Surface')
        lib.renderSurface(self.geom, 2/10, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])
        #todo label

class Box(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Surface')
        firstCorner, secondCorner = self.geom
        lib.renderBox(firstCorner, secondCorner, 2/10, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])

#************************************************************************

class Points(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        for key in self.geom:
           Point(self.geom[key], self.labelText+str(key), self.styler).render(lib)

class Line(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Wire')
        pnt1,pnt2 = self.geom;
        Cylinder((pnt1, pnt2, setting['GeomBoldLevel']*self.boldFactor),'',self.styler).render(lib)
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

            lib.renderTrihedron(size, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])

            Point(gp_Pnt(0,0,0),'',self.styler).render(lib)

            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                Point(gp_Pnt(d,0,0),'',self.styler).render(lib)
                Point(gp_Pnt(0,d,0),'',self.styler).render(lib)
                Point(gp_Pnt(0,0,d),'',self.styler).render(lib)

        #todo label


class Styler:
    def __init__(self, drawStyle, drawHints, scaleStr, originXYZ):

        self.originXYZ = originXYZ
        self.scaleStr = scaleStr
        splitted = scaleStr.split(':')
        self.scale = (int(splitted[1])/int(splitted[0]))         

        self.drawHints = drawHints.copy() 
        self.drawStyle = drawStyle 
        
        self.vals = dict()

        self.initPrimitive('MainPoint', (90,90,10), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('MainWire', (10,10,90), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('MainSurface',(10,10,90), 0, 5,'PLASTIC', (70,70,70) ,30)
     
        self.initPrimitive('InfoPoint', (40,40,40), 0,3,'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('InfoWire', (40,40,40), 0, 3,'PLASTIC',  (70,70,70) ,30)
        self.initPrimitive('InfoSurface', (40,40,40),0, 3,'PLASTIC', (70,70,70) ,30)
      
        self.initPrimitive('FocusPoint', (90,10,10), 0, 5,'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('FocusWire', (90,10,10), 0, 3,'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('FocusSurface', (90,10,10), 50, 3,'PLASTIC', (70,70,70) ,30)
     
        
    def getDrawSetting(self, primitive):
        keyPrefix = self.drawStyle + primitive
        ret = dict()
        for key in self.vals:
            if key.startswith(keyPrefix):
               sStart,sPrefix, sEnd = key.partition(keyPrefix)
               ret[sEnd] = self.vals[key]
        for key in self.drawHints:
            if self.drawHints[key] != None:
                ret[key] = self.drawHints[key]         
        return ret 

    def initPrimitive(self, paramKeyPrefix, geomColor, geomTransp, geomBoldLevel, geomMaterial, labelColor, labelSize):
        self.setVal(paramKeyPrefix+'GeomColor',geomColor)
        self.setVal(paramKeyPrefix+'GeomTransp',geomTransp)
        self.setVal(paramKeyPrefix+'GeomBoldLevel',geomBoldLevel)
        self.setVal(paramKeyPrefix+'GeomMaterial',geomMaterial)
        self.setVal(paramKeyPrefix+'LabelColor',labelColor)
        self.setVal(paramKeyPrefix+'LabelSize',labelSize)
        self.setVal(paramKeyPrefix+'LabelIsRender',False)
        
    def setVal(self, valKey, val):
        self.vals[valKey] = val

    def getVal(self, valKey):
        return self.vals[valKey]

class Scene:

    def __init__(self, forGetFunctions):

        self.drawables = []
        self.drawHints = { }
        self.drawStyle = 'Main'
        self.drawLabelText = None
        
        self.vals = dict()
        self.cache = dict()
        self.forGetFunctions =  forGetFunctions

        self.setValsFromCLI()
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

        styler = Styler('Info', {}, self.getVal('SCENE_SCALE'), self.getVal('SCENE_ORIGIN'))

        if self.getVal('SCENE_IS_DESK'):
            self.putToRender( Desk(None,'Desk',styler) )         
        if self.getVal('SCENE_IS_AXIS'):
            self.putToRender( Axis(None,'Axis',styler) )         

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
        self.drawLabelText = labelText
        self.drawHints['LabelIsRender'] = True
        self.drawHints['LabelColor'] = labelColor 
        self.drawHints['LabelSize'] = labelSize

    def draw(self, geomName, param1 = None, param2 = None):
    
        geom =  self.get(geomName, param1, param2)
        styler = Styler(self.drawStyle, self.drawHints, self.getVal('SCENE_SCALE'), self.getVal('SCENE_ORIGIN'))
        
        if geomName.endswith('Point'):
            drawable = Point(geom, self.drawLabelText, styler)
        elif geomName.endswith('Points'):
            drawable = Points(geom, self.drawLabelText,styler)
        elif geomName.endswith('Line'):
            drawable = Line(geom, self.drawLabelText,styler)
        elif geomName.endswith('Wire'):
            drawable = Wire(geom, self.drawLabelText,styler)
        elif geomName.endswith('Surface'):
            drawable = Surface(geom, self.drawLabelText,styler)
        else:    
            drawable = Foo(geom, self.drawLabelText, styler)
            
        self.putToRender(drawable)
        print('==> PutToRender', drawable.__class__.__name__, 'drawStyle',self.drawStyle)
        
        self.drawLabelText = None
        self.drawHints['LabelIsRender'] = False
        self.drawHints['LabelColor'] = None
        self.drawHints['LabelSize'] = None

        
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

