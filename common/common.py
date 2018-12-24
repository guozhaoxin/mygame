#encoding:utf8
__author__ = 'gold'

import win32api,win32con

def chooseExit():
    '''
    show the choosen box to decide if exit the game or not
    :return:int,1:exit;
                0:never exit
    '''
    choice = win32api.MessageBox(0, "exit the game?", "yes",win32con.MB_YESNO)
    if choice == 7:
        return 0
    return 1
