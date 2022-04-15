from _scene_obj import Env, Scene, Hook, Label, Box, Sphere, Cylinder, Cone, Tube, Surface, Rotation, Translation 

sc = None
env = Env()

def env(envName, envDefault):
    env.env(envName, envDefault)

def sceneInit(): 
    global sc
    sc = Scene()

def sceneInitCache(globalForGetFunctions):
    sc.initCache(globalForGetFunctions)

def sceneRender(sceneName = None, styles = None):
    sc.render(sceneName, styles)

def getHook(pnt, r) :
    sc.getPrimitive(Sphere((pnt, r)))

def getLabel(pnt, text, size, delta): 
    sc.getPrimitive(Label((pnt, text, size, delta)))

def getBox(pnt1, pnt2):
    sc.getPrimitive(Box((pnt1,pnt2)))

def getSphere(pnt, r) :
    sc.getPrimitive(Sphere((pnt, r)))
    
def getCone(pnt1, pnt2, r1, r2):    
    sc.getPrimitive(Cone((pnt1, pnt2, r1, r2)))

def getCylinder(pnt1, pnt2, r):    
    sc.getPrimitive(Cylinder((pnt1, pnt2, r)))

def getTube(wire, radius):
    sc.getPrimitive(Tube((wire, radius)))

def getSurface(surface):
    sc.getPrimitive(Surface(surface))

def getGroup():
    sc.getGroup()

def getFunc(funcName, param1 = None, param2 = None):
    sc.get(funcName, param1 = None, param2 = None)

def makeTranslate(dx, dy, dz):
    sc.makeTransform(Translation(dx, dy, dz))

def makeRotate(pnt, dir, angle):
    sc.makeTransform(Rotation(pnt, dir, angle))

def setStyle(styleName):
    sc.setStyle(styleName)

def setLayer(styleName):
    sc.setLayer(styleName)

def put(name):
    sc.put(name)

def drop():
    sc.drop()
    
