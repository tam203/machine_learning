from math import floor
import random

"""
This is our adventure game. All logic is treated as a black box.
"""

def battle(strength, speed, weapon, spells):
    """
    Out battle function takes the stats and adds some random and then calculates a win (1) or lose (0)
    """
    score = floor(((strength - 5) + speed * 2 + weapon + (spells + 2) * 0.5) -14 -9*random.random())
    return 0 if score < 0 else 1

def generateKnightStats():
    return [random.randint(0,10) for i in xrange(4)]

def statsToString(stats):
    return ("a knight of strength {0} with {1} speed knowing {3} spells and weilding a level {2} weapon".format( *stats))

def battleResultToText(result):
    return "a glorius victory" if result >= 1 else "painful death"


def haveSomeBattles(number=1000):
    """
    Helper function to have lot's of fights!
    """
    battleResults = []
    knightStats = []
    for round in xrange(number):
        stats = generateKnightStats()
        knightStats.append(stats)
        battleResults.append(battle(*stats))
    return (knightStats, battleResults)