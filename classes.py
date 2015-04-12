import time, random

class Thing():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

class Being():
    def __init__(self, name, x, y, img, health, weapon, role, level, ally):
        self.name = name
        self.x = x
        self.y = y
        self.img = img
        self.health = health
        self.weapon = weapon
        self.role = role
        self.level = level
        self.ally = ally
        
    def __str__(self):
        return "%s with a %s. Please don't interpolate me." % (self.name, self.weapon)

    def attack(self, target):
        if target.ally == self.ally:
            print("Target is on your team!")
        elif self.weapon.durability <= 0:
            print('Your weapon is broken!')
        else:
            target.health -= self.weapon.damage
            self.weapon.durability -= 1
            print('%s did %s damage to %s' % (self.name, self.weapon.damage, target.name))
            target.check_health()
            self.weapon.check_durability()
            if self.weapon.check_durability == False:
                print("%s's %s broke!" % (self.name, self.weapon.name))

    def check_health(self):
        if self.health <= 0:
            print('%s is dead.' % (self.name))
            return False
        else:
            print("%s's health is at %s" % (self.name, self.health))
            return True

    def check_clicked(self, x, y, chosenx, choseny):
        if self.x == chosenx and self.y == choseny:
            return True
        else:
            return False


class Weapon():
    def __init__(self, name, damage, durability):
        self.name = name
        self.damage = damage
        self.durability = durability
    def __str__(self):
        return "%s" % (self.name)
    def check_durability(self):
        if self.durability <= 0:
            return False
        else:
            print("%s's durability is at %s" % (self.name, self.durability))
            return True
