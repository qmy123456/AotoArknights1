import time

from src import config, operation, utils


def friendXinlai():
    operation.clickNextNode((372, 574))
    operation.backClick((125, 222), 3)
    operation.clickNextNode((1002, 160), 5)
    for i in range(15):
        operation.backClick((1174, 634), 3)
    time.sleep(3)
    operation.backClick((265, 40))
    operation.clickNextNode((90, 280))


def shopXinlai():
    operation.clickNextNode((840, 470))
    operation.clickNextNode((1187, 105))
    operation.backClick((1006, 37))
    operation.backClick((650, 30))
    operation.backClick((650, 30))

    operation.backClick((130, 270))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((380, 270))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((630, 270))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((880, 270))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((1130, 270))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((130, 520))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((380, 520))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((630, 520))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((880, 520))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((1130, 520))
    isBuy()
    operation.backClick((650, 30))

    operation.backClick((265, 40))
    operation.clickNextNode((90, 280))


def isBuy():
    name = getName()
    if name not in config.xinlaiwupin:
        if name == 'null':
            print('已购买')
            operation.backClick((650, 30))
            return
        print(name+':购买')
        operation.backClick((920, 580))
    else:
        print(name + ':不购买')
        operation.backClick((650, 30))


def getName():
    return utils.retainStr(operation.pfindStr((197, 194)))


def start():
    print('开始信赖')
    friendXinlai()
    time.sleep(5)
    shopXinlai()


def testStart():
    shopXinlai()

