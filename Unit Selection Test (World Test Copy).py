import pygame, sys, time, random
from pygame.locals import *
from pprint import pprint

pygame.init()

FPS = 60
fpsClock= pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
water = (0,0,255)
forest = (66,159,47)
desert = (225,219,59)
mountain = (80,80,80)

mouseClicked = False
death = None

#Asking setup questions. Graphicize and prettiezize later.
print("How big would you like the world to be?")

worldHeight = int(input())
worldWidth  = worldHeight
pixelsPerGrid = int(1000/worldHeight)

print("Who would you like to play as, Fireball Joe, The Palladin King, or the \nOrb of Hungering?")
char = input()
if char  == 'joe':
    you = pygame.image.load('joe.png')
elif char == 'king':
    you = pygame.image.load('pally.png')
elif char == 'orb':
    you = pygame.image.load('orb.png')
elif char == 'orc':
    you = pygame.image.load('orc_king.png')

#Hero Units
joe = pygame.image.load('joe.png')
pally = pygame.image.load('pally.png')
orb = pygame.image.load('orb.png')
orcKing = pygame.image.load('orc_king.png')

#Standard Units
guyRed  = pygame.image.load('guyRed.png')
orcFighter1 = pygame.image.load('Orc_Fighter_1.png')
orcFighter1dead = pygame.image.load('Orc_Fighter_1_Dead.png')

frozen = None
pygame.key.set_repeat(125, 125)

displaySurf = pygame.display.set_mode((1000,1000), 0,32)
pygame.display.set_caption('Orcs Test World')

def generateTerrain(width, height, elevation):
    terrain=[]
    for x in range(width):
        terrain.append([])
        for y in range (height):
            if elevation[y][x] <= 10:
                terrain[x].append('water')
            elif elevation[y][x] > 10 and elevation[y][x] < 20:
                trn = random.randint(1,2)
                if trn == 1:
                    terrain[x].append('forest')
                if trn == 2:
                    terrain[x].append('desert')
            elif elevation[y][x] >= 20:
                terrain[x].append('mountain')

    return terrain

def generateUnit(width, height):
    unit=[]
    for x in range(width):
        unit.append([])
        for y in range (height):
            unit[x].append(random.randint(1,100))
    for x in range (width):
        for y in range (height):
            if unit[y][x] >40:
                unit[y][x] = 'nothing'
            elif unit[y][x] <= 20:
                unit[y][x] = 'orcFighter1'
            elif unit[y][x] >20 and unit[y][x] <= 40:
                unit[y][x] = 'humanFighter1'
                

    return unit

def generateElevation(width, height):
    elevation=[]
    for x in range(width):
        elevation.append([])
        for y in range (height):
            elevation[x].append(-1)

    elevation[0][0] = random.randint(11,19)
    
    for x in range(width):
        for y in range (height):
            if elevation[y][x] >= 2 and elevation [y][x] <= 28:
                if x != 0:
                    if elevation[y][x-1] == -1:
                        elevation[y][x-1] = elevation[y][x] + random.randint(-2,2)
                if x != width-1:
                    if elevation[y][x+1] == -1:
                        elevation[y][x+1] = elevation[y][x] + random.randint(-2,2)
                if y != 0:
                    if elevation[y-1][x] == -1:
                        elevation[y-1][x] = elevation[y][x] + random.randint(-2,2)
                if y != height-1:
                    if elevation[y+1][x] == -1:
                        elevation[y+1][x] = elevation[y][x] + random.randint(-2,2)
            if elevation[y][x] == 1 or elevation[y][x] == 29:
                if x != 0:
                    if elevation[y][x-1] == -1:
                        elevation[y][x-1] = elevation[y][x] + random.randint(-1,1)
                if x != width-1:
                    if elevation[y][x+1] == -1:
                        elevation[y][x+1] = elevation[y][x] + random.randint(-1,1)
                if y != 0:
                    if elevation[y-1][x] == -1:
                        elevation[y-1][x] = elevation[y][x] + random.randint(-1,1)
                if y != height-1:
                    if elevation[y+1][x] == -1:
                        elevation[y+1][x] = elevation[y][x] + random.randint(-1,1)
            if elevation[y][x] == 0:
                if x != 0:
                    if elevation[y][x-1] == -1:
                        elevation[y][x-1] = elevation[y][x] + 2
                if x != width-1:
                    if elevation[y][x+1] == -1:
                        elevation[y][x+1] = elevation[y][x] + 2
                if y != 0:
                    if elevation[y-1][x] == -1:
                        elevation[y-1][x] = elevation[y][x] + 2
                if y != height-1:
                    if elevation[y+1][x] == -1:
                        elevation[y+1][x] = elevation[y][x] + 2
            if elevation[y][x] == 30:
                if x != 0:
                    if elevation[y][x-1] == -1:
                        elevation[y][x-1] = elevation[y][x] - 2
                if x != width-1:
                    if elevation[y][x+1] == -1:
                        elevation[y][x+1] = elevation[y][x] - 2
                if y != 0:
                    if elevation[y-1][x] == -1:
                        elevation[y-1][x] = elevation[y][x] - 2
                if y != height-1:
                    if elevation[y+1][x] == -1:
                        elevation[y+1][x] = elevation[y][x] - 2



    return elevation




def drawView(width,height,scale,terrain,buildings,units, you, youx, youy):

    #Drawing Terrain
    for x in range (width):    
        for y in range (height):
            if terrain[y][x] == 'water':
                pygame.draw.rect(displaySurf, water, (pixelsPerGrid*x,pixelsPerGrid*y,pixelsPerGrid,pixelsPerGrid))
            elif terrain[y][x] == 'forest':
                pygame.draw.rect(displaySurf, forest, (pixelsPerGrid*x,pixelsPerGrid*y,pixelsPerGrid,pixelsPerGrid))
            elif terrain[y][x] == 'desert':
                pygame.draw.rect(displaySurf, desert, (pixelsPerGrid*x,pixelsPerGrid*y,pixelsPerGrid,pixelsPerGrid))
            elif terrain[y][x] == 'mountain':
                pygame.draw.rect(displaySurf, mountain, (pixelsPerGrid*x,pixelsPerGrid*y,pixelsPerGrid,pixelsPerGrid))

    #Drawing Units
    for x in range (width):
        for y in range (height):
            if terrain[y][x] != 'water':
                #Hero Units
                if unit[y][x] == 'joe':
                    displaySurf.blit(pygame.transform.scale(joe, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))
                if unit[y][x] == 'pally':
                    displaySurf.blit(pygame.transform.scale(pally, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))
                if unit[y][x] == 'orb':
                    displaySurf.blit(pygame.transform.scale(orb, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))
                if unit[y][x] == 'orcKing':
                    displaySurf.blit(pygame.transform.scale(orcKing, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))

                #Standard Units
                if unit[y][x] == 'nothing':
                    pass
                if unit[y][x] == 'orcFighter1':
                    displaySurf.blit(pygame.transform.scale(orcFighter1, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))
                if unit[y][x] == 'humanFighter1':
                    displaySurf.blit(pygame.transform.scale(guyRed,  (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))
                if unit[y][x] == 'orcFighter1dead':
                    displaySurf.blit(pygame.transform.scale(orcFighter1dead,  (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*x, pixelsPerGrid*y))
        
    #Drawing Lines
    LineCount = 0
    while LineCount <= height-1:
        LineCount = LineCount + 1
        pygame.draw.line(displaySurf, black, (0,LineCount*pixelsPerGrid), (1000,LineCount*pixelsPerGrid),1)
        pygame.draw.line(displaySurf, black, (LineCount*pixelsPerGrid, 0), (LineCount*pixelsPerGrid, 1000),1)

    #Drawing You   
    displaySurf.blit(pygame.transform.scale(you, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*youx, pixelsPerGrid*youy))


    
        
#List of things.
elevation = generateElevation(worldWidth,worldHeight)
terrain = generateTerrain(worldWidth, worldHeight, elevation)
unit = generateUnit(worldWidth, worldHeight)

youx = random.randint(0,worldWidth-1)
youy = random.randint(0,worldHeight-1)
while terrain[youy][youx] == 'water' or terrain[youy][youx] == 'mountain' or unit[youy][youx] != 'nothing':
    youx = random.randint(0,worldWidth-1)
    youy = random.randint(0,worldHeight-1)
if char == 'joe':
    unit[youy][youx] = joe
if char == 'king':
    uni[youy][youx] = pally
if char == 'orb':
    unit[youy][youx] = orb
if char == 'orc':
    unit[youy][youx] = orcKing


while True:
    
    displaySurf.fill(white)
    drawView(worldWidth,worldHeight,0,terrain,0,0,you,youx,youy,)

    if unit[youy][youx] != 'nothing' and unit [youy][youx] != 'orcFighter1dead':
        chance = random.randint(1,100)
        if chance < 25:
            death = time.time() + 2
            you = pygame.image.load('dead.png')
        if chance >= 25:
            if unit[youy][youx] == 'orcFighter1':
                unit[youy][youx] = 'orcFighter1dead'
            else:
                unit[youy][youx] = 'nothing'

    if death and time.time() >= death:
        pygame.quit()
        sys.exit()
            

        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and not frozen and not death:
            if event.key in (K_w, K_UP) and youy > 0:
                youy = youy - 1
                frozen = time.time() + .4
            elif event.key in (K_s, K_DOWN) and youy < worldHeight-1:
                youy = youy + 1
                frozen = time.time() + .4
            elif event.key in (K_a, K_LEFT) and youx > 0:
                youx = youx - 1
                frozen = time.time() + .4
            elif event.key in (K_d, K_RIGHT) and youx < worldWidth-1:
                youx = youx + 1
                frozen = time.time() + .4
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouseClicked = True
        if frozen and time.time() >= frozen:
            frozen = None

        if mouseClicked == True:
            chosencoordx = mousex/pixelsPerGrid
            chosenx = int(chosencoordx)
            chosencoordy = mousey/pixelsPerGrid
            choseny = int(chosencoordy)
            print(chosenx, choseny, you, unit[youy][youx])
            if unit[choseny][chosenx] == 'orcFighter1':
                unit[choseny][chosenx] = 'nothing'
                if char == 'joe':
                    unit[youy][youx] = joe
                if char == 'king':
                    unit[youy][youx] = pally
                if char == 'orb':
                    unit[youy][youx] = orb
                    print('switched')
                if char == 'orc':
                    unit[youy][youx] = 'orcKing'
                    print('switched')
                you = orcFighter1
                youy = choseny
                youx = chosenx
            else:
                pass
            mouseClicked = False

    
    pygame.display.update()
    fpsClock.tick(FPS)
