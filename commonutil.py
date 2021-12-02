# commonutil
import numpy as np

def getdata(colnum, data):
    resultlist = []
    for i, d in enumerate(data):
        resultlist.append(data[i][colnum])
    return resultlist

def getavg(start, avgnum, datalist):
    result = list(map(int, datalist[start:start + avgnum]))
    return int(np.average(result))


