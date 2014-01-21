import matplotlib.pyplot as plt
import numpy as np

class Fragment:

    def __init__(self, flat):
        self.ddopWeight = 0
        self.dopsWeight = 0
        #Depth of the fragment:
        depth = 0
        maxDepth = 0
        for c in flat:
            if c=='(':
               depth = depth +1
            if c ==')':
               depth = depth -1
            if depth>maxDepth:
               maxDepth = depth
        self.depth = maxDepth
        #Root of the fragment:
        self.root = flat.split()[0][1:]


    def setDops(self,weight):
        self.dopsWeight = weight

    def setDdop(self,weight):
        self.ddopWeight = weight
        
    def updateDops(self, weight):
        self.dopsRun = self.dopsRun + 1
        self.dopsWeight = ((self.run -1)/self.run) * self.dopsWeight    + (1/self.run)*weight

def simplePlot(fragments):
    plt.figure()
    number = len(fragments)
    ddop = [0]*number
    dops = [0]*number
    color = [0]*number
    i = 0
    for flat,frag in fragments.iteritems():
        ddop[i] = frag.ddopWeight
        dops[i] = frag.dopsWeight
        color[i] = frag.depth
        i = i+1
    plt.xlabel('Weight assigned by Double-Dop')
    plt.ylabel('Weight assigned by DOP*')

    plt.scatter(ddop,dops,c=color,edgecolors='None')
    plt.ylim([-0.01,1])
    plt.xlim([-0.01,1])
    plt.show()
    print toPlot




def getFragments(ddopFile, dopsFile):
    fragments = dict()
    f = open(dopsFile, 'r')
    nDops = 0
    for line in f:
        nDops += 1
        [flatFragment,weight] = line.split("\t")
        flatFragment = flatFragment.translate(None, '@')
        weight = float(weight)
        if flatFragment not in fragments:
            fragments[flatFragment] = Fragment(flatFragment)
        fragments[flatFragment].setDops(weight)
    f.close()

    f = open(ddopFile, 'r')
    nDdop = 0
    for line in f:
        nDdop += 1
        [flatFragment,weight] = line.split("\t")
        [numerator,denominator] = weight.split("/")
        weight = float(numerator)/float(denominator)
        if flatFragment not in fragments:
            fragments[flatFragment] = Fragment(flatFragment)
        fragments[flatFragment].setDdop(weight)
    f.close()

    overlap = nDops + nDdop - len(fragments)
    print 'Dop* has ', nDops,' fragments'
    print 'Double-DOP has ', nDdop,' fragments'
    print 'There are ',overlap,' shared fragments'

    return fragments


dopsFile = "dopstarfrags.txt"
ddopFile = "ddopfrags.txt"
fragments = getFragments(ddopFile, dopsFile)
simplePlot(fragments)


