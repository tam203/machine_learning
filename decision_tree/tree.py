from __future__ import division
from math import log
from pprint import pprint


def entropy(data):
    """
    Entropy is the key to all this, we try to always split the tree in a way
    that will result in more order (less entropy)
    """
    numItems = len(data)
    numberOf1 = sum(data)
    numberOf0 = numItems - numberOf1
    prob1s = (numberOf1/numItems) if numItems > 0 else 0
    prob0s = (numberOf0/numItems) if numItems > 0 else 0
    entropy = 0
    if prob1s > 0:
        entropy += -prob1s * log(prob1s, 2)
    if prob0s > 0:
        entropy += -prob0s * log(prob0s, 2)

    return entropy


def infoGainOnSplit(x, y, splitOnIndex, ifGreaterThan):
    """
    Work out if we split on a given index (knight statistic e.g. strength) being greater than a given value (i.e. 5)
    how much information would we gain. Key to deciding how to split the tree.
    """
    entropyBefore = entropy(y)
    n = len(x)
    result = applyNode({'index':splitOnIndex, 'value':ifGreaterThan}, x , y)
    left = result['left']['y']
    right = result['right']['y']
    leftEntropy = entropy(left)
    rightEntropy = entropy(right)
    entropyAfter = (len(left)/n) *leftEntropy + (len(right)/n) * rightEntropy


    return entropyBefore - entropyAfter

def bestValToSplitOn(x,y,splitIndex):
    """
    Given that we are going to split on a particular index (i.e strenght). What is the best value to split at
    e.g. strength > 5 or strength > 3 etc
    """
    bestGain = 0
    splitOnVal = 0
    for i in xrange(-50, 51):
        gain = infoGainOnSplit(x, y, splitIndex, i)
        if gain > bestGain:
            bestGain = gain
            splitOnVal = i

    return splitOnVal, bestGain


def bestIndexToSplitOn(x, y):
    """
    What is the best index (e.g. strength, speed, spells) to split on.
    Loop through all of them and see what our information gain could be.
    """
    bestGain = 0
    bestSplitOnIndex = 0
    bestSplitOnVal = 0
    for i in xrange(len(x[0])):
        splitOnVal, gain = bestValToSplitOn(x, y, i)
        if gain > bestGain:
            bestGain = gain
            bestSplitOnVal = splitOnVal
            bestSplitOnIndex = i

    return bestSplitOnIndex, bestSplitOnVal, bestGain


def getclass(y):
    """
    Given a set of results (array of 1s and 0s) work our which is most common, this is the `class`
    that will be associated with a leaf for the tree. Also work out or confidence in this class, i.e.
    what fraction of y is of the given class.
    """
    mostCommonClass = 1 if sum(y) > (len(y)/2) else 0
    numOfMostCommon = sum(y) if mostCommonClass == 1 else len(y) - sum(y)
    certainty = numOfMostCommon / len(y)
    return (mostCommonClass, certainty)

def makeTree(x,y,maxdepth=4, currTree=None):
    """
    Make the tree. The tree is just a dictionary with an "action" the thing this node splits by and
     "left" and "right" which is the next branch of the tree. All branches/leafs should terminate in
     a dictionary with a 'class' attribute. This is the class we predict if you end up at this leaf
     when descending the tree.
    """
    currTree = {} if currTree is None else currTree


    if maxdepth <= 0:
        currTree['class'], currTree['certainty'] = getclass(y)
        return currTree

    splitIndex, splitVal, gain = bestIndexToSplitOn(x, y)

    if gain <= 0:
        currTree['class'], currTree['certainty'] = getclass(y)
        return currTree

    currTree['left'] = {}
    currTree['right'] = {}

    currTree['action'] = {'index':splitIndex, 'value':splitVal}
    result = applyNode(currTree['action'], x, y)
    makeTree(result['left']['x'], result['left']['y'], maxdepth-1, currTree['left'])
    makeTree(result['right']['x'], result['right']['y'], maxdepth-1, currTree['right'])
    return currTree


def applyNode(node, x, y):
    "Run the action associated with a tree node. Returns a dict with the data split in to left and right."
    lx = []
    ly = []
    rx = []
    ry = []
    for i in xrange(len(y)):
        testx = x[i]
        testy = y[i]
        if testx[node['index']] > node['value']:
            lx.append(testx)
            ly.append(testy)
        else:
            rx.append(testx)
            ry.append(testy)

    return {'left':{
            'x':lx,'y':ly},
        'right':{
            'x':rx,'y':ry}}


def applyTree(tree, xi):
    """
    Use a tree to make a prediction for xi (one of our knights). Just recursively apply each node.
    """
    if tree.has_key('class'):
        return tree['class']

    action = tree['action']

    if xi[action['index']] > action['value']:
        return applyTree(tree['left'], xi)
    else:
        return applyTree(tree['right'], xi)



if __name__ == '__main__':

    #print entropy([0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

    #
    #x = [[0,10],[5,10],[5,2]]
    #y = [1, 1, 0]
    #print entropy(y)
    #print infoGainOnSplit(x, y, 0, 0)

    # #[[#isTriangle, #isBig]]
    # shapeStats = [[1,0],[1,1],[1,0],[0,0],[0,1]]
    # shapeIsRed = [0,1,0,0,1]
    # print entropy(shapeIsRed)
    # print infoGainOnSplit(shapeStats, shapeIsRed, 1, 0)
    # #print infoGainOnSplit(shapeStats, shapeIsRed, 1, 0)



    x = [
        [12,6],
        [9,7,1],
        [8,7,1],
        [9,7,5],
        [1,1]
    ]

    y = [
        0,
        1,
        1,
        0,
        0,
    ]

    tree = makeTree(x, y, 2)
    pprint(tree)
    for xi in [[1,1,6],[0,0,6],[0,9,0]]:
        print "For vals %s the tree says %s" % (xi, applyTree(tree, xi))