import re
import time

from src import utils, config, operation
from src.jijian import jijianTool


# 获取干员心情
def getWorkersMood(orc):
    l = [[], 24]  # 干员名称,最小心情
    i = 0
    for k in orc:
        if utils.retainStr(k[1][0]) == '心情':
            if k[1][1] > 0.7:
                mo = re.compile(r'^(\d\d|\d)').search(orc[i + 1][1][0])
                if mo is None:
                    i += 1
                    continue
                mood = int(mo.group())
                l[0].append(orc[i - 1][1][0])
                if mood < l[1]:
                    l[1] = mood

            else:
                print('相似度不足无法判定')
        i += 1
    print('干员心情:' + str(l))
    return l


# 判断是否换干员 a换a组 b换b组 c不换
def isSwapWorker(workers, checkList):
    l = utils.list2to1(checkList)
    for i in workers[0]:
        if i in l:
            return 'a'
        if workers[1] < config.maoyiMood:
            return 'b'
    return 'c'


# # 根据ocr和预设干员 点击坐标
# def clickPageWorkers(ocr, checkList, swapord):
#     if len(swapord[1]) >= 1:
#         for o in ocr:
#             if utils.retainStr(o[1][0]) in swapord[0]:
#                 if utils.retainStr(o[1][0]) in swapord[1]:
#                     continue
#                 operation.backClick(utils.getPoint2Rect(o[0]))
#                 num = utils.backDelStr(utils.retainNum(operation.pfindStr((326, 106))), 2)
#                 print('干员心情:' + str(num))
#                 if int(num) >= 20:
#                     swapord[1].append(utils.retainStr(o[1][0]))
#                     print(swapord)
#                 else:
#                     operation.backClick(utils.getPoint2Rect(o[0]))
#                     print('干员心情不足不添加')
#     else:
#         for o in ocr:
#             if len(swapord[1]) == 0:
#                 for c in checkList:
#                     if utils.retainStr(o[1][0]) in c:
#                         operation.backClick(utils.getPoint2Rect(o[0]))
#                         num = utils.backDelStr(utils.retainNum(operation.pfindStr((326, 106))), 2)
#                         print('干员心情:' + str(num))
#                         if int(num) >= 20:
#                             swapord[0] = c
#                             swapord[1].append(utils.retainStr(o[1][0]))
#                             print(swapord)
#                             continue
#                         else:
#                             operation.backClick(utils.getPoint2Rect(o[0]))
#                             print('干员心情不足不添加')
#
#             else:
#                 if utils.retainStr(o[1][0]) in swapord[0]:
#                     operation.backClick(utils.getPoint2Rect(o[0]))
#                     num = utils.backDelStr(utils.retainNum(operation.pfindStr((326, 106))), 2)
#                     print('干员心情:' + str(num))
#                     if int(num) >= 20:
#                         swapord[1].append(utils.retainStr(o[1][0]))
#                         print(swapord)
#                     else:
#                         operation.backClick(utils.getPoint2Rect(o[0]))
#                         print('干员心情不足不添加')


# 换班逻辑
def maoyihuanban(p):  # swapord 0需要选中的干员 1以选中干员
    swapord = [[], []]
    # 贸易站换干员逻辑
    operation.clickNextNode(p)
    operation.backClick((640, 140))
    operation.backClick((60, 270), 2)
    operation.screenshot()  # 截屏
    ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
    swapres = isSwapWorker(getWorkersMood(ocrres), config.bMaoyi)

    if swapres == 'a':
        print('监测到b组 换a组')
        # 进入换人页面
        operation.clickNextNode((930, 150))
        operation.backClick((480, 220))
        operation.backClick((630, 220))
        operation.backClick((480, 480))
        operation.screenshot()  # 截屏
        ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
        jijianTool.clickPageWorkers(ocrres, config.aMaoyi, swapord)
        if len(swapord[1]) == 3:
            operation.clickNextNode((1170, 680))
            print('更换成功')
        elif len(swapord[1]) < 3:
            isback = True
            for i in range(4):
                jijianTool.nextWorkers()
                operation.screenshot()  # 截屏
                ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
                jijianTool.clickPageWorkers(ocrres, config.aMaoyi, swapord)
                if len(swapord[1]) >= 3:
                    print('更换成功')
                    isback = False
                    operation.clickNextNode((1170, 680))
                    break
            if isback:
                operation.clickNextNode((80, 40))
                print('未找到干员不进行更换')

    elif swapres == 'b':
        print('监测到a组心情不足 换b组')
        # 进入换人页面
        operation.clickNextNode((930, 150))
        operation.backClick((480, 220))
        operation.backClick((630, 220))
        operation.backClick((480, 480))
        operation.screenshot()  # 截屏
        ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
        jijianTool.clickPageWorkers(ocrres, config.bMaoyi, swapord)
        if len(swapord[1]) == 3:
            operation.clickNextNode((1170, 680))
            print('更换成功')
        elif len(swapord[1]) < 3:
            isback = True
            for i in range(4):
                jijianTool.nextWorkers()
                operation.screenshot()  # 截屏
                ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
                jijianTool.clickPageWorkers(ocrres, config.bMaoyi, swapord)
                if len(swapord[1]) >= 3:
                    print('更换成功')
                    isback = False
                    operation.clickNextNode((1170, 680))
                    break
            if isback:
                operation.clickNextNode((80, 40))
                print('未找到干员不进行更换')
    else:
        print('不需要更换')
    operation.backClick((640, 140))
    operation.clickNextNode((100, 37))
    time.sleep(2)


def start():
    maoyihuanban(config.maoyiP1)
    maoyihuanban(config.maoyiP2)


def testStart():
    maoyihuanban(config.maoyiP1)
