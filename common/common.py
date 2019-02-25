#encoding:utf8
__author__ = 'gold'

# import win32api,win32con
import tkinter as tk
from tkinter import filedialog,messagebox
import pygame
import sys


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


def exitGame():
    '''
    when the game is closed,execute pygame.quit and sys.exit
    :return:
    '''
    pygame.quit()
    sys.exit()


def chooseExit():
    return messagebox.askyesno('exit the game','exit?')

def saveGame(data,method):
    '''
    let the player decide if save the game or not.
    :param data: the game current data to save
    :param method: a function object to indicate how to save the game.
    :return: None
    '''
    choice = messagebox.askyesno('save the game','save?')
    if choice:
        method(data)
        messagebox.Message(title = "save",message = "save success").show()

def importGameData(readMethod):
    '''
    let the player decide if import a saved game's data or not
    :param readMethod: a function object,used to indicate how to load a saved game data,the function accept on parameter to indicate the data's path.
    :return: data,the saved game data.
    '''
    data = None
    while True:
        choice = messagebox.askyesno('choose','choose an old game?')
        if choice:
            file = chooseFile()
            if not file:
                messagebox.showerror('error','file error!')
                continue
            data = readMethod(file)
            if not data:
                messagebox.showerror('error','file error!')
            else:
                break
        else:
            break
    return data

def init():
    '''
    this method is used to execute some initial for every game at the beginning.
    :return:
    '''
    pygame.init()
    tk.Tk().withdraw()