import datetime
import time

import win32gui
import win32ui

from src import operation, utils
from src.jijian import jijian
from src.xinlai import xinlai


def openMoniqi():
    operation.deskClick(2, "left", 'pic/moniqi.png', 1)
    print("打开模拟器")


def init():
    operation.parentWin = win32gui.FindWindow('LDPlayerMainFrame', '雷电模拟器')
    operation.moniqiWin = operation.getMoniqiWin()

    win32gui.SetForegroundWindow(operation.parentWin)
    operation.winMove()

    if operation.moniqiWin == 0:
        print('未找到模拟器请重试')
        exit()
    print('为了保证程序正常运行,执行中请勿调整窗口大小!')

    # 创建paddle
    operation.myPaddle = operation.getPaddle()

    # 创建截图
    left, top, right, down = win32gui.GetWindowRect(operation.moniqiWin)
    operation.scWidth = right - left
    operation.scHeight = down - top
    operation.scHdc = win32gui.GetWindowDC(operation.moniqiWin)
    operation.scDc = win32ui.CreateDCFromHandle(operation.scHdc)
    operation.scMdc = operation.scDc.CreateCompatibleDC()
    operation.scBm = win32ui.CreateBitmap()
    operation.scBm.CreateCompatibleBitmap(operation.scDc, operation.scWidth, operation.scHeight)
    operation.scMdc.SelectObject(operation.scBm)


def getWeek():
    data = datetime.datetime.now()
    return datetime.date(data.year, data.month, data.day).weekday()


def inputCheck(s, num):
    s = utils.retainLetter(s).lower()
    if len(s) == 0:
        return True
    for k in s:
        if ord(k) > 96 + num:
            return True
    return False


if __name__ == '__main__':
    print('明日方舟自动脚本启动~')
    # openMoniqi()
    init()
    time.sleep(1)
    # benList1 = [['红票', '盾奶小', '盾奶大', '法狙小', '法狙大'], ['技巧书', '龙门币', '法狙小', '法狙大', '剑特小', '剑特大'],
    #             ['技巧书', '先辅小', '先辅大', '剑特小', '剑特大'], ['红票', '龙门币', '盾奶小', '盾奶大', '先辅小', '先辅大'],
    #             ['技巧书', '盾奶小', '盾奶大', '法狙小', '法狙大'], ['红票', '龙门币', '先辅小', '先辅大', '法狙小', '法狙大', '剑特小', '剑特大'],
    #             ['技巧书', '红票', '龙门币', '盾奶小', '盾奶大', '先辅小', '先辅大', '剑特小', '剑特大']]
    # benList2 = ['上一次作战', '1-7', '剿灭', '经验本']
    # week = getWeek()
    # benList3 = benList2 + benList1[week]
    # lenNum = len(benList3)
    # for i in range(lenNum):
    #     print('['+chr(97+i)+']'+benList3[i]+' ', end='')
    # print()
    # print('今天周'+str(week+1)+',博士请选择今天刷什么(多次填写字母按照顺序刷,最后一个字母循环刷,体力不足自动结束.如填写ccb就表示刷2次剿灭剩下体力刷1-7)')
    # cho = input()
    # while inputCheck(cho, lenNum):
    #     print('不在选项范围内,请重新输入:')
    #     cho = input()
    # for i in range(len(cho) - 1):
    #     index = ord(cho[i]) - 97
    #     print('执行:' + benList3[index])
    # print('循环执行:' + benList3[ord(cho[-1]) - 97])


    # operation.backClick2Img(config.appIcon)
    # operation.backClick2Img(config.startIcon)
    # operation.backClick2Img(config.loginIcon)
    # print('进入游戏')
    # time.sleep(15)

    # ocrRes = operation.strOCR()  # 识别结果
    # pprint.pprint(ocrRes)
    # longMenBiNum = utils.retainNum(utils.findStr2P(ocrRes, config.longMenBiPoint))
    # heChengYuNum = utils.retainNum(utils.findStr2P(ocrRes, config.heChengYuPoint))
    # yuanShiNum = utils.retainNum(utils.findStr2P(ocrRes, config.yuanShiPoint))
    # tiLiNum = utils.retainNum(utils.findStr2P(ocrRes, config.tiLiPoint))
    # print('当前龙门币数量为' + str(longMenBiNum) + '  当前合成玉数量为' + str(heChengYuNum) + '  当前原石数量为' + str(
    #     yuanShiNum) + '  当前体力为' + str(tiLiNum))

    # for i in range(100):
    #     operation.screenshotPath('pic/temp/login%s.bmp' % i)
    #     time.sleep(0.5)

    operation.screenshotPast()
    jijian.start()
    time.sleep(5)
    xinlai.start()
