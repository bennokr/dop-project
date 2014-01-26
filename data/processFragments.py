import pickle

fragments = dict()

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

def readFragments(fragsFile, N):
    global fragments
    f = open(fragsFile, 'r')
    nFrags = 0
    for line in f:
        nFrags += 1
        [flatFragment,weight] = line.split("\t")
        flatFragment = flatFragment.translate(None, '@')

        if "/" in weight:
            [numerator,denominator] = weight.split("/")
            weight = float(numerator)/float(denominator)
        else:
            weight = float(weight)

        if flatFragment not in fragments:
            fragments[flatFragment] = Fragment(flatFragment)  #create a new Fragment object
        fragments[flatFragment].addRun(N, weight)
    f.close()
    print 'reading from:', fragsFile,'number of fragments:', nFrags

def interpolateRuns(toInterpolate,out):
    for flat, fragment in fragments.iteritems():
        interpolated = 0
    #    print 'weight', fragment.weights
        for n in toInterpolate:
            interpolated += fragment.weights[n] / float(len(toInterpolate))
    #    print 'interpolated', interpolated
        fragment.addRun(out,interpolated)

def smoothUnkn(original,PCFG,out,pUnkn):
    for flat, fragment in fragments.iteritems():
        discounted = (1-pUnkn)* fragment.weights[original]
        smoother = (pUnkn) * fragment.weights[PCFG]
        # discount all original weights and smooth all PCFG fragments
        # If an original fragment is ALSO a CFG fragment, take the weighted average
        fragment.addRun(out,discounted + smoother)

def readFolds(prefix, start,folds):
    #read in all folds, write to position start...start+folds-1:
    for n in range(folds):
        f = prefix+str(n)+'.txt'
        readFragments(f,start+n)
    #interpolate the folds, write to position start+folds
    interpolateRuns(range(start,start+folds), start+folds)


def grammarToFile(N, fileName):
    #write the resulting grammar to file:
    f = open(fileName,'w')
    for flat, fragment in fragments.iteritems():
        if fragment.weights[N] >= 0:
           f.write(fragment.flat+'\t'+str(fragment.weights[N])+'\n')
    f.close()
    print "Grammar written to file:", fileName


def main():
    nFolds = 1
    global globalRuns
    globalRuns = 1 + nFolds+2 + nFolds+1 + 1


    #read in the PCFG grammar to position 0:
    f = "wsj/wsj_pseudoPCFG_1000.txt"
    PCFG = 0
    readFragments(f,PCFG)

    start = 1
    DOPS = start + nFolds + 1
    #read in the DOP* folds, interpolated grammar at position (start+nFolds):
    readFolds('wsj/wsj_dops_split_500_500_', start,nFolds)
    pUnkn = 0.005#float(unparsed)/float(corpusSize)
    smoothUnkn(start+nFolds,PCFG,DOPS,pUnkn)
    grammarToFile(DOPS, 'wsj/wsj_dops_split_500_500_processed')
    print 'processed DOP*'

    start = DOPS+1
    DDOPS = start+nFolds
    #read in the DDOP (split) folds, interpolated grammar at position (start+nFolds):
    readFolds('wsj/wsj_ddop_split_500_500_', start,nFolds)
    grammarToFile(DDOPS, 'wsj/wsj_ddop_split_500_500_processed')
    print 'processed DDOP (split)'

    DDOP1 = DDOPS +1
    #read in the DDOP grammar
    readFragments('wsj/wsj_ddop_1vall_1000_1.txt',start)
    print 'processed DDOP'

    #write the python data structure to file:
    filename ='WSJgrammars_processed'+'.py'
    f = open(filename,'w')
    f.write("fragments = " + str(fragments)+'\n')
    f.write("DOPS = "+str(DOPS)+'\n')
    f.write("DDOPS = "+str(DDOPS)+'\n')
    f.write("DDOP1 = "+str(DDOP1)+'\n')
    f.close()


main()

