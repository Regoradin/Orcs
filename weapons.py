import random
from classes import *

#Weapon stats are name, damage, durability.
club_wooden = Weapon('wooden club', 25, 2)
sword_wooden = Weapon('wooden sword', 50, 3)
sword_golden = Weapon('golden sword', 10, 50)
nothing = Weapon('nothing', 0, None)
#Can I have None as an infinite value? ie does None - 1 = None?
