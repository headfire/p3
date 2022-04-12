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
       dLabel = 10 * self.scale
       pntLabel = gp_Pnt(pnt.X()+dLabel,pnt.Y()+dLabel,pnt.Z()+dLabel)
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


    def _axis(self, style):

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

            self._drawTrihAis(trihAis, style)

            self._drawPoint(gp_Pnt(0,0,0), style)

            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                self._drawPoint(gp_Pnt(d,0,0), style)
                self._drawPoint(gp_Pnt(0,d,0), style)
                self._drawPoint(gp_Pnt(0,0,d), style)

    def drawAxis(self, style):
        self._axis(style)

    def _desk(self, style):
            originX, originY, originZ = self.originXYZ
            scale = self.scale
            xBox, yBox, zBox = 1500*scale, 1000*scale, 40*scale
            desk = BRepPrimAPI_MakeBox (gp_Pnt( -xBox/2-originX, -yBox/2-originY, -zBox-originZ), xBox, yBox, zBox)
            self._drawShape(desk.Solid(), style)
            scaleLabelPoint = gp_Pnt( -xBox/2-originX, -yBox/2-originY, zBox/3-originZ)
            self._drawLabel( scaleLabelPoint, 'A0 M' + self.scaleStr, style )
            
    def drawDesk(self, style):
          self._desk(style)     


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
        print (pnt)    
        self._drawPoint(pnt, style)


'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class Drawable:

    def __init__(self, obj, drawSetting):

        self.vals = dict()
        
        self.obj = obj
        self.style = drawSetting['style']
        self.color = drawSetting['color']
        self.labelText = drawSetting['labelText']
        self.labelColor = drawSetting['labelColor']
        self.labelSize = drawSetting['labelSize']

        self.initRGBASMT('StyleMAINPoint', 90,90,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('StyleMAINWire', 10,10,90,100, 8,'PLASTIC','SOLID')
        self.initRGBASMT('StyleMAINSurface',10,10,90,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('StyleMAINLabel', 90,10,10,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('StyleINFOPoint', 30,30,30,100,3,'PLASTIC','BALL')
        self.initRGBASMT('StyleINFOWire', 30,30,30,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('StyleINFOSurface', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('StyleINFOLabel', 30,30,30,100,20,'PLASTIC','SOLID')


        self.initRGBASMT('StyleFOCUSPoint', 90,10,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('StyleFOCUSWire', 90,10,10,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('StyleFOCUSSurface', 90,10,10,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('StyleFOCUSLabel', 90,90,90,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('StyleChromePoint', 10,10,10,100,4,'PLASTIC','EMPTY')
        self.initRGBASMT('StyleChromeWire', 10,10,10,100,3,'PLASTIC','DASH')
        self.initRGBASMT('StyleChromeSurface', 10,10,10,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('StyleChromeLabel', 10,10,10,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('StyleDeskPoint', 30,30,30,100,4,'PLASTIC','BALL')
        self.initRGBASMT('StyleDeskWire', 30,30,30,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('StyleDeskSurface', 30,30,30,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('StyleDeskLabel', 30,30,30,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('StyleAxisPoint', 30,30,30,100,2,'PLASTIC','BALL')
        self.initRGBASMT('StyleAxisWire', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('StyleAxisSurface', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('StyleAxisLabel', 30,30,30,100,20,'PLASTIC','SOLID')

        
    def setStyle(self, style, color = None):
        self.style = style
        self.color = color
        
    def getTrueStyle(self):
        return self.getVals('Style' + self.style)
        
    def setVals(self, keyPrefix ,vals):
        for key in vals:
           self.setVal(keyPrefix+key, vals[key])

    def getVals(self, keyPrefix):
        ret = dict()
        for key in self.vals:
            if key.startswith(keyPrefix):
               sStart,sPrefix, sEnd = key.partition(keyPrefix)
               ret[sEnd] = self.vals[key]
        return ret

    def initRGBASMT(self, paramKeyPrefix, r,g,b,a,s,m,t):
        self.setVal(paramKeyPrefix+'R',r)
        self.setVal(paramKeyPrefix+'G',g)
        self.setVal(paramKeyPrefix+'B',b)
        self.setVal(paramKeyPrefix+'A',a)
        self.setVal(paramKeyPrefix+'S',s)
        self.setVal(paramKeyPrefix+'M',m)
        self.setVal(paramKeyPrefix+'T',t)

    def initXYZ(self, paramKeyPrefix, x,y,z):
        self.setVal(paramKeyPrefix+'X',x)
        self.setVal(paramKeyPrefix+'Y',y)
        self.setVal(paramKeyPrefix+'Z',z)
        
    def setVal(self, valKey, val):
        self.vals[valKey] = val

    def getVal(self, valKey):
        return self.vals[valKey]
        

class Foo(Drawable):
    def render(self, lib):
        if self.labelText != None:
            lib.drawLabel(self.obj, self.labelText, self.getTrueStyle(), self.color)

class Point(Drawable):
    def render(self, lib):
        lib.drawPoint(self.obj, self.getTrueStyle(), self.color)
        if self.labelText != None:
            lib.drawLabel(self.obj, self.labelText, self.getTrueStyle(), self.color)
        
class Points(Drawable):
    def render(self, lib):
        for key in self.obj:
            lib.drawPoint(self.obj[key], self.getTrueStyle(), self.color)
            if self.labelText != None:
                lib.drawLabel(self.obj[key],self.labelText+str(key), self.getTrueStyle(), self.color)
        
class Wire(Drawable):
    def render(self, lib):
        lib.drawShape(self.obj, self.getTrueStyle(), self.color)

class Circle(Drawable):
    def render(self, lib):
        pnt1,pnt2,pnt3 = self.obj;
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        lib.drawShape(edge, self.getTrueStyle(), self.color)

class Line(Drawable):
    def render(self, lib):
          pnt1,pnt2 = self.obj;
          edge = BRepBuilderAPI_MakeEdge(pnt1, pnt2).Edge()
          lib.drawShape(edge, self.getTrueStyle(), self.color)

class Surface(Drawable):
    def render(self, lib):
        lib.drawShape(self.obj, self.getTrueStyle(), self.color)
            
class Desk(Drawable):
    def render(self, lib):
        lib.drawDesk(self.getTrueStyle())
            
class Axis(Drawable):
    def render(self, lib):
        lib.drawAxis(self.getTrueStyle())

class Scene:

    def __init__(self, forGetFunctions):

        self.drawables = []
        self.drawSetting = { 'style':'MAIN','color':None,'labelText':None,'labelColor':None,'labelSize':None }
        
        self.vals = dict()
        self.cache = dict()
        self.forGetFunctions =  forGetFunctions
        self.style = None
        self.color = None
        
        self.labelText = None
        self.labelColor = None
        self.labelSize = None

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

        self.setVal('RENDER_TARGET', 'screen')
        
        self.setVal('SCENE_SCALE', '1:1')
        self.setVal('SCENE_IS_DESK', True)
        self.setVal('SCENE_IS_AXIS', True)
        self.setVal('SCENE_ORIGIN', (0,0,0))

        self.setVal('SLIDE_NUM', 0)
        self.setVal('SLIDE_NAME', 'noname')

        self.setStyle('INFO')
        if self.getVal('SCENE_IS_DESK'):
            self.putToRender( Desk(None, self.drawSetting) )        
        if self.getVal('SCENE_IS_AXIS'):
            self.putToRender( Axis(None, self.drawSetting) )         


        lib = self.initRenderLib()
        
        for drawable in self.drawables:
            print('===> Render', drawable.__class__.__name__, drawable.style, drawable.obj) #self.geoms[key]
            drawable.render(lib)

        lib.start()

    def setStyle(self, style, color = None): 
        self.drawSetting['style'] = style
        self.drawSetting['color'] = color
        
    def label(self, labelText, labelColor = None, labelSize = None): 
        self.drawSetting['labelText'] = labelText
        self.drawSetting['labelColor'] = labelColor 
        self.drawSetting['labelSize'] = labelSize

    def draw(self, geomName, param1 = None, param2 = None):
    
        geom =  self.get(geomName, param1, param2)
        
        if geomName.endswith('Point'):
            drawable = Point(geom, self.drawSetting)
        elif geomName.endswith('Points'):
            drawable = Points(geom, self.drawSetting)
        elif geomName.endswith('Line'):
            drawable = Line(geom, self.drawSetting)
        elif geomName.endswith('Wire'):
            drawable = Wire(geom, self.drawSetting)
        elif geomName.endswith('Surface'):
            drawable = Surface(geom, self.drawSetting)
        else:    
            drawable = Foo(geom)
            
        self.putToRender(drawable)
        
        self.drawSetting['labelText'] = None
        self.drawSetting['labelColor'] = None
        self.drawSetting['labelSize'] = None

        
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
    
    

if __name__ == '__main__':
    pass

