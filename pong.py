import pygame
import random
import sys
import numpy
from pygame.locals import *

pygame.init()

mainClock = pygame.time.Clock()

WINDOWWIDTH = 600
WINDOWHEIGHT = 400
PADDLESPEED = 6
#BALLSPEEDX = 9
BALLSPEEDX = 20
BALLSPEEDY = 9
PADDLEWIDTH = 15
PADDLEHEIGHT = 80
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def waitForPlayerToPressKey():
    font = pygame.font.SysFont(None, 48)
    drawText('Pong', font, windowSurface, (WINDOWWIDTH / 2) - 35, (WINDOWHEIGHT / 3))
    drawText('Press spacebar to play.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    while True:
        for pause_event in pygame.event.get():
            if pause_event.type == QUIT:
                terminate()
            if pause_event.type == KEYDOWN:
                if pause_event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return
while True:
    waitForPlayerToPressKey()
    angle = random.choice([0, 180]) * float(numpy.pi / 180)
    ball = pygame.Rect(WINDOWWIDTH / 2, WINDOWHEIGHT / 2, 10, 10)
    leftPaddle = pygame.Rect(20, WINDOWHEIGHT / 2 - PADDLEHEIGHT / 2, PADDLEWIDTH, PADDLEHEIGHT)
    rightPaddle = pygame.Rect(WINDOWWIDTH - 20 - PADDLEWIDTH, WINDOWHEIGHT / 2 - PADDLEHEIGHT / 2, PADDLEWIDTH, PADDLEHEIGHT)
    moveUpLeft = moveUpRight = moveDownLeft = moveDownRight = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    moveUpLeft = True
                if event.key == K_z:
                    moveDownLeft = True
                if event.key == K_k:
                    moveUpRight = True
                if event.key == K_m:
                    moveDownRight = True
            if event.type == KEYUP:
                if event.key == K_a:
                    moveUpLeft = False
                if event.key == K_z:
                    moveDownLeft = False
                if event.key == K_k:
                    moveUpRight = False
                if event.key == K_m:
                    moveDownRight = False
        ball.left += numpy.cos(angle) * BALLSPEEDX
        ball.top += numpy.sin(angle) * BALLSPEEDY
        if ball.right < 0:
            break
        if ball.left > WINDOWWIDTH:
            break
        if ball.bottom > WINDOWHEIGHT:
            ball.bottom = WINDOWHEIGHT
            BALLSPEEDY *= -1
        if ball.top < 0:
            ball.top = 0
            BALLSPEEDY *= -1
        if moveUpLeft == True and leftPaddle.top > 0:
            leftPaddle.top -= PADDLESPEED
        if moveDownLeft == True and leftPaddle.bottom < WINDOWHEIGHT:
            leftPaddle.top += PADDLESPEED
        if moveUpRight == True and rightPaddle.top > 0:
            rightPaddle.top -= PADDLESPEED
        if moveDownRight == True and rightPaddle.bottom < WINDOWHEIGHT:
            rightPaddle.top += PADDLESPEED
        if leftPaddle.colliderect(ball):
            ball.left = leftPaddle.right + 1
            dist = (leftPaddle.centery - ball.centery)
            if dist > 30:
                angle = numpy.pi / 4
            elif dist > 20:
                angle = numpy.pi / 6
            elif dist > 10:
                angle = numpy.pi / 12
            elif dist < -30:
                angle = 7 * numpy.pi / 4
            elif dist < -20:
                angle = 11 * numpy.pi / 6
            elif dist < -10:
                angle = 23 * numpy.pi / 12
            else:
                angle = 0
            BALLSPEEDY = -abs(BALLSPEEDY)
            BALLSPEEDX *= -1
        if rightPaddle.colliderect(ball):
            ball.right = rightPaddle.left - 1
            dist = (rightPaddle.centery - ball.centery)
            if dist > 30:
                angle = 3 * numpy.pi / 4
            elif dist > 20:
                angle = 5 * numpy.pi / 6
            elif dist > 10:
                angle = 11 * numpy.pi / 12
            elif dist < -30:
                angle = 5 * numpy.pi / 4
            elif dist < -20:
                angle = 7 * numpy.pi / 6
            elif dist < -10:
                angle = 13 * numpy.pi / 12
            else:
                angle = 0
            BALLSPEEDY = -abs(BALLSPEEDY)
            BALLSPEEDX *= -1
        windowSurface.fill((0, 0, 0))
        pygame.draw.rect(windowSurface, (255, 255, 255), ball)
        pygame.draw.rect(windowSurface, (255, 255, 255), leftPaddle)
        pygame.draw.rect(windowSurface, (255, 255, 255), rightPaddle)
        pygame.display.update()
        mainClock.tick(60)

