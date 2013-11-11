import time, random
from classes import *

sword = Weapon('sword', 10, 15)
axe = Weapon('axe', 20, 5)

bob = Being('bob', 1, 2, 'bobimg', 100, sword, 1, 'mage', 1)
fred = Being('fred', 2, 1, 'fredimg', 100, axe, 1, 'rogue', 1)


while bob.check_health() != False or fred.check_health() != False:
    bob_choice = random.randint(1,2)
    if bob_choice == 1:
        bob.attack(fred)
    if bob_choice == 2:
        bob.heal()
    fred_choice = random.randint(3,4)
    if fred_choice == 3:
        
