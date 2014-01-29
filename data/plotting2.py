import matplotlib.pyplot as plt
from  matplotlib import cm
import matplotlib.colors as cl
import numpy as np
from collections import defaultdict

def plotColors(N, NDescription, M, MDescription):
    number = len(fragments)
    X = defaultdict(list)
    Y = defaultdict(list)

    for flat,frag in fragments.iteritems():
        depth = frag.depth
        X[depth].append(frag.weights[N])
        Y[depth].append(frag.weights[M])
        #color[i] = frag.depth

    fig = plt.figure()
    plt.xscale('symlog',linthreshx=0.0000001)#, nonposx='clip')
    plt.xlim([0,1])
    plt.yscale('symlog',linthreshy=0.0000001)#, nonposx='clip')
    plt.ylim([0,1])

    colorm = cl.Colormap('Blues',11)
    colors = colorm(np.arange(10))
   # for depth in range(1,10):

    for depth in X:
        if depth>10:
           plt.scatter(X[depth],Y[depth],c=colors[11], edgecolors = 'None', label='depth '+str(depth))
        else:
            plt.scatter(X[depth],Y[depth],c=colors[depth], edgecolors = 'None', label='depth '+str(depth))


    plt.xlabel(NDescription)
    plt.ylabel(MDescription)
    plt.legend()
    global plotn
    plt.savefig('plots/plot'+str(plotn), dpi=300)
    plotn+=1
    #plt.show()




def plotTwo(N, NDescription, M, MDescription):
    number = len(fragments)
    X = [0]*number
    Y = [0]*number
    depth = [0]*number
    colors = [0]*number
    i = 0
    for flat,frag in fragments.iteritems():
        X[i] = frag.weights[N]
        Y[i] = frag.weights[M]
        depth[i] = frag.depth
        i+=1


    for minDepth in range(1,11):
        indexes = [i for i in range(len(depth)) if depth[i]>minDepth]
        colors = [depth[i] for i in indexes]
        toPlotX = [X[i] for i in indexes]
        toPlotY = [Y[i] for i in indexes]

       # toPlotX = [X[i] for i in range(len(colors)) if depth[i]>minDepth]
       # toPlotY = [Y[i] for i in range(len(Y)) if depth[i]>minDepth]


        fig = plt.figure()
        plt.xscale('symlog',linthreshx=0.0000001)#, nonposx='clip')
        plt.xlim([0,1])
        plt.yscale('symlog',linthreshy=0.0000001)#, nonposx='clip')
        plt.ylim([0,1])

        p = plt.scatter(toPlotX,toPlotY,norm = cl.LogNorm(),c = colors,edgecolors='None',cmap = cm.hot)
        plt.xlabel(NDescription)
        plt.ylabel(MDescription)
        plt.colorbar(p)
        plt.title('Fragments of depth from'+str(minDepth))
        global plotn
        plt.savefig('plots/plot'+str(plotn), dpi=300)
        plotn+=1
    #plt.show()


def tinyPlots():
    readFragments("tiny/tiny_ddop_1vall_7_1.txt",1)
    readFragments("tiny/tiny_ddop_split_3_4_1.txt",2)
    readFragments("tiny/tiny_dops_1vall_7_1.txt",3)
    readFragments("tiny/tiny_dops_split_3_4_1.txt",4)
    plotTwo(1,"Double-DOP 1vsAll: 7",2,"Double-DOP split: 3/4", 0)
#    plotTwo(1,"Double-DOP 1vsAll: 7",3,"DOP* 1vsAll: 7", 0)
#    plotTwo(2,"Double-DOP split: 3/4",4,"DOP* split: 3/4", 0)
#    plotTwo(3,"DOP* 1vsAll: 7",4,"DOP* split: 3/4", 0)

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

    f4 = "wsj/wsj_dops_1vall_1000_1.txt"
    readFragments(f4,4)
    d4 = "DOP* 1 vs all: 20050"

    plotTwo(1,d1,2,d2,1,1)
    plotTwo(1,d1,3,d3,1,1)
    plotTwo(3,d3,4,d4,1,1)
    plotTwo(2,d2,4,d4,1,1)

    plotTwo(1,d1,2,d2,1,2)
    plotTwo(1,d1,3,d3,1,2)
    plotTwo(3,d3,4,d4,1,2)
    plotTwo(2,d2,4,d4,1,2)


#WSJPlots20050()
#WSJPlots1000()


import processFragments as pf



def main():
    global plotn
    plotn = 0
    pf.globalRuns = 3
    global fragments
    fragments = pf.fragments


#     f1 = "wsj/wsj_ddop_split_500_500_0.txt"
#     pf.readFragments(f1,1)
#     d1 = "Double-DOP split: 500/500"
#     f2 = "wsj/wsj_ddop_1vall_1000_1.txt"
#     pf.readFragments(f2,2)
#     d2 = "Double-DOP 1 vs all: 1000"
#     plotTwo(1,d1,2,d2)

    f0 = "resultingGrammars/ddopSplit.txt"
    pf.readFragments(f0,0)
    d0 = "Maximal Overlap with split"

    f1 = "resultingGrammars/dops.txt"
    pf.readFragments(f1,1)
    d1 = "Shortest derivation with split"

    f2 = "resultingGrammars/ddop.txt"
    pf.readFragments(f2,2)
    d2 = "Maximal Overlap 1 vs all"

    plotTwo(0,d0,1,d1)
    plotTwo(0,d0,2,d2)
    plotTwo(1,d1,2,d2)

if __name__ == '__main__':
    main()
