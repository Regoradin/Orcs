import random
from classes import *
from weapons import *

bob = Being('bob', 1, 2, 'bobimg', 100, club_wooden, 'mage', 1, 'red')
fred = Being('fred', 2, 1, 'fredimg', 100, club_wooden, 'rogue', 1, 'blue')
joe = Being('joe', 1, 3, 'joeimg', 100, sword_wooden, 'rogue', 1, 'friend')
oliver = Being('oliver', 1, 4, 'oliverimg', 1000, sword_wooden, 'god', 100, 'friend')

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

control = bob
print(control.y)
control.y -= 1
print(control.y)
