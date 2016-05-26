from battle import *
import pprint
import tree


# Create a knight
sir_cumstance = generateKnightStats()

# Tell us about him
print "Sir Cumstance is ", statsToString(sir_cumstance)

# Have an adventure
print "he was exploring the glade and meet an evil wizard, who atacked..."

# With a battle
# Python note: The * notation is unpacking e.g.
#  battle(*sir_cumstance) = battle(sir_cumstance[0], sir_cumstance[1], sir_cumstance[2], sir_cumstance[3])
result = battle(*sir_cumstance)
print "the result is..."
print battleResultToText(result)

# Have 100 battles to collect some data to learn from
knightStats, battleResults = haveSomeBattles(1000)
i = 4
print "One of the battles (number %s) was %s resulting in %s" %(i, statsToString(knightStats[i]), battleResultToText(battleResults[i]))
print "%s%% of battles won" % (100*sum(battleResults)/len(battleResults))



# Create a decision tree by learning from the battle data
battleTree = tree.makeTree(knightStats, battleResults, 4)

# We can experiment with different tree depths, this can lead to over fitting the data,
# especially if we have a small data set.
# battleTree = tree.makeTree(knightStats, battleResults, 100)

# Remind our self's which index is which skill
print "strength (index 0), speed (index 1), weapon level (index 2), spells (index 3)"

# Print out tree
pprint.pprint(battleTree)


# Test the accuracy of out tree by having lots of battles
correct = []
for i in xrange(1000):
    s = generateKnightStats()
    p = tree.applyTree(battleTree, s)
    r = battle(*s)
    correct.append(1-abs(r - p))
    #print "Given: " + (statsToString(s)) + "\nI predict: " + battleResultToText(p) + "\nResult is: " + battleResultToText(r) + "\n"

print "We predicted %s out of %s correct, that's %s%%" % (sum(correct), len(correct), ((sum(correct)*100.0)/len(correct)))


# If your not careful you can make the mistake of testing against your learning data which won't give you representative results!
# Try upping the tree depth and lowering the number of training examples to see the effect of over fitting.
correct = []
for s,r in zip(knightStats, battleResults):
    p = tree.applyTree(battleTree,  s)
    correct.append(1-abs(r - p))
print "`testting` against my training data I got %s out of %s correct, that's %s%%." % (sum(correct), len(correct), ((sum(correct)*100.0)/len(correct)))

