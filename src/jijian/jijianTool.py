from src import utils, operation


# 根据ocr和预设干员 点击坐标
def clickPageWorkers(ocr, checkList, swapord):
    if len(swapord[1]) >= 1:
        for o in ocr:
            name = utils.retainStr(o[1][0]).lower()
            if name in swapord[0]:
                if name in swapord[1]:
                    continue
                operation.backClick(utils.getPoint2Rect(o[0]))
                num = utils.backDelStr(utils.retainNum(operation.pfindStr((347, 109))), 2)
                print('干员心情:' + str(num))
                if int(num) >= 20:
                    swapord[1].append(name)
                    print(swapord)
                else:
                    operation.backClick(utils.getPoint2Rect(o[0]))
                    print('干员心情不足不添加')
    else:
        for o in ocr:
            name = utils.retainStr(o[1][0]).lower()
            if len(swapord[1]) == 0:
                for c in checkList:
                    if name in c:
                        operation.backClick(utils.getPoint2Rect(o[0]))
                        num = utils.backDelStr(utils.retainNum(operation.pfindStr((347, 109))), 2)
                        print('干员心情:' + str(num))
                        if int(num) >= 20:
                            swapord[0] = c
                            swapord[1].append(name)
                            print(swapord)
                            continue
                        else:
                            operation.backClick(utils.getPoint2Rect(o[0]))
                            print('干员心情不足不添加')

            else:
                if name in swapord[0]:
                    operation.backClick(utils.getPoint2Rect(o[0]))
                    num = utils.backDelStr(utils.retainNum(operation.pfindStr((347, 109))), 2)
                    print('干员心情:' + str(num))
                    if int(num) >= 20:
                        swapord[1].append(name)
                        print(swapord)
                    else:
                        operation.backClick(utils.getPoint2Rect(o[0]))
                        print('干员心情不足不添加')


# 判断是否换干员 a换a组 b换b组 c不换
def isSwapWorker(workers, checkList, mood=12):
    l = utils.list2to1(checkList)
    for i in workers[0]:
        if i in l:
            return 'a'
        if workers[1] < mood:
            return 'b'
    return 'c'


def nextWorkers():
    operation.backXMove((1080, 650), -910, 25)

