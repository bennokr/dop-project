import matplotlib.pyplot as plt
from  matplotlib import cm
from matplotlib import ticker as tk
import matplotlib.colors as cl
import numpy as np
from collections import defaultdict


def fragmentsToPlottable():
    # Go over the dictionairy of fragments 
    # and set their features in the following globals variables:
    global L, M, N                            # weights according to three runs
    global depth, width, subs, term, roots    # other features of the fragments

    number = len(fragments)
    L, M, N = [[0]*number for i in range(3)]
    depth, width, subs, term = [[0]*number for i in range(4)]
    roots = {'NP':[],'VP':[],'S':[],'PP':[],'ADJP':[],'SBAR':[],'QP':[]}  # Most occurring roots

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
    # Start plotting:
    # Create plots for each feature and for each of the most occuring roots

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

        # plot this feature starting at a certain value (minProp)
        for minProp in range(1,3):
            if minProp>1:
               title+=', from '+str(minProp)

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
    # Create an actual plot and save it to plots/<plotn>.png
    # 'toPlotX' and 'toPlotY' are the locations of the points
    # 'colors' corresponds to the features
    # 'title' is the title for this plot

    # Formatting of the plot
    thres = 0.000001
    fig = plt.figure()
    plt.xscale('symlog',linthreshx=thres)
    plt.xlim([0,1])
    plt.yscale('symlog',linthreshy=thres)
    plt.ylim([0,1])
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.tick_params(axis='both', which='minor', labelsize=15)

    # Set color scheme for the feature
    maxFeat = max(colors)
    colormap = plt.get_cmap('hot')

    plt.scatter(toPlotX,toPlotY,norm = cl.LogNorm(),c = colors,edgecolors='None',cmap = colormap)

    plt.axhline(y=thres,linestyle='dashed', color='black')
    plt.axvline(x=thres,linestyle='dashed', color='black')
    plt.xlabel(Xdescription, fontsize=20)
    plt.ylabel(Ydescription, fontsize=20)
    
    # Make colorbar
    l_f = tk.LogFormatter(labelOnlyBase=False)
    if maxFeat < 30:
       myticks = range(0,maxFeat+1,5)
    else:
       myticks = range(0,maxFeat+1,10)
    bar = plt.colorbar(format=l_f,ticks=myticks)
    bar.ax.tick_params(labelsize=15)

    # Add the title and save to file
    plt.title(title, fontsize=25)
    global plotn
    plt.savefig('plots/'+str(plotn), dpi=300)#, format='PDF')
    print 'Saved plot:', plotn
    plotn+=1
    #plt.show()



def readFragsSmall():
    # Read a small dataset (for testing)
    global fragments
    fragments = pf.fragments
    global dL,dM,dN

    f0 = "wsj/wsj_dops_split_500_500_0.txt"
    pf.readFragments(f0,0)
    dL = "Weight according to SD-S"

    f1 = "wsj/wsj_ddop_split_500_500_0.txt"
    pf.readFragments(f1,1)
    dM = "Weight according to SD-S"

    f2 = "wsj/wsj_ddop_1vall_1000_1.txt"
    pf.readFragments(f2,2)
    dN = "Weight according to SD-F"

def readFragsLarge():
    # Read the real data
    global fragments
    fragments = pf.fragments
    global dL, dM, dN

    fL = "resultingGrammars/ddopSplit.txt"
    pf.readFragments(fL,0)
    dL = "Weight according to MO-S"#Maximal Overlap - Split"

    fM = "resultingGrammars/dops.txt"
    pf.readFragments(fM,1)
    dM = "Weight according to SD-S"#Shortest Derivation - Split"

    fN = "resultingGrammars/ddop.txt"
    pf.readFragments(fN,2)
    dN = "Weight according to MO-F"#Maximal Overlap - Full"

def fragsToArff():
    # Write an .arff file, so we can perform Weka clustering
    # NB the headers in the file need to be added
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
    # Read the fragments into a dictionary
    # Convert them to arrays of values for plotting
    # Create and save plots

    print 'Reading fragments...'
#    readFragsSmall()
    readFragsLarge()
    print 'Done'

    print 'Converting to plottable...'
    fragmentsToPlottable()
    print 'Done'

    print 'Creating plots...'
    global plotn
    plotn = 0
    goPlot()
    print 'Done'

#    fragsToArff()

import processFragments as pf
pf.globalRuns = 3
if __name__ == '__main__':
    main()
