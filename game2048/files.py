#encoding:utf8
__author__ = 'gold'

import time
import sys
import os
import win32api,win32con

gamesParDoc =  './' + 'SavedGames/'
numSet = set([2 ** i for i in range(1,12)] + [0])

def saveMatrix(matrix):
    if not os.path.exists(gamesParDoc):
        os.mkdir(gamesParDoc)
    filename = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.txt'
    filePath = gamesParDoc + filename
    print(filePath)
    with open(filePath,'w') as f:
        for vector in matrix:
            line = ' '.join(map(lambda x:str(x),vector))
            f.write(line)
            f.write('\n')

def split2numlist(s:str):
    if not s:
        return
    numList = []
    index = 0
    while index < len(s):
        if len(numList) > 4:
            return
        if not s[index].isdigit():
            index += 1
            continue
        end = index
        while end < len(s) and s[end].isdigit():
            end += 1
        num = int(s[index:end])
        if num not in numSet:
            return
        numList.append(num)
        index = end
    return numList


def readMatrix(file):
    matrix = []
    try:
        with open(file,'r') as f:
            for line in f.readlines():
                curLineList = split2numlist(line)
                if len(curLineList) != 4:
                    raise Exception('wrong format')
                matrix.append(curLineList)
                if len(matrix) > 4:
                    raise Exception('wrong format')
            return matrix
    except:
        return None

def chooseSavedMatrix():
    choice = win32api.MessageBox(0, "choose an old game?", "choose game", win32con.MB_YESNO)
    return choice


if __name__ == '__main__':
    if os.path.exists(gamesParDoc):
        print('exit')
    else:
        os.mkdir(gamesParDoc)
        print('yexi')