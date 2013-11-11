import time, random

class Thing():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

class Being():
    def __init__(self, name, x, y, img, health, weapon, mana, role, level):
        self.name = name
        self.x = x
        self.y = y
        self.img = img
        self.health = health
        self.weapon = weapon
        self.role = role
        self.level = level
        
    def __str__(self):
        return "%s with a %s. Please don't interpolate me." % (self.name, self.weapon)

    def attack(self, target):
        target.health -= self.weapon.damage
        self.weapon.durability -= 1
        print('%s did %s damage to %s.' % (self.name, self.weapon.damage, target.name))
        target.check_health()
        if self.weapon.check_durability == False:
            print("%s's %s broke!" % (self.name, self.weapon.name))
        self.mana += 1

    def check_health(self):
        if self.health <= 0:
            print('%s is dead.' % (self.name))
            return False
        else:
            print("%s's health is at %s" % (self.name, s elf.health))
            return True

    def heal(self):
        if self.role == 'mage':
            self.heal += 3
            self.mana -= 1

    def backstab(self, target):
        if self.role == 'rogue':
            self.mana -= 2
            target.health -= self.weapon.damage*2
            self.weapon.durability -= 1
            print('%s did %s damage to %s.' % (self.name, self.weapon.damage, target.name))
            target.check_health()
            if self.weapon.check_durability == False:
                print("%s's %s broke!" % (self.name, self.weapon.name))
            self.mana += 1

class Weapon():
    def __init__(self, name, damage, durability):
        self.name = name
        self.damage = damage
        self.durability = durability
    def check_durability(self):
        if self.durability <= 0:
            return False
        else:
            print("%s's durability is at %s" % (self.name, self.durability))
            return True
