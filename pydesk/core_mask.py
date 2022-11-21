def isNameMask(nameMask: str, nameValue: str):
    if nameMask.endswith('*'):
        return nameValue.startswith(nameMask.replace('*', ''))
    else:
        return nameValue == nameMask


def isClassMask(classMask, classValues):
    for classValue in classValues.split('-'):
        if classValue == classMask:
            return True
    return False


def isClassesMask(classesMask: str, classesValue: str):
    if classesMask == '*':
        return True
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
    return isNameMask(nameMask, nameValue) and isClassesMask(classesMask, classesValue)


def isMask(objChainMask, objChainValue):
    objChainMaskList = objChainMask.split('>')
    objChainValueList = objChainValue.split('>')
    iMask = len(objChainMaskList)
    iValue = len(objChainValueList)
    while (iMask > 0) and (iValue > 0):
        if isObjMask(objChainMaskList[iMask-1], objChainValueList[iValue-1]):
            iMask -= 1
            iValue -= 1
        else:
            iValue -= 1
    return iMask == 0


def check(mask, value, expected):
    result = isMask(mask, value)
    if result == expected:
        print('Test OK', mask, value, result)
    else:
        print('Test ERROR', mask, value, expected, 'RESULT', result)


if __name__ == "__main__":

    check('item', 'item', True)
    check('item', 'item200', False)
    check('*', 'item', True)
    check('item*', 'item200', True)
    check('item3*', 'item200', False)
    check('item', 'item:box', True)
    check('item:box', 'item:box', True)
    check('item:line', 'item:box', False)
    check('item:line-box', 'item:box', False)
    check('item:box', 'item:line-box', True)
    check('item:line-box', 'item:line-box', True)
    check('item:line-box-info', 'item:line-box', False)
    check('item:line-box-info', 'item:info-line-box', True)
    check('i*:line-box-info', 'item:info-line-box', True)
    check('item2>item', 'item2>item', True)
    check('item2>item', 'item2>item0>item', True)
    check('item3>item2>item', 'item000>item3>item2>item0>item00>item', True)
    check('item3>item4>item', 'item000>item3>item2>item0>item00>item', False)
    check('*', 'item000>item3', True)
