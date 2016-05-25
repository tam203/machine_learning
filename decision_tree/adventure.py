import pprint

from battle import *
import tree

# sirCumstance = generateKnightStats()
# print "Our knight Sir Cumstance is " +  statsToString(sirCumstance)
#
# print "on our knights adventure he comes accross a evil wizard which he fights."
#
# thefight = battle(*sirCumstance)
#
# print "after a violent struggle the result is " + battleResultToText(thefight)


knightStats, battleResults = haveSomeBattles(3)
i = 1
print "One of the battles (number %s) was %s resulting in %s" %(i, statsToString(knightStats[i]), battleResultToText(battleResults[i]))
print "%s%% of battles won" % (100*sum(battleResults)/len(battleResults))

battleTree = tree.makeTree(knightStats, battleResults, 4)
# #battleTree = tree.makeTree(knightStats, battleResults, 100)

print "strength (index 0), speed (index 1), weapon level (index 2), spells (index 3)"
pprint.pprint(battleTree)
# # Test the result
correct = []
for i in xrange(1000):
    s = generateKnightStats()
    p = tree.applyTree(battleTree, s)
    r = battle(*s)
    correct.append(1-abs(r - p))
    print "Given: " + (statsToString(s)) + "\nI predict: " + battleResultToText(p) + "\nResult is: " + battleResultToText(r) + "\n"

print "I got %s out of %s correct, that's %s%%" % (sum(correct), len(correct), ((sum(correct)*100.0)/len(correct)))
#

#
correct = []
for s,r in zip(knightStats, battleResults):
    p = tree.applyTree(battleTree, s)
    correct.append(1-abs(r - p))
print "I got %s out of %s correct, that's %s%%" % (sum(correct), len(correct), ((sum(correct)*100.0)/len(correct)))
