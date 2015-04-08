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
controlled = None
death = None
unit_check = None
friendly_units_total = 0


#Asking setup questions. Graphicize and prettiezize later.
print("How big would you like the world to be?")


#worldHeight and worldWidth are is space numbers. pixelsPerGrid is the number of pixels in length each grid space is. This is only set up for square grids.
worldHeight = int(input())
worldWidth  = worldHeight
pixelsPerGrid = int(500/worldHeight)
squares = worldHeight * worldWidth

#Standard Units
selector = pygame.image.load('selector.png')

guyRed  = pygame.image.load('guyRed.png')
orcFighter1 = pygame.image.load('Orc_Fighter_1.png')
orc_fighter_1_red = pygame.image.load('Orc_Fighter_1_team_red.png')
orc_fighter_1_blue = pygame.image.load('Orc_Fighter_1_team_blue.png')
orcFighter1dead = pygame.image.load('Orc_Fighter_1_Dead.png')

orc_king_pic = pygame.image.load('orc_king.png')


frozen = None
pygame.key.set_repeat(125, 125)

displaySurf = pygame.display.set_mode((500,500), 0,32)
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
def checkUnit(new_being, target_grid):
    if target_grid[new_being.y][new_being.x] != None:
        print('collision with person')
        new_being.x = random.randint(0, worldWidth-1)
        new_being.y = random.randint(0, worldHeight-1)
        checkUnit(new_being, target_grid)
    if terrain[new_being.y][new_being.x] in ['water', 'mountain']:
        print('collision with terrain')
        new_being.x = random.randint(0, worldWidth-1)
        new_being.y = random.randint(0, worldHeight-1)
        checkUnit(new_being, target_grid)

#Exactly like checkUnit, except that it takes a coordinate instead of a being, and instead of randomizing a new location, it simply passes True or False depending on whether or not there is a person, mountain, or ocean in the way.
def checkMove(target_grid, x, y):
    if target_grid[y][x] != None:
        print('collision with person')
        return 'collision_person'
    if terrain[y][x] in ['water', 'mountain']:
        print('collision with terrain')
        return 'collision_terrain'
    else:
        return True
def generateUnit(width, height):
    global friendly_units_total
    friendly_units_total = 0
    unit = []
    #Makes basic orcs to cover 20% of the map
    for x in range(int(squares*.2)):
        new_being = Being('Orc' + str(x), random.randint(0, worldWidth-1), random.randint(0, worldHeight-1), 'holdimg', 'holdhealth', 'holdweapon', 'holdrole', 1, 'holdally')
        #When ranger implemented SET TO RANDOM
        y = 1
        #y = random.randint(1,2)
        z = random.randint(1,2)
        if y == 1:
            new_being.role = 'fighter'
            new_being.health = 100
            new_being.img = random.choice([orc_fighter_1_red, orc_fighter_1_blue])
            if z == 1:
                new_being.weapon = club_wooden
            if z == 2:
                new_being.weapon = sword_wooden
            if new_being.img == orc_fighter_1_red:
                new_being.ally = 'red'
            if new_being.img == orc_fighter_1_blue:
                new_being.ally = 'blue'
            checkUnit(new_being, target_grid)
            
        unit.append(new_being)
        target_grid[new_being.y][new_being.x] = new_being
        friendly_units_total += 1
            
    for x in unit:
        print(x)
    return unit

#This will create a nested list grid, like for elevation, that contains beings or Nones in each space. These spaces can be called individually for targeting abilities/clicks,
#instead of completely cycling through the unit list. 
def generateTargetGrid(width, height):
    target_grid = []
    for x in range (width):
        target_grid.append([])
        for y in range (height):
            target_grid[x].append(None)
            
    return target_grid

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
        displaySurf.blit(pygame.transform.scale(z.img, (pixelsPerGrid, pixelsPerGrid)),(pixelsPerGrid*z.x, pixelsPerGrid*z.y))
    if controlled != None:
        displaySurf.blit(pygame.transform.scale(selector, (pixelsPerGrid, pixelsPerGrid)), (pixelsPerGrid*controlled.x, pixelsPerGrid*controlled.y))
    #Drawing Lines
    LineCount = 0
    while LineCount <= height-1:
        LineCount = LineCount + 1
        pygame.draw.line(displaySurf, black, (0,LineCount*pixelsPerGrid), (1000,LineCount*pixelsPerGrid),1)
        pygame.draw.line(displaySurf, black, (LineCount*pixelsPerGrid, 0), (LineCount*pixelsPerGrid, 1000),1)

 
        
#List of things.
elevation = generateElevation(worldWidth,worldHeight)
terrain = generateTerrain(worldWidth, worldHeight, elevation)
target_grid = generateTargetGrid(worldWidth, worldHeight)
unit = generateUnit(worldWidth, worldHeight)

print("~~~~~~~~~~~~~~~WORLD GENERATED~~~~~~~~~~~~~~ \n")

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
        elif event.type == KEYDOWN and not frozen and not death and controlled != None:
            target_grid[controlled.y][controlled.x] = None
            if event.key in (K_w, K_UP) and controlled.y > 0:
                if checkMove(target_grid, controlled.x, controlled.y -1) == True:
                    controlled.y -= 1
                if checkMove(target_grid, controlled.x, controlled.y -1) == 'collision_person':
                    controlled.attack(target_grid[controlled.x][controlled.y -1])
                frozen = time.time() + .2
            elif event.key in (K_s, K_DOWN) and controlled.y < worldHeight-1:
                if checkMove(target_grid, controlled.x, controlled.y +1) == True:
                    controlled.y += 1
                if checkMove(target_grid, controlled.x, controlled.y +1) == 'collision_person':
                    controlled.attack(target_grid[controlled.x][controlled.y +1])
                frozen = time.time() + .2
            elif event.key in (K_a, K_LEFT) and controlled.x > 0:
                if checkMove(target_grid, controlled.x -1, controlled.y) == True:
                    controlled.x -= 1
                if checkMove(target_grid, controlled.x -1, controlled.y) == 'collision_person':
                    controlled.attack(target_grid[controlled.x-1][controlled.y])
                frozen = time.time() + .2
            elif event.key in (K_d, K_RIGHT) and controlled.x < worldWidth-1:
                if checkMove(target_grid, controlled.x +1, controlled.y) == True:
                    controlled.x += 1
                if checkMove(target_grid, controlled.x +1, controlled.y) == 'collision_person':
                    controlled.attack(target_grid[controlled.x +1][controlled.y])
                frozen = time.time() + .2
            target_grid[controlled.y][controlled.x] = controlled
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
            controlled = target_grid[choseny][chosenx]
            if controlled != None:
                print(controlled.name)
                print (controlled.ally)
            else:
                controlled = None
            mouseClicked = False

    
    pygame.display.update()
    fpsClock.tick(FPS)
