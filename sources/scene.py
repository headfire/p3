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

LINE_TYPES = ['SOLID', 'DASH', 'DOT', 'DOTDASH' ]

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
    
    def __init__(self, decors):
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
        self.dLabel = 50 * scaleA/scaleB
        self._decoration(isDesk, isAxis, scaleA, scaleB, deskDX, deskDY, deskDZ)

    def _axisStyle(self):
        
        st = dict()
        st['color'] = (40/100, 40/100, 40/100)
        st['tran']  = 0
        st['pointType'] = 'BALL'                
        st['lineType'] = 'SOLID'                
        st['pointSize'] = 2
        st['lineWidth'] = 1               
        st['material'] = 'PLASTIC'
        
        return st 
 
    def _deskStyle(self):
        
        st = dict()
        st['color'] = (70/100, 70/100, 70/100)
        st['tran']  = 0
        st['pointType'] = 'BALL'                
        st['lineType'] = 'SOLID'                
        st['pointSize'] = 2
        st['lineWidth'] = 1               
        st['material'] = 'PLASTIC'
        
        return st 
 

    def _styleAis(self, ais, styleName, styleValue):
        if styleName == 'color':
            r,g,b = styleValue 
            color =  Quantity_Color(r, g, b, Quantity_TOC_RGB)
            ais.SetColor(color)
            if isinstance(ais, AIS_Trihedron):  
                ais.SetArrowColor(color)
                ais.SetTextColor(color)
        elif styleName == 'tran':
                ais.SetTransparency(styleValue)
        elif styleName == 'material':
             aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(styleValue))
             ais.SetMaterial(aspect)
        elif styleName == 'lineType':         
             lineType = LINE_TYPES.index(styleValue)
             ais.Attributes().WireAspect().SetTypeOfLine(lineType)
             ais.Attributes().LineAspect().SetTypeOfLine(lineType)
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
                text, style['LabelS'], (style['LabelR'],style['LabelG'],style['LabelB']), False)            
       
    def _drawPoint(self, pnt, style):
        ais = AIS_Point(Geom_CartesianPoint(pnt))
        self._styleAis(ais, 'color', (style['PointR'],style['PointG'], style['PointB']))                
        self._styleAis(ais, 'tran', style['PointA'])                
        self._styleAis(ais, 'material', style['PointM'])                
        self._styleAis(ais, 'pointType', style['PointT'])                
        self._styleAis(ais, 'pointSize', style['PointS'])                
        self.display.Context.Display(ais, False) 
    
    def _drawShape(self, shape, style):
        ais = AIS_Shape(shape)
        self._styleAis(ais, 'color', (style['ShapeR'],style['ShapeG'], style['ShapeB']))                
        self._styleAis(ais, 'tran', style['ShapeA'])                
        self._styleAis(ais, 'material', style['ShapeM'])                
        self.display.Context.Display(ais, False) 
            
  
    def _axis(self, size):
        
            style = self._axisStyle()
          
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
            
            trih = AIS_Trihedron(geomAxis)
            trih.SetSize(size)
            
            self._drawAis(trih, style)
            
            self._drawPoint(gp_Pnt(0,0,0), style)
            
            cnt = int( size // step)
            for i in range (1, cnt):
                d = i* step
                self._drawPoint(gp_Pnt(d,0,0), style)
                self._drawPoint(gp_Pnt(0,d,0), style)
                self._drawPoint(gp_Pnt(0,0,d), style)
                
     
    def _desk(self, scaleA, scaleB, deskDX, deskDY, deskDZ): 
            style = self._deskStyle()
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
           
    def drawLabel(self, pnt, text, style):
        self._drawLabel(pnt, text, style)
            
    def drawShape(self, shape, style):
        self._drawShape(shape, style)
            
    def drawPoint(self, pnt, style):
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
        self.key = 0
        # todo get arguments and init params

    
    def setGeom(self, geomKey, geomType, geomObj, geomStyle):
        self.geoms[geomKey + str(self.key)] = (geomType, geomObj, geomStyle)
        self.key += 1

    def getGeom(self, geomKey):
        (geomType, geomObj, geomStyle) = geoms[geomKey]
        return geomObj

    def getParam(self, paramKey):
        return self.params[paramKey]

    def initParam(self, paramKey, paramValue):
        if not (paramKey in self.params):
            self.params[paramKey] = paramValue
        return self.params[paramKey]

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
        
    def getParams(self, keyPrefix):

        ret = dict()
           
        for key in self.params: 
            if key.startswith(keyPrefix): 
               sStart,sPrefix, sEnd = key.partition(keyPrefix)
               ret[sEnd] = self.params[key] 
               
        return ret       
           
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
        '''
        
        return st
     
         
    def render(self):

        SysRenderTarget = self.initParam('SysRenderTarget', 'screen')

        self.initParam('SysDecorIsDesk', True)
        self.initParam('SysDecorIsAxis', True)
        self.initParam('SysDecorScaleA', 1)
        self.initParam('SysDecorScaleB', 1)
        self.initXYZ('SysDecorDeskD', 0, 0, 0)
        SysDecors = self.getParams('SysDecor')

        self.initParam('SysPrecisionShape', 0.2)
        self.initParam('SysPrecisionWire', 0.2)
        SysPrecisions = self.getParams('SysPrecision')

        self.initRGBASMT('stInfoPoint', 30,30,30,100,3,'PLASTIC','BALL')
        self.initRGBASMT('stInfoWire', 30,30,30,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('stInfoShape', 30,30,30,100,1,'PLASTIC','SOLID')
        self.initRGBASMT('stInfoLabel', 30,30,30,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('stMainPoint', 90,90,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('stMainWire', 10,10,90,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('stMainShape', 70,10,70,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('stMainLabel', 90,10,10,100,20,'PLASTIC','SOLID')

        self.initRGBASMT('stFocusPoint', 90,10,10,100,4,'PLASTIC','BALL')
        self.initRGBASMT('stFocusWire', 90,10,10,100,3,'PLASTIC','SOLID')
        self.initRGBASMT('stFocusShape', 90,10,10,100,2,'PLASTIC','SOLID')
        self.initRGBASMT('stFocusLabel', 90,10,10,100,20,'PLASTIC','SOLID')

    
        fullSlideName = self.sceneName + '_' + self.getParam('SlideName') + '_test'
        scriptDir = os.path.dirname(__file__)
        stlRelDir = os.path.join(scriptDir, '..', 'models', fullSlideName)
        stlDir = os.path.abspath(stlRelDir)
        webRelDir = os.path.join(scriptDir, '..','slides', fullSlideName)
        webDir = os.path.abspath(webRelDir)
        
        if SysRenderTarget == 'test':    
          self.lib = TestLib(SysDecors, SysPrecisions, ebDir, stlDir)
        elif SysRenderTarget == 'screen':
          self.lib = ScreenLib(SysDecors)
        elif  SysRenderTarget == 'web': 
            self.lib = WebLib(SysDecors, SysPrecisions, webDir)
        elif  SysRenderTarget == 'stl': 
            self.lib = StlLib(SysDecors, SysPrecisions, stlDir)
    
        for objKey in self.objs:
            (objType, objGeometry, objStyle) = self.objs[objKey]
            style = self.getParams(objStyle)
            if objType == 'point':
                (pnt) = objGeometry;
                self.lib.drawPoint(pnt, style)
            elif objType == 'line':   
                (pnt1,pnt2) = objGeometry;
                edge = BRepBuilderAPI_MakeEdge(pnt1, pnt2).Edge()
                self.lib.drawShape(edge, style)
            elif objType == 'circle':
                (pnt1,pnt2,pnt3) = objGeometry;
                geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
                edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
                self.lib.drawShape(edge, style)
            elif objType == 'shape':
                shape = objGeometry
                self.lib.drawShape(shape, style)
            elif objType == 'label':
                (pntPlace, strTitle) = objGeometry
                self.lib.drawLabel(pntPlace, strTitle, style)
                
        self.lib.start()
 
    def label(self, pntPlace, strTitle, style):
        self.setGeom('label', 'label',(pntPlace, strTitle), style)
    
    def point(self, pnt, style):
        self.setGeom('point','point', (pnt), style)
        
    def line(self, pnt1, pnt2, style):
        self.setGeom('line','line', (pnt1, pnt2), style)
    
    def circle(self, pnt1, pnt2, pnt3, style):
        self.setGeom('circle','circle', (pnt1, pnt2, pnt3), style)
    
    def shape(self, shape,  style):
        self.setGeom('shape','shape', shape, style)
    
'''
***********************************************
 Procedural interface
***********************************************
'''

if __name__ == '__main__':
    
     
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
    sc.setParam('sysDecoration',(True, True, 1, 50, 0, 0, -3))
    
    testPoint(sc)
    testLine(sc)
    testCircle(sc)
    testShape(sc)
    
    sc.render()
