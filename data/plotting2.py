import matplotlib.pyplot as plt
from  matplotlib import cm
import matplotlib.colors as cl
import numpy as np
from collections import defaultdict


def fragmentsToPlottable():
    global L, M, N
    global depth, width, subs, term, roots

    number = len(fragments)
    L, M, N = [[0]*number for i in range(3)]
    depth, width, subs, term = [[0]*number for i in range(4)]
    roots = {'NP':[],'VP':[],'S':[],'PP':[],'ADJP':[],'SBAR':[],'QP':[]}

    i = 0
    for flat,frag in fragments.iteritems():
        L[i] = frag.weights[0]
        M[i] = frag.weights[1]
        N[i] = frag.weights[2]
        depth[i] = frag.depth
        width[i] = frag.width
        subs[i] = frag.substitutionSites
        term[i] = frag.terminals
        if frag.root in roots:
            roots[frag.root].append(i)
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


        for minProp in range(1,3):
            if minProp>1:
               title+=', starting at '+str(minProp)

            indexes = [i for i in range(len(props)) if props[i]>minProp]
            colors = [props[i] for i in indexes]

            toPlotL = [L[i] for i in indexes]
            toPlotM = [M[i] for i in indexes]
            toPlotN = [N[i] for i in indexes]
            plot(toPlotL,dL,toPlotM,dM,colors,title)
            plot(toPlotN,dN,toPlotM,dM,colors,title)
            plot(toPlotN,dN,toPlotL,dL,colors,title)

    for root, indexes in roots.iteritems():
        title = 'Depth of the fragments rooted at '+root
        colors = [depth[i] for i in indexes]
        toPlotL = [L[i] for i in indexes]
        toPlotM = [M[i] for i in indexes]
        toPlotN = [N[i] for i in indexes]
        plot(toPlotL,dL,toPlotM,dM,colors,title)
        plot(toPlotN,dN,toPlotM,dM,colors,title)
        plot(toPlotN,dN,toPlotL,dL,colors,title)

def plot(toPlotX,Xdescription,toPlotY,Ydescription,colors,title):
    thres = 0.000001
    fig = plt.figure()
    plt.xscale('symlog',linthreshx=thres)
    plt.xlim([0,1])
    plt.yscale('symlog',linthreshy=thres)
    plt.ylim([0,1])

    maxFeat = max(colors)
    colormap = plt.get_cmap('hot')

    plt.scatter(toPlotX,toPlotY,norm = cl.LogNorm(),c = colors,edgecolors='None',cmap = colormap)

    plt.axhline(y=thres,linestyle='dashed', color='black')
    plt.axvline(x=thres,linestyle='dashed', color='black')

    plt.xlabel(Xdescription)
    plt.ylabel(Ydescription)

    from matplotlib.ticker import LogFormatter
    l_f = LogFormatter(labelOnlyBase=False)
    plt.colorbar(format=l_f,ticks=range(0,maxFeat+1,5))

    plt.title(title)
    global plotn
    plt.savefig('plots/'+str(plotn), dpi=300)
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
    dN = "Double-DOP full: 1000"

def readFragsLarge():
    global fragments
    fragments = pf.fragments
    global dL, dM, dN

    fL = "resultingGrammars/ddopSplit.txt"
    pf.readFragments(fL,0)
    dL = "Weight according to Maximal Overlap - Split"

    fM = "resultingGrammars/dops.txt"
    pf.readFragments(fM,1)
    dM = "Weight according to Shortest Derivation - Split"

    fN = "resultingGrammars/ddop.txt"
    pf.readFragments(fN,2)
    dN = "Weight according to Maximal Overlap - Full"

def fragsToArff():
    f = open('wekabaar.arff','w')
    for flat,fragment in fragments.iteritems():
        f.write(str(fragment.depth)+',')
        f.write(str(fragment.substitutionSites)+',')
        f.write(str(fragment.terminals)+',')
        if fragment.root in ['NP','VP','S','PP','ADJP','SBAR','QP']:
           f.write(str(fragment.root)+',')
        else:
           f.write('other,')
        f.write(str(fragment.weights[0])+',')
        f.write(str(fragment.weights[0])+',')
        f.write(str(fragment.weights[0])+'\n')
    f.close()

def main():


    global plotn
#    plotn = 0
#    readFragsSmall()
    readFragsLarge()
#    fragmentsToPlottable()
#    goPlot()
    fragsToArff()


if __name__ == '__main__':
    main()
