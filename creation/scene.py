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
from OCC.Core.AIS import AIS_Point, AIS_InteractiveObject, AIS_Trihedron, AIS_Shape, AIS_Line, AIS_Circle
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Aspect import Aspect_TOM_BALL, Aspect_TOL_DASH, Aspect_TOL_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.GC import  GC_MakeCircle

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


'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''


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
        if self.parentDirs:
            self.workDir = self.parentDirs.pop()
        else :
            raise Exception('Try up from root level')
        if self.parentEnvs:
            self.workEnv = self.parentEnvs.pop()
        else: 
            raise Exception('Try up from root level')
        
    def levelDown(self, dirName):
        #process child objects
        if dirName in self.workDir:
           newWorkDir = self.workDir[dirName]
        else: 
           newWorkDir = dict()
           self.workDir[dirName] = newWorkDir
        self.parentDirs.append(self.workDir)
        self.workDir = newWorkDir
        
        #process styles
        newEnv = dict(self.workEnv)
        self.parentEnvs.append(self.workEnv)
        self.workEnv = newEnv

    def debug(self):
        self.debugType = 'cliDebug'
        

'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class NativeTextStub:
    def __init__(self, gpPnt, text):
        self.textColor = (0,0,0)
        self.textHeight = 20
        self.position = gpPnt
        self.text = text
        self.struct = None        
        self.visible = True

class NativeLib:
    
    def __init__(self, gpPnt, text):
        self.isInit = False
        
    def isScreenInit(self):
        return self.isInit
    
    def initScreen(self):
        if not self.initFlag:
           self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display()
           self.isInit = True;   
           
    def startScreen(self):
        if self.isInit:
           self.display.FitAll()
           self.start_display()
           
    def activateNativeObj(self, nativeObj):
        return   
    def deactivateNativeObj(self, nativeObj):
        self.stylingNativeObj(self, nativeObj, 'visible', False)
           
    def stylingNativeObj(self, nativeObj, styleName, styleValue):
       #Todo must begin
       obj = nativeObj 
       propName = styleName
       propValue = styleValue
       #Todo must end
       if obj == None:
            return
       if isinstance(obj, NativeTextStub):
            if propName == 'visible':
               if propValue == True: 
                  if self.isInit:
                       obj.struct = self.display.DisplayMessage(obj.position, obj.text, obj.textHeight, 
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
                 if self.isInit != None:
                    if isinstance(obj, AIS_InteractiveObject):
                       if propValue:
                           self.display.Context.Display(obj, False) 
                       else:    
                           self.display.Context.Erase(obj, False)    
       if isinstance(obj, AIS_Point): 
            if propName == 'pointSize':         
                   obj.Attributes().PointAspect().SetScale(propValue)
    
    def transformNativeObj(self, nativeObj, nativeTranformation):
        pass
    
    def transformXYZ(self, xyz, nativeTranformation):
        pass
    
    def dumpNativeObj(self, nativeObj):
        return nativeObj.__class__.__name__         

    def detectCenter(self, nativeObj):
        if not nativeObj:  #pass non exist obj name 
            return (0,0,0)
        x,y,z = 0,0,0
        if isinstance(nativeObj, AIS_Point):
            pnt = nativeObj.Component().Pnt()
            x = pnt.X()
            y = pnt.Y()
            z = pnt.Z()
        elif  self.isInit:
            box = Bnd_Box()
            nativeObj.BoundingBox(box)
            xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
            x = (xmax+xmin)/2
            y = (ymax+ymin)/2
            z = (zmax+zmin)/2
        return (x,y,z)   
        
     
'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class SceneObject:
    def __init__(self, parentSceneObject, objType):
        self.type = objType
        self.native = None
        self.childs = dict()
        if parentSceneObject:
           self.parent = parentSceneObject 
           self.styles = dict()
           self.currentLayerName = parentSceneObject.currentLayerName 
        else:   
           #root object creation
           self.parent = None
           self.setStylesToDefault()
        self.handles = dict()  # center and label must init
        
    def getChild(self, objName):
        if objName in self.childs:
            return self.childs[objName]
        else:
            return None
    def setChild(self, objName, sceneObj):
        oldObj = self.getChild(objName)
        if oldObj:
            oldObj.deactivate()
        self.childs[objName] = sceneObj
        sceneObj.activate()
        
    def applyStyle(self, styleName, styleValue):
        lib.stylingNativeObj(self.native, styleName, styleValue)    
        
    def applyTransform(self, nativeTransform) :
        lib.transformNativeObj(self.native, nativeTransform)        
        
    def activate(self):
        lib.activateNativeObj(self.native, self.isVisible)
        
    def deactivate(self):    
        lib.deactivateNativeObj(self.native)
        for key in self.childs:
           self.childs[key].deactivate()
        
    def setCurrentLayer(self, layerName) :
        self.currentLayerName = layerName
        
    def getStyle(self, styleName):  
       key = self.currentLayerName +'.' + styleName
       if key in  currObj.styles:
          return self.styles[key]
      
    def setStyle(self, styleName, styleValue):  
       key = self.curLayerName +'.' + styleName
       self.styles[key] = styleValue
       
    def setStylesToDefault(self):     
        self.styles = dict()
    
        self.setCurrentLayer('hide')
        self.setStyle('visible', False)                
        self.setStyle('color', (0, 0, 1))             
        self.setStyle('transparency', 0 )             
        self.setStyle('lineType', 'solid')             
        self.setStyle('lineWidth', 3)             
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (55/255, 74/255, 148/255))             
        self.setStyle('textHeight', 20)             
        
        self.setCurrentLayer('info')
        self.setStyle('visible', True)                
        self.setStyle('color', (0.5, 0.5, 0.5))             
        self.setStyle('transparency', 0 )             
        self.setStyle('lineType', 'dash')             
        self.setStyle('lineWidth', 1)             
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (0.5, 0.5, 0.5))             
        self.setStyle('textHeight', 20)             
          
        self.setCurrentLayer('base')
        self.setStyle('visible', True)                
        self.setStyle('color', (1, 0, 0))             
        self.setStyle('transparency', 0 )             
        self.setStyle('lineType', 'dash')             
        self.setStyle('lineWidth', 2)             
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (189/255, 60/255, 45/255))             
        self.setStyle('textHeight', 20)             
        
        self.setCurrentLayer('main')
        self.setStyle('visible', True)                
        self.setStyle('color', (0, 0, 1))             
        self.setStyle('transparency', 0 )             
        self.setStyle('lineType', 'solid')             
        self.setStyle('lineWidth', 3)             
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (55/255, 74/255, 148/255))             
        self.setStyle('textHeight', 20)             
    
        #last layer 'main' for begining paint
        
    def detectCenter(self):
        lib.detectCenter(self.native)

'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

lib = NativeLib()
rootObj = SceneObject(None,'level')
currObj = rootObj


def _sceneDrawAis(name, aisObj, drawType):
    #order important
    obj = SceneObject(currObj, drawType)
    obj.native = aisObj 
    _SceneSetObj(name, obj)
    SceneApplyStyle(name, 'color', SceneGetStyle('color'))                
    SceneApplyStyle(name, 'transparency', SceneGetStyle('transparency'))                
    SceneApplyStyle(name, 'lineType', SceneGetStyle('lineType'))                
    SceneApplyStyle(name, 'lineWidth', SceneGetStyle('lineWidth'))                
    SceneApplyStyle(name, 'pointType', SceneGetStyle('pointType'))                
    if isinstance(aisObj, AIS_Point):
         aisObj.SetMarker(Aspect_TOM_BALL)
    SceneApplyStyle(name, 'pointSize', SceneGetStyle('pointSize'))                
    SceneApplyStyle(name, 'visible', SceneGetStyle('visible'))                


def _SceneSetObj(objName, obj):
    currObj.setChild(objName, obj)

def _SceneGetObj(objName):
    return currObj.getChild(objName)


def SceneScreenInit():
   lib.initScreen() 
   
def SceneScreenClear():
   global currObj
   global rootObj
   rootObj = SceneObject(None,'level')
   currObj = rootObj()
   lib.clearScreen()
   
def SceneScreenStart():
   if lib.isScreenInit() :
     lib.startScreen()
   else:
     dumpObj(rootObj)   

def SceneGetNative(objName, obj):
    obj = _SceneGetObj(objName)
    if obj:
       return obj.native
    else:
       return None

def SceneLayer(layerName):  
    currObj.setCurrentLayer(layerName)
 
def SceneSetStyle(styleName, styleValue):  
    currObj.setStyle(styleName, styleValue)

def SceneGetStyle(styleName):  
    currObj.setStyle(styleName)
  
def SceneApplyStyle(objName, styleName, styleValue):
    obj = _SceneGetObj(objName)
    if obj:
        obj.applyStyle(styleName, styleValue)
    
def SceneLevelUp():
    global currObj
    if currObj.parent:
       currObj = currObj.parent
    else:
      raise 'Try level up from root level'    
    
def SceneLevelDown(childName):
    global currObj
    childObj = currObj.getChild(childName)
    if not childObj:
      childObj = SceneObject(currObj, 'level')
    else:
      childObj.styles = dict(currObj)
      childObj.currrentLayerName = currObj.currrentLayerName
    currObj = childObj  



def SceneDrawText(name, gpPnt, text):
    native = NativeTextStub(gpPnt, text)
    obj = SceneObject(currObj, 'text')
    obj.native = native
    _SceneSetObj(name, obj)
    SceneApplyStyle(name, 'textColor', SceneGetStyle('textColor'))                
    SceneApplyStyle(name, 'textHeight', SceneGetStyle('textHeight'))                
    SceneApplyStyle(name, 'visible', SceneGetStyle('visible'))                

def SceneDrawLabel(labeledObjName, text = None):
    if text == None:
         text = labeledObjName
    labeledObj = _SceneGetObj(labeledObjName)     
    if labeledObj :
        x,y,z = labeledObj.detectCenter()     
        SceneDrawText(labeledObjName + '_label', gp_Pnt(x+0.2, y+0.2, z+0.2), text)
  
def SceneDrawTrihedron(objName, size):
    gpPnt = gp_Pnt(0,0,0)
    gpDir1 = gp_Dir(gp_Vec(0,0,1))
    gpDir2 = gp_Dir(gp_Vec(1,0,0))
    geomAxis = Geom_Axis2Placement(gpPnt, gpDir1, gpDir2)
    
    trih = AIS_Trihedron(geomAxis)
    trih.SetSize(11)
    
    _sceneDrawAis(objName, trih)
  
def SceneDrawAxis(name):
    
    def drawPoint(name, xyz, pointSize):
        SceneDrawPoint(name, xyz)
        SceneApplyStyle(name, 'pointSize', pointSize)
        
    SceneLevelDown(name)

    SceneLayer('info')    
    SceneDrawTrihedron('trihedron',11)
    
    drawPoint('center', (0,0,0), 2.5)
    
    for i in range (1,10):
        drawPoint('x'+ str(i), (i,0,0), 1.5)
        drawPoint('y'+ str(i), (0,i,0), 1.5)
        drawPoint('z'+ str(i), (0,0,i), 1.5)
          
    SceneLevelUp()

def SceneDrawPoint(objName, xyz):
    x,y,z = xyz
    gpPnt = gp_Pnt(x,y,z)
    geomPnt = Geom_CartesianPoint(gpPnt)
    aisPnt = AIS_Point(geomPnt)
    _sceneDrawAis(objName, aisPnt)

def SceneDrawLine(objName, xyzStart, xyzEnd):
    x1,y1,z1 = xyzStart
    gpPnt1 = gp_Pnt(x1,y1,z1)
    geomPnt1 = Geom_CartesianPoint(gpPnt1)

    x2,y2,z2 = xyzEnd
    gpPnt2 = gp_Pnt(x2,y2,z2)
    geomPnt2 = Geom_CartesianPoint(gpPnt2)
    
    aisLine = AIS_Line(geomPnt1,geomPnt2)
    _sceneDrawAis(objName, aisLine)
    

def SceneDrawCircle3(objName, xyz1, xyz2, xyz3):
    
    x1, y1, z1 = xyz1
    x2, y2, z2 = xyz2
    x3, y3, z3 = xyz3
    
    gpPnt1 = gp_Pnt(x1, y1, z1)
    gpPnt2 = gp_Pnt(x2, y2, z2)
    gpPnt3 = gp_Pnt(x3, y3, z3)
    
    geomCircle = GC_MakeCircle(gpPnt1, gpPnt2, gpPnt3).Value()
    aisCircle = AIS_Circle(geomCircle)
    
    _sceneDrawAis('circle', aisCircle)
 
def SceneDrawCircle(objName, r):
    pass
'''
    gpPnt1 = gp_Pnt(x1, y1, z1)
    gpPnt2 = gp_Pnt(x2, y2, z2)
    gpPnt3 = gp_Pnt(x3, y3, z3)
    geomPnt1 = Geom_CartesianPoint(gpPnt1)
    geomPnt2 = Geom_CartesianPoint(gpPnt2)
    geomPnt3 = Geom_CartesianPoint(gpPnt3)
    geomCircle = GC_MakeCircle(gpPnt1, gpPnt2, gpPnt3).Value()
    aisCircle = 
    SceneDrawAis('circle', AIS_Circle(geom_circle))
    _sceneDrawAis(objName, aisLine)
 '''   



if __name__ == '__main__':
    
        
    def  testPoint(name):
        
        SceneLevelDown(name)
        
        SceneLayer('main')
        SceneDrawPoint('point', (3,4,5))
        SceneDrawLabel('point')
        
        SceneLevelUp()
    

    def testLine(name):
        
        SceneLevelDown(name)
        
        xyzPnt = (2,3,4)
        
        SceneLayer('info')
        SceneDrawPoint('pnt', xyzPnt)    
        SceneDrawLabel('pnt', 'pnt+')
        
        xyzStart = (5,0,3)
        xyzEnd = (0,5,3)
        
        SceneLayer('main')
        SceneDrawLine('line', xyzStart, xyzEnd)
        SceneDrawLabel('line')
        
        SceneLayer('base')
        SceneDrawPoint('lineStart', xyzStart)
        SceneDrawLabel('lineStart', 'lineStart+')
        
     
        SceneLayer('hide')
        SceneDrawPoint('lineEnd', xyzEnd)
        SceneDrawLabel('lineEnd')
    
        SceneLevelUp()
    
    def  testCircle3(name):
        
        SceneLevelDown(name)
        
        xyz1 = (1,1,10)
        xyz2 = (5,2,5)
        xyz3 = (5,-5,5)
        
        SceneLayer('main')
        SceneDrawCircle3('circle', xyz1, xyz2, xyz3)
        SceneDrawLabel('circle')
        
        SceneLayer('base')
        SceneDrawPoint('p1', xyz1)
        SceneDrawLabel('p1')
        SceneDrawPoint('p2', xyz2)
        SceneDrawLabel('p2')
        SceneDrawPoint('p2', xyz3)
        SceneDrawLabel('p3')
       
        SceneLevelUp()
        
    def testMessage(name):
        
        SceneLevelDown(name)
        
        SceneLayer('main')
        SceneDrawText('meesage', gp_Pnt(5,5,5), 'Hello OpenCascade!')
        
        SceneLevelUp()

    SceneScreenInit() 
    
    SceneDrawAxis('axis')
    
    testMessage('mess')
    testLine('point')
    testLine('line')
    testCircle3('circle3')
    
    SceneScreenStart()
