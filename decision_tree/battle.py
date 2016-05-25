from math import floor
import random

def battle(strength, speed, weapon, spells):
    score = floor(((strength - 5) + speed * 2 + weapon + (spells + 2) * 0.5) -14 -9*random.random())
    score = 0 if score < 0 else 1
    return score

def generateKnightStats():
    return [random.randint(0,10) for i in xrange(4)]

def statsToString(stats):
    return ("a knight of strength {0} with {1} speed knowing {3} spells and weilding a level {2} weapon".format( *stats))

def battleResultToText(result):
    return "a glorius victory" if result >= 1 else "painful death"


def haveSomeBattles(number=1000):
    battleResults = []
    knightStats = []
    for round in xrange(number):
        stats = generateKnightStats()
        knightStats.append(stats)
        battleResults.append(battle(*stats))
    return (knightStats, battleResults)