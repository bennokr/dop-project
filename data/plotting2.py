import matplotlib.pyplot as plt
#from pylab import *
import numpy as np

fragments = dict()

class Fragment:
    def __init__(self, flat):
        self.weights = [0]*10
        self.splits = [0]*10

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

    def addRun(self, N, weight):
    # Replace the weight for run N with this weight
        self.weights[N] = weight
        self.splits[N] += 1

    def updateRun(self, N, weight):
    # Interpolate the existing results for run N with the new weight
        current = self.splits[N]
        self.weights[N] = (current/(current+1)) * self.weights[N]    + (1/(current+1))*weight
        self.splits[N] += 1


def plotTwo(N, NDescription, M, MDescription, log):
    number = len(fragments)
    X = [0]*number
    Y = [0]*number
    color = [0]*number
    i = 0
    for flat,frag in fragments.iteritems():
        X[i] = frag.weights[N]
        Y[i] = frag.weights[M]
        color[i] = frag.depth
        i = i+1
    fig = plt.figure()
    plt.scatter(X,Y,c=color,edgecolors='None')

    a = plt.gca()
    a.set_xlabel(NDescription)
    a.set_ylabel(MDescription)

    if log:
        #NB: zero values will not be displayed, and raise a warning
        a.set_xlim([0.001,1])
        a.set_xscale('log')
        a.set_ylim([0.001,1])
        a.set_yscale('log')
    else:
        a.set_xlim([-0.1,1])
        a.set_ylim([-0.1,1])

    plt.show()

def readFragments(fragsFile, N):
    #fragments: a dictionary of Strings (flat fragments) to Fragment objects
    #fragsFile: a path to a file with fragments and corresponding weights
    #description: a String that describes the run
    global fragments
    f = open(fragsFile, 'r')
    nFrags = 0
    for line in f:
        nFrags += 1
        [flatFragment,weight] = line.split("\t")
        flatFragment = flatFragment.translate(None, '@')

        if "/" in weight:
            [numerator,denominator] = weight.split("/")# temporary: DDOP
            weight = float(numerator)/float(denominator) # temporary: DDOP
        else:
            weight = float(weight)


        if flatFragment not in fragments:
            fragments[flatFragment] = Fragment(flatFragment)  #create a new Fragment object
        fragments[flatFragment].addRun(N, weight)
    f.close()
    print fragsFile,nFrags


def tinyPlots():
    readFragments("tiny/tiny_ddop_1vall_7_1.txt",1)
    readFragments("tiny/tiny_ddop_split_3_4_1.txt",2)
    readFragments("tiny/tiny_dops_1vall_7_1.txt",3)
    readFragments("tiny/tiny_dops_split_3_4_1.txt",4)
    plotTwo(1,"Double-DOP 1vsAll: 7",2,"Double-DOP split: 3/4", 0)
    plotTwo(1,"Double-DOP 1vsAll: 7",3,"DOP* 1vsAll: 7", 0)
    plotTwo(2,"Double-DOP split: 3/4",4,"DOP* split: 3/4", 0)
    plotTwo(3,"DOP* 1vsAll: 7",4,"DOP* split: 3/4", 0)

def WSJPlots20050():
    f1 = "wsj/wsj_ddop_split_20000_50_1.txt"
    readFragments(f1,1)
    d1 = "Double-DOP split: 50/20000"

    f2 = "wsj/wsj_dops_split_20000_50_1.txt"
    readFragments(f2,2)
    d2 = "DOP* split: 50/20000"

    f3 = "wsj/wsj_ddop_1vall_20050_1.txt"
    readFragments(f3,3)
    d3 = "Double-DOP 1 vs all: 20050"

    f4 = "wsj/wsj_dops_1vall_20050_1.txt"
    readFragments(f4,4)
    d4 = "DOP* 1 vs all: 20050"

    plotTwo(1,d1,2,d2,1)
    plotTwo(1,d1,3,d3,1)
    plotTwo(3,d1,4,d3,1)
    plotTwo(2,d1,4,d3,1)

def WSJPlots1000():
    f1 = "wsj/wsj_ddop_split_500_500_1.txt"
    readFragments(f1,1)
    d1 = "Double-DOP split: 500/500"

    f2 = "wsj/wsj_dops_split_500_500_1.txt"
    readFragments(f2,2)
    d2 = "DOP* split: 500/500"

    f3 = "wsj/wsj_ddop_1vall_1000_1.txt"
    readFragments(f3,3)
    d3 = "Double-DOP 1 vs all: 1000"

#    f4 = "wsj/wsj_dops_1vall_1000_1.txt"
#    readFragments(f4,4)
#    d4 = "DOP* 1 vs all: 20050"

    plotTwo(1,d1,2,d2,1)
    plotTwo(1,d1,3,d3,1)
#    plotTwo(3,d1,4,d3,1)
#    plotTwo(2,d1,4,d3,1)

WSJPlots20050()
#WSJPlots1000()