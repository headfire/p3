def isGoodName(nameMask: str, nameValue: str):
    if nameMask.endswith('*'):
        return nameValue.startswith(nameMask.replace('*', ''))
    else:
        return nameValue == nameMask


def isClassMask(classMask, classValues):
    for classValue in classValues.split('-'):
        if classValue == classMask
            return True
    return False


def isClassesMask(classesMask: str, classesValue: str):
    for classMask in classesMask.split('-'):
        if not isClassMask(classMask, classesValue):
            return False
    return True


def isObjMask(objMask, objValue):

    objMaskList = objMask.split(':')
    nameMask = '*'
    if len(objMaskList) > 0:
        nameMask = objMaskList[0]
    classesMask = '*'
    if len(objMaskList) > 1:
        classesMask = objMaskList[1]

    objValueList = objValue.split(':')
    nameValue = ''
    if len(objValueList) > 0:
        nameValue = objValueList[0]
    classesValue = ''
    if len(objValueList) > 1:
        classesValue = objValueList[1]

    return isGoodName(nameMask, nameValue) and isGoodClasses(classesMask, classesValue)

def isMask(objChainMask, objChainValues)

    objChainMaskList =  objChainMask.split('>')
    objChainMaskList =  objChainMask.split('>')

