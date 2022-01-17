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
    
    def __init__(self, decoration):
        self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display(
            None, (1024, 768), True, [128, 128, 128], [128, 128, 128]
          )
        isDesk, isAxis, scaleA, scaleB, deskDX, deskDY, deskDZ = decoration
        self.dLabel = 20 * scaleA/scaleB
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
                text, 20, style['color'], False)            
       
    def _drawPoint(self, pnt, style):
        ais = AIS_Point(Geom_CartesianPoint(pnt))
        self._drawAis(ais, style)
    
    def _drawShape(self, shape, style):
        ais = AIS_Shape(shape)
        self._drawAis(ais, style)
            
    def _drawAis(self, ais, style):
        for styleName in style:
           self._styleAis(ais, styleName, style[styleName])                
           
        self.display.Context.Display(ais, False) 
        #self.display.Context.Erase(ais, False)    
  
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
 
    def __init__(self):
       self.lib = TestLib()             
     
    def _getNormalStyle(self, styleVal):
        
        if isinstance(styleVal, dict):
           return styleVal
       
        if styleVal == None:
           styleVal = 'stMain' 
           
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
     
    def init(self, initMode, decoration, precision, exportDir):
       if initMode == 'screen':
          self.lib = ScreenLib(decoration)
       elif  initMode == 'web': 
         self.lib = WebLib(decoration, precision, exportDir)
       elif  initMode == 'stl': 
         self.lib = StlLib(decoration, precision, exportDir)
         
    def start(self):
        self.lib.start()
 
    def style(self, style):
        return self._getNormalStyle(style)
 
    def label(self, pnt, label, style):
        style = self._getNormalStyle(style)
        self.lib.drawLabel(pnt, label, style)
    
    def point(self, pnt, style):
        style = self._getNormalStyle(style)
        self.lib.drawPoint(pnt, style)
        
    def line(self, pnt1, pnt2, style):
        style = self._getNormalStyle(style)
        edge = BRepBuilderAPI_MakeEdge(pnt1, pnt2).Edge()
        self.lib.drawShape(edge, style)
    
    def circle(self, pnt1, pnt2, pnt3, style):
        style = self._getNormalStyle(style)
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self.lib.drawShape(edge, style)
    
    def shape(self, shape,  style):
        style = self._getNormalStyle(style)
        self.lib.drawShape(shape, style)
    
'''
***********************************************
 Procedural interface
***********************************************
'''

sc = Scene()
    
def ScInit(initMode = 'screen', decoration = (True,True, 1,1,0,0,0), precision=(1.,1.), exportDir = None):
    return sc.init(initMode, decoration, precision, exportDir)
 
def ScStyle(styleVal = None):
    return  sc.style(styleVal)

def ScPoint(pnt, style = None):
    return sc.point(pnt, style)

def ScLine(pnt1, pnt2, style = None):
    return sc.line(pnt1, pnt2, style)

def ScCircle(pnt1, pnt2, pnt3, style = None):
    return sc.circle(pnt1, pnt2, pnt3, style)

def ScShape(shape, style = None):
    return sc.shape(shape, style)

def ScLabel(pnt, text, style = None):
    return sc.label(pnt, text, style)

def ScStart():
    return sc.start()


if __name__ == '__main__':
    
     
    def  testPoint():
        
        pnt = gp_Pnt(3,4,5)
        ScPoint(pnt,'stInfo')
        ScLabel(pnt, 'point', 'stInfo')
    

    def testLine():
        
        gpPnt = gp_Pnt(2,3,4)
        
        ScPoint(gpPnt, 'stInfo')    
        ScLabel(gpPnt, 'pnt+', 'stInfo')
        
        gpPntStart = gp_Pnt(5,0,3)
        gpPntEnd = gp_Pnt(0,5,3)
        
        ScLine(gpPntStart, gpPntEnd, 'stMain')
        
        ScPoint(gpPntStart, 'stMain')
        ScLabel(gpPntStart, 'lineStart+', 'stMain')
        
        ScPoint(gpPntEnd, 'stMain')
        ScLabel(gpPntEnd, 'lineEnd', 'stMain')
    
    
    def  testCircle():
        
        gpPnt1 = gp_Pnt(1,1,10)
        gpPnt2 = gp_Pnt(5,2,5)
        gpPnt3 = gp_Pnt(5,-5,5)
        
        ScCircle(gpPnt1, gpPnt2, gpPnt3, 'stFocus')
        
        ScPoint(gpPnt1, 'stFog')
        ScLabel(gpPnt1,'p1', 'stFog')
        ScPoint(gpPnt2, 'stFog')
        ScLabel(gpPnt2,'p2','stFog')
        ScPoint(gpPnt3, 'stFog')
        ScLabel(gpPnt3,'p3', 'stFog')
  
    def  testShape():
        
        sp1 = BRepPrimAPI_MakeSphere(3).Shape()
        ScShape(sp1, 'stGold')
        
        sp2 = BRepPrimAPI_MakeSphere(4).Shape()
        ScShape(sp2, 'stFog')
        
        
        stCustom1   = ScStyle((  100,   35,   24,   100,   3,  3, 'GOLD'    ))
        sp3 = BRepPrimAPI_MakeSphere(gp_Pnt(3,6,2), 2.5).Shape()
        ScShape(sp3,  stCustom1)
        
        
        stCustom2   = ScStyle((  98,  100,  12,   100,   3,  3, 'CHROME'    ))
        sp4 = BRepPrimAPI_MakeSphere(gp_Pnt(3,3,3),2).Shape()
        ScShape(sp4, stCustom2)
        
  
    decoration = (True, True, 1, 50, 0, 0, -3)
    
    ScInit('screen', decoration) 
    
    testPoint()
    testLine()
    testCircle()
    testShape()
    
    ScStart()
