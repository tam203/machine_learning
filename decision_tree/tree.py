from __future__ import division
from math import log
from pprint import pprint

def bestValToSplitOn(x,y,splitIndex):
    bestGain = 0
    splitOnVal = 0
    for i in xrange(-50, 51):
        gain = infoGainOnSplit(x, y, splitIndex, i)
        if gain > bestGain:
            bestGain = gain
            splitOnVal = i

    return splitOnVal, bestGain


def bestIndexToSplitOn(x, y):
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
    mostCommonClass = 1 if sum(y) > (len(y)/2) else 0
    certainty = 1
    return

def makeTree(x,y,maxdepth=4, currTree=None):
    currTree = {} if currTree is None else currTree


    if maxdepth <= 0:
        currTree['class'] = getclass(y)
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
    if tree.has_key('class'):
        return tree['class']

    action = tree['action']

    if xi[action['index']] > action['value']:
        return applyTree(tree['left'], xi)
    else:
        return applyTree(tree['right'], xi)


def infoGainOnSplit(x, y, splitOnIndex, ifGreaterThan):
    entropyBefore = entropy(y)
    n = len(x)
    result = applyNode({'index':splitOnIndex, 'value':ifGreaterThan}, x , y)
    left = result['left']['y']
    right = result['right']['y']
    leftEntropy = entropy(left)
    rightEntropy = entropy(right)
    entropyAfter = (len(left)/n) *leftEntropy + (len(right)/n) * rightEntropy


    return entropyBefore - entropyAfter

def entropy(data):
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



if __name__ == '__main__':

    #print entropy([0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

    #
    #x = [[0,10],[5,10],[5,2]]
    #y = [1, 1, 0]
    #print entropy(y)
    #print infoGainOnSplit(x, y, 0, 0)

    #[[#isTriangle, #isBig]]
    shapeStats = [[1,0],[1,1],[1,0],[0,0],[0,1]]
    shapeIsRed = [0,1,0,0,1]
    print entropy(shapeIsRed)
    print infoGainOnSplit(shapeStats, shapeIsRed, 1, 0)
    #print infoGainOnSplit(shapeStats, shapeIsRed, 1, 0)



    # x = [
    #     [12,6],
    #     [9,7,1],
    #     [8,7,1],
    #     [9,7,5],
    #     [1,1]
    # ]
    #
    # y = [
    #     0,
    #     1,
    #     1,
    #     0,
    #     0,
    # ]
    #
    # tree = makeTree(x, y, 2)
    # pprint(tree)
    # for xi in [[1,1,6],[0,0,6],[0,9,0]]:
    #     print "For vals %s the tree says %s" % (xi, applyTree(tree, xi))