from _scene_obj import Scene, Env

sc = None
env = Env()

def env(envName, envDefault):
    env.env(envName, envDefault)

def sceneInit(globalForGetFunctions, sceneName=None, styles = None): 
    global sc
    sc = Scene(globalForGetFunctions, sceneName, styles)

def sceneRender(funcName, param1 = None, param2 = None):
    sc.render(funcName, param1 = None, param2 = None)

def getLabel(pnt, text, size, delta): 
    sc.getLabel(pnt, text, size, delta)

def getSphere(pnt, r) :
    sc.getSphere(pnt, r)
    
def getCone(pnt1, pnt2, r1, r2):    
    sc.getCone(pnt1, pnt2, r1, r2)

def getBox(pnt1, pnt2):
    sc.getBox(pnt1, pnt2)

def getTube(wire, radius):
    sc.getTube(wire, radius)

def getSurface(surface):
    sc.getSurface(surface)

def makeTranslate(dx, dy, dz):
    sc.translate(dx, dy, dz)

def makeRotate(pnt, direct, angle):
    sc.rotate(pnt, direct, angle)

def setStyle(styleName):
    sc.style(styleName)

def setLayer(styleName):
    sc.layer(styleName)

def put(name):
    sc.put(name)
    
def get(funcName, param1 = None, param2 = None):
    sc.get(funcName, param1 = None, param2 = None)
