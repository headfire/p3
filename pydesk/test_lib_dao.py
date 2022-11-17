from lib_dao import *
from core_render import *

import sys

sceneName = 'dao_05'
sceneTarget = 'screen'
scenePath = '.'

if len(sys.argv) > 1:
    sceneName = sys.argv[1]
if len(sys.argv) > 2:
    sceneTarget = sys.argv[2]
if len(sys.argv) > 3:
    scenePath = sys.argv[3]

daoLib = DaoDrawLib()
scene = None

if sceneName == 'dao_01':
    scene = daoLib.getDaoClassicSlide()
elif sceneName == 'dao_02':
    scene = daoLib.getDaoOffsetSlide()
elif sceneName == 'dao_03':
    scene = daoLib.getDaoExampleSliceSlide()
elif sceneName == 'dao_04':
    scene = daoLib.getManySliceSlide()
elif sceneName == 'dao_05':
    scene = daoLib.getDaoSkinningSlide()
elif sceneName == 'dao_06':
    scene = daoLib.getDaoIngYangSlide()
elif sceneName == 'dao_07':
    scene = daoLib.getDaoCaseSlide()

# hints.setScale(5, 1)
# hints.setPathToSave(scenePath)

# desk = daoLib.getDeskDrawBoard()

target = None

if sceneTarget == 'screen':
    target = ScreenRenderLib(1000, 800)
    target.styler.addStyles(daoLib.getStyles())
elif sceneTarget == 'web':
    pass
    # target = WebRenderLib(hints)
elif sceneTarget == 'webfast':
    pass
    # target = WebFastRenderLib(hints)
elif sceneTarget == 'stl':
    pass
    # target = StlRenderLib

target.renderStart()
target.render(scene.doSt(SCALE, 0.5))
# target.render(desk, daoLib.makeMove().setMove(0, 0, -60))
target.renderFinish()
