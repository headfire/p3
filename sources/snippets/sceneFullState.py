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
    if isinstance(obj, SceneObject):
      ret['childs'] = obj.childs
    elif isinstance(obj,gp_Pnt):
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


'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''

class NativeStubText:
    def __init__(self, gpPnt, text):
        self.textColor = (0,0,0)
        self.textHeight = 20
        self.position = gpPnt
        self.text = text
        self.struct = None        
        self.visible = 1

class NativeLib:
    def __init__(self):
        self.isInit = False
        
    def isScreenInit(self):
        return self.isInit
    
    def initScreen(self):
        if not self.isInit:
           self.display, self.start_display, self.add_menu,  self.add_function_to_menu  = init_display()
           self.isInit = True;   
           
    def startScreen(self):
        if self.isInit:
           self.display.FitAll()
           self.start_display()
           
    def activateNativeObj(self, nativeObj, styles):
        
        #order important
    
        self.stylingNativeObj(nativeObj, 'color', styles.get('color',(1,1,1)) )                
        self.stylingNativeObj(nativeObj, 'material', styles.get('material', 'DEFAULT'))                
        self.stylingNativeObj(nativeObj, 'transparency', styles.get('transparency', 0))                
        self.stylingNativeObj(nativeObj, 'lineWidth',styles.get('lineWidth', 1))                
        self.stylingNativeObj(nativeObj, 'lineType', styles.get('lineType', 'SOLID'))                
        
        self.stylingNativeObj(nativeObj, 'textColor', styles.get('textColor', (1,1,1)))                
        self.stylingNativeObj(nativeObj, 'textHeight', styles.get('textHeight', 20))                
     
        self.stylingNativeObj(nativeObj, 'pointType', styles.get('pointType', 'BALL'))                
        self.stylingNativeObj(nativeObj, 'pointSize', styles.get('pointSize', 3))                
        
        self.stylingNativeObj(nativeObj, 'visible', styles.get('visible', 1))                
    
    def deactivateNativeObj(self, nativeObj):
        self.stylingNativeObj(nativeObj, 'visible', 0)
           
    def stylingNativeObj(self, obj, styleName, styleValue):
       if obj == None:
            return
       if isinstance(obj, NativeStubText):
            if styleName == 'visible':
               if styleValue > 0.5: 
                  if self.isInit:
                    obj.struct = self.display.DisplayMessage(obj.position, 
                         obj.text, obj.textHeight, obj.textColor, False)            
                    obj.visible = 1
            elif styleName == 'textColor':
                obj.textColor = styleValue
            elif styleName == 'textHeight':
                obj.textHeight = styleValue
       if isinstance(obj, AIS_InteractiveObject):  
             if styleName == 'color':
                 r,g,b = styleValue 
                 color =  Quantity_Color(r, g, b, Quantity_TOC_RGB)
                 obj.SetColor(color)
                 if isinstance(obj, AIS_Trihedron):  
                     obj.SetArrowColor(color)
                     obj.SetTextColor(color)
             elif styleName == 'transparensy':
                     obj.SetTransparency(styleValue)
             elif styleName == 'material':
                  aspect = Graphic3d_MaterialAspect(MATERIAL_TYPES.index(styleValue))
                  obj.SetMaterial(aspect)
             elif styleName == 'lineType':         
                  lineType = LINE_TYPES.index(styleValue)
                  obj.Attributes().WireAspect().SetTypeOfLine(lineType)
                  obj.Attributes().LineAspect().SetTypeOfLine(lineType)
             elif styleName == 'lineWidth':         
                 obj.Attributes().LineAspect().SetWidth(styleValue)
                 obj.Attributes().WireAspect().SetWidth(styleValue)
             elif styleName == 'visible':         
                 if self.isInit:
                    if styleValue > 0.5:
                        self.display.Context.Display(obj, False) 
                    else:    
                        self.display.Context.Erase(obj, False)    
             if isinstance(obj, AIS_Point): 
                 if styleName == 'pointType':         
                      obj.SetMarker(POINT_TYPES.index(styleValue))
                 if styleName == 'pointSize':         
                      obj.Attributes().PointAspect().SetScale(styleValue)
         
    def transformNativeObj(self, nativeObj, nativeTranformation):
        pass
    
    def transformGpPnt(self, gpPnt, nativeTranformation):
        pass
    
    def dumpNativeObj(self, nativeObj):
        return nativeObj.__class__.__name__         

    def detectCenter(self, nativeObj):
        if not nativeObj:  #pass non exist obj name 
            return gp_Pnt(0,0,0)
        if isinstance(nativeObj, AIS_Point):
            return nativeObj.Component().Pnt()
        if  self.isInit:
            box = Bnd_Box()
            nativeObj.BoundingBox(box)
            xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
            x = (xmax+xmin)/2
            y = (ymax+ymin)/2
            z = (zmax+zmin)/2
            return gp_Pnt(x,y,z)
        return gp_Pnt(0,0,0)
        
     
'''
*****************************************************
*****************************************************
*****************************************************
*****************************************************
'''


class SceneObject:
    def __init__(self, parentSceneObject = None, nativeObj = None, nativeLib = None) :
        self.parent = parentSceneObject
        if self.parent:
           self.nativeLib = parentSceneObject.nativeLib
        else:   
           #root object creation
           if nativeLib:
              self.nativeLib = nativeLib
           else:
              raise Exception('Need nativeLib for root SceneObject')
        self.nativeObj = nativeObj
        self.childs = dict()
        self.handles = dict()  # center and label must init
        self.autoNum = dict()
        
    def getChild(self, objName):
        if objName in self.childs:
            return self.childs[objName]
        else:
            return None
        
    def setChild(self, objName, sceneObj, styles):
        if objName.find('#')!= -1:
           num = self.autoNum.get(objName,0)
           self.autoNum[objName] = num + 1                   
           objName = objName.replace('#', str(num))
        oldObj = self.getChild(objName)
        if oldObj:
            oldObj.deactivate()
        if sceneObj:    
           self.childs[objName] = sceneObj
           sceneObj.objName = objName
           sceneObj.activate(styles)
        else:   
           self.childs.pop(objName, None)
           
    def applyStyle(self, styleName, styleValue):
        self.nativeLib.stylingNativeObj(self.nativeObj, styleName, styleValue)    
        
    def applyTransform(self, nativeTransform) :
        self.nativeLib.transformNativeObj(self.nativeObj, nativeTransform)        
        
    def activate(self, styles):
        self.nativeLib.activateNativeObj(self.nativeObj, styles)
        
    def deactivate(self):    
        self.nativeLib.deactivateNativeObj(self.nativeObj)
        for key in self.childs:
           self.childs[key].deactivate()
        
    def detectCenter(self):
        return self.nativeLib.detectCenter(self.nativeObj)


'''
****************************************************************
'''

class SceneStylesSetting:
    
    def __init__(self):
        
        self.layers = dict()
        self.curLayer = None
        self.initStyles()
        self.setLayer('default')
        
    def setLayer(self, layerName):
        if layerName in self.layers:
           self.curLayer = self.layers[layerName]
        else: 
           self.curLayer = dict()
           self.layers[layerName] = self.curLayer
        
    def getLayerStyles(self):
        return self.curLayer
        
    def getStyle(self, styleName):  
        return self.curLayer.get(styleName)
      
    def setStyle(self, styleName, styleValue):  
        self.curLayer[styleName] = styleValue
        
       
    def initStyles(self):
        
        self.setLayer('hide')
        self.setStyle('visible', 0)                
        self.setStyle('color', (0, 0, 1))             
        self.setStyle('transparency', 0 )             
        self.setStyle('material', 'DEFAULT' )             
        self.setStyle('lineType', 'SOLID')             
        self.setStyle('lineWidth', 3)            
        self.setStyle('pointType', 'BALL')            
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (55/255, 74/255, 148/255))             
        self.setStyle('textHeight', 20)             
        
        self.setLayer('info')
        self.setStyle('visible', 1)                
        self.setStyle('color', (0.5, 0.5, 0.5))             
        self.setStyle('material', 'DEFAULT' )             
        self.setStyle('transparency', 0 )             
        self.setStyle('lineType', 'DASH')             
        self.setStyle('lineWidth', 1)             
        self.setStyle('pointType', 'BALL')            
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (0.5, 0.5, 0.5))             
        self.setStyle('textHeight', 20)             
          
        self.setLayer('base')
        self.setStyle('visible', 1)                
        self.setStyle('color', (1, 0, 0))             
        self.setStyle('transparency', 0 )             
        self.setStyle('material', 'DEFAULT' )             
        self.setStyle('lineType', 'DASH')             
        self.setStyle('lineWidth', 2)             
        self.setStyle('pointType', 'BALL')            
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (189/255, 60/255, 45/255))             
        self.setStyle('textHeight', 20)             
        
        self.setLayer('fog')
        self.setStyle('visible', 1)                
        self.setStyle('color', (0, 0.7, 0))             
        self.setStyle('transparency', 0.4 )             
        self.setStyle('lineType', 'SOLID')             
        self.setStyle('lineWidth', 2)             
        self.setStyle('pointType', 'BALL')            
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (0, 0.7, 0))             
        self.setStyle('textHeight', 20)             
        
        self.setLayer('main')
        self.setStyle('visible', 1)                
        self.setStyle('color', (0, 0, 1))             
        self.setStyle('transparency', 0 )             
        self.setStyle('material', 'PLASTIC' )             
        self.setStyle('lineType', 'SOLID')             
        self.setStyle('lineWidth', 3)             
        self.setStyle('pointType', 'BALL')            
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (55/255, 74/255, 148/255))             
        self.setStyle('textHeight', 20)             

        self.setLayer('pres')
        self.setStyle('visible', 1)                
        self.setStyle('color', (0.7, 0.7, 0))             
        self.setStyle('transparency', 0 )             
        self.setStyle('material', 'GOLD' )             
        self.setStyle('lineType', 'SOLID')             
        self.setStyle('lineWidth', 5)             
        self.setStyle('pointType', 'BALL')            
        self.setStyle('pointSize', 3 )             
        self.setStyle('textColor', (55/255, 74/255, 148/255))             
        self.setStyle('textHeight', 20)             
        
'''
****************************************************************
'''

class Scene:
    def __init__(self, nativeLib):
        self.nativeLib = nativeLib
        self.rootObj = SceneObject(None,'level', nativeLib)
        self.curObj = self.rootObj
        self.curStylesSetting = SceneStylesSetting()
        self.stylesStack = list()
        return 
    
    def _setObj(self, objName, obj):
        self.curObj.setChild(objName, obj, self.curStylesSetting.getLayerStyles())
    
    def _getObj(self, objName):
        return self.curObj.getChild(objName)
    
    def _applyStyle(self, objName, styleName, styleValue):
        obj = self._getObj(objName)
        if obj:
            obj.applyStyle(styleName, styleValue)
 
    def _drawNative(self, objName, nativeObj):
        obj = SceneObject(self.curObj, nativeObj)
        self._setObj(objName, obj)

  
    def screenInit(self):
       self.nativeLib.initScreen() 
       
    def screenClear(self):
       self.rootObj = SceneObject(None,'level', self.NativeLib)
       self.curObj = self.rootObj
       self.nativeLib.clearScreen()
       
    def screenStart(self):
       if self.nativeLib.isScreenInit() :
           self.nativeLib.startScreen()
       else:
          print('Virtual run is complete')    
          print('Use SceneScreenInit()')    
         #dumpObj(self.rootObj)
         #dumpObj(self.curObj)
    
    def getNative(self, objName):
        obj = self._getObj(objName)
        if obj:
           return obj.nativeObj
        else:
           return None
    
    def layer(self, layerName):  
        self.curStylesSetting.setLayer(layerName)
     
    def setStyle(self, styleName, styleValue):  
        self.curStylesSetting.setStyle(styleName, styleValue)
    
    def getStyle(self, styleName):  
        return self.curStylesSetting.getStyle(styleName)
      
    def applyStyle(self, objName, styleName, styleValue):
        self._applyStyle(objName, styleName, styleValue)
 
    def setDefaultStyles(self, objName, styleName, styleValue):
        self.curStyleSetting = SceneStylesSetting()
 
    def levelUp(self):
        if self.curObj.parent:
           self.curObj = self.curObj.parent
           self.curStylesSetting = self.stylesStack.pop()
        else:
          raise 'Try level up from root level'    
          
        
    def levelDown(self, childName = None):
        childObj = self.curObj.getChild(childName)
        if not childObj:
          childObj = SceneObject(self.curObj, 'level')
          self._setObj(childName, childObj)
        self.curObj = childObj  
        self.stylesStack.append(self.curStylesSetting)
        self.curStylesSetting = deepcopy(self.curStylesSetting)
           
    '''
    ************************************************************
    '''
    
    def drawText(self, objName, gpPnt, text):
        nativeObj = NativeStubText(gpPnt, text)
        self._drawNative(objName, nativeObj)
       
    def drawLabel(self, labeledObjName, text = None):
        if text == None:
             text = labeledObjName
        labeledObj = self._getObj(labeledObjName)     
        if labeledObj :
            gpPnt = labeledObj.detectCenter()     
            gpPntPlace = gp_Pnt(gpPnt.X()+0.2,gpPnt.Y()+0.2,gpPnt.Z()+0.2)
            self.drawText(labeledObjName + '_label', gpPntPlace, text)
      
    def drawTrihedron(self, objName, size):
        gpPnt = gp_Pnt(0,0,0)
        gpDir1 = gp_Dir(gp_Vec(0,0,1))
        gpDir2 = gp_Dir(gp_Vec(1,0,0))
        geomAxis = Geom_Axis2Placement(gpPnt, gpDir1, gpDir2)
        
        trih = AIS_Trihedron(geomAxis)
        trih.SetSize(11)
        
        self._drawNative(objName, trih)
      
    def drawAxis(self, objName):
        
        def localPoint(objName, gpPnt):
            self.drawPoint(objName, gpPnt)
            self.applyStyle(objName, 'pointSize', 1.5)
            
        self.levelDown(objName)
    
        self.layer('info')    
        self.drawTrihedron('trihedron',11)
        
        localPoint('center', gp_Pnt(0,0,0))
        
        for i in range (1,10):
            localPoint('x'+ str(i), gp_Pnt(i,0,0))
            localPoint('y'+ str(i), gp_Pnt(0,i,0))
            localPoint('z'+ str(i), gp_Pnt(0,0,i))
              
        self.levelUp()
    
    def drawPoint(self, objName, gpPnt):
        geomPnt = Geom_CartesianPoint(gpPnt)
        nativeObj = AIS_Point(geomPnt)
        sc._drawNative(objName, nativeObj)
        
    def drawPoints(self, objNamePrefix, pnts):
        if isinstance(pnts, list) or isinstance(pnts, tuple):
           i = 0 
           for pnt in pnts:
              self.drawPoints(objNamePrefix + '_' + str(i), pnt)
              i+=1
        else:    
           SceneDrawPoint(objNamePrefix, pnts)
           SceneDrawLabel(objNamePrefix)
    
    def drawLine(self, objName, gpPnt1, gpPnt2):
        geomPnt1 = Geom_CartesianPoint(gpPnt1)
        geomPnt2 = Geom_CartesianPoint(gpPnt2)
        nativeObj = AIS_Line(geomPnt1,geomPnt2)
        sc._drawNative(objName, nativeObj)
    
    def drawCircle(self, objName, gpPnt1, gpPnt2, gpPnt3):
        geomCircle = GC_MakeCircle(gpPnt1, gpPnt2, gpPnt3).Value()
        nativeObj = AIS_Circle(geomCircle)
        self._drawNative(objName, nativeObj)
     
    def drawShape(self, objName, shape):
         nativeObj = AIS_Shape(shape)
         self._drawNative(objName, nativeObj)
         
    def erase(self, objName):
        self._setObj(objName, None)
        
    
'''
***********************************************
Functional interface
***********************************************
'''

sc = Scene(NativeLib())
    
def SceneScreenInit():
    return sc.screenInit()
def SceneScreenClear():
    return sc.screenClear()
def SceneScreenStart():
    return sc.screenStart()
def SceneGetNative(objName):
    return sc.getNative(objName)
def SceneLayer(layerName):  
     return sc.layer(layerName)
def SceneSetStyle(styleName, styleValue):  
    return sc.setStyle(styleName, styleValue)
def SceneGetStyle(styleName):  
    return sc.getStyle(styleName)
def SceneApplyStyle(objName, styleName, styleValue):
    return sc.applyStyle(objName, styleName, styleValue)
def SceneSetDefaultStyles(objName, styleName, styleValue):
    return sc.setDefaultStyles(objName, styleName, styleValue)
def SceneLevelUp():
    return sc.levelUp()
def SceneLevelDown(childName = None):
    return sc.levelDown(childName)
def SceneDrawText(objName, gpPnt, text):
    return sc.drawText(objName, gpPnt, text)
def SceneDrawLabel(labeledObjName, text = None):
    return sc.drawLabel(labeledObjName, text)
def SceneDrawTrihedron(objName, size):
    return sc.drawTrihedron(objName, size)
def SceneDrawAxis(objName):
    return sc.drawAxis(objName)
def SceneDrawPoint(objName, gpPnt):
    return sc.drawPoint(objName,  gpPnt)
def SceneDrawPoints(objName, gpPnt):
    return sc.drawPoints(objName,  gpPnt)
def SceneDrawLine(objNamePrefix,  gpPnt1,  gpPnt2):
    return sc.drawLine(objNamePrefix,  gpPnt1, gpPnt2)
def SceneDrawCircle(objName,  gpPnt1,  gpPnt2,  gpPnt3):
    return sc.drawCircle(objName,  gpPnt1,  gpPnt2,  gpPnt3)
def SceneDrawShape(objName, shape):
    return sc.drawShape(objName, shape)
def SceneErase(objName):
    return sc.erase(objName)
        
'''
***********************************************
Testing
***********************************************
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
        
        gpPnt = gp_Pnt(2,3,4)
        
        SceneLayer('info')
        SceneDrawPoint('pnt', gpPnt)    
        SceneDrawLabel('pnt', 'pnt+')
        
        gpPntStart = gp_Pnt(5,0,3)
        gpPntEnd = gp_Pnt(0,5,3)
        
        SceneLayer('main')
        SceneDrawLine('line', gpPntStart, gpPntEnd)
        SceneDrawLabel('line')
        
        SceneLayer('base')
        SceneDrawPoint('lineStart', gpPntStart)
        SceneDrawLabel('lineStart', 'lineStart+')
        
     
        SceneLayer('hide')
        SceneDrawPoint('lineEnd', gpPntEnd)
        SceneDrawLabel('lineEnd')
    
        SceneLevelUp()
    
    def  testCircle(name):
        
        SceneLevelDown(name)
        
        gpPnt1 = gp_Pnt(1,1,10)
        gpPnt2 = gp_Pnt(5,2,5)
        gpPnt3 = gp_Pnt(5,-5,5)
        
        SceneLayer('pres')
        SceneDrawCircle('circle', gpPnt1, gpPnt2, gpPnt3)
        SceneDrawLabel('circle')
        
        SceneLayer('fog')
        SceneDrawPoint('p1', gpPnt1)
        SceneDrawLabel('p1')
        SceneDrawPoint('p2', gpPnt2)
        SceneDrawLabel('p2')
        SceneDrawPoint('p3', gpPnt3)
        SceneDrawLabel('p3')
       
        SceneLevelUp()
        
    def testMessage(name):
        
        SceneLevelDown(name)
        
        SceneLayer('main')
        SceneDrawText('meesage', gp_Pnt(5,5,5), 'Hello OpenCascade!')
        
        SceneLevelUp()

    def testSphere(name):
        SceneLevelDown(name)
        SceneDrawShape('sphere', BRepPrimAPI_MakeSphere(3).Shape())
        SceneLevelUp()
   
    def testDrawPoints(name):
        SceneLevelDown(name)
        cnt = 3
        pntsX = []  
        for iX in range(cnt):
          pntsY = []  
          for iY in range(cnt):
              pntsZ = []
              for iZ in range(cnt):
                  pntsZ += [gp_Pnt(iX,iY,iZ)]
              pntsY += [pntsZ]
          pntsX += [pntsY]
              
        SceneDrawPoints('p', pntsX)
        
        SceneLevelUp()
   

    SceneScreenInit() 
    
    SceneDrawAxis('axis')
    
    testMessage('mess')
    testLine('point')
    testLine('line')
    testCircle('circle')
    testSphere('sphere')
    testDrawPoints('points')
      
    #dumpObj(sc.curStylesSetting)
    
    SceneScreenStart()
