# Example file showing a basic pygame "game loop"
import pygame
from enum import Enum
import random
import math

# Snake body stylizing
CUBE_COLOR1 = (119, 235, 52)
CUBE_COLOR2 = (52, 105, 21)
CUBE_SIZE = 10

# Apple style
APPLE_COLOR = (235, 61, 52)

# Amount of apples
APPLESAMOUNT = 3

# For moving speed
TIMEUNTILMOVE = .05

# for fps displaying
TIMEUNTILUPDATE = 0

# display
WIDTH = 720
HEIGHT = 920

# one block of snake body
class Snake:
    def __init__(self, posX, posY, color = APPLE_COLOR) -> None:
        self.rect = pygame.Rect(posX, posY, CUBE_SIZE, CUBE_SIZE)
        self.prevPos = pygame.Vector2(self.rect.x, self.rect.y)
        self.color = color

    def previousPos(self) -> pygame.Vector2:
        return self.prevPos

    def move(self, x, y) -> None:
        self.prevPos = pygame.Vector2(self.rect.x, self.rect.y)
        self.rect.move_ip(x, y)

    def draw(self) -> None:
        pygame.draw.rect(screen, self.color, self.rect)

    def getX(self) -> int:
        return self.rect.x
    
    def getY(self) -> int:
        return self.rect.y
    
    def setPos(self, pos) -> None:
        self.prevPos = pygame.Vector2(self.rect.x, self.rect.y)
        self.rect.update(pos.x, pos.y, self.rect.width, self.rect.height)

    def getCollider(self) -> pygame.Rect:
        return self.rect
    
    def check(self, collider) -> bool:
        return self.rect.colliderect(collider)

# move direction
class MoveDir(Enum):
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4

# pygame setup
pygame.init()
pygame.font.init() # for font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
running = True
dt = 0
fps = 1

# For moving speed
nextMove = TIMEUNTILMOVE

# For fps update
nextUpdate = TIMEUNTILUPDATE

# font 
my_font = pygame.font.SysFont('Comic Sans MS', 30)
move = MoveDir.BOTTOM

# variables for game
# snake parts starting with head
parts = [Snake(screen.get_width() / 2, screen.get_height() / 2)]
apples = [pygame.Rect(10, 10, 0, 0)] * APPLESAMOUNT;
score = 0

# func that end game
def gameOver():
    global running, score
    running = False
    print("Game Over ! Finished with", str(score), "point(s)")

# set apple rect pos to random pos
def spawnApple(apples):
    for i in range(len(apples)):
        apples[i] = pygame.Rect(round(random.randint(CUBE_SIZE, screen.get_width() - CUBE_SIZE) / CUBE_SIZE) * CUBE_SIZE, round(random.randint(CUBE_SIZE, screen.get_height() - CUBE_SIZE) / CUBE_SIZE) * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)

# function that add snake part
def addSnake(): 
    global parts
    lastIndex = len(parts) - 1
    pos = parts[lastIndex].previousPos()
    if(len(parts)%2):
        parts.append(Snake(pos.x, pos.y, CUBE_COLOR1))
    else: 
        parts.append(Snake(pos.x, pos.y, CUBE_COLOR2))

# spawn apple before game
spawnApple(apples)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((52, 158, 235))

    # RENDER YOUR GAME HERE
    #score rendering
    text_surface = my_font.render("Score: "+ str(score), False, (0, 0, 0))
    screen.blit(text_surface, (5, 5))

    text_surface = my_font.render("Fps: "+ str(fps), False, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() - 5 - text_surface.get_width(), 5))

    #render apple
    for apple in apples:
        pygame.draw.rect(screen, APPLE_COLOR, apple)

    # render snake
    for part in parts:
        part.draw()

    # Set move directory
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move = MoveDir.LEFT
    if keys[pygame.K_RIGHT]:
        move = MoveDir.RIGHT
    if keys[pygame.K_DOWN]:
        move = MoveDir.BOTTOM
    if keys[pygame.K_UP]:
        move = MoveDir.TOP

    # move head
    nextMove -= dt
    if nextMove <= 0:
        match move:
            case MoveDir.LEFT:
                parts[0].move(-CUBE_SIZE, 0)
            case MoveDir.TOP:
                parts[0].move(0, -CUBE_SIZE)
            case MoveDir.RIGHT:
                parts[0].move(CUBE_SIZE, 0)
            case MoveDir.BOTTOM:
                parts[0].move(0, CUBE_SIZE)
        nextMove = TIMEUNTILMOVE
        
        # if got apple add next element
        for i in range(len(apples)):
            if(parts[0].check(apples[i])):
                #add body part
                addSnake()

                # randomly place apple
                apples[i] = pygame.Rect(round(random.randint(CUBE_SIZE, screen.get_width() - CUBE_SIZE) / CUBE_SIZE) * CUBE_SIZE, round(random.randint(CUBE_SIZE, screen.get_height() - CUBE_SIZE) / CUBE_SIZE) * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)

                # add score
                score += 1

        # change pos of other elements
        for i in range(len(parts)):
            if i == 0: continue

            # checks if head touched any other body element
            if parts[0].check(parts[i].getCollider()): gameOver()

            # sets next body part pos as previous part last position
            parts[i].setPos(parts[i - 1].previousPos())

    # check if out of bounds
    if parts[0].getX() >= screen.get_width() or parts[0].getX() + parts[0].getCollider().width <= 0 or parts[0].getY() >= screen.get_height() or parts[0].getY() + parts[0].getCollider().height <= 0:
        gameOver()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # delta time
    dt = clock.tick(60) / 1000 # limits FPS to 60

    # refresh fps
    nextUpdate -= dt
    if nextUpdate <= 0:
        nextUpdate = TIMEUNTILUPDATE
        fps = math.ceil(clock.get_fps())

pygame.quit()