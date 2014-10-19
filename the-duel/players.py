#!/usr/bin/env python
# The Duel, by Michael Sarfati
# This module contains a name generator, the class for the Dueler, and the AI decision
# making system.

from random import randint, choice
import re

def nameGen():
    'A random name generator ;-)'
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    vowel = 'aeiouy'
    conson = re.sub('[' + vowel + ']', "", alphabet)
    name = choice(alphabet).upper() + choice(vowel) + choice(conson) + choice(vowel)
    return name

class Dueler:
    'Standard duelist class for all players -- both the AI and the User.'

    def __init__(self, name, isAI=False):
        self.name = str(name)
        self.hp = 100
        self.totalHp = 100
        self.isAI = isAI # For AI behaviour

    def health(self):
        'Used for display, and AI behaviour.'
        status = {
                1:(1,'healthy'), 
                2:(2,'wounded'),
                3:(3,'severe'),
                4:(4,'critical'),
                5:(5,'dead'),
            }
        if self.hp >= 75:
            return status[1]
        elif self.hp in range(51, 75):
            return status[2]
        elif self.hp in range(35, 51):
            return status[3]
        elif self.hp in range(1, 35):
            return status[4]
        elif self.hp < 0:
            return status[5]

    def slash(self, target):
        'Slash attack'
        damage = randint(-25,-18)
        target.hp += damage
        print(\
        "\t{selfName} slashes {targetName} for {damage} points".format(
                selfName=self.name,
                targetName=target.name,
                damage=str(abs(damage))))

    def thrust(self, target):
        'Thrust attack'
        damage = randint(-35, -10)
        target.hp += damage
        print(\
        "\t{selfName} thrusts {targetName} for {damage} points".format(
                selfName=self.name,
                targetName=target.name,
                damage=str(abs(damage))))

    def heal(self):
        'Self-heal -- always heals self'
        damage = randint(18, 25)
        self.hp += damage
        if self.hp > 100:
            self.hp = 100
        print(\
        "\t{selfName} heals themself for {damage} points".format(
                selfName=self.name,
                damage=str(abs(damage))))

class AI:
    'Decision thread for the enemy player. Controls its instance of Dueler and Moves'
    def __init__(self, dueler, difficulty=0):
        'Dueler is the name of the character created for the AI. Usually, "e"'
        if dueler.isAI == True:
            self.dueler = dueler
        self.difficulty = difficulty # Easy/Medium/Hard -- don't worry about this now

    def select(self):
        # Return codes: 1= slash, 2= thrust, 3=heal 
        # Read in the summary of the AI's dueler's health
        status = self.dueler.health()[0] 
        if status == 1:
            return choice([1, 2])
        if status == 2:
            return choice([1, 2, 1, 2, 1, 2, 3])
        if status == 3:
            return choice([1, 2, 3])
        if status == 4:
            # Gives an attack a 1 in 4 chance of being selected when status is critical
            doWhat = choice([1,2,3,4,5])
            if doWhat in range(1,3):
                return choice([1, 2])
            else:
                return 3
