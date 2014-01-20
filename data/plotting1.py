import matplotlib.pyplot as plt
import numpy as np

class Fragment:

    def __init__(self, flat):
        self.ddopWeight = 0
        self.dopsWeight = 0
        depth = 0
        maxDepth = 0
        for c in flat:
            if c=='(':
               depth = depth +1
            if c ==')':
               depth = depth -1
            if depth>maxDepth:
               maxDepth = depth
       # print flat, maxDepth
        self.depth = maxDepth
#        self.root =

    def setDops(self,weight):
        self.dopsWeight = weight

    def setDdop(self,weight):
        self.ddopWeight = weight

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

#    toPlot = [frag.ddopWeight,frag.dopsWeight,frag.depth) for flat,frag in fragments.iteritems()]
#    plt.scatter(toPlot
    plt.scatter(ddop,dops,c=color,edgecolors='None')
    plt.show()
    print toPlot

fragments = dict()
count = 0

f = open('tiny-dopstar-frags.txt', 'r')
for line in f:
    count = count + 1
  #  print line
    [flatFragment,weight] = line.split("\t")
    flatFragment = flatFragment.translate(None, '@')
    weight = float(weight)
    if flatFragment not in fragments:
        fragments[flatFragment] = Fragment(flatFragment)
    fragments[flatFragment].setDops(weight)
f.close()

f = open('tiny-ddop-frags.txt', 'r')
for line in f:
    count = count + 1
  #  print line
    [flatFragment,weight] = line.split("\t")

    [numerator,denominator] = weight.split("/")
    weight = float(numerator)/float(denominator)
    if flatFragment not in fragments:
        fragments[flatFragment] = Fragment(flatFragment)
    fragments[flatFragment].setDdop(weight)
f.close()


#print fragments
print len(fragments)
print count
simplePlot(fragments)


