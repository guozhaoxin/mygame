#encoding:utf8
__author__ = 'gold'

import pygame
import pygame.locals
from pygame.locals import K_LEFT,K_RIGHT,K_DOWN,K_UP,KEYDOWN,K_ESCAPE
import sys
import win32api,win32con

from game2048.merge import getNewMatrix,setMatrix,leftMerge,rightMerge,bottomMerge,topMerge,\
    win,lose,getState,not_over
from game2048.files import saveMatrix,chooseSavedMatrix,readMatrix
from common.common import chooseExit,chooseSaveGame,chooseFile

SIZE = 500 #the size of the whole panel of the game(not include the surrounding edges)
GRID_LEN = 4 #the row and col count of the square
LINE_SIZE = 5 #the border width of every square

BACKGROUND_COLOR_GAME = (146, 135, 112) #the background color of the main panel
BACKGROUND_COLOR_CELL_EMPTY = (158, 148, 138) #the color of the empty cell
BACKGROUND_COLOR_DICT = {
    0:(171, 202, 188),
    2:(238, 228, 218),
    4:(237, 224, 200),
    8:(242, 177, 121),
    16:(245, 149, 99),
    32:(246, 124, 95),
    64:(246, 94, 59),
    128:(237, 207, 114),
    256:(237, 204, 97),
    512:(237, 200, 80),
    1024:(237, 197, 63),
    2048:(237, 194, 46)
} #this dict is used to assign every square a different color according their value

CELL_NUM_COLOR = {
    2:(137, 194, 46),
    4:(237, 197, 63),
    8:(37, 240, 80),
    16:(237, 254, 197),
    32:(7, 207, 114),
    64:(59, 94, 246),
    128:(246, 124, 95),
    256:(245, 149, 99),
    512:(242, 177, 121),
    1024:(237, 224, 200),
    2048:(238, 228, 218)
} #this dict is used assign every num(more than 0) a differen color,so they can be distinguished from their
  #square and the main panel and other num.
font = 'freesansbold.ttf' #this is the font of the number
font_size = 40 #this is the size of the number

win_lose_font = 'arial' #this is the win or lose str font at the end of the game
win_lose_size = 80 #the win or lose str size on the panel
win_lose_color = (158, 148, 138) #the color of the win or lose str on the panel


def drawPanel(matrix):
    '''
    this function is used to draw the main panel according the matrix
    this function will scan the matrix which is n * n matrix containing num power of 2 and 0,
    then according to the value it meet,it draw the num square on corresponding row and col position.
    :param matrix: [[int,],],a matrix size of n * n,and nums in this matrix are all power of 2 or 0.
    :return:None
    '''
    DISPLAYSURF.fill(BACKGROUND_COLOR_GAME) #fill the main panel,every graph is drawn on the panel
    lengthen = SIZE // GRID_LEN #get the size of every square(including the edges of the square),
                                #we can store the value in a fixed variable avoiding repetitive calculation.

    for row in range(len(matrix)):
        for col in range(len(matrix)):
            color = BACKGROUND_COLOR_DICT[matrix[row][col]] #get the rect color according to corresponding value in the matrix
            x = lengthen * col
            y = lengthen * row
            pygame.draw.rect(DISPLAYSURF,color,(x + LINE_SIZE,y + LINE_SIZE,lengthen - 2 * LINE_SIZE,lengthen - 2 * LINE_SIZE))
            if matrix[row][col] > 0:
                fontObj = pygame.font.Font(font,font_size)
                textSurfaceObj = fontObj.render(str(matrix[row][col]),False,CELL_NUM_COLOR[matrix[row][col]])
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (x + lengthen // 2,y + lengthen // 2)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawRes(matrix,result):
    drawPanel(matrix)
    fontObj = pygame.font.SysFont(win_lose_font,win_lose_size)
    textSurObj = fontObj.render(result,False,win_lose_color)
    textRectObj = textSurObj.get_rect()
    textRectObj.center = (SIZE // 2,SIZE // 2)
    DISPLAYSURF.blit(textSurObj,textRectObj)


def runGame(matrix):
    '''
    the run game part
    :return:
    '''
    drawPanel(matrix)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                value = chooseExit()
                if value != 0:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    value = chooseExit()
                    if value == 6:
                        chooseSaveGame(matrix,saveMatrix)
                        pygame.quit()
                        sys.exit()
                    else:
                        continue
                ok = False
                if event.key == K_LEFT:
                    ok = leftMerge(matrix)
                elif event.key == K_RIGHT:
                    ok = rightMerge(matrix)
                elif event.key == K_UP:
                    ok = topMerge(matrix)
                elif event.key == K_DOWN:
                    ok = bottomMerge(matrix)
                if ok:
                    setMatrix(matrix)
                drawPanel(matrix)
                pygame.display.update()

        status = getState(matrix)
        if status != not_over:
            drawRes(matrix,status)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

def main():
    global DISPLAYSURF
    matrix = None
    while True:
        choice = chooseSavedMatrix()
        if choice == 6:
            file = chooseFile()
            if not file:
                win32api.MessageBox(0,'file error','wrong',win32con.MB_OK)
                continue
            matrix = readMatrix(file)
            if not matrix:
                win32api.MessageBox(0, 'file error', 'wrong', win32con.MB_OK)
            else:
                break
        else:
            break
    if not matrix:
        matrix = getNewMatrix(GRID_LEN)  #the matrix to represent the num on the panel
        setMatrix(matrix)
        setMatrix(matrix)
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SIZE,SIZE))
    pygame.display.set_caption('2048')

    runGame(matrix)


if __name__ == '__main__':
    main()