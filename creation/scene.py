"""
#  TEMPLATE START

from scene import (SceneIsObj, SceneGetObj, SceneApply, SceneRegObj,
SceneMakeColor, SceneLayer, SceneSetStyle, SceneGetStyle ,SceneLevelUp, SceneLevelDown,
SceneDebug, SceneStart, SceneEnd)

from scene import DrawAxis


def PaintMyObject(name, size)
    SceneLevelDown(name)
    PaintPoint(1,1,1)
    SceneLevelUp()

if __name__ == '__main__':
    
    
    SceneDebug()
    SceneStart()
    
    DrawAxis('axis')
    
    PaintMyOnject('object', 10)
    
    SceneEnd()

#  TEMPLATE END
    
"""

"""
To do  

DrawMessage
DrawLabel
env level restore
color object dump
SceneRegisterCreation
SceneRegisterAnimation
SceneRegisterMenu

"""


from OCC.Display.SimpleGui import init_display
    
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.Geom import Geom_Axis2Placement, Geom_CartesianPoint, Geom_Point
from OCC.Core.AIS import AIS_Point, AIS_InteractiveObject, AIS_Trihedron, AIS_Shape, AIS_Line
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Aspect import Aspect_TOM_BALL, Aspect_TOM_STAR, Aspect_TOL_DASH, Aspect_TOL_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.Bnd import Bnd_Box

import json

SHAPE_TYPES = ['TopAbs_COMPOUND', 'TopAbs_COMPSOLID', 'TopAbs_SOLID', 'TopAbs_SHELL',
  'TopAbs_FACE', 'TopAbs_WIRE', 'TopAbs_EDGE', 'TopAbs_VERTEX', 'TopAbs_SHAPE']

 

def objToStr(obj) :
    ret = dict()
    ret['CLASS'] = str(obj.__class__.__name__)
    if isinstance(obj,gp_Pnt):
       ret['xyz'] = '(' + str(obj.X()) + ',' + str(obj.Y()) + ',' + str(obj.Z()) + ')'
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

def smartGetDict(d, mask):
    values = dict()
    for key in d:
         if key.startswith(mask):
              subkey = key[len(mask)+1:len(key)] 
              values[subkey] = d[key]
    return values 


class Scene :
    
    def __init__(self):
        
        self.debugType = 'noDebug'
        self.display = None
        self.display = None 
        self.start_display = None 
        self.add_menu  = None  
        self.add_function_to_menu = None
        
        self.root = dict()
        self.parentDirs = list()
        self.workDir = self.root
        
        self.parentEnvs = list()
        self.workEnv = dict()


    def setEnv(self, key, val):
        self.workEnv[key] = val 
    
    def isEnv(self, key):
        return key in self.workEnv
    
    def getEnv(self, key):
        if key in self.workEnv:
            return self.workEnv[key]
        return None 
 
    def getEnvs(self, mask):
        return smartGetDict(self.workEnv, mask)
             
    def isDirItem(self, key):
        return key in self.workDir
    
    def setDirItem(self, key, val):
        self.workDir[key] = val
    
    def getDirItem(self, key):
        if key in self.workDir:
           return self.workDir[key]
        return None
             
    def getDirItems(self, mask):
        return smartGetDict(self.workDir, mask)
        
    def dumpDir(self):
        dumpObj(self.workDir)
        
    def dumpEnv(self):
        dumpObj(self.workEnv)
        
    def getDir(self):
        return self.workDir
  
    def levelUp(self):
        self.workDir = self.parentDirs.pop() 
        
    def levelDown(self, dirName):
        parentDir = self.workDir
        if dirName in self.workDir:
           newWorkDir = self.workDir[dirName]
        else: 
           newWorkDir = dict()
           self.workDir[dirName] = newWorkDir
        self.parentDirs.append(self.workDir)
        self.workDir = newWorkDir

    def debug(self):
        self.debugType = 'cliDebug'
        
    def start(self): 
      if self.debugType != 'cliDebug':
         self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display()
     
    def end(self) :
      if self.debugType != 'cliDebug':
         self.display.FitAll()
         self.start_display()
      else:
         self.dumpEnv()           
         self.dumpDir()           

#############################
# Process object function   #
#############################
class SceneMessageObj:
    def __init__(self, gpPnt, text):
        self.textColor = (0,0,0)
        self.textHeight = 20
        self.position = gpPnt
        self.text = text
        self.visible = True
        self.struct = None        
       

def process(obj, propName, propValue, display):
       if obj == None:
            return
       if isinstance(obj, SceneMessageObj):
            if propName == 'visible':
               if propValue == True: 
                  if display != None:
                       obj.struct = display.DisplayMessage(obj.position, obj.text, obj.textHeight, 
                                        obj.textColor, False)            
                       obj.visible = True
            elif propName == 'textColor':
                obj.textColor = propValue
            elif propName == 'textHeight':
                obj.textHeight = propValue
             
       if isinstance(obj, AIS_InteractiveObject):  
             if propName == 'color':
                 r,g,b = propValue 
                 color =  Quantity_Color(r, g, b, Quantity_TOC_RGB)
                 obj.SetColor(color)
                 if isinstance(obj, AIS_Trihedron):  
                     obj.SetArrowColor(color)
                     obj.SetTextColor(color)
             elif propName == 'lineWidth':         
                 obj.Attributes().LineAspect().SetWidth(propValue)
                 obj.Attributes().WireAspect().SetWidth(propValue)
             elif propName == 'lineType':         
                  if propValue == 'solid':
                      obj.Attributes().WireAspect().SetTypeOfLine(Aspect_TOL_SOLID)
                      obj.Attributes().LineAspect().SetTypeOfLine(Aspect_TOL_SOLID)
                  elif propValue == 'dash':
                      obj.Attributes().WireAspect().SetTypeOfLine(Aspect_TOL_DASH)
                      obj.Attributes().LineAspect().SetTypeOfLine(Aspect_TOL_DASH)
             elif propName == 'visible':         
                 if display != None:
                    if isinstance(obj, AIS_InteractiveObject):
                       if propValue:
                           display.Context.Display(obj, False) 
                       else:    
                           display.Context.Erase(obj, False)    
       if isinstance(obj, AIS_Point): 
            if propName == 'pointType':
                if propValue == 'ball':
                   obj.SetMarker(Aspect_TOM_BALL)
                elif propValue == 'star':
                   obj.SetMarker(Aspect_TOM_STAR)
            elif propName == 'pointSize':         
                   obj.Attributes().PointAspect().SetScale(propValue)
  

#############################
# Function style interface  #
#############################

sc = Scene()    

def SceneSetObj(objName, obj):
    return sc.setDirItem('obj.' + objName, obj)

def SceneGetObj(objName):
    return sc.getDirItem('obj.' + objName)


# use None fo delete object
def SceneRegObj(objName, obj):
    SceneSetObj(objName, obj)

def SceneLayer(layerName):  
    sc.setEnv('currentLayer', layerName) 

def SceneSetStyle(styleName, styleValue):  
    currentLayer = sc.getEnv('currentLayer') 
    sc.setEnv('layers.'+ currentLayer +'.' + styleName, styleValue)

def SceneGetStyle(styleName):  
    currentLayer = sc.getEnv('currentLayer') 
    return sc.getEnv('layers.'+ currentLayer +'.' + styleName)

def SceneApplyStyle(objName, propName, propValue):
    obj = SceneGetObj(objName)
    process(obj, propName, propValue, sc.display)    
    
def SceneLevelUp():
    return sc.levelUp()
    
def SceneLevelDown(levelName):
    return sc.levelDown(levelName)

def SceneDebug():
    return sc.debug()
    
def SceneStart(): 

    SceneLayer('hide')
    SceneSetStyle('visible', False)                
    SceneSetStyle('color', (0, 0, 1))             
    SceneSetStyle('transparency', 0 )             
    SceneSetStyle('lineType', 'solid')             
    SceneSetStyle('lineWidth', 3)             
    SceneSetStyle('pointType', 'ball')             
    SceneSetStyle('pointSize', 3 )             
    SceneSetStyle('textColor', (55/255, 74/255, 148/255))             
    SceneSetStyle('textHeight', 20)             
    
    SceneLayer('info')
    SceneSetStyle('visible', True)                
    SceneSetStyle('color', (0.5, 0.5, 0.5))             
    SceneSetStyle('transparency', 0 )             
    SceneSetStyle('lineType', 'dash')             
    SceneSetStyle('lineWidth', 1)             
    SceneSetStyle('pointType', 'ball')             
    SceneSetStyle('pointSize', 3 )             
    SceneSetStyle('textColor', (0.5, 0.5, 0.5))             
    SceneSetStyle('textHeight', 20)             
  
    SceneLayer('base')
    SceneSetStyle('visible', True)                
    SceneSetStyle('color', (1, 0, 0))             
    SceneSetStyle('transparency', 0 )             
    SceneSetStyle('lineType', 'dash')             
    SceneSetStyle('lineWidth', 2)             
    SceneSetStyle('pointType', 'ball')             
    SceneSetStyle('pointSize', 3 )             
    SceneSetStyle('textColor', (189/255, 60/255, 45/255))             
    SceneSetStyle('textHeight', 20)             
    
    SceneLayer('main')
    SceneSetStyle('visible', True)                
    SceneSetStyle('color', (0, 0, 1))             
    SceneSetStyle('transparency', 0 )             
    SceneSetStyle('lineType', 'solid')             
    SceneSetStyle('lineWidth', 3)             
    SceneSetStyle('pointType', 'ball')             
    SceneSetStyle('pointSize', 3 )             
    SceneSetStyle('textColor', (55/255, 74/255, 148/255))             
    SceneSetStyle('textHeight', 20)             
    
    #last layer 'main' for begining paint
    
    return sc.start()

def SceneDrawAis(name, aisObj):
    #order important
    SceneRegObj(name, aisObj)
    SceneApplyStyle(name, 'color', SceneGetStyle('color'))                
    SceneApplyStyle(name, 'transparency', SceneGetStyle('transparency'))                
    SceneApplyStyle(name, 'lineType', SceneGetStyle('lineType'))                
    SceneApplyStyle(name, 'lineWidth', SceneGetStyle('lineWidth'))                
    SceneApplyStyle(name, 'pointType', SceneGetStyle('pointType'))                
    SceneApplyStyle(name, 'pointSize', SceneGetStyle('pointSize'))                
    SceneApplyStyle(name, 'visible', SceneGetStyle('visible'))                


def SceneDrawMessage(name, gpPnt, text):
    mObj = SceneMessageObj(gpPnt, text)
    SceneRegObj(name, mObj)
    SceneApplyStyle(name, 'textColor', SceneGetStyle('textColor'))                
    SceneApplyStyle(name, 'textHeight', SceneGetStyle('textHeight'))                
    SceneApplyStyle(name, 'visible', SceneGetStyle('visible'))                

    
def SceneDrawLabel(aisObjName, text = None):
    if text == None:
         text = aisObjName
    aisObj = SceneGetObj(aisObjName)
    if isinstance(aisObj, AIS_Point):
        pnt = aisObj.Component().Pnt()
        x = pnt.X()
        y = pnt.Y()
        z = pnt.Z()
    else:
        box = Bnd_Box()
        aisObj.BoundingBox(box)
        xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
        x = (xmax+xmin)/2
        y = (ymax+ymin)/2
        z = (zmax+zmin)/2
    x += 0.2    
    y += 0.2    
    z += 0.2    
    SceneDrawMessage(aisObjName + '_label', gp_Pnt(x,y,z), text)

    
def SceneEnd() :
    return sc.end()
  
  
def SceneDrawAxis(name):
    
    def drawPoint(name, xyz, pointType):
        x,y,z = xyz 
        gpPnt = gp_Pnt(x, y, z)
        geomPnt = Geom_CartesianPoint(gpPnt)
        SceneDrawAis(name, AIS_Point(geomPnt))
        SceneApplyStyle(name, 'pointType', pointType)
        SceneApplyStyle(name, 'pointSize', 2)
        
    SceneLevelDown(name)

    SceneLayer('info')    
    
    gp_pnt = gp_Pnt(0,0,0)
    gp_dir_1 = gp_Dir(gp_Vec(0,0,1))
    gp_dir_2 = gp_Dir(gp_Vec(1,0,0))
    geom_axis = Geom_Axis2Placement(gp_pnt, gp_dir_1, gp_dir_2)
    
    trih = AIS_Trihedron(geom_axis)
    trih.SetSize(11)
    
    SceneDrawAis('trihedron', trih)
    
    drawPoint('center', (0,0,0), 'ball')
    
    for i in range (1,10):
        drawPoint('x'+ str(i), (i,0,0), 'star')
        drawPoint('y'+ str(i), (0,i,0), 'star')
        drawPoint('z'+ str(i), (0,0,i), 'star')
          
    SceneLevelUp()


if __name__ == '__main__':
    
    from OCC.Core.AIS import AIS_Line
    
    #SceneDebug()
    SceneStart() 
    
    SceneDrawAxis('axis')
    
    SceneLayer('info')

    gpPnt = gp_Pnt(2, 3, 4)
    geomPnt = Geom_CartesianPoint(gpPnt)
    aisPoint =  AIS_Point(geomPnt)
    
    SceneDrawAis('pnt', aisPoint)
    SceneDrawLabel('pnt', 'pnt+')
    
    SceneLayer('main')
    gpPnt1 = gp_Pnt(1, 1, 1)
    gpPnt2 = gp_Pnt(4, 4, 7)    
    geomPnt1 = Geom_CartesianPoint(gpPnt1)
    geomPnt2 = Geom_CartesianPoint(gpPnt2)
    aisLineStart = AIS_Point(geomPnt1)
    aisLineEnd = AIS_Point(geomPnt2)
    aisLine = AIS_Line(geomPnt1,geomPnt2)
    SceneDrawAis('line', aisLine)
    SceneDrawLabel('line')
    
    SceneLayer('base')

    SceneDrawMessage('mess', gp_Pnt(5,5,5), 'hello', )
    
    SceneDrawAis('lineStart', aisLineStart)
    SceneDrawLabel('lineStart')
    
    SceneLayer('hide')
    SceneDrawAis('lineEnd', aisLineEnd)
    SceneDrawLabel('lineEnd')
    
    
    SceneEnd()
