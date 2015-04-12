import random
from classes import *

#Weapon stats are name, damage, durability.
def makeClubWooden():
    club_wooden = Weapon('wooden club', 25, 2)
    return club_wooden

def makeSwordWooden():
    sword_wooden = Weapon('wooden sword', 50, 3)
    return sword_wooden

sword_golden = Weapon('golden sword', 10, 50)

nothing = Weapon('nothing', 0, None)
