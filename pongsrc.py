import pygame, sys
from pygame.locals import *
import random

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 200

#Global Variables to be used through our program
BOARDWIDTH = 600
BOARDHEIGHT = 300
WINDOWHEIGHT = 500
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
COMPUTERSCORE = 0
PLAYERSCORE = 0

# Set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Draws the arena the game will be played in.
def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    #draw dashed net
    current = 0
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (current + 30)), 5)
    current += 48
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (current + 30)), 5)
    current += 48
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (current + 30)), 5)
    current += 48
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (current + 30)), 5)
    current += 48
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (current + 30)), 5)
    current += 48
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (current + 30)), 5)
    current += 48
    pygame.draw.line(DISPLAYSURF, WHITE, ((BOARDWIDTH / 2), current), ((BOARDWIDTH / 2), (BOARDHEIGHT + PADDLEOFFSET)), 5)
    current += 48

    #draw bottom of board
    pygame.draw.line(DISPLAYSURF, WHITE, (0, BOARDHEIGHT+PADDLEOFFSET), (BOARDWIDTH, BOARDHEIGHT + PADDLEOFFSET), 5)



#Draws the paddle Vertical
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > BOARDHEIGHT - LINETHICKNESS:
        paddle.bottom = BOARDHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#Draws paddle Horizontal Player
def drawPaddleH1(paddle):
    #player paddle wont go past right boundry
    if paddle.right > BOARDWIDTH - LINETHICKNESS:
        paddle.right = BOARDWIDTH - LINETHICKNESS
    #player paddle wont go past left boundry
    elif paddle.left < BOARDWIDTH/2 - LINETHICKNESS:
        paddle.left = BOARDWIDTH / 2 - LINETHICKNESS
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#Draw Paddle Horizontal AI
def drawPaddleH2(paddle):
    #AI paddle wont go past left boundry
    if paddle.left < 0 -LINETHICKNESS:
        paddle.left = 0 -LINETHICKNESS
    elif paddle.right > BOARDWIDTH/2 - LINETHICKNESS:
        paddle.right = BOARDWIDTH / 2 - LINETHICKNESS
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)


#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

#check collision with paddle
#return new direction
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        collision_sound = pygame.mixer.Sound('ouch.wav')
        collision_sound.play()
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        collision_sound = pygame.mixer.Sound('ouch.wav')
        collision_sound.play()
        return -1
    else:
        return 1
def checkHitBallH1(ball, paddle3, paddle4, ballDirY):
    if ballDirY == -1 and paddle3.top == ball.bottom and paddle3.left < ball.left and paddle3.right > ball.right:
        collision_sound = pygame.mixer.Sound('ouch.wav')
        collision_sound.play()
        return -1
    elif ballDirY == 1 and paddle4.bottom == ball.top and paddle4.left < ball.left and paddle4.right > ball.right:
        collision_sound = pygame.mixer.Sound('ouch.wav')
        collision_sound.play()
        return -1
    else:
        return 1
def checkHitBallH2(ball, paddle6, paddle5, ballDirY):
    if ballDirY == 1 and paddle5.top == ball.bottom and paddle5.right > ball.right and paddle5.left <ball.left:
        collision_sound = pygame.mixer.Sound('ouch.wav')
        collision_sound.play()
        return -1
    elif ballDirY == -1 and paddle6.bottom == ball.top and paddle6.right > ball.right and paddle6.left < ball.left:
        collision_sound = pygame.mixer.Sound('ouch.wav')
        collision_sound.play()
        return -1
    else:
        return 1


def ballOut1(ball, player_score, npc_score):
    if ball.x < 0:
        player_score += 1
        return player_score
    if ball.y < 0 and ball.x < BOARDWIDTH/2:
        player_score +=1
        return player_score
    if ball.y > BOARDHEIGHT and ball.x < BOARDWIDTH/2:
        player_score += 1
        return player_score
    else:
        return  player_score

def ballOut2(ball, player_score, npc_score):
    if ball.y < 0 and ball.x > BOARDWIDTH/2:
        npc_score += 1
        return npc_score
    if ball.y > BOARDHEIGHT and ball.x > BOARDWIDTH/2:
        npc_score += 1
        return npc_score
    if ball.x > BOARDWIDTH:
        npc_score = npc_score + 1
        return npc_score
    else:
        return npc_score

def displayScore(player_score, npc_score):
    resultSurf1 = BASICFONT.render('NPC = %s' %(npc_score), True, WHITE)
    resultRect1 = resultSurf1.get_rect()
    resultRect1.topleft = (BOARDWIDTH/4, WINDOWHEIGHT - 50)
    DISPLAYSURF.blit(resultSurf1, resultRect1)

    resultSurf2 = BASICFONT.render('Player = %s' % (player_score), True, WHITE)
    resultRect2 = resultSurf2.get_rect()
    resultRect2.topleft = ((BOARDWIDTH / 4)*3, WINDOWHEIGHT - 50)
    DISPLAYSURF.blit(resultSurf2, resultRect2)

#Computer AI
def ai(ball, ballDirX, paddle1):
    #if ball is moving away, center paddle
    if paddle1.centery < ball.centery:
        paddle1.y += 1
    else:
        paddle1.y -= 1
    return paddle1

def ai2(ball, ballDirY, paddle3):
    if paddle3.centerx > ball.centerx:
        paddle3.x -= 1
    else:
        paddle3.x += 1
    return paddle3

def ai2(ball, ballDirY, paddle4):
    if paddle4.centerx > ball.centerx:
        paddle4.x -= 1
    else:
        paddle4.x += 1
    return paddle4


#Main function
def main():
    pygame.init()
    global DISPLAYSURF
    player_score = 0
    npc_score = 0

    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((BOARDWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = BOARDWIDTH / 2 - LINETHICKNESS / 2
    ballY = BOARDHEIGHT / 2 - LINETHICKNESS / 2
    playerOnePosition = (BOARDHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (BOARDHEIGHT - PADDLESIZE) / 2

    #Keeps track of ball direction
    ballDirX = -1 ## -1 = left 1 = right
    ballDirY = -1 ## -1 = up 1 = down

    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS,PADDLESIZE)
    #pad1 = pygame.Surface.get_rect(paddle1)
    paddle2 = pygame.Rect(BOARDWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    paddle3 = pygame.Rect(BOARDWIDTH / 4, PADDLEOFFSET, PADDLESIZE, LINETHICKNESS)
    paddle4 = pygame.Rect(BOARDWIDTH / 4, BOARDHEIGHT - PADDLEOFFSET, PADDLESIZE, LINETHICKNESS)
    paddle5 = pygame.Rect((BOARDWIDTH / 4) * 3, PADDLEOFFSET, PADDLESIZE, LINETHICKNESS)
    paddle6 = pygame.Rect((BOARDWIDTH / 4) * 3, BOARDHEIGHT - LINETHICKNESS, PADDLESIZE, LINETHICKNESS)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawPaddleH1(paddle5)
    drawPaddleH1(paddle6)
    drawPaddleH2(paddle3)
    drawPaddleH2(paddle4)
    drawBall(ball)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    paddle2.y += 20
                elif event.key == K_UP:
                    paddle2.y -= 20
                elif event.key == K_LEFT:
                    paddle6.x -= 20
                    paddle5.x -= 20
                elif event.key == K_RIGHT:
                    paddle6.x += 20
                    paddle5.x += 20


        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawPaddleH1(paddle5)
        drawPaddleH1(paddle6)
        drawPaddleH2(paddle3)
        drawPaddleH2(paddle4)
        drawBall(ball)

        extra_paddles = pygame.image.load('extra_paddles.jpg')
        side_paddles = pygame.image.load('side_paddles.jpg')
        ball_img = pygame.image.load('ball_img.png')
        board_img = pygame.image.load('board.png')
        DISPLAYSURF.blit(side_paddles, paddle1)
        DISPLAYSURF.blit(side_paddles, paddle2)
        DISPLAYSURF.blit(extra_paddles, paddle6)
        DISPLAYSURF.blit(extra_paddles, paddle5)
        DISPLAYSURF.blit(extra_paddles, paddle4)
        DISPLAYSURF.blit(extra_paddles, paddle3)
        DISPLAYSURF.blit(ball_img, ball)

        #ball movement
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        ballDirY = ballDirY * checkHitBallH1(ball, paddle3, paddle4, ballDirY)
        ballDirY = ballDirY * checkHitBallH2(ball, paddle5, paddle6, ballDirY)

        #check if ball went out of bounds
        player_score = ballOut1(ball, player_score, npc_score)
        npc_score = ballOut2(ball, player_score, npc_score)

        #make computer's paddle move
        paddle1 = ai(ball, ballDirX, paddle1)
        paddle3 = ai2(ball, ballDirY, paddle3)
        paddle4 = ai2(ball, ballDirY, paddle4)

        displayScore(player_score, npc_score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()