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


from threejs import ThreeJsRenderer, StlRenderer

import os

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
        self.dLabel = 20 * scaleA/scaleB
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

class Scene:
    
    def __init__(self, sceneName):
    
        self.sceneName = sceneName
        self.lib = None             
        self.geoms = dict()
        self.params = dict()
        
        # todo get arguments and init params

        self.initRGBASMT('TemplStyleInfoPoint', 30,30,30,100,3,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleInfoWire', 30,30,30,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleInfoSurface', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleInfoLabel', 30,30,30,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('TemplStyleMainPoint', 90,90,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleMainWire', 10,10,90,100, 8,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleMainSurface',10,10,90,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleMainLabel', 90,10,10,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('TemplStyleFocusPoint', 90,10,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('TemplStyleFocusWire', 90,10,10,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleFocusSurface', 90,10,10,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('TemplStyleFocusLabel', 90,10,10,100,20,'PLASTIC','SOLID')

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
    
    def setGeom(self, key, geomType, geomObj):
        self.geoms[key] = {'type':geomType, 'geom':geomObj, 'style':'Main', 'color':None }

    def getGeom(self, key):
        return  self.geoms[key][geom]

    def setStyle(self, key, style):
        self.geoms[key]['style'] = style

    def setColor(self, key, RGBA):
        self.geoms[key]['color'] = RGBA

    def getParam(self, paramKey):
        return self.params[paramKey]

    def initParam(self, paramKey, paramValue):
        if not (paramKey in self.params):
            self.params[paramKey] = paramValue
        return self.params[paramKey]

    def initParams(self, keyPrefix ,params):
        for key in params:
           self.initParam(keyPrefix+key, params[key])

    def getParams(self, keyPrefix):
        ret = dict()
        for key in self.params: 
            if key.startswith(keyPrefix): 
               sStart,sPrefix, sEnd = key.partition(keyPrefix)
               ret[sEnd] = self.params[key] 
        return ret       

    def initRGBASMT(self, paramKeyPrefix, r,g,b,a,s,m,t):
        self.initParam(paramKeyPrefix+'R',r)
        self.initParam(paramKeyPrefix+'G',g)
        self.initParam(paramKeyPrefix+'B',b)
        self.initParam(paramKeyPrefix+'A',a)
        self.initParam(paramKeyPrefix+'S',s)
        self.initParam(paramKeyPrefix+'M',m)
        self.initParam(paramKeyPrefix+'T',t)

    def initXYZ(self, paramKeyPrefix, x,y,z):
        self.initParam(paramKeyPrefix+'X',x)
        self.initParam(paramKeyPrefix+'Y',y)
        self.initParam(paramKeyPrefix+'Z',z)
        
           
     
         
    def render(self):

        SysRenderTarget = self.initParam('SysRenderTarget', 'screen')
        SysSlideNumLenght = self.initParam('SysSlideNumLenght', 5)

        self.initParam('SysDecorIsDesk', True)
        self.initParam('SysDecorIsAxis', True)
        self.initParam('SysDecorScaleA', 1)
        self.initParam('SysDecorScaleB', 1)
        self.initXYZ('SysDecorDeskD', 0, 0, 0)
        SysDecors = self.getParams('SysDecor')

        self.initParam('SysPrecisionShape', 0.2)
        self.initParam('SysPrecisionWire', 0.2)
        SysPrecisions = self.getParams('SysPrecision')

        self.initParams('Style', self.getParams('TemplStyle'))

        StyleDesk = self.getParams('StyleDesk')
        StyleAxis = self.getParams('StyleAxis')

        SysSlideNLenght = self.initParam('SysSlideNLenght', 2)
        SlideN = self.initParam('SlideN',0)
        SlideNStr = ('{:0'+str(SysSlideNLenght)+'}').format(SlideN)
        
        fullSlideName = self.sceneName + '_' + SlideNStr + '_test'
        scriptDir = os.path.dirname(__file__)
        stlRelDir = os.path.join(scriptDir, '..', 'models', fullSlideName)
        stlDir = os.path.abspath(stlRelDir)
        webRelDir = os.path.join(scriptDir, '..','slides', fullSlideName)
        webDir = os.path.abspath(webRelDir)
        
        #for key in self.params:
          #print(key,'=',self.params[key])
        
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
            geomObj = self.geoms[key]
            #print(geomObj['style'])
            style = self.getParams('Style'+geomObj['style'])
            #print(style)
            color = geomObj['color']
            geom = geomObj['geom']
            t = geomObj['type'] 
            if t == 'point':
                pnt = geom;
                self.lib.drawPoint(pnt, style, color)
            elif t == 'line':   
                pnt1,pnt2 = geom;
                edge = BRepBuilderAPI_MakeEdge(pnt1, pnt2).Edge()
                self.lib.drawShape(edge, style, color)
            elif t == 'circle':
                pnt1,pnt2,pnt3 = geom;
                geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
                edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
                self.lib.drawShape(edge, style, color)
            elif t == 'shape':
                shape = geom
                #print(style)
                self.lib.drawShape(shape, style, color)
            elif t == 'label':
                pntPlace, strTitle = geom
                self.lib.drawLabel(pntPlace, strTitle, style, color)
                
        self.lib.start()
 
    def label(self, key, pntPlace, strTitle):
        self.setGeom(key, 'label', (pntPlace, strTitle))

    def labels(self, key, pnts, label):
        index = 0
        for pnt in pnts:
           self.label(key+str(index+1), pnt, label+str(index+1))
           index += 1
    
    def drawPoint(self, key, pnt):
        self.setGeom(key, 'point', (pnt))

    def drawPoints(self, key, pnts):
        index = 0
        for pnt in pnts:
           self.point(key+str(index+1), pnt)
           index += 1
        
    def drawLine(self, key, pnt1, pnt2):
        self.setGeom(key,'line', (pnt1, pnt2))
    
    def drawCircle(self, key, pnt1, pnt2, pnt3):
        self.setGeom(key, 'circle', (pnt1, pnt2, pnt3))
    
    def drawSolid(self, key, shape):
        self.setGeom(key, 'shape', shape)

    def drawWire(self, key, shape):
        self.setGeom(key, 'shape', shape)
    
'''
***********************************************
 Procedural interface
***********************************************
'''

if __name__ == '__main__':
    
    def testParams(sc):
        sc.initParam('PrefixS01',1)
        sc.initParam('PrefixS02',2)
        Prefixes = sc.getParams('Prefix')
        print(Prefixes)
     
    def  testPoint(sc):
        
        pnt = gp_Pnt(3,4,5)
        sc.point(pnt,'stInfo')
        sc.label(pnt, 'point', 'stInfo')
    

    def testLine(sc):
        
        gpPnt = gp_Pnt(2,3,4)
        
        sc.point(gpPnt, 'stInfo')    
        sc.label(gpPnt, 'pnt+', 'stInfo')
        
        gpPntStart = gp_Pnt(5,0,3)
        gpPntEnd = gp_Pnt(0,5,3)
        
        sc.line(gpPntStart, gpPntEnd, 'stMain')
        
        sc.point(gpPntStart, 'stMain')
        sc.label(gpPntStart, 'lineStart+', 'stMain')
        
        sc.point(gpPntEnd, 'stMain')
        sc.label(gpPntEnd, 'lineEnd', 'stMain')
    
    def  testCircle(sc):
        
        gpPnt1 = gp_Pnt(1,1,10)
        gpPnt2 = gp_Pnt(5,2,5)
        gpPnt3 = gp_Pnt(5,-5,5)
        
        sc.circle(gpPnt1, gpPnt2, gpPnt3, 'stFocus')
        
        sc.point(gpPnt1, 'stFog')
        sc.label(gpPnt1,'p1', 'stFog')
        sc.point(gpPnt2, 'stFog')
        sc.label(gpPnt2,'p2','stFog')
        sc.point(gpPnt3, 'stFog')
        sc.label(gpPnt3,'p3', 'stFog')
  
    def  testShape(sc):
        
        sp1 = BRepPrimAPI_MakeSphere(3).Shape()
        sc.shape(sp1, 'stGold')
        
        sp2 = BRepPrimAPI_MakeSphere(4).Shape()
        sc.shape(sp2, 'stFog')
        
        
        stCustom1   = sc.style((  100,   35,   24,   100,   3,  3, 'GOLD'    ))
        sp3 = BRepPrimAPI_MakeSphere(gp_Pnt(3,6,2), 2.5).Shape()
        sc.shape(sp3,  stCustom1)
        
        
        stCustom2   = sc.style((  98,  100,  12,   100,   3,  3, 'CHROME'    ))
        sp4 = BRepPrimAPI_MakeSphere(gp_Pnt(3,3,3),2).Shape()
        sc.shape(sp4, stCustom2)
        
  
    sc = Scene('Test');
    sc.initParam('SysDecorScaleB',50)
    sc.initParam('SysDecorDeskDZ',-3)
    
    testParams(sc)

    #testPoint(sc)
    #testLine(sc)
    #testCircle(sc)
    #testShape(sc)
    
    #sc.render()
    
    '''   
               #      r%    g%     b%     op%     pnt  line   mat 
    if styleVal == 'stInfo':
       styleVal = (   30,   30,   30,    100,     3,     2,  'PLASTIC' )
    elif styleVal == 'stMain':
       styleVal = (   10,   10,   90,    100,      3,     4,  'PLASTIC' )
    elif styleVal == 'stFocus':
       styleVal = (   90,   10,   10,     30,      3,     2,  'CHROME' )
    elif styleVal == 'stGold':
       styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
    elif styleVal == 'stFog':
       styleVal = (   90,   90,   90,    30,       3,      4,   'PLASTIC'  )
       
    r, g, b, op, ps ,lw, mat = styleVal
    
    st = dict() 
    
    st['color'] = (r/100, g/100, b/100)
    st['tran']  = 1-op/100
    st['pointType'] = 'BALL'                
    st['lineType'] = 'SOLID'                
    st['pointSize'] = ps
    st['lineWidth'] = lw               
    st['material'] = mat
    
    return st
    '''
