#encoding:utf8
__author__ = 'gold'

import time
import os
import win32api,win32con

gamesParDoc =  './' + 'SavedGames/' # this is the ralative document to save all saved-games files.
numSet = set([2 ** i for i in range(1,12)] + [0]) # this set contains values that only can be accepted in this game,
                                                  # and these values all 0 or num power of 2 less than 4096.
def saveMatrix(matrix):
    '''
    save the matrix so the player can continue work on the matrix next time.
    :param matrix: [[int],],you konw.
    :return:
    '''

    #firstly check if the doc exists or not.
    if not os.path.exists(gamesParDoc):
        os.mkdir(gamesParDoc)

    filename = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.txt' # the file to save the game now,use date
                                                                             # and time as filename in case of
                                                                             # duplicate name

    filePath = gamesParDoc + filename
    with open(filePath,'w') as f:
        for vector in matrix:
            line = ' '.join(map(lambda x:str(x),vector))
            f.write(line)
            f.write('\n')

def split2numlist(s:str):
    '''
    this function is used to split any string object to a num list,
    :param s: str,the str obj to be splited into a num list
    :return: [[int],],a integer matrix ,size n * n
    '''
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
    '''
    read a file to generate the game's matrix;
    this function will have to judge if the file is a valid vile,this means:
        1 this file contains and only 4 lines;
        2 every line in this file will only be splited 4 parts
        3 every line in this line only contains space or digit(0-9)
        4 the nums in this file can only be (0,2,4,8,16,32,64,128,256,512,1024,2048)
    if one of the above condition can not match,a Exception will be raised;
    else return the corresponding matrix and the file will be removed in this func.
    :param file: str,a absolute file name
    :return:[[int],],as you know,bute if the file's format is wrong,the function will raise a Exception.
    '''
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
        if len(matrix) != 4:
            raise Exception('wrong format')
        os.remove(file)
        return matrix
    except:
        return None

def chooseSavedMatrix():
    '''
    this function is used to let the player decide if save the game or not
    :return: int, 0: save
                  1: never save
    '''
    choice = win32api.MessageBox(0, "choose an old game?", "choose game", win32con.MB_YESNO)
    return choice - 6


if __name__ == '__main__':
    if os.path.exists(gamesParDoc):
        print('exit')
    else:
        os.mkdir(gamesParDoc)
        print('yexi')