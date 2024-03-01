import time

from src import operation
from src.jijian import maoyi, chijin, jingyan, fadian, sushe, bangong, xiansuo


def start():

    operation.clickNextNode((950, 600), 5)

    fadian.start()
    time.sleep(1)

    maoyi.start()
    time.sleep(1)

    chijin.start()
    time.sleep(1)

    jingyan.start()
    time.sleep(1)

    bangong.start()
    time.sleep(1)

    xiansuo.start()
    time.sleep(1)

    sushe.start()
    time.sleep(1)

    operation.backClick((1220, 93))
    operation.backClick((188, 684))
    operation.backClick((188, 684))
    operation.backClick((188, 684))
    operation.backClick((188, 684))
    operation.backClick((188, 684))

    operation.backClick((464, 42))
    operation.clickNextNode((68, 38))


def testStart():
    print('test')
    maoyi.testStart()
