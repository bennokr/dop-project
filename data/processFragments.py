globalRuns = 0
fragments = dict()

class Fragment:
    def __init__(self, flat):
        self.flat = flat
        self.weights = [0]*globalRuns
        self.computeDepth(self.flat)
        self.findRoot(self.flat)

        #possibly add: 
        # - number of words
        # - number of substitution sites

    def computeDepth(self, flat):
        depth = 0
        maxDepth = 0
        for c in flat:
            if c=='(':
                depth = depth +1
            if c ==')':
                depth = depth -1
            if depth>maxDepth:
               maxDepth = depth
        self.depth =  maxDepth-1
    def findRoot(self, flat):
        self.root = flat.split()[0][1:]
        #split at whitespace, take the first part, omit the first character '('

    def addRun(self, N, weight):
    # Replace the weight for run N with this weight
        self.weights[N] = weight

def readFragments(fragsFile, N):
# Read the fragments from <fragsFile>
# If necessary, add them to the fragments dictionary
# Update the fragments' weight in the dictionary
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
            #create a new Fragment object
            fragments[flatFragment] = Fragment(flatFragment)

        fragments[flatFragment].addRun(N, weight)
    f.close()
    print 'read from:', fragsFile,'number of fragments:', nFrags

def readRules(pcfgFile, N):
# Read the grammar from <pcfgFile>
# If necessary, add them to the fragments dictionary
# Update the fragments' weight in the dictionary
    global fragments
    f = open(pcfgFile, 'r')
    nFrags = 0
    root = ''
    rootcount = 0
    flatFragments = {}
    for line in f:
        nFrags += 1
        # bitpar rules format:
        # count HEAD CHILD1 [CHILD2 ...]
        bitParLine = line.split("\t")
        if (bitParLine[1] != root)
            # add all to fragments
            for frag, count in flatFragments:
                if frag not in fragments:
                    #create a new Fragment object
                    fragments[frag] = Fragment(flatFragment)
                fragments[frag].addRun(N, float(count)/float(rootcount))
            # reset root count
            flatFragments = {}
            root = bitParLine[1]
            rootcount = int(bitParLine[0])

        children = ['(%s )'%s for s in bitParLine[2:]]
        #(1 (2 ) ...)
        rule = '(%s %s)' % (root, ' '.join(children)))
        count = int(bitParLine[0])
        flatFragments[rule] = count
        rootcount += count
    # add all last time
    for frag, count in flatFragments:
        if frag not in fragments:
            #create a new Fragment object
            fragments[frag] = Fragment(flatFragment)
        fragments[frag].addRun(N, float(count)/float(rootcount))
    f.close()
    print 'read from:', pcfgFile,'number of fragments:', nFrags

def readLex(pcfgFile, N):
# Read the grammar from <pcfgFile>
# If necessary, add them to the fragments dictionary
# Update the fragments' weight in the dictionary
    global fragments
    f = open(pcfgFile, 'r')
    nFrags = 0
    for line in f:
        nFrags += 1
        # bitPar lex format:
        # WORD        TAG1 count1   [TAG2 count2 ...]
        bitParLine = line.split("\t")
        pairs = [p.split(' ') for p in bitParLine[1:]]
        total = sum([int(p[1]) for p in pairs])
        # Loop over possibilities
        for p in pairs:
            flatFragment = "(%s %s)" % (bitParLine[0], p[0])
            weight = float(p[1])/total
            if flatFragment not in fragments:
                #create a new Fragment object
                fragments[flatFragment] = Fragment(flatFragment)
            fragments[flatFragment].addRun(N, weight)
    f.close()
    print 'read from:', pcfgFile,'number of fragments:', nFrags

def interpolateRuns(toInterpolate,out):
    #interpolate the weights assigned
    # by the runs in 'toInterpolate' (a list of indices),
    # store the result in run 'out'
    for flat, fragment in fragments.iteritems():
        interpolated = 0
        for n in toInterpolate:
            interpolated += fragment.weights[n] / float(len(toInterpolate))
        fragment.addRun(out,interpolated)

def smoothUnkn(original,PCFG,out,pUnkn):
    #Smooth the run 'original' with the run 'PCFG'
    # and store the result in run 'out':
    # - discount original weights with (1-pUnkn)
    # - and smooth all PCFG fragments with pUnkn
    # NB: if an original fragment is ALSO a CFG fragment,
    #     take the weighted average
    for flat, fragment in fragments.iteritems():
        discounted = (1-pUnkn)* fragment.weights[original]
        smoother = (pUnkn) * fragment.weights[PCFG]
        fragment.addRun(out,discounted + smoother)

def grammarToFile(N, fileName):
    #Write the grammar in run 'N' to file
    f = open(fileName,'w')
    for flat, fragment in fragments.iteritems():
        if fragment.weights[N] > 0:
           f.write(fragment.flat+'\t'+str(fragment.weights[N])+'\n')
    f.close()
    print "Grammar written to file:", fileName


def readFolds(prefix, start,folds):
    #read in all folds, write to position start...start+folds-1:
    for n in range(folds):
        f = prefix+str(n)+'.txt'
        readFragments(f,start+n)


def processDOPS():
    #Process DOP* results:
    # read in the folds, interpolate them,
    # read in the PCFG grammar, smoothen

    pUnkn = 0.005#float(unparsed)/float(corpusSize)

    #initialize the dictionary
    global fragments
    fragments = dict()
    # we need 10+3 positions for processing:
    # for each fold, the interpolation,
    #  the PCFG grammar, and the result
    global globalRuns
    globalRuns = nFolds+3

    readFolds('wsj/wsj_dops_split_500_500_', 0,nFolds)
    
    INTERPOLATED = nFolds
    interpolateRuns(range(nFolds), INTERPOLATED)

    PCFG = INTERPOLATED+1
    f = "wsj/wsj_pseudoPCFG_1000.txt"
    readFragments(f,PCFG)
    
    DOPS = PCFG+1
    smoothUnkn(INTERPOLATED,PCFG,DOPS,pUnkn)

    grammarToFile(DOPS, 'wsj/wsj_dops_split_500_500_processed.txt')
    print 'processed DOP*'

def processDDOPS():
    #Process DDOP SPLIT results:
    # read in the folds, interpolate them

    pUnkn = 0.005#float(unparsed)/float(corpusSize)

    #initialize the dictionary
    global fragments
    fragments = dict()
    # we need 10+1 positions for processing:
    # for each fold, and the interpolation
    global globalRuns
    globalRuns = nFolds+3

    readFolds('wsj/wsj_ddop_split_500_500_', 0,nFolds)
    
    DDOPS = nFolds
    interpolateRuns(range(nFolds), DDOPS)

    grammarToFile(DDOPS, 'wsj/wsj_ddop_split_500_500_processed.txt')
    print 'processed DDOP (split)'


def processFrags():
    global nFolds
    nFolds = 1
    processDOPS()
    processDDOPS()

if __name__ == '__main__':
    processFrags()
