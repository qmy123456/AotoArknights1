import copy

from src import operation, config, utils
from src.jijian import jijianTool


def configClue():
    pList = [[385, 225], [580, 300], [785, 200], [1000, 245], [668, 505], [870, 450], [434, 484]]
    # 接受库加入线索
    operation.screenshot()  # 截屏
    ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
    for i in pList:
        for k in ocrres:
            if utils.isPointInQuad(k[0], i):
                num = pList.index(i) + 1
                print('线索' + str(num) + '未安装')
                operation.backClick(i)
                operation.backClick((1224, 26))
                operation.backClick((950, 250))
                operation.backClick((690, 75))
    # 自有库加入线索
    operation.screenshot()  # 截屏
    ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
    for i in pList:
        for k in ocrres:
            if utils.isPointInQuad(k[0], i):
                num = pList.index(i) + 1
                print('线索' + str(num) + '未安装')
                operation.backClick(i)
                operation.backClick((1064, 30))
                operation.backClick((950, 250))
                operation.backClick((690, 75))
    # 剩下就是未找到的
    operation.screenshot()  # 截屏
    ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
    nothaveList = []
    for i in pList:
        for k in ocrres:
            if utils.isPointInQuad(k[0], i):
                num = pList.index(i) + 1
                nothaveList.append(num)
                print('线索' + str(num) + '没有')
    return nothaveList


def clickWorker(workers, num):
    clickNum = 0
    operation.screenshot()  # 截屏
    ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
    if len(workers) == 2:  # 有一个干员
        p1 = utils.findPoint2S(ocrres, workers[1])
        if p1 is not None:
            operation.backClick(p1)
            clickNum = 1

    elif len(workers) >= 3:  # 有两个干员
        if num == 1:
            p1 = utils.findPoint2S(ocrres, workers[1])
            if p1 is not None:
                operation.backClick(p1)
                clickNum = 1
        else:
            p1 = utils.findPoint2S(ocrres, workers[1])
            if p1 is not None:
                operation.backClick(p1)
                clickNum += 1
            p2 = utils.findPoint2S(ocrres, workers[2])
            if p2 is not None:
                operation.backClick(p2)
                clickNum += 1
    return clickNum


def huanban(nothaveList):
    clueWorkers = copy.deepcopy(config.xiansuoWorkers)
    clueOrder = {3: 1, 4: 2, 5: 3, 6: 4, 1: 5, 2: 6, 7: 7, 8: 8}

    operation.screenshot()  # 截屏
    ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果

    name1 = utils.findStr2P(ocrres, (990, 125))
    mood1 = int(utils.backDelStr(utils.retainNum(utils.findStr2P(ocrres, (1140, 155))), 2))
    if mood1 < config.xiansuoMood:
        for i in clueWorkers:
            if name1 in i:
                i.remove(name1)

    name2 = utils.findStr2P(ocrres, (990, 263))
    mood2 = int(utils.backDelStr(utils.retainNum(utils.findStr2P(ocrres, (1140, 300))), 2))
    if mood2 < config.xiansuoMood:
        for i in clueWorkers:
            if name1 in i:
                i.remove(name2)

    operation.clickNextNode((900, 160))
    operation.backClick((480, 225))
    operation.backClick((480, 480))

    # 进入换人页面
    clickNum = 0
    if len(nothaveList) == 1:
        for i in clueWorkers:
            if nothaveList[0] == i[0]:
                clickNum += clickWorker(i, 2)

    elif len(nothaveList) >= 2:
        #  根据clueOrder 给 nothaveList 排序
        nothaveListOrder = sorted(nothaveList, key=lambda x: clueOrder[x])
        for i in range(2):
            for k in clueWorkers:
                if nothaveListOrder[i] == k[0]:
                    clickNum += clickWorker(k, 1)
    else:
        if len(clueWorkers[7]) >= 2:
            clickNum += clickWorker(clueWorkers[7], 2)

    if clickNum < 2:
        jijianTool.nextWorkers()
        if len(nothaveList) == 1:
            for i in clueWorkers:
                if nothaveList[0] == i[0]:
                    clickNum += clickWorker(i, 2)

        elif len(nothaveList) >= 2:
            #  根据clueOrder 给 nothaveList 排序
            nothaveListOrder = sorted(nothaveList, key=lambda x: clueOrder[x])
            for i in range(2):
                for k in clueWorkers:
                    if nothaveListOrder[i] == k[0]:
                        clickNum += clickWorker(k, 1)
        else:
            if len(clueWorkers[7]) >= 2:
                clickNum += clickWorker(clueWorkers[7], 2)
        if clickNum < 2:
            operation.backClick((480, 225))
            operation.backClick((480, 480))
    operation.clickNextNode((1200, 680))
    operation.backClick((640, 140))
    operation.clickNextNode((80, 35))


def start():
    operation.clickNextNode((1200, 200))
    operation.backClick((640, 140))
    operation.clickNextNode((474, 625))
    operation.backClick((1194, 181))
    operation.backClick((800, 580))
    operation.backClick((996, 91))
    operation.backClick((1200, 290))
    operation.backClick((1078, 686))
    operation.backClick((720, 65))

    nothaveList = configClue()
    if len(nothaveList) == 0:
        print('线索全部找到')
        operation.backClick((684, 655), 2)
        operation.backClick((474, 625))
        nothaveList = configClue()

    operation.clickNextNode((62, 40))
    operation.backClick((77, 308))
    huanban(nothaveList)
