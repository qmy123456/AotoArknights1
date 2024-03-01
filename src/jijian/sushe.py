import re

from src import config, operation, utils
from src.jijian import jijianTool


# def sushehuanban(p):
#     louP = (((880, 205), 1), ((880, 345), 2), ((880, 485), 3))
#     louP2 = (((25, 115), 4), ((25, 255), 5))  # (880, 470)and(880, 610) - (855, 355)
#     lou = []
#     # huanbanP = [[[480, 220], 1], [[480, 480], 2], [[630, 220], 3], [[630, 480], 4], [[760, 220], 5]]
#     huanbanP = [[480, 220], [480, 480], [630, 220], [630, 480], [760, 220]]
#
#     # operation.backClick(p)
#     # operation.backClick((600, 400))
#     # operation.backClick((65, 280))
#     peopelNum = getPeopleNum()
#     if peopelNum <= 0:
#         print('宿舍没人')
#         operation.backClick((920, 160))
#     else:
#         print('宿舍有' + str(peopelNum) + '个人')
#         yfaceList = operation.findAllImgRect('pic/gface.png')
#         utils.filterSimilar(yfaceList, 5)
#         print(yfaceList)
#         for i in louP:
#             for k in yfaceList:
#                 if utils.isPointInRect(k, i[0]):
#                     lou.append([i[1]])
#                     continue
#         if peopelNum == 4:
#             print(lou)
#         elif peopelNum == 5:
#             operation.backYMove((1030, 500), -400, 20)
#             yfaceList2 = operation.findAllImgRect2P('pic/gface.png', (855, 355), (1250, 625))
#             utils.filterSimilar(yfaceList2, 5)
#             print(yfaceList2)
#             for i in louP2:
#                 for k in yfaceList2:
#                     if utils.isPointInRect(k, i[0]):
#                         lou.append([i[1]])
#                         continue
#             print(lou)
#         for i in lou:
#             i.append(huanbanP[i[0]-1])
#         print(lou)
#     # operation.backClick((920, 160))
#
#     # operation.screenshot((400, 215), (1279, 531))
#     # res = operation.myPaddle.ocr(config.exeImg)
#
#     # operation.screenshot((400, 215), (1279, 249))
#     # image = cv2.imread(config.exeImg, cv2.IMREAD_GRAYSCALE)
#     # cv2.imwrite(config.exeImg, image)
#
#     # operation.strOCR()
#     # res1 = operation.myPaddle.ocr(config.exeImg)
#     # pprint.pprint(res1)
#
#     # operation.screenshot((400, 500), (1279, 517))
#     # res1 = operation.myPaddle.ocr(config.exeImg)
#     # pprint.pprint(res1)
#
#     # operation.backXMove((1080, 650), -910, 10)
#
#     # operation.screenshot()
#     # operation.findAllImg('pic/yface.png')


def getPeopleNum():
    resocr = operation.pfindStr((1225, 686))
    mo = re.compile(r'\d').search(resocr)
    if mo is None:
        return 0
    return int(mo.group())


def sushehuanban(p):
    operation.clickNextNode(p)
    operation.backClick((600, 100))
    operation.backClick((65, 280))
    operation.backClick((1200, 32))
    operation.clickNextNode((1044, 151))

    n = clickWorkers(0)
    while n < 5:
        jijianTool.nextWorkers()
        n = clickWorkers(n)

        faceList = operation.findAllImgRect('pic/gface.png', 0.7)
        if len(faceList) >= 12:
            print('不需要换班了')
            operation.clickNextNode((1175, 680))
            operation.backClick((600, 100))
            operation.clickNextNode((80, 40))
            return False

    operation.clickNextNode((1175, 680))
    operation.backClick((600, 100))
    operation.clickNextNode((80, 40))
    return True


def clickWorkers(n):
    workClick = [[480, 230], [630, 230], [770, 230], [915, 230], [1060, 230], [1200, 230], [480, 510], [630, 510],
                 [770, 510], [915, 510], [1060, 510], [1200, 510]]
    workList = operation.findAllImgRect('pic/work.png', 0.7)
    for i in workList:
        for k in workClick:
            if utils.isPointInRect(i, k):
                workClick.remove(k)
                continue
    for i in workClick:
        n += 1
        operation.backClick(i)
        if n >= 5:
            return len(workClick)
    return n


def start():
    if sushehuanban(config.susheP1):
        if sushehuanban(config.susheP2):
            if sushehuanban(config.susheP3):
                sushehuanban(config.susheP4)


def testStart():
    print('test')
    sushehuanban(config.susheP3)
