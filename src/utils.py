import math
import re


# 计算点是否存在在四边形中
def isPointInQuad(quad, p):
    x = p[0]
    y = p[1]
    A = quad[0]
    B = quad[3]
    C = quad[2]
    D = quad[1]
    a = (B[0] - A[0]) * (y - A[1]) - (B[1] - A[1]) * (x - A[0])
    b = (C[0] - B[0]) * (y - B[1]) - (C[1] - B[1]) * (x - B[0])
    c = (D[0] - C[0]) * (y - C[1]) - (D[1] - C[1]) * (x - C[0])
    d = (A[0] - D[0]) * (y - D[1]) - (A[1] - D[1]) * (x - D[0])
    if (a > 0 and b > 0 and c > 0 and d > 0) or (a < 0 and b < 0 and c < 0 and d < 0):
        return True
    return False


def isPointInRect(rect, p):
    x = p[0]
    y = p[1]
    # x1 = rect[0][0]
    # y1 = rect[0][1]
    # x2 = rect[1][0]
    # y2 = rect[1][1]
    A = rect[0]
    B = [rect[0][0], rect[1][1]]
    C = rect[1]
    D = [rect[1][0], rect[0][1]]
    a = (B[0] - A[0]) * (y - A[1]) - (B[1] - A[1]) * (x - A[0])
    b = (C[0] - B[0]) * (y - B[1]) - (C[1] - B[1]) * (x - B[0])
    c = (D[0] - C[0]) * (y - C[1]) - (D[1] - C[1]) * (x - C[0])
    d = (A[0] - D[0]) * (y - D[1]) - (A[1] - D[1]) * (x - D[0])
    if (a > 0 and b > 0 and c > 0 and d > 0) or (a < 0 and b < 0 and c < 0 and d < 0):
        return True
    return False


# 通过文字找点
def findPoint2S(ocr, s):
    for i in ocr:
        if i[1][0] == s:
            if i[1][1] > 0.7:
                return getPoint2Rect(i[0])
            else:
                print('相似度不足无法判定')
    return None


# 通过点找文字
def findStr2P(ocr, p):
    for i in ocr:
        if isPointInQuad(i[0], p):
            if i[1][1] > 0.7:
                return i[1][0]
            else:
                print('相似度不足无法判定')
                return 'null0'
    print('没有在' + str(p) + '点找到文字')
    return 'null0'


# 匹配字母
def retainLetter(s):
    if s is None:
        return 'null'
    mo = re.compile(r'[A-Za-z]+').findall(s)
    l = ''
    for i in mo:
        l += i
    return l


# 匹配数字
def retainNum(s):
    if s is None:
        return 'null'
    mo = re.compile(r'\d+').findall(s)
    l = ''
    for i in mo:
        l += i
    return l


# 匹配字母汉字
def retainStr(s):
    if s is None:
        return 'null'
    mo = re.compile(r'[\u4e00-\u9fa5A-Za-z]+').findall(s)
    l = ''
    for i in mo:
        l += i
    return l


# 谁便获取矩形中一点坐标
def getPoint2Rect(rect: object) -> object:
    return (rect[1][0] - rect[0][0]) / 2 + rect[0][0], (rect[1][1] - rect[0][1]) / 2 + rect[0][1]


# 把2维数组变1维
def list2to1(o):
    res = []
    for i in o:
        for k in i:
            res.append(k)
    return res


def backDelStr(s, num):
    listStr = list(s)
    for i in range(num):
        if len(listStr) != 0:
            del listStr[-1]
    st = ''
    for i in listStr:
        st += i
    return st


# 根据y轴给矩形坐标排序
def rectOrderY(rectList):
    # orderList = []
    lenNum = len(rectList)
    for i in range(lenNum):
        for j in range(lenNum - i - 1):
            if rectList[j] > rectList[j + 1]:
                t = 0
                t = rectList[j + 1][0][1]
                rectList[j + 1][0][1] = rectList[j][0][1]
                rectList[j][0][1] = t


def filterSimilar(rectList, sim):
    needDel = []
    lenNum = len(rectList)
    for i in range(0, lenNum - 1):
        p1 = getPoint2Rect(rectList[i])
        for k in range(i + 1, lenNum):
            p2 = getPoint2Rect(rectList[k])
            if pDistance(p1, p2) < sim:
                needDel.append(rectList[k])
    for i in needDel:
        if i in rectList:
            rectList.remove(i)


def pDistance(p1, p2):
    p3 = (p2[0] - p1[0], p2[1] - p1[1])
    return math.hypot(p3[0], p3[1])
