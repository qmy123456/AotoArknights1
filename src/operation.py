import ctypes
import sys
import time

import cv2
import numpy
import pyautogui
import win32api
import win32con
import win32gui
from paddleocr import PaddleOCR

from src import config, utils

parentWin = None
moniqiWin = None
myPaddle = None

scHdc = None
scDc = None
scMdc = None
scBm = None
scWidth = None
scHeight = None


def getParentWin():
    return win32gui.FindWindow('LDPlayerMainFrame', '雷电模拟器')


def getMoniqiWin():
    return win32gui.FindWindowEx(parentWin, None, 'RenderWindow', 'TheRender')


def getPaddle():
    return PaddleOCR()


def win2Top():
    win32gui.SetForegroundWindow(parentWin)


def winMove():
    ctypes.windll.user32.SetWindowPos(parentWin, 0, 99, 66, 0, 0, 0x0001 | 0x0004)  # 改变位置


# win+D 显示桌面
def winD():
    win32api.keybd_event(91, 0, 0, 0)  # 按下win键
    win32api.keybd_event(68, 0, 0, 0)  # 按下d键
    win32api.keybd_event(91, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放Ctrl键
    win32api.keybd_event(68, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)


# 无遮挡点击
def deskClick(clickTimes, lOrR, img, reTry):
    if reTry == 1:
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                break
            print("等待程序加载,1秒后重试")
            time.sleep(1)
    elif reTry == -1:
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
            time.sleep(0.5)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.5)


# 根据传入图片后台点击
def backClick2Img(img, sleepTime=1, reTry=0):
    print('src:' + img)
    p = findImgPoint(img, reTry)
    backClick(p, sleepTime)


# 根据点坐标后台点击
def backClick(p, sleepTime=1):
    if p is None:
        return
    location = win32api.MAKELONG(int(p[0]), int(p[1]))
    win32api.PostMessage(moniqiWin, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, location)
    win32api.PostMessage(moniqiWin, win32con.WM_LBUTTONUP, None, location)
    time.sleep(sleepTime)
    print('鼠标点击位置' + str(p) + 'sleepTime:' + str(sleepTime))


# 鼠标移动 p点 偏移量 速度 休眠时间
def backXMove(p, size, speed, sleepTime=2):
    if p is None:
        return
    if size == 0:
        return
    win32api.PostMessage(moniqiWin, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(p[0], p[1]))

    if size < 0:
        speed = -speed
    ran = range(0, size + speed, speed)
    for i in ran:
        win32api.PostMessage(moniqiWin, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,
                             win32api.MAKELONG(p[0] + i, p[1]))
        time.sleep(0.1)
    win32api.PostMessage(moniqiWin, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,
                         win32api.MAKELONG(p[0] + ran[-1], p[1]))
    time.sleep(0.1)

    win32api.PostMessage(moniqiWin, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                         win32api.MAKELONG(p[0] + ran[-1], p[1]))
    time.sleep(sleepTime)


# 鼠标移动 p点 偏移量 速度 休眠时间
def backYMove(p, size, speed, sleepTime=2):
    if p is None:
        return
    if size == 0:
        return

    win32api.PostMessage(moniqiWin, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(p[0], p[1]))

    if size < 0:
        speed = -speed

    for i in range(0, size, speed):
        win32api.PostMessage(moniqiWin, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,
                             win32api.MAKELONG(p[0], p[1] + i))
        time.sleep(0.1)

    win32api.PostMessage(moniqiWin, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                         win32api.MAKELONG(p[0], p[1] + size))
    time.sleep(sleepTime)


def closeScreenshot():
    # 销毁
    win32gui.DeleteObject(scBm.GetHandle())
    scMdc.DeleteDC()
    scDc.DeleteDC()
    win32gui.ReleaseDC(moniqiWin, scHdc)


# 截取图片
def screenshot():
    # 画图
    scMdc.BitBlt((0, 0), (scWidth, scHeight), scDc, (0, 0), win32con.SRCCOPY)
    # 保存成图片
    scBm.SaveBitmapFile(scMdc, config.exeImg)


# p1左上角 p2右下角
def screenshot2P(p1, p2):
    y = p2[1] - p1[1]
    x = p2[0] - p1[0]

    # 画图
    scMdc.BitBlt((0, 0), (x, y), scDc, p1, win32con.SRCCOPY)
    # 保存成图片
    scBm.SaveBitmapFile(scMdc, config.exeImg)


# 截取图片
def screenshotPast():
    # 画图
    scMdc.BitBlt((0, 0), (scWidth, scHeight), scDc, (0, 0), win32con.SRCCOPY)
    # 保存成图片
    scBm.SaveBitmapFile(scMdc, config.pastexeImg)


# 截取图片
def screenshotPath(path):
    # 画图
    scMdc.BitBlt((0, 0), (scWidth, scHeight), scDc, (0, 0), win32con.SRCCOPY)
    # 保存成图片
    scBm.SaveBitmapFile(scMdc, path)


# def screenshot():
#     # 截取exe图片
#     left, top, right, down = win32gui.GetWindowRect(moniqiWin)
#     width = right - left
#     height = down - top
#     # 获取设备上下文
#     hdc = win32gui.GetWindowDC(moniqiWin)
#     # 获取设备描述表
#     dc = win32ui.CreateDCFromHandle(hdc)
#     # 获取兼容的设备描述表
#     mdc = dc.CreateCompatibleDC()
#     # 创建位图
#     bm = win32ui.CreateBitmap()
#     # 创建兼容的位图
#     bm.CreateCompatibleBitmap(dc, width, height)
#     # 替换对象
#     mdc.SelectObject(bm)
#     # 画图
#     mdc.BitBlt((0, 0), (width, height), dc, (0, 0), win32con.SRCCOPY)
#     # 保存成图片
#     bm.SaveBitmapFile(mdc, config.exeImg)
#     # 销毁
#     win32gui.DeleteObject(bm.GetHandle())
#     mdc.DeleteDC()
#     dc.DeleteDC()
#     win32gui.ReleaseDC(moniqiWin, hdc)


# 图片匹配
def findImgPoint(img, reTry=0):
    # 获取需要匹配图片对象信息
    template = cv2.imread(img)
    h, w, l = template.shape
    # 图片匹配
    while reTry <= 0:
        screenshot()
        exebmp = cv2.imread(config.exeImg)
        result = cv2.matchTemplate(exebmp, template, cv2.TM_CCOEFF_NORMED)
        minval, maxval, minloc, maxloc = cv2.minMaxLoc(result)
        print('图片相似度:' + str(maxval))
        if maxval > 0.8:
            temp = list(maxloc)
            temp[0] += int(h / 2)
            temp[1] += int(w / 2)
            return temp
        else:
            print("等待程序加载,1秒后重试")
            time.sleep(1)

    i = 0
    while i < reTry:
        screenshot()
        exebmp = cv2.imread(config.exeImg)
        result = cv2.matchTemplate(exebmp, template, cv2.TM_CCOEFF_NORMED)
        minval, maxval, minloc, maxloc = cv2.minMaxLoc(result)
        print('图片相似度' + str(maxval))
        if maxval > 0.8:
            temp = list(maxloc)
            temp[0] += int(h / 2)
            temp[1] += int(w / 2)
            return temp
        else:
            i += 1
            print("等待程序加载,1秒后重试")
            time.sleep(1)
            if i >= reTry:
                print("加载超时")


def strOCR():
    screenshot()  # 截屏
    return myPaddle.ocr(config.exeImg)  # 识别结果


# 根据点p找文字
def pfindStr(p):
    return utils.findStr2P(strOCR(), p)


def findDrawAllImg(img):
    screenshot()
    template = cv2.imread(img)
    h, w, l = template.shape
    exebmp = cv2.imread(config.exeImg)
    result = cv2.matchTemplate(exebmp, template, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = numpy.where(result >= 0.7)
    for x, y in zip(xloc, yloc):
        cv2.rectangle(exebmp, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.imwrite('pic/temp/res.png', exebmp)


def findAllImgRect(img, sim):
    screenshot()
    template = cv2.imread(img)
    h, w, l = template.shape
    exebmp = cv2.imread(config.exeImg)
    result = cv2.matchTemplate(exebmp, template, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = numpy.where(result >= sim)
    rectList = []
    for x, y in zip(xloc, yloc):
        p = [[x, y], [x + w, y + h]]
        rectList.append(p)
    utils.filterSimilar(rectList, 5)
    return rectList


def findAllImgRect2P(img, p1, p2, sim):
    screenshot2P(p1, p2)
    template = cv2.imread(img)
    h, w, l = template.shape
    exebmp = cv2.imread(config.exeImg)
    result = cv2.matchTemplate(exebmp, template, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = numpy.where(result >= sim)
    rectList = []
    for x, y in zip(xloc, yloc):
        p = [[x, y], [x + w, y + h]]
        rectList.append(p)
    utils.filterSimilar(rectList, 5)
    return rectList


def img_similarity(img1_path, img2_path):
    img = cv2.imread(img1_path)
    img1 = cv2.imread(img2_path)
    # 计算图img的直方图
    H1 = cv2.calcHist([img], [1], None, [256], [0, 256])
    H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理

    # 计算图img2的直方图
    H2 = cv2.calcHist([img1], [1], None, [256], [0, 256])
    H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)

    # 利用compareHist()进行比较相似度
    similarity = cv2.compareHist(H1, H2, 0)
    return similarity


def isIn(sim=0.9):
    res = img_similarity(config.exeImg, config.pastexeImg)
    print('图片相似度'+str(res))
    if res < sim:
        return False
    else:
        return True


def clickNextNode(p, sleepTime=1, maxTry=10):
    backClick(p, sleepTime)
    screenshot()
    inNum = 0
    while isIn():
        print('进入失败,再次尝试')
        backClick(p, sleepTime)
        screenshot()
        inNum += 1
        if inNum > maxTry:
            print('失败次数太多 脚本自动关闭')
            sys.exit()
            return
    screenshotPast()
