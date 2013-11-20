import random
from classes import *
from weapons import *

sword = Weapon('sword', 10, 15)
axe = Weapon('axe', 20, 5)
death = Weapon('death', 10000, 5000)

bob = Being('bob', 1, 2, 'bobimg', 100, sword, 'mage', 1, 'friend')
fred = Being('fred', 2, 1, 'fredimg', 100, axe, 'rogue', 1, 'friend')
joe = Being('joe', 1, 3, 'joeimg', 100, sword, 'rogue', 1, 'friend')
oliver = Being('oliver', 1, 4, 'oliverimg', 1000, death, 'god', 100, 'friend')

units = [bob, joe, fred]
#while oliver.x != units.x and oliver.y != units.y:
    #print(units.name)

for z in range (3):
    print(units[z].name)

##while bob.check_health() != False or fred.check_health() != False:
##    bob_choice = random.randint(1,2)
##    if bob_choice == 1:
##        bob.attack(fred)
##    if bob_choice == 2:
##        bob.heal()
##    fred_choice = random.randint(3,4)
##    if fred_choice == 3:
        
bob.attack(fred)
