from _scene_obj import Env, Scene, Hook, Label, Box, Sphere, Cylinder, Cone, Tube, Surface, Rotation, Translation 

class Scene:

    def __init__(self):
        self.cache = dict()
        self.stackArr = []
        self.group = Drawable(None)

    def initCache(self, globalForGetFunctions):
        self.forGetFunctions =  globalForGetFunctions

    def stack(self, drawable):
        self.stackArr.append(drawable)
        
    def last(self):   
        return self.stackArr[-1]
        
    def unstack(self):
        return self.stackArr.pop()    

    def render(self, sceneName = None, styles = None):
        lib = ScreenLib(styles)
        self.getGroup()
        toRender = self.unstack()
        toRender.dump()
        toRender.render(lib)
        lib.start()
    
    def getPrimitive(self, drawable):      
        self.stack(drawable)

    def getGroup(self):
        self.stack(self.group)    
        self.group = Drawable(None) 
          
    def getFunc(self, funcName, param1 = None, param2 = None):
    
        params = ''
        if param1 != None:
          params += str(param1)
        if param2 != None:
          params += ',' + str(param2) 
        cacheKey = funcName+'('+ params + ')'      
        
        if  cacheKey in self.cache:  
            print('==> Get from cache',cacheKey)         
            self.stack(self.cache[cacheKey].copy())
        else:
            if param1 == None:
                self.forGetFunctions[funcName]()
            elif param2 == None:
                self.forGetFunctions[funcName](param1)
            else:
                self.forGetFunctions[funcName](param1, param2)
            print('==> Compute', cacheKey)
            
    def makeTransform(self, transform):
        self.last().makeTransform(transform)

    def setStyle(self, styleName):
        self.last().setStyle(styleName)
    
    def setLayer(self, styleName):
        self.last().setLayer(styleName)

    def put(self, name):
        self.group.putChild(name, self.unstack())

    def drop(self):
        self.unstack()

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
    
