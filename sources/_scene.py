from OCC.Display.SimpleGui import init_display

from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.Geom import Geom_Axis2Placement, Geom_CartesianPoint, Geom_Point
from OCC.Core.AIS import AIS_Point, AIS_Trihedron, AIS_Shape, AIS_Line
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox

from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.GC import  GC_MakeCircle


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

    def __init__(self, decors, StyleDesk, StyleAxis):
        self.StyleDesk = StyleDesk
        self.StyleAxis = StyleAxis
        self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display(
            None, (1024, 768), True, [128, 128, 128], [128, 128, 128]
          )
        isDesk = decors['IsDesk']
        isAxis = decors['IsAxis']
        scaleA = decors['ScaleA']
        scaleB = decors['ScaleB']
        deskDX = decors['DeskDX']
        deskDY = decors['DeskDY']
        deskDZ = decors['DeskDZ']
        self.dLabel = 10 * scaleA/scaleB
        self._decoration(isDesk, isAxis, scaleA, scaleB, deskDX, deskDY, deskDZ)



    def _styleAis(self, ais, styleName, styleValue):
        if styleName == 'color':
            r,g,b = styleValue
            color =  Quantity_Color(r/100, g/100, b/100, Quantity_TOC_RGB)
            ais.SetColor(color)
            if isinstance(ais, AIS_Trihedron):
                ais.SetArrowColor(color)
                ais.SetTextColor(color)
        elif styleName == 'tran':
                ais.SetTransparency(styleValue/100)
        elif styleName == 'material':
             aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(styleValue))
             ais.SetMaterial(aspect)
        elif styleName == 'lineType':
             #print(LINE_TYPES[styleValue])
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

    def _drawLabel(self, pnt, text, style):
       pntLabel = gp_Pnt(pnt.X()+self.dLabel,pnt.Y()+self.dLabel,pnt.Z()+self.dLabel)
       self.display.DisplayMessage(pntLabel,
                text, style['LabelS'], (style['LabelR']/100,style['LabelG']/100,style['LabelB']/100), False)

    def _drawPoint(self, pnt, style):
        ais = AIS_Point(Geom_CartesianPoint(pnt))
        self._styleAis(ais, 'color', (style['PointR'],style['PointG'], style['PointB']))
        self._styleAis(ais, 'tran', 1-style['PointA']/100)
        self._styleAis(ais, 'material', style['PointM'])
        self._styleAis(ais, 'pointType', style['PointT'])
        self._styleAis(ais, 'pointSize', style['PointS'])
        self.display.Context.Display(ais, False)

    def _drawShape(self, shape, style):
        ais = AIS_Shape(shape)
        #print(style)
        self._styleAis(ais, 'color', (style['SurfaceR'],style['SurfaceG'], style['SurfaceB']))
        self._styleAis(ais, 'tran', 1-style['SurfaceA']/100)
        self._styleAis(ais, 'material', style['SurfaceM'])
        self._styleAis(ais, 'pointType', style['PointT'])
        self._styleAis(ais, 'pointSize', style['PointS'])
        self._styleAis(ais, 'lineType', style['WireT'])
        self._styleAis(ais, 'lineWidth', style['WireS'])
        self.display.Context.Display(ais, False)

    def _drawTrihAis(self, ais, style):
        self._styleAis(ais, 'color', (style['SurfaceR'],style['SurfaceG'], style['SurfaceB']))
        self._styleAis(ais, 'tran', 1-style['SurfaceA']/100)
        self._styleAis(ais, 'material', style['SurfaceM'])
        self._styleAis(ais, 'pointType', style['PointT'])
        self._styleAis(ais, 'pointSize', style['PointS'])
        self._styleAis(ais, 'lineType', style['WireT'])
        self._styleAis(ais, 'lineSize', style['WireS'])
        self.display.Context.Display(ais, False)


    def _axis(self, size):

            style = self.StyleAxis

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

            self._drawTrihAis(trihAis, style)

            self._drawPoint(gp_Pnt(0,0,0), style)

            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                self._drawPoint(gp_Pnt(d,0,0), style)
                self._drawPoint(gp_Pnt(0,d,0), style)
                self._drawPoint(gp_Pnt(0,0,d), style)


    def _desk(self, scaleA, scaleB, deskDX, deskDY, deskDZ):
            style = self.StyleDesk
            scale = scaleA/scaleB
            xBox, yBox, zBox = 1500*scale, 1000*scale, 40*scale
            desk = BRepPrimAPI_MakeBox (gp_Pnt( -xBox/2+deskDX, -yBox/2+deskDY, -zBox+deskDZ), xBox, yBox, zBox)
            self._drawShape(desk.Solid(), style)
            scalePoint = gp_Pnt( -xBox/2+deskDX, -yBox/2+deskDY, zBox/3+deskDZ)
            self._drawLabel( scalePoint, 'A0 M' + str(scaleB) + ':' + str(scaleA), style )


    def _decoration(self, isDesk, isAxis, scaleA, scaleB, deskDX, deskDY, deskDZ):


        if isDesk:
            self._desk(scaleA, scaleB, deskDX, deskDY, deskDZ)


        if isAxis:
            axisSize = 500*scaleA/scaleB
            self._axis(axisSize)


    def start(self):
         self.display.FitAll()
         self.start_display()

    def drawLabel(self, pnt, text, style, color):
        if color != None:
            r,g,b,a = color
            style['LabelR'] = r
            style['LabelG'] = g
            style['LabelB'] = b
            style['LabelA'] = a
        self._drawLabel(pnt, text, style)

    def drawShape(self, shape, style, color):
        if color != None:
            r,g,b,a = color
            style['SurfaceR'] = r
            style['SurfaceG'] = g
            style['SurfaceB'] = b
            style['SurfaceA'] = a
        self._drawShape(shape, style)

    def drawPoint(self, pnt, style, color):
        if color != None:
            r,g,b,a = color
            style['PointR'] = r
            style['PointG'] = g
            style['PointB'] = b
            style['PointA'] = a
        self._drawPoint(pnt, style)


'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class Drawable:

    def __init__(self, obj, tp):
    
        self.vals = dict()
        self.obj = obj
        self.style = 'Main'
        self.color = None
        self.tp = tp

        self.initRGBASMT('TemplStyleMAINPoint', 90,90,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleMAINWire', 10,10,90,100, 8,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleMAINSurface',10,10,90,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleMAINLabel', 90,10,10,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('TemplStyleINFOPoint', 30,30,30,100,3,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleINFOWire', 30,30,30,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleINFOSurface', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleINFOLabel', 30,30,30,100,20,'PLASTIC','SOLID')


        self.initRGBASMT('TemplStyleFOCUSPoint', 90,10,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleFOCUSWire', 90,10,10,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleFOCUSSurface', 90,10,10,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleFOCUSLabel', 90,90,90,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('TemplStyleChromePoint', 10,10,10,100,4,'PLASTIC','EMPTY')
        self.initRGBASMT('TemplStyleChromeWire', 10,10,10,100,3,'PLASTIC','DASH')
        self.initRGBASMT('TemplStyleChromeSurface', 10,10,10,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleChromeLabel', 10,10,10,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('TemplStyleDeskPoint', 30,30,30,100,4,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleDeskWire', 30,30,30,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleDeskSurface', 30,30,30,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleDeskLabel', 30,30,30,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('TemplStyleAxisPoint', 30,30,30,100,2,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleAxisWire', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleAxisSurface', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleAxisLabel', 30,30,30,100,20,'PLASTIC','SOLID')

        
    def setStyle(self, style, color = None):
        self.style = style
        self.color = color
        
    def initVals(self, keyPrefix ,vals):
        for key in vals:
           self.initVal(keyPrefix+key, vals[key])

    def getVals(self, keyPrefix):
        ret = dict()
        for key in self.vals:
            if key.startswith(keyPrefix):
               sStart,sPrefix, sEnd = key.partition(keyPrefix)
               ret[sEnd] = self.vals[key]
        return ret

    def initRGBASMT(self, paramKeyPrefix, r,g,b,a,s,m,t):
        self.initVal(paramKeyPrefix+'R',r)
        self.initVal(paramKeyPrefix+'G',g)
        self.initVal(paramKeyPrefix+'B',b)
        self.initVal(paramKeyPrefix+'A',a)
        self.initVal(paramKeyPrefix+'S',s)
        self.initVal(paramKeyPrefix+'M',m)
        self.initVal(paramKeyPrefix+'T',t)

    def initXYZ(self, paramKeyPrefix, x,y,z):
        self.initVal(paramKeyPrefix+'X',x)
        self.initVal(paramKeyPrefix+'Y',y)
        self.initVal(paramKeyPrefix+'Z',z)
    def initVal(self, valKey, val):
        if not (valKey in self.vals):
            self.vals[valKey] = val

    def val(self, valKey):
        if (valKey in self.vals):
            return self.vals[valKey]
        else:
            raise Exception('Non init value ' +valKey)        
        

class Point:
    pass
class Wire:
    pass
class Surface:
    pass

class Scene:

    def __init__(self, forGetFunctions):

        self.lib = None
        self.geoms = dict()
        self.vals = dict()
        self.cache = dict()
        self.objNum = 0;
        self.forGetFunctions =  forGetFunctions
        self.style = None
        self.color = None
        # todo get arguments and init params
        for param in sys.argv:
           key,sep,val = param.partition('=')
           if val != '':
             try:
               self.initVal(key, int(val))
             except ValueError:
               print('Non int param')          
    

    def initVal(self, valKey, val):
        if not (valKey in self.vals):
            self.vals[valKey] = val

    def val(self, valKey):
        if (valKey in self.vals):
            return self.vals[valKey]
        else:
            raise Exception('Non init value ' +valKey)        


    def initObj(self, tp, style, obj, color = None):
        dr = Drawable(obj, tp)
        dr.setStyle(style, color)
        self.geoms[self.objNum] = dr
        self.objNum += 1;

    def obj(self, key):
        return  self.geoms[key]['geom']

    def setToGeoms(self, geomKeyPrefix, paramName, paramValue):
        for geomKey in self.geoms:
          if geomKey.startswith(geomKeyPrefix):
             self.geoms[geomKey][paramName] = paramValue

    def setStyle(self, geomKeyPrefix, styleName):
        self.setToGeoms(geomKeyPrefix, 'style', styleName)

    def setColor(self, geomKeyPrefix, RGBA100):
        self.setToGeoms(geomKeyPrefix, 'color', RGBA100)


    def render(self):

        slideName = self.val('SLIDE_NAME') + str(self.val('SLIDE_NUM')) + "_test"
        self.initVal('SysRenderTarget', 'screen')
        

        self.initVal('SysDecorIsDesk', True)
        self.initVal('SysDecorIsAxis', True)
        self.initVal('SysDecorScaleA', 1)
        self.initVal('SysDecorScaleB', 1)
        self.initVal('SysDecorDeskDX', 0)
        self.initVal('SysDecorDeskDY', 0)
        self.initVal('SysDecorDeskDZ', 0)
        SysDecors = self.getVals('SysDecor')

        self.initVal('SysPrecisionShape', 0.2)
        self.initVal('SysPrecisionWire', 0.2)
        SysPrecisions = self.getVals('SysPrecision')

        self.initVals('Style', self.getVals('TemplStyle'))

        StyleDesk = self.getVals('StyleDesk')
        StyleAxis = self.getVals('StyleAxis')

        scriptDir = os.path.dirname(__file__)
        stlRelDir = os.path.join(scriptDir, '..', 'models', slideName)
        stlDir = os.path.abspath(stlRelDir)
        webRelDir = os.path.join(scriptDir, '..','slides', slideName)
        webDir = os.path.abspath(webRelDir)

        #for key in self.params:
          #print(key,'=',self.params[key])
        SysRenderTarget = self.val('SysRenderTarget') 
        if SysRenderTarget == 'test':
          self.lib = TestLib(SysDecors, SysPrecisions, ebDir, stlDir)
        elif SysRenderTarget == 'screen':
          self.lib = ScreenLib(SysDecors, StyleDesk, StyleAxis)
        elif  SysRenderTarget == 'web':
            self.lib = WebLib(SysDecors, SysPrecisions, webDir)
        elif  SysRenderTarget == 'stl':
            self.lib = StlLib(SysDecors, SysPrecisions, stlDir)

        #for key in self.geoms:
            #print(key, self.geoms[key])

        for key in self.geoms:
            dr = self.geoms[key]
            #print(geomObj['style'])
            style = self.getVals('Style' + dr.style)
            #print(style)
            color = dr.color
            geom = dr.obj
            t = dr.tp
            
            print('===> Render','[',key,'] =', dr.style, dr.obj) #self.geoms[key]
            
            if dr.style == 'HIDE':
                pass  
            elif t == 'point':
                self.lib.drawPoint(dr.obj, style, color)
            elif t == 'line':
                pnt1,pnt2 = dr.obj;
                edge = BRepBuilderAPI_MakeEdge(pnt1, pnt2).Edge()
                self.lib.drawShape(edge, style, dr.color)
            elif t == 'circle':
                pnt1,pnt2,pnt3 = dr.obj;
                geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
                edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
                self.lib.drawShape(edge, style, dr.color)
            elif t == 'shape':
                self.lib.drawShape(dr.obj, style, dr.color)
            elif t == 'label':
                pntPlace, strTitle = dr.obj
                self.lib.drawLabel(pntPlace, strTitle, style, dr.color)

        self.lib.start()

    def drawPoint(self, style, pnt, text):
        self.initObj('point', style, pnt, self.color)
        self.initObj('label', style, (pnt, text), self.color)

    def drawLine(self, style, the2Points):
        self.initObj('line', style, the2Points, self.color)

    def drawCircle(self, style, the3Points):
        self.initObj('circle', style, the3Points, self.color)

    def drawSurface(self, style, surface):
        self.initObj('shape', style, surface, self.color)

    def drawWire(self, style, wire):
        self.initObj('shape', style, wire, self.color)

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
    
    def drawObj(self, objName, key, obj):
       if objName.endswith('Point') or objName.endswith('Points'):
           self.drawPoint(self.style, obj, key)
       elif objName.endswith('Wire') or objName.endswith('Wires'):
           self.drawWire(self.style, obj)
       elif objName.endswith('Surface') or objName.endswith('Surfaces'):
           self.drawSurface(self.style, obj)
       elif objName.endswith('Line') or objName.endswith('Lines'):
           self.drawLine(self.style, obj)
        
    def draw(self, objName, param1 = None, param2 = None):
       obj =  self.get(objName, param1, param2)
       if isinstance(obj, dict): 
           for key in obj:
             self.drawObj(objName, key, obj[key])
       else:    
           self.drawObj(objName, '' ,obj)
    
    def setStyle(self, style, color = None): 
        self.style = style
        self.color = color

if __name__ == '__main__':
    pass

