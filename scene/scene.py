"""
#  TEMPLATE START

from scene import (SceneIsObj, SceneGetObj, SceneApply, SceneRegObj,
SceneMakeColor, SceneLayer, SceneSetStyle, SceneGetStyle ,SceneLevelUp, SceneLevelDown,
SceneDebug, SceneStart, SceneEnd)

from scene import DrawAxis


def PaintMyObject(name, size)
    SceneLevelDown(name)
    SceneDrawPoint(gp_Pnt(1,1,1))
    SceneLevelUp()

if __name__ == '__main__':
    
    # may comment this line for debug
    SceneScreenInitDebug()
    
    
    DrawAxis('axis')
    
    PaintMyOnject('object', 10)
    
    SceneScreenStart()
  
#  TEMPLATE END
    
"""

"""
To do  

color object dump
SceneRegisterCreation
SceneRegisterAnimation
SceneRegisterMenu

"""

from OCC.Display.SimpleGui import init_display
    
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.Geom import Geom_Axis2Placement, Geom_CartesianPoint, Geom_Point
from OCC.Core.AIS import AIS_Point, AIS_InteractiveObject, AIS_Trihedron, AIS_Shape, AIS_Line, AIS_Circle
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Aspect import Aspect_TOM_BALL
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere


#from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
#                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)

from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.GC import  GC_MakeCircle
from copy import deepcopy

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

'''
def printShapeItems(shape):
    for TYPE in TOPO_TYPES:
        items = getShapeItems(shape, TOPO_TYPES.index(TYPE))  
        print(TYPE +':'+str(len(items)))   
'''


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

class NativeLib:
    def __init__(self):
        self.isInit = False
 
    def _drawAxis(self):
        
        style = self.style((0.5,0.5,0.5), 0, 1.5, 1)
        
        pnt = gp_Pnt(0,0,0)
        dir1 = gp_Dir(gp_Vec(0,0,1))
        dir2 = gp_Dir(gp_Vec(1,0,0))
        geomAxis = Geom_Axis2Placement(pnt, dir1, dir2)
        
        trih = AIS_Trihedron(geomAxis)
        trih.SetSize(11)
        
        self.drawAis(trih, style, 1)
        
        self.drawAis(AIS_Point(Geom_CartesianPoint(gp_Pnt(0,0,0))), style, 1)
        
        for i in range (1,10):
            self.drawAis(AIS_Point(Geom_CartesianPoint(gp_Pnt(i,0,0))), style, 1)
            self.drawAis(AIS_Point(Geom_CartesianPoint(gp_Pnt(0,i,0))), style, 1)
            self.drawAis(AIS_Point(Geom_CartesianPoint(gp_Pnt(0,0,i))), style, 1)
 
    
    def isScreenInit(self):
        return self.isInit
    
    def initScreen(self):
        if not self.isInit:
           self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display()
           self.isInit = True;   
           
    def startScreen(self):
        if self.isInit:
           self._drawAxis()
           self.display.FitAll()
           self.start_display()
           
    def drawText(self, pnt, text, style, visible):
       if style ==  None:
           style = self.style()
       if visible == None:
           visible = 1       
       if self.isInit:
         if visible > 0.5:
             self.display.DisplayMessage(pnt, 
                text, 20, style.get('color',(1,1,1)), False)            
        
    def drawAis(self, ais, style, visible):
         if style ==  None:
               style = self.style()
         if visible == None:
               visible = 1       
         if self.isInit: 
                  
               #order important
               for styleName in style:
                  self.styleAis(ais, styleName, style[styleName])                
                  
               if visible > 0.5:
                      self.display.Context.Display(ais, False) 
               else:    
                      self.display.Context.Erase(ais, False)    
               
    def styleAis(self, ais, styleName, styleValue):
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
  
    def style(self, color = None, tran = None ,
                  pointSize = None, lineWidth = None, material = None):
        st = dict() 
        st['color'] = n(color,(1,1,1))
        st['tran'] = n(tran, 0)
        st['pointType'] = 'BALL'                
        st['lineType'] = 'SOLID'                
        st['pointSize'] = n(pointSize,3)
        st['lineWidth'] = n(lineWidth,1)                
        st['material'] = n( material, 'DEFAULT')
        return st
  
              
     
'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class Scene:
    def __init__(self, nativeLib):
        self.nativeLib = nativeLib
        return 
 
    def init(self):
       self.nativeLib.initScreen() 
       
       
    def start(self):
       if self.nativeLib.isScreenInit() :
          self.nativeLib.startScreen()
       else:
          print('Virtual run is complete')    
          print('Use ScInit()')    
    
    def style(self, color, tran ,pointSize, lineWidth, material):
        return self.nativeLib.style(color, tran ,pointSize, lineWidth, material)
       
    def label(self, pnt, label, style, visible):
        pntLabel = gp_Pnt(pnt.X()+0.2, pnt.Y()+0.2, pnt.Z()+0.2)
        self.nativeLib.drawText(pntLabel, label, style, visible)
        
    
    def point(self, pnt, style, visible):
        geomPnt = Geom_CartesianPoint(pnt)
        ais= AIS_Point(geomPnt)
        self.nativeLib.drawAis(ais, style, visible)
        
    def line(self, pnt1, pnt2, style, visible):
        geomPnt1 = Geom_CartesianPoint(pnt1)
        geomPnt2 = Geom_CartesianPoint(pnt2)
        ais = AIS_Line(geomPnt1,geomPnt2)
        self.nativeLib.drawAis(ais, style, visible)
    
    def circle(self, pnt1, pnt2, pnt3, style, visible):
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        ais = AIS_Circle(geomCircle)
        self.nativeLib.drawAis(ais, style, visible)
    
    def shape(self, shape,  style, visible):
         ais = AIS_Shape(shape)
         self.nativeLib.drawAis(ais, style, visible)
         
        
    
'''
***********************************************
 Procedural interface
***********************************************
'''

sc = Scene(NativeLib())
    
def ScInit():
    return sc.init()

def ScStyle(color = None, tran = None, pointSize = None, lineWidth = None, material = None):
    return  sc.style(color, tran , pointSize, lineWidth, material)

def ScPoint(pnt, style = None, visible = 1):
    return sc.point(pnt, style, visible)

def ScLine(pnt1, pnt2, style = None, visible = 1):
    return sc.line(pnt1, pnt2, style, visible)

def ScCircle(pnt1, pnt2, pnt3, style = None, visible = 1):
    return sc.circle(pnt1, pnt2, pnt3, style, visible = 1)

def ScShape(shape, style = None, visible = 1):
    return sc.shape(shape, style, visible)

def ScLabel(pnt, text, style = None, visible = 1):
    return sc.label(pnt, text, style, visible)

def ScStart():
    return sc.start()

'''
Todo

ScFace
ScLineArray
ScArcArray
ScLineMark
ScAngleMark
ScSphere
ScCone
ScCyl
ScBox
ScTor

ScDo (virtual mashine command)
'''

'''

***********************************************
Testing
***********************************************
'''

if __name__ == '__main__':
    
    stInfo = ScStyle( (0.5,0.5,0.5), None,  None, None, None)
    stMain = ScStyle((0.1,0.1,0.9),  None,  None,    4,    None )
    stBase = ScStyle((0.9,0.1,0.1),  None,  None, None, None)
    stGold = ScStyle((0.9,0.9,0.1),  None,  None, 4 ,'GOLD')
    stFog = ScStyle((0.1,0.9,0.1),  0.7, None, None ,'GOLD')
     
    def  testPoint():
        
        pnt = gp_Pnt(3,4,5)
        ScPoint(pnt,stInfo)
        ScLabel(pnt, 'point', stInfo)
    

    def testLine():
        
        gpPnt = gp_Pnt(2,3,4)
        
        ScPoint(gpPnt, stInfo)    
        ScLabel(gpPnt, 'pnt+', stInfo)
        
        gpPntStart = gp_Pnt(5,0,3)
        gpPntEnd = gp_Pnt(0,5,3)
        
        ScLine(gpPntStart, gpPntEnd, stMain)
        
        ScPoint(gpPntStart, stMain)
        ScLabel(gpPntStart, 'lineStart+', stMain)
        
        ScPoint(gpPntEnd, stMain, 0)
        ScLabel(gpPntEnd, 'NotVisibleError!!!', stMain, 0)
    
    
    def  testCircle():
        
        gpPnt1 = gp_Pnt(1,1,10)
        gpPnt2 = gp_Pnt(5,2,5)
        gpPnt3 = gp_Pnt(5,-5,5)
        
        ScCircle(gpPnt1, gpPnt2, gpPnt3, stGold)
        
        ScPoint(gpPnt1, stFog)
        ScLabel(gpPnt1,'p1', stFog)
        ScPoint(gpPnt2, stFog)
        ScLabel(gpPnt2,'p2',stFog)
        ScPoint(gpPnt3, stFog)
        ScLabel(gpPnt3,'p3',stFog)
  
    def  testShape():
        sp1 = BRepPrimAPI_MakeSphere(3).Shape()
        ScShape(sp1, stGold)
        sp2 = BRepPrimAPI_MakeSphere(4).Shape()
        ScShape(sp2, stFog)
  
    
    ScInit() 
    
    testPoint()
    testLine()
    testCircle()
    testShape()
    
    ScStart()
