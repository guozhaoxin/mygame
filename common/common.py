#encoding:utf8
__author__ = 'gold'

import win32api,win32con
import tkinter as tk
from tkinter import filedialog


def chooseExit():
    '''
    show the choosen box to decide if exit the game or not
    :return:int,1:exit;
                0:never exit
    '''
    choice = win32api.MessageBox(0, "close the game?", "close game",win32con.MB_YESNO)
    return choice

def chooseFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path != '':
        return file_path
    return

def chooseSaveGame(data,method):
    choice = win32api.MessageBox(0, "save the game?", "save game",win32con.MB_YESNO)
    if choice == 6:
        method(data)
        win32api.MessageBox(0,'success to save','info',win32con.MB_OK)