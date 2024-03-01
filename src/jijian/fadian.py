from src import config, operation, utils


def yongdian():
    if config.yongdian == 0:
        print('加速贸易站 不支持')
    else:
        if config.yongdian == 1:
            print('加速赤金')
            operation.clickNextNode(config.chijinP1)
        else:
            print('加速经验卡')
            operation.clickNextNode(config.jingyanP1)

        operation.clickNextNode((84, 616))
        operation.backClick((1218, 539))
        operation.backClick((950, 333))
        operation.backClick((950, 584))
        operation.backClick((1120, 645))
        operation.clickNextNode((85, 38))
        operation.clickNextNode((85, 38))


def fadianhuanban(p):
    # 贸易站换干员逻辑
    operation.clickNextNode(p)
    operation.backClick((625, 108))
    operation.backClick((60, 270), 2)
    num = utils.backDelStr(utils.retainNum(operation.pfindStr((1158, 157))), 2)
    print('干员心情:' + str(num))
    if int(num) < config.jingyanMood:
        print('心情不足更换干员')
        operation.clickNextNode((920, 150), 2)
        operation.backClick((480, 500))
        operation.clickNextNode((1180, 680), 2)
    else:
        print('心情充足不更换')
    operation.backClick((625, 108))
    operation.clickNextNode((80, 40))


def start():
    yongdian()
    fadianhuanban(config.fadianP1)
    fadianhuanban(config.fadianP2)
    fadianhuanban(config.fadianP3)


def testStart():
    yongdian()
