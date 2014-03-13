import pygame, sys, time, random
from pygame.locals import *
from classes import *
from weapons import *
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
unit_check = None
friendly_units_total = 0


#Asking setup questions. Graphicize and prettiezize later.
print("How big would you like the world to be?")

worldHeight = int(input())
worldWidth  = worldHeight
pixelsPerGrid = int(1000/worldHeight)
squares = worldHeight * worldWidth

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

#Checks if anything (other (friendly) units) is in x's place, where x is a being object
def checkUnit(friendly_units_total, new_being, unit_list):
    for unit in unit_list:
        if new_being.y == unit.y and new_being.x == unit.x:
            print('collision detected', new_being)
            new_being.x = random.randint(0, worldWidth-1)
            new_being.y = random.randint(0, worldHeight-1)
            checkUnit(friendly_units_total, new_being, unit_list)
    if terrain[new_being.y][new_being.x] in ['water', 'mountain']:
        new_being.x = random.randint(0, worldWidth-1)
        new_being.y = random.randint(0, worldHeight-1)
        checkUnit(friendly_units_total, new_being, unit_list)

def generateUnit(width, height):
    global friendly_units_total
    friendly_units_total = 0
    unit = []
    for x in range(int(squares/5)):
        new_being = Being('Orc' + str(x), random.randint(0, worldWidth-1), random.randint(0, worldHeight-1), 'holdimg', 'holdhealth', 'holdweapon', 'holdrole', 1, 'friend')
        #When ranger implemented SET TO RANDOM
        y = 1
        #y = random.randint(1,2)
        z = random.randint(1,2)
        if y == 1:
            new_being.role = 'fighter'
            new_being.health = 100
            new_being.img = orcFighter1
            if z == 1:
                new_being.weapon = club_wooden
            if z == 2:
                new_being.weapon = sword_wooden
            checkUnit(friendly_units_total, new_being, unit)
            
        unit.append(new_being)
        friendly_units_total += 1
    
            

    for x in unit:
        print(x.name)
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




def drawView(width,height,scale,terrain,buildings,unit):

    global friendly_units_total
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
    for z in unit:
        if z.img == orcFighter1:
            displaySurf.blit(pygame.transform.scale(orcFighter1, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*z.x, pixelsPerGrid*z.y))
    #Drawing Lines
    LineCount = 0
    while LineCount <= height-1:
        LineCount = LineCount + 1
        pygame.draw.line(displaySurf, black, (0,LineCount*pixelsPerGrid), (1000,LineCount*pixelsPerGrid),1)
        pygame.draw.line(displaySurf, black, (LineCount*pixelsPerGrid, 0), (LineCount*pixelsPerGrid, 1000),1)

 
        
#List of things.
elevation = generateElevation(worldWidth,worldHeight)
terrain = generateTerrain(worldWidth, worldHeight, elevation)
unit = generateUnit(worldWidth, worldHeight)

while True:
    displaySurf.fill(white)
    drawView(worldWidth,worldHeight,0,terrain,0,unit)

##    if unit[youy][youx] != 'nothing' and unit [youy][youx] != 'orcFighter1dead':
##        chance = random.randint(1,100)
##        if chance < 25:
##            death = time.time() + 2
##            you = pygame.image.load('dead.png')
##        if chance >= 25:
##            if unit[youy][youx] == 'orcFighter1':
##                unit[youy][youx] = 'orcFighter1dead'
##            else:
##                unit[youy][youx] = 'nothing'
##
##    if death and time.time() >= death:
##        pygame.quit()
##        sys.exit()
            

        
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
                if char == 'orcKing':
                    unit[youy][youx] = 'orcKing'
                    print('switched')
                you = orcFighter1
                char = 'orcFighter1'
                youy = choseny
                youx = chosenx
            else:
                pass
            mouseClicked = False

    
    pygame.display.update()
    fpsClock.tick(FPS)
