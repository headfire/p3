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


def isMask(objChainMask, objChainValue)
    objChainMaskList =  objChainMask.split('>')
    objChainValueList =  objChainValue.split('>')
    iMask, iValue = 0, 0
    while (iMask<len(objChainMaskList)) and (iValue<len(objChainMaskList)):
        if isObjMask(objChainMaskList[i],objChainValueList):
            iMask += 1
            iValue += 1
        else:
            iValue += 1
    return  (iMask == len(objChainMaskList)) and iValue == len(objChainMaskList)


def check(mask, value, result)
    if isMask(mask, value) == result:
        print('Test OK', mask, value, result)
    else:
        print('Test ERROR', mask, value, result)

if __name__ == "__main__":

   check('item','item', True)