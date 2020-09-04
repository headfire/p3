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

import random

from OCC.Display.WebGl import threejs_renderer

from OCC.Extend.ShapeFactory import translate_shp, rotate_shp_3_axis

"""
n_toruses = 100

idx = 0
for i in range(n_toruses):
    torus_shp = BRepPrimAPI_MakeTorus(10 + random.random()*10, random.random()*10).Shape()
    # random position and orientation and color
    angle_x = random.random()*360
    angle_y = random.random()*360
    angle_z = random.random()*360
    rotated_torus = rotate_shp_3_axis(torus_shp, angle_x, angle_y, angle_z, 'deg')
    tr_x = random.uniform(-70, 50)
    tr_y = random.uniform(-70, 50)
    tr_z = random.uniform(-50, 50)
    trans_torus = translate_shp(rotated_torus, gp_Vec(tr_x, tr_y, tr_z))
    rnd_color = (random.random(), random.random(), random.random())
    my_ren.DisplayShape(trans_torus, export_edges=True, color=rnd_color, transparency=random.random())
    print("%i%%" % (idx * 100 / n_toruses), end="")
    idx += 1
"""


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
        self.mode = 'test'
   
    def _drawAxis(self):
        
        style = self.getNormalStyle('stServ')
        
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
 
    
    
    def init(self, initMode):
        if self.mode == 'test':
            if initMode == 'screen':
              self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display()
              self.mode = initMode   
            if initMode == 'web':
              self.web = threejs_renderer.ThreejsRenderer('D:\headfire\coding\webgl')
              self.mode = initMode   
    
    def start(self):
        if self.mode == 'test':
           print('Scene in test mode is OK')
        if self.mode == 'screen':
           self._drawAxis()
           self.display.FitAll()
           self.start_display()
        if self.mode == 'web':
           self.web.render()        
           
           
    def drawText(self, pnt, text, style, visible):
       style = self.getNormalStyle(style) 
       if visible == None:
           visible = 1       
       if self.mode == 'screen':
         if visible > 0.5:
             self.display.DisplayMessage(pnt, 
                text, 20, style.get('color',(1,1,1)), False)            
  
    """
    DisplayShape(self,
                     shape,
                     export_edges=False,
                     color=(0.65, 0.65, 0.7),
                     specular_color=(0.2, 0.2, 0.2),
                     shininess=0.9,
                     transparency=0.,
                     line_color=(0, 0., 0.),
                     line_width=1.,
                     mesh_quality=1.):
    """    
    def drawShape(self, shape, style, visible):
        style = self.getNormalStyle(style)
        if self.mode == 'screen':
            ais = AIS_Shape(shape)
            self.drawAis(ais, style, visible)
        if self.mode == 'web':
            self.web.DisplayShape(shape, 
                     False,
                     style['color'],
                     (0.2, 0.2, 0.2),
                     0.9,
                     0.,
                     (0, 0., 0.),
                     1.,
                     0.2)
    
  
    def drawAis(self, ais, style, visible):
        if self.mode == 'screen': 
                  
               #order important
               style = self.getNormalStyle(style)
               for styleName in style:
                  self.styleAis(ais, styleName, style[styleName])                
                  
               if visible == None:
                       visible = 1       
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
                 
    
    def getNormalStyle(self, styleVal):
        
        if isinstance(styleVal, dict):
           return styleVal
       
        if styleVal == None:
           styleVal = 'stMain' 
           
                   #      r%    g%     b%     op%     pnt  line   mat 
        if styleVal == 'stServ':
           styleVal = (   50,   50,   50,    100,      2,     1,  'PLASTIC'  )
        elif styleVal == 'stInfo':
           styleVal = (   50,   50,   50,     50,      3,     1,  'PLASTIC' )
        elif styleVal == 'stMain':
           styleVal = (   10,   10,   90,    100,      3,     4,  'PLASTIC' )
        elif styleVal == 'stFocus':
           styleVal = (   90,   10,   10,     30,      3,     2,  'CHROME' )
        elif styleVal == 'stGold':
           styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
        elif styleVal == 'stFog':
           styleVal = (   90,   90,   90,    30,      3,     4,   'PLASTIC'  )
           
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
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class Scene:
    def __init__(self, nativeLib):
        self.nativeLib = nativeLib
        return 
 
    def init(self, initMode = 'screen'):
       self.nativeLib.init(initMode) 
       
       
    def start(self):
        self.nativeLib.start()
    
    def style(self, styleVal = None):
        return self.nativeLib.getNormalStyle(styleVal)
       
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
         self.nativeLib.drawShape(shape, style, visible)
         
        
    
'''
***********************************************
 Procedural interface
***********************************************
'''

sc = Scene(NativeLib())
    
def ScInit(initMode = 'screen'):
    return sc.init(initMode)

def ScStyle(styleVal = None):
    return  sc.style(styleVal)

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
        
        ScPoint(gpPntEnd, 'stMain', 0)
        ScLabel(gpPntEnd, 'NotVisibleError!!!', 'stMain', 0)
    
    
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
        
  
    
    ScInit() 
    
    testPoint()
    testLine()
    testCircle()
    testShape()
    
    ScStart()
