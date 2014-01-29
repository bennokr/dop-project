import matplotlib.pyplot as plt
from  matplotlib import cm
import matplotlib.colors as cl
import numpy as np
from collections import defaultdict


def fragmentsToPlottable():
    global L
    global M
    global N
    global depth
    global width
    global subs
    global term
    number = len(fragments)
    L = [0]*number
    M = [0]*number
    N = [0]*number
    depth = [0]*number
    width = [0]*number
    subs = [0]*number
    term = [0]*number

    i = 0
    for flat,frag in fragments.iteritems():
        L[i] = frag.weights[0]
        M[i] = frag.weights[1]
        N[i] = frag.weights[2]
        depth[i] = frag.depth
        width[i] = frag.width
        subs[i] = frag.substitutionSites
        term[i] = frag.terminals
        i+=1

def goPlot():
    feats = ['depth','width','subs','term']
    for feat in feats:
        if feat == 'depth':
           props = depth
           title = 'Depth of the fragments'
        if feat == 'width':
           props = width
           title = 'Width of the fragments'
        if feat == 'subs':
           props = subs
           title = 'Number of substitution sites'
        if feat == 'term':
           props = term
           title = 'Number of terminals (words)'

        for minProp in range(1,2):
            indexes = [i for i in range(len(props)) if props[i]>minProp]
            colors = [props[i] for i in indexes]

            toPlotL = [L[i] for i in indexes]
            toPlotM = [M[i] for i in indexes]
            toPlotN = [N[i] for i in indexes]
            plot(toPlotL,dL,toPlotM,dM,colors,title)
            plot(toPlotN,dN,toPlotM,dM,colors,title)
            plot(toPlotL,dL,toPlotN,dN,colors,title)

def plot(toPlotX,Xdescription,toPlotY,Ydescription,colors,title):
    thres = 0.000001
    fig = plt.figure()
    plt.xscale('symlog',linthreshx=thres)
    plt.xlim([0,1])
    plt.yscale('symlog',linthreshy=thres)
    plt.ylim([0,1])

    maxFeat = max(colors)
    colormap = cm = plt.get_cmap('hot',maxFeat)
    
    plt.scatter(toPlotX,toPlotY,norm = cl.LogNorm(),c = colors,edgecolors='None',cmap = colormap)

    plt.axhline(y=thres,linestyle='dashed', color='black')
    plt.axvline(x=thres,linestyle='dashed', color='black')

    plt.xlabel(Xdescription)
    plt.ylabel(Ydescription)
#    v =
    bar = plt.colorbar()
    bar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(range(1,maxFeat+1)):#['$0$','$1$','$2$','$>3$']):#enumerate(range(1,max(colors+1))):
        bar.ax.text(.5, (2 * j + 1) / float(maxFeat*2), str(lab), ha='center', va='center')
#    bar.ax.get_yaxis().labelpad = 15
#    bar.ax.set_ylabel('# of contacts', rotation=270)
#    bar.set_ticks(np.linspace(0, 1, max(colors), endpoint=True))
#    bar.set_ticklabels(range(1,max(colors)+1))
#    bar.draw_all()
#    ticks = v, ticklabels=range(1,max(colors)+1)
    plt.title(title)
#        plt.title('Fragments of depth from'+str(minDepth))
    global plotn
    plt.savefig('plots/'+str(plotn), dpi=300)
    plotn+=1
    #plt.show()


def plotTwo(N, NDescription, M, MDescription):

        fig = plt.figure()
        plt.xscale('symlog',linthreshx=0.0000001)#, nonposx='clip')
        plt.xlim([0,1])
        plt.yscale('symlog',linthreshy=0.0000001)#, nonposx='clip')
        plt.ylim([0,1])

        colormap = cl.colorMap('hot',maxFeat)

        plt.scatter(toPlotX,toPlotY,norm = cl.LogNorm(),c = colors,edgecolors='None',cmap = colormap)

        plt.xlabel(NDescription)
        plt.ylabel(MDescription)
        v = np.linspace(0, 1, maxProp, endpoint=True)
        plt.colorbar(ticks = v)
        plt.title(feat)
#        plt.title('Fragments of depth from'+str(minDepth))
        global plotn
        plt.savefig('plots/'+feat+str(plotn), dpi=300)
        plotn+=1
    #plt.show()

import processFragments as pf
pf.globalRuns = 3


def readFragsSmall():
    global fragments
    fragments = pf.fragments
    global dL,dM,dN

    f0 = "wsj/wsj_dops_split_500_500_0.txt"
    pf.readFragments(f0,0)
    dL = "Weight according to Shortest Derivation with Split"

    f1 = "wsj/wsj_ddop_split_500_500_0.txt"
    pf.readFragments(f1,1)
    dM = "Double-DOP split: 500/500"
    f2 = "wsj/wsj_ddop_1vall_1000_1.txt"
    pf.readFragments(f2,2)
    dN = "Double-DOP 1 vs all: 1000"

def readFragsLarge():
    global fragments
    fragments = pf.fragments
    global dL, dM, dN

    fL = "resultingGrammars/ddopSplit.txt"
    pf.readFragments(fL,0)
    dL = "Weight according to Maximal Overlap with Split"

    fM = "resultingGrammars/dops.txt"
    pf.readFragments(fM,1)
    dM = "Weight according to Shortest Derivation with Split"

    fN = "resultingGrammars/ddop.txt"
    pf.readFragments(fN,2)
    dN = "Weight according to Maximal Overlap 1 vs all"

def main():


    global plotn
    plotn = 30
    readFragsLarge()
    fragmentsToPlottable()
    goPlot()


if __name__ == '__main__':
    main()
