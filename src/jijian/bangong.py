from src import config, operation, utils


def start():
    operation.clickNextNode((1257, 413))
    operation.backClick((640, 140))
    operation.backClick((65, 280))
    num = utils.backDelStr(utils.retainNum(operation.pfindStr((1151, 157))), 2)
    name = utils.retainStr(operation.pfindStr((988, 126)))
    print(name + '心情:' + str(num))
    slist = set(config.allBangong)
    if name in slist:
        slist.remove(name)

    if int(num) < config.bangongMood:
        print('心情不足更换干员')
        operation.clickNextNode((920, 150), 2)
        operation.screenshot()  # 截屏
        ocrres = operation.myPaddle.ocr(config.exeImg)  # 识别结果
        isFind = False
        for i in slist:
            for k in ocrres:
                if i in k[1][0]:
                    operation.backClick(utils.getPoint2Rect(k[0]))
                    isFind = True
                    break
        if not isFind:
            operation.backClick((480, 500))

        operation.clickNextNode((1180, 680), 2)
    else:
        print('心情充足不更换')
    operation.backClick((640, 140))
    operation.clickNextNode((80, 40))
