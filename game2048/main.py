#encoding:utf8
__author__ = 'gold'

import sys,os

# the under line must be executed as to ensure the main.py can work without adding
# mygame to the environment
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import pygame
from pygame.locals import K_LEFT,K_RIGHT,K_DOWN,K_UP,KEYDOWN,K_ESCAPE
# import win32api,win32con

from game2048.merge import getNewMatrix,leftMerge,rightMerge,bottomMerge,topMerge,\
    getState,not_over,random2
from game2048.files import saveMatrix,readMatrix
from common.common import chooseExit,exitGame,importGameData,saveGame,prepare

SIZE = 500  # the size of the whole panel of the game(not include the surrounding edges)
GRID_LEN = 4  # the row and col count of the square
LINE_SIZE = 5  # the border width of every square
lengthen = SIZE // GRID_LEN  # get the size of every square(including the edges left-right or top-bottom of the square)
assert lengthen > LINE_SIZE * 2  # the lengthen of the square must be larger than the LINE'S size

BACKGROUND_COLOR_GAME = (146, 135, 112)  # the background color of the main panel
BACKGROUND_COLOR_CELL_EMPTY = (158, 148, 138)  # the color of the empty cell
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
} # this dict is used to assign every square a different color according to their value

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

win_lose_font = 'freesansbold.ttf' #this is the win or lose str font at the end of the game
win_lose_size = 80 #the win or lose str size on the panel
win_lose_color = (145, 44, 238) #the color of the win or lose str on the panel


def drawPanel(matrix):
    '''
    this function is used to draw the main panel according the matrix
    this function will scan the matrix which is n * n matrix containing nums 0 and power of 2,
    then according to the value it meets every time,it draws the num square on corresponding row and col position.
    :param matrix: [[int,],],a matrix size of n * n,and nums in this matrix are all 0 or power of 2.
    :return:None
    '''

    DISPLAYSURF.fill(BACKGROUND_COLOR_GAME) #fill the main panel,every graph is drawn on the panel

    for row in range(len(matrix)):
        for col in range(len(matrix)):
            color = BACKGROUND_COLOR_DICT[matrix[row][col]] #get the rect color according to corresponding value in the matrix
            x = lengthen * col
            y = lengthen * row

            #the code under is to draw square on the main panel,we can modify this part in a new independent method.
            #firstly draw the square
            pygame.draw.rect(DISPLAYSURF,color,(x + LINE_SIZE,y + LINE_SIZE,lengthen - 2 * LINE_SIZE,lengthen - 2 * LINE_SIZE))
            #we only draw those nums whose value is larger than 0
            if matrix[row][col] > 0:
                textSurfaceObj,textRectObj = drawFont(str(matrix[row][col]),font,font_size,x + lengthen // 2,y + lengthen // 2,color = CELL_NUM_COLOR[matrix[row][col]])
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawRes(matrix,result):
    '''
    this function is used to draw the result;
    no matter the player win or lose the game,the corresponding result will be drawn here.
    :param matrix: [[int],],n * n matrix,representing the matrix of the game.
    :param result: str,the result of the game,win or lose,besiedes you can pass any other str here.
    :return: None
    '''
    drawPanel(matrix) #firstly draw the main panel, as the player can be sure he wins or loses.
    textSurObj,textRectObj = drawFont(result,win_lose_font,win_lose_size,SIZE // 2,SIZE // 2,color = win_lose_color)
    DISPLAYSURF.blit(textSurObj,textRectObj)

def drawFont(content:str,font:str,fontsize:int,centerx:int,centery:int,color = win_lose_color,antialias:bool = False,backColor = None):
    '''
    this method is used to draw some str on a given position with given font and fontsize;
    while the font object will be returned
    :param content: str,the content to be drawn.
    :param font: str,indicating the font name used to draw the font object.
    :param fontsize: int,indicating the size of the font object
    :param centerx: int, the center x of the content on the main panel
    :param centery: int,the center y of the content on the main panel
    :param antialias: bool,if antialias or not
    :param color:tuple or other appropriate type to represent a kind of color obj, here it's the color of the
            color of the content
    :param backColor: consistent with the param color,but is the color of the background of the content
    :return: pygame.surface.Surface, to bear the Font object;
             the textRectObj
    '''
    fontObj = pygame.font.SysFont(font,fontsize,bold = True)
    textSurfaceObj = fontObj.render(content,antialias,color,backColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (centerx,centery)
    return textSurfaceObj,textRectObj

def mergeHandler(matrix,event):
    '''
    this function is used to update the matrix according the player's keydown,and tell the game if it needs to generate
    a new num.
    example:
        if the player presses left,then this function calls leftMerge to update the matrix and return if the matrix can
            really move from right to left.
    :param matrix:[[int],],as you know
    :param event: the key-down event,the func must use this param to decide what to do
    :return:bool,if the matrix needs update,then return True,which will generate a new num in the matrix at a random valid pos,
                  else the matrix is never updated, ie when all the nums are on the left of the matrix while the
                  player presses the left-key,then the matrix cannot updated and no a random num will be generated.
    '''
    ok = False
    if event.key == K_LEFT:
        ok = leftMerge(matrix)
    elif event.key == K_RIGHT:
        ok = rightMerge(matrix)
    elif event.key == K_UP:
        ok = topMerge(matrix)
    elif event.key == K_DOWN:
        ok = bottomMerge(matrix)
    return ok

def drawMainUp(matrix):
    '''
    this function is used to draw the matrix on the main panel and update the DISPLAYSURF
    :param matrix: [[int],], n * n matrix
    :return:
    '''
    drawPanel(matrix)
    pygame.display.update()

def runGame(matrix):
    '''
    this method is used to run the game
    :param matrix,[[int],],the matrix , as you know
    :return
    '''
    drawMainUp(matrix)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                exitChoose = chooseExit()
                if exitChoose:
                    exitGame()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exitChoose = chooseExit()
                    if exitChoose:
                        saveGame(matrix,saveMatrix)
                        exitGame()
                    else:
                        continue

                ok = mergeHandler(matrix,event)
                if ok:
                    random2(matrix)
                drawMainUp(matrix)
        status = getState(matrix)
        if status != not_over: #this means the game has over not matter win or lose.
            drawRes(matrix,status)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    exitGame()

def main():
    '''
    this is the main function, run the function to run the game,and this function can be invoked by anyone.
    :return:
    '''
    global DISPLAYSURF
    matrix = importGameData(readMatrix)
    if not matrix:
        matrix = getNewMatrix(GRID_LEN)  #the matrix to represent the num on the panel
        random2(matrix)
        random2(matrix)
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SIZE,SIZE))
    pygame.display.set_caption('2048')

    runGame(matrix)


if __name__ == '__main__':
    prepare()
    main()