from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_XOY, gp_YOZ
from OCC.Core.Geom import Geom_Axis2Placement, Geom_CartesianPoint, Geom_Point
from OCC.Core.AIS import AIS_Point, AIS_Trihedron, AIS_Shape, AIS_Line
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe, BRepOffsetAPI_MakePipeShell
from OCC.Core.TopoDS import TopoDS_Edge

import OCC.Core.BRepPrimAPI

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox

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

    def __init__(self, scaleStr, originXYZ):
        self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display(
            None, (1024, 768), True, [128, 128, 128], [128, 128, 128]
          )
          
        self.originXYZ = originXYZ
        self.scaleStr = scaleStr
        splitted = scaleStr.split(':')
        self.scale = (int(splitted[1])/int(splitted[0]))         


    def _styleAis(self, ais, styleName, styleValue):
        if styleName == 'color':
            r,g,b = styleValue
            color =  Quantity_Color(r/100, g/100, b/100, Quantity_TOC_RGB)
            ais.SetColor(color)
            if isinstance(ais, AIS_Trihedron):
                ais.SetArrowColor(color)
                ais.SetTextColor(color)
        elif styleName == 'transp':
                ais.SetTransparency(styleValue/100)
        elif styleName == 'material':
             aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(styleValue))
             ais.SetMaterial(aspect)
        elif styleName == 'lineType':
             ais.Attributes().LineAspect().SetTypeOfLine(LINE_TYPES[styleValue])
             ais.Attributes().WireAspect().SetTypeOfLine(LINE_TYPES[styleValue])
        elif styleName == 'lineWidth':
            ais.Attributes().LineAspect().SetWidth(styleValue)
            ais.Attributes().WireAspect().SetWidth(styleValue)
        if isinstance(ais, AIS_Point):
            if styleName == 'pointType':
                 ais.SetMarker(POINT_TYPES.index(styleValue))
            if styleName == 'pointSize':
                 ais.Attributes().PointAspect().SetScale(styleValue)

    def drawLabel(self, pnt, labelText, style):
        dLabel = 10 * self.scale
        pntLabel = gp_Pnt(pnt.X()+dLabel,pnt.Y()+dLabel,pnt.Z()+dLabel)
        r,g,b = style['LabelColor']
        self.display.DisplayMessage(pntLabel,
            labelText, style['LabelSize'], (r/100, g/100, b/100), False)

    def renderSphere(self, centerPoint, radius, quality, color, transp, material):
        theShape = OCC.Core.BRepPrimAPI.BRepPrimAPI_MakeSphere(centerPoint, radius).Shape()
        self.renderShapeObj(theShape, color, transp, material)
        pass
        
    def renderPipe(self, aWire, radius, quality, color, transp, material):
    
        startPoint, tangentDir = getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, radius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire =  BRepBuilderAPI_MakeWire(profileEdge).Wire()
        
        pipeShell = BRepOffsetAPI_MakePipe(aWire, profileWire)
        pipeShape = pipeShell.Shape()
        
        self.renderShapeObj(pipeShape, color, transp, material)
        
    def renderShapeObj(self, theShape, color100, transp100, materialName):
        ais = AIS_Shape(theShape)
        r,g,b = color100
        aisColor =  Quantity_Color(r/100, g/100, b/100, Quantity_TOC_RGB)
        ais.SetColor(aisColor)
        ais.SetTransparency(transp100/100)
        aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(materialName))
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)
        
        

    def drawPoint(self, pnt, style):
        ais = AIS_Point(Geom_CartesianPoint(pnt))
        self._styleAis(ais, 'color', style['GeomColor'])
        self._styleAis(ais, 'transp', style['GeomTransp'])
        self._styleAis(ais, 'material', style['GeomMaterial'])
        self._styleAis(ais, 'pointType', 'BALL')
        self._styleAis(ais, 'pointSize', style['GeomBoldLevel'])
        self.display.Context.Display(ais, False)

    def drawShape(self, shape, style):
        ais = AIS_Shape(shape)
        self._styleAis(ais, 'color', style['GeomColor'])
        self._styleAis(ais, 'transp', style['GeomTransp'])
        self._styleAis(ais, 'material', style['GeomMaterial'])
        self._styleAis(ais, 'pointType', 'BALL')
        self._styleAis(ais, 'pointSize', style['GeomBoldLevel'])
        self._styleAis(ais, 'lineType', 'SOLID')
        self._styleAis(ais, 'lineWidth', style['GeomBoldLevel'])
        self.display.Context.Display(ais, False)

    def drawTrihAis(self, ais, style):
        self._styleAis(ais, 'color', style['GeomColor'])
        self._styleAis(ais, 'transp', style['GeomTransp'])
        self._styleAis(ais, 'material', style['GeomMaterial'])
        self._styleAis(ais, 'pointType', 'BALL')
        self._styleAis(ais, 'pointSize', style['GeomBoldLevel'])
        self._styleAis(ais, 'lineType', 'SOLID')
        self._styleAis(ais, 'lineWidth', style['GeomBoldLevel'])
        self.display.Context.Display(ais, False)


    def drawAxis(self, style):

            size = 500*self.scale

            step = size/10
            ss = [1,5,10,50,100,500,1000,5000,10000]
            for s in ss:
               if step<s:
                   step=s/5
                   break

            pnt = gp_Pnt(0,0,0)
            dir1 = gp_Dir(gp_Vec(0,0,1))
            dir2 = gp_Dir(gp_Vec(1,0,0))
            geomAxis = Geom_Axis2Placement(pnt, dir1, dir2)

            trihAis = AIS_Trihedron(geomAxis)
            trihAis.SetSize(size)

            self.drawTrihAis(trihAis, style)

            self.drawPoint(gp_Pnt(0,0,0), style)

            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                self.drawPoint(gp_Pnt(d,0,0), style)
                self.drawPoint(gp_Pnt(0,d,0), style)
                self.drawPoint(gp_Pnt(0,0,d), style)

    def drawDesk(self, style):
            originX, originY, originZ = self.originXYZ
            scale = self.scale
            xBox, yBox, zBox = 1500*scale, 1000*scale, 40*scale
            desk = BRepPrimAPI_MakeBox (gp_Pnt( -xBox/2-originX, -yBox/2-originY, -zBox-originZ), xBox, yBox, zBox)
            self.drawShape(desk.Solid(), style)
            scaleLabelPoint = gp_Pnt( -xBox/2-originX, -yBox/2-originY, zBox/3-originZ)
            self.drawLabel( scaleLabelPoint, 'A0 M' + self.scaleStr, style )
  
    #todo start -> run
    def start(self):
         self.display.FitAll()
         self.start_display()


class Drawable:
    def __init__(self, geom, labelText, styler):
        self.geom = geom
        self.styler = styler
        self.labelText = labelText

class Foo(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        lib.drawLabel(self.geom, setting)

class Point(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        center = self.geom
        lib.renderSphere(center, setting['GeomBoldLevel']/10*2.5*2, 2/10, setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])
        lib.drawLabel(self.geom, '', setting)
        
class Points(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Point')
        for key in self.geom:
           Point(self.geom[key], self.labelText+str(key), self.styler).render(lib)
        
class Wire(Drawable):
    def render(self, lib):
        setting = self.styler.getDrawSetting('Wire')
        print('**************', setting)
        lib.drawShape(self.geom, setting)
        lib.renderPipe(self.geom, setting['GeomBoldLevel']/10*2*1.3, 2/10,setting['GeomColor'], setting['GeomTransp'], setting['GeomMaterial'])

class Circle(Drawable):
    def render(self, lib):
        pnt1,pnt2,pnt3 = self.geom;
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        lib.drawShape(edge, self.styler.getDrawSetting('Wire'))

class Line(Drawable):
    def render(self, lib):
          pnt1,pnt2 = self.geom;
          edge = BRepBuilderAPI_MakeEdge(pnt1, pnt2).Edge()
          lib.drawShape(edge, self.styler.getDrawSetting('Wire'))

class Surface(Drawable):
    def render(self, lib):
        lib.drawShape(self.geom, self.styler.getDrawSetting('Surface'))
            
class Desk(Drawable):
    def render(self, lib):
        lib.drawDesk(self.styler.getDrawSetting('Surface'))
            
class Axis(Drawable):
    def render(self, lib):
        lib.drawAxis(self.styler.getDrawSetting('Surface'))


class Styler:
    def __init__(self, drawStyle, drawHints = {} ):

        self.drawHints = drawHints.copy() 
        self.drawStyle = drawStyle 
        
        self.vals = dict()

        self.initPrimitive('MainPoint', (90,90,10), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('MainWire', (10,10,90), 0, 5, 'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('MainSurface',(10,10,90), 0, 5,'PLASTIC', (70,70,70) ,30)
     
        self.initPrimitive('InfoPoint', (40,40,40), 0,3,'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('InfoWire', (40,40,40), 0, 3,'PLASTIC',  (70,70,70) ,30)
        self.initPrimitive('InfoSurface', (40,40,40),0, 3,'PLASTIC', (70,70,70) ,30)
      
        self.initPrimitive('FocusPoint', (90,10,10), 0, 3,'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('FocusWire', (90,10,10), 0, 3,'PLASTIC', (70,70,70) ,30)
        self.initPrimitive('FocusSurface', (90,10,10), 0, 3,'PLASTIC', (70,70,70) ,30)
     
        
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
            lib = ScreenLib(self.getVal('SCENE_SCALE'), self.getVal('SCENE_ORIGIN'))
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

        if self.getVal('SCENE_IS_DESK'):
            self.putToRender( Desk(None, 'Desk' ,Styler('Info') ) )         
        if self.getVal('SCENE_IS_AXIS'):
            self.putToRender( Axis(None, 'Axis'  ,Styler('Info') )  )        


        lib = self.initRenderLib()
        
        for drawable in self.drawables:
            print('==> Render', drawable.__class__.__name__, drawable.geom) #self.geoms[key]
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
        styler = Styler(self.drawStyle, self.drawHints)
        
        if geomName.endswith('Point'):
            drawable = Point(geom, self.drawLabelText, labelText, styler)
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
        print('PutToRender', drawable.__class__.__name__, 'drawStyle',self.drawStyle)
        
        self.labelText = None
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
            print('=>Get from cache',cacheKey)         
            return self.cache[cacheKey]
        else:
            if param1 == None:
                obj = self.forGetFunctions['get'+objName]()
            elif param2 == None:
                obj = self.forGetFunctions['get'+objName](param1)
            else:
                obj = self.forGetFunctions['get'+objName](param1, param2)

            print('=>Compute', cacheKey)         
            self.cache[cacheKey] = obj
            return obj       

'''
double parameter = 0.1;
gp_Pnt p1 = PointonCurve(curve,parameter);
gp_Vec v1 = getVectorTangentToCurveAtPoint(curve,parameter);
TopoDS_Shape l1 = Lineptdir(p1,v1,0,100)

use the following functions to get the point and vector at parameter.

They are extracts from the openshapefactory project.

https://code.google.com/p/openshapefactory/source/browse/SFMQTDLL/src/sr...


TopoDS_Edge Lineptdir(gp_Pnt origin, gp_Vec dir, double length1, double length2)
{

Handle(Geom_Curve) spinaxis = new Geom_Line (origin,dir);
spinaxis = new Geom_TrimmedCurve (spinaxis, length1, length2);
double fp = spinaxis->FirstParameter();
double ep = spinaxis->LastParameter();

TopoDS_Edge Result = BRepBuilderAPI_MakeEdge(spinaxis,fp,ep);

return Result;

}

const gp_Pnt& PointonCurve(TopoDS_Shape SupportEdge, Standard_Real uRatio)

{
gp_Pnt p1;
if (SupportEdge.IsNull())
{
return p1;
}
const TopoDS_Edge& aEdge = TopoDS::Edge (SupportEdge);
Standard_Real aFP, aLP, aP;
Handle(Geom_Curve) aCurve = BRep_Tool::Curve(aEdge, aFP, aLP);
aP = aFP + (aLP - aFP) * uRatio;
p1 = aCurve->Value(aP);

return p1;
}    
'''

if __name__ == '__main__':
    pass

