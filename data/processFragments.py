import matplotlib.pyplot as plt
#from pylab import *
import numpy as np

fragments = dict()
plotn = 8
#runs = 10

class Fragment:
    def __init__(self, flat):
        self.flat = flat

        self.weights = [0]*globalRuns
        self.splits = [0]*globalRuns

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
        self.depth = maxDepth-1
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


def readFragments(fragsFile, N):#, todo):
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

   #     if todo = 'new'
        fragments[flatFragment].addRun(N, weight)
   #     if todo = 'interpolate'
   #        fragments[flatFragment].updateRun(N, weight)
    f.close()
    print 'reading from:', fragsFile,'number of fragments:', nFrags
#    return nFrags

def interpolateRuns(toInterpolate,out):
    for flat, fragment in fragments.iteritems():
        interpolated = 0
        for n in toInterpolate:
            interpolated += fragment.weights[n] / len(toInterpolate)
        fragment.addRun(out,interpolated)

def smoothUnkn(original,PCFG,out,pUnkn):
    for flat, fragment in fragments.iteritems():
        discounted = (1-pUnkn)* fragment.weights[original]
        smoother = (pUnkn) * fragment.weights[PCFG]
        # discount all original weights and amooth all CFG fragments
        # If an original fragment is ALSO a CFG fragment, take the weighted average
        fragment.addRun(out,discounted + smoother)


def loadDopsSplit():
    folds = 1
#    folds = 10
    global globalRuns
    globalRuns = folds +3
    HCUnparsed = 50
    corpusSize = 1000
    pUnkn = HCUnparsed/corpusSize

    first = "wsj/wsj_dops_split_500_500_"
    last = ".txt"

    #read in all folds, write to position 0...folds-1:
    for n in range(folds):
        f = first+str(n)+last
        readFragments(f,n)

    #interpolate the runs, write to position folds:
    interpolateRuns(range(folds),folds)

    #read in the PCFG grammar to position folds+1:
    f = "wsj/wsj_pseudoPCFG_1000.txt"
    readFragments(f,folds+1)

    #smoothen interpolated (folds) with PCFG (folds+1), weighted pUnkn, write to position folds+2:
    smoothUnkn(folds, folds+1, folds+2, pUnkn)

    #write the python data structure to file:
    filename = first+'processed'+'.py'
    f = open(filename,'w')
    f.write("fragments = " + str(fragments))
    f.close()

    #write the resulting grammar to file:
    filename = first+'processed'+last
    f = open(filename,'w')
    for flat, fragment in fragments.iteritems():
        f.write(fragment.flat+'\t'+str(fragment.weights[folds+2])+'\n')
    f.close()

    print 'Dop* split grammar processed, size of the grammar:', len(fragments)
    print 'written to file:', filename

loadDopsSplit()


