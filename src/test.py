import copy
import datetime

if __name__ == '__main__':
    data = datetime.datetime.now()
    print(data)
    a = datetime.date(data.year, data.month, data.day).weekday()
