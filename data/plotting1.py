import matplotlib.pyplot as plt
#from pylab import *
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
        self.root = flat.split()[0][1:]   #split at whitespace, take the first part, omit the first character '('


    def setDops(self,weight):
        self.dopsWeight = weight

    def setDdop(self,weight):
        self.ddopWeight = weight

    def updateDops(self, weight):
        self.dopsRun = self.dopsRun + 1
        self.dopsWeight = ((self.run -1)/self.run) * self.dopsWeight    + (1/self.run)*weight

def onlyPlot(X, xlabel, Y, ylabel, color):
    fig = plt.figure()
    plt.scatter(X,Y,c=color,edgecolors='None')

    a = plt.gca()
    a.set_xlabel(xlabel)
    a.set_ylabel(ylabel)

# Linear scale:
#    a.set_xlim([-0.1,1])
#    a.set_ylim([-0.1,1])

#Logarithmic scale
#NB: zero values will not be displayed, and raise a warning
    a.set_xlim([0.001,1])
    a.set_xscale('log')
    a.set_ylim([0.001,1])
    a.set_yscale('log')


    plt.show()

def plotDopsVsDdop(fragments):
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
    onlyPlot(ddop, 'Weights assigned by Double-DOP', dops,'Weights assigned by DOP*',color)


def getFragments(ddopFile, dopsFile):
    fragments = dict()
    f = open(dopsFile, 'r')
    nDops = 0
    for line in f:
        nDops += 1
        [flatFragment,weight] = line.split("\t")
        #flatFragment = flatFragment.translate(None, '@')
        #weight = float(weight)

        [numerator,denominator] = weight.split("/")# temporary: DDOP
        weight = float(numerator)/float(denominator) # temporary: DDOP

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

#dopsFile = "tiny-dopstar-frags.txt"
#ddopFile = "tiny-ddop-frags.txt"
dopsFile = "ddopfragsALL.txt"
ddopFile = "ddopfrags.txt"
fragments = getFragments(ddopFile, dopsFile)
plotDopsVsDdop(fragments)


