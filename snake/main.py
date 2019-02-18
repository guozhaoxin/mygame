#coding: utf-8
__author__ = 'gold'
__date__ = '2019/2/3'
__time__ = '18:36'
__filename__ = 'main.py'

import random,pygame,sys
from pygame.locals import *
import time
import math
from threading import Thread
import win32api,win32con


wormCoords = None
gameState = 'S'
appleState = True
speedBase = 8
FPS = speedBase
runningTime = 0
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0,'Window width must be a multiple of size'
assert WINDOWHEIGHT % CELLSIZE == 0,'Window height must be a multiple of size'

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255,255,255)
BLUE = (32,11,225)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (0,155,0)
DARKGRAY = (40,40,40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf',100)
    titleSurf1 = titleFont.render('wormy!',True,WHITE,DARKGREEN)
    titleSurf2 = titleFont.render('wormy!',True,GREEN)

    degrees1 = 0
    degrees2 = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1,degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2,WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1,rotatedRect1)
        rotatedSurf2 = pygame.transform.rotate(titleSurf2,degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2,WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2,rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() #在游戏正式开始之前清理事件队列
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7

def terminate():
    global gameState,DISPLAYSURF
    gameState = 'P'
    choice = win32api.MessageBox(0, "确定退出游戏？", "退出",win32con.MB_YESNO)
    if choice == 7:
        gameState = 'R'
        return
    gameState = 'S'
    pygame.quit()
    sys.exit()

def getRandomLocation(wormCoords):
    while True:
        a = {'x':random.randint(0,CELLWIDTH - 1),'y':random.randint(0,CELLHEIGHT - 1)}
        for coord in wormCoords:
            if a['x'] == coord['x'] and a['y'] == coord['y']:
                break
        else:
            break
    return a

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf',150)
    gameSurf = gameOverFont.render('GAME',True,WHITE)
    overSurf = gameOverFont.render('OVER',True,WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2,10)
    overRect.midtop = (WINDOWWIDTH / 2,gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf,gameRect)
    DISPLAYSURF.blit(overSurf,overRect)
    drawPressKeyMsg()
    pygame.display.update()

    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    global runningTime
    scoreSurf = BASICFONT.render('Score:%s' % (score),True,WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 100,10)
    DISPLAYSURF.blit(scoreSurf,scoreRect)

    timeSurf = BASICFONT.render('%s s' %(math.ceil(runningTime)),True,WHITE)
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (WINDOWWIDTH - 100,10 + scoreRect.height + 5)
    DISPLAYSURF.blit(timeSurf,timeRect)

    FPSSurf = BASICFONT.render('FPS:%s' %(FPS - 8),True,WHITE)
    FPSRect = FPSSurf.get_rect()
    FPSRect.topleft = (WINDOWWIDTH - 100,10 + scoreRect.height + timeRect.height + 5 + 5)
    DISPLAYSURF.blit(FPSSurf,FPSRect)

def drawWorm(wormCoords):
    x = wormCoords[HEAD]['x'] * CELLSIZE
    y = wormCoords[HEAD]['y'] * CELLSIZE
    wormHeadRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(DISPLAYSURF,BLUE,wormHeadRect)
    wormHeadInnerRect = pygame.Rect(x + 4,y + 4,CELLSIZE - 8,CELLSIZE - 8)
    pygame.draw.rect(DISPLAYSURF,RED,wormHeadInnerRect)
    for coord in wormCoords[1:]:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegementRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,DARKGREEN,wormSegementRect)
        wormInnerSegementRect = pygame.Rect(x + 4,y + 4,CELLSIZE - 8,CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF,GREEN,wormInnerSegementRect)

def drawApple(coord):
    global appleState

    if appleState:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,RED,appleRect)

def drawGrid():
    for x in range(0,WINDOWWIDTH,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,DARKGRAY,(x,0),(x,WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,DARKGRAY,(0,y),(WINDOWWIDTH,y))

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('press a key to play',True,DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect() #拿到啥了这是
    pressKeyRect.topleft = (WINDOWWIDTH - 200,WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None

    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def runGame():
    global speedBase,FPS,runningTime,wormCoords,gameState,musicState
    FPS = speedBase
    startx = random.randint(5,CELLWIDTH - 6)
    starty = random.randint(5,CELLHEIGHT - 6)
    wormCoords = [{'x':startx,'y':starty},{'x':startx - 1,'y':starty},{'x':startx - 2,'y':starty}]
    direction = RIGHT
    apple = getRandomLocation(wormCoords) #获得一个随机的事务
    gameState = 'R'

    #检查键盘事件
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_SPACE:
                    result = pause()
                    if result:
                        terminate()
                    gameState = 'R'
                elif event.key == K_ESCAPE:
                    terminate()
        #检查碰撞
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 \
            or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation(wormCoords)
            Thread(target=musicCapturePlay).start()
        else:
            del wormCoords[-1] #要删除最后一个，不过这样的方法确实更快

        #更改蛇身上的元素位置
        if direction == UP:
            newHead = {'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x':wormCoords[HEAD]['x'] - 1,'y':wormCoords[HEAD]['y']}
        else:
            newHead = {'x':wormCoords[HEAD]['x'] + 1,'y':wormCoords[HEAD]['y']}
        wormCoords.insert(0,newHead)

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        # drawScore(len(wormCoords) - 3)
        pygame.display.update()
        pygame.display.set_caption('score:%s time:%ss FPS:%s' % (len(wormCoords) - 3,math.ceil(runningTime),FPS - speedBase))
        FPSCLOCK.tick(FPS)


def pause():
    global gameState
    gameState = 'P'
    pauseFont = pygame.font.Font('freesansbold.ttf',100)
    pauseSurf = pauseFont.render('Paused',True,RED)
    pauseRect = pauseSurf.get_rect()
    pauseRect.midtop = (WINDOWWIDTH / 2,100)
    DISPLAYSURF.blit(pauseSurf,pauseRect)

    continueFont = pygame.font.Font('freesansbold.ttf',30)
    continueSurf = continueFont.render('press space to continue',True,WHITE)
    continueRect = continueSurf.get_rect()
    continueRect.midtop = (WINDOWWIDTH / 2,pauseRect.height + 100 + 10)
    DISPLAYSURF.blit(continueSurf,continueRect)
    pygame.display.update()

    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            if event.type == KEYUP and event.key == K_SPACE:
                return

def changeFPS():
    global gameState,FPS,wormCoords
    startLengthen = 0
    step = 0
    while True:
        if gameState == 'R' and wormCoords:
            nowLengthen = len(wormCoords) - 3
            if nowLengthen != startLengthen:
                step += 1
                startLengthen = nowLengthen
                if step % 20 == 0:
                    FPS += 1
                    step = 0
        elif gameState == 'S':
            step = 0
            startLengthen = 0
            FPS = speedBase
        elif gameState == 'P':
            continue

def countTime():
    global gameState,runningTime
    startTime = time.time()
    while True:
        if gameState == 'R':
            runningTime += time.time() - startTime
            startTime = time.time()
        elif gameState == 'P':
            startTime = time.time()
        elif gameState == 'S':
            startTime = time.time()
            runningTime = 0
        time.sleep(.2)

def changeAppleState():
    global appleState,gameState
    while True:
        if gameState == 'R':
            appleState = not appleState
        if appleState:
            time.sleep(0.8)
        else:
            time.sleep(0.2)

def musicCapturePlay():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load('./musics/卡通.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)

def musicOver():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load('./musics/回答正确与否.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)


def main():
    global  FPSCLOCK,DISPLAYSURF,BASICFONT,gameState
    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DISPLAYSURF.get_locked()
    BASICFONT = pygame.font.Font('freesansbold.ttf',18)
    pygame.display.set_caption('wormy')

    showStartScreen()

    changeFPSThread = Thread(target=changeFPS)
    changeFPSThread.setDaemon(True)
    changeFPSThread.start()
    countTimeThread = Thread(target=countTime)
    countTimeThread.setDaemon(True)
    countTimeThread.start()
    appleStateThread = Thread(target=changeAppleState)
    appleStateThread.setDaemon(True)
    appleStateThread.start()

    while True:
        pygame.event.get() 
        runGame()
        Thread(target=musicOver).start()
        gameState = 'S'
        showGameOverScreen()

if __name__ == '__main__':
    main()