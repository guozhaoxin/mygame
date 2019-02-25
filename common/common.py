#encoding:utf8
__author__ = 'gold'

# import win32api,win32con
import tkinter as tk
from tkinter import filedialog,messagebox
import pygame
import sys

# def chooseExit():
#     '''
#     show the choosen box to decide if exit the game or not
#     :return:int,1: never exit;
#                 0: exit
#     '''
#     choice = win32api.MessageBox(0, "close the game?", "close game",win32con.MB_YESNO)
#     return choice - 6

def chooseFile():
    '''
    this method is used to let the player choose a file to continue a saved game
    :return: str,represent a file's absolute path the player chooses,else None
    '''
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path != '':
        return file_path
    return

# def chooseSaveGame(data,method):
#     '''
#     the player decides to save the game or not
#     :param data: [[int],],
#     :param method:a callable object, a function to save the game,it needs a param to save
#     :return:
#     '''
#     choice = win32api.MessageBox(0, "save the game?", "save game",win32con.MB_YESNO)
#     if choice == 6:
#         method(data)
#         win32api.MessageBox(0,'success to save','info',win32con.MB_OK)

def exitGame():
    '''
    when the game is closed,execute pygame.quit and sys.exit
    :return:
    '''
    pygame.quit()
    sys.exit()


def chooseExit():
    return messagebox.askyesno('exit the game','exit?')

def chooseSaveGame(data,method):
    '''
    let the player decide if save the game or not.
    :param data: the game current data to save
    :param method: a function object to indicate how to save the game.
    :return: None
    '''
    choice = messagebox.askyesno('save the game','save?')
    if choice:
        method(data)
        messagebox.Message(title = "save",message = "success").show()