from collections import defaultdict
import re

globalRuns = 0
fragments = dict()

class Fragment:
    def __init__(self, flat):
        self.flat = flat
        self.weights = [0]*globalRuns
        self.computeDepth(flat)
        self.computeWidth(flat)
        self.findRoot(flat)

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

    def computeWidth(self,flat):
  #      subs = re.findall('\(\S+ \)',flat)
  #      print subs
  #
  #      term = re.findall('\(\S+ [^\(\)]+\)',flat)
  #      print term

        self.substitutionSites = len(re.findall('\(\S+ \)',flat))
        self.terminals = len(re.findall('\(\S+ [^\(\)]+\)',flat))
        self.width=self.substitutionSites+self.terminals


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
        #[flatFragment,weight] = line.split("\t")

        parts = line.split("\t")
        if len(parts)<2:
           print "problem with line:",line
           continue

        flatFragment = parts[0]
        weight = parts[1]

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
    print 'read from:', fragsFile,'number of fragments:',nFrags

def readPCFG(ruleFile, lexFile, N):
    global fragments
    rootCounts = defaultdict(int)
    frags = set()

    f = open(lexFile, 'r')
    for line in f:
        frags,rootCounts =lex2Frags(line,frags,rootCounts)
    f.close()
    f = open(ruleFile, 'r')
    for line in f:
        frags,rootCounts = rule2Frag(line,frags,rootCounts)
    f.close()

    for frag in frags:
        root = frag[0]
        flat = frag[1]
        count = frag[2]
        if flat not in fragments:
            fragments[flat] = Fragment(flat)
        fragments[flat].addRun(N,float(count)/float(rootCounts[root]))
    print 'read from:',ruleFile,lexFile, 'number of PCFG rules:',len(frags)


def lex2Frags(line, frags, rootCounts):
    line = line.strip()
    bitParLine = line.split("\t")
    terminal = bitParLine[0]
    pairs = [p.split(' ') for p in bitParLine[1:]]
    # Loop over possibilities
    for p in pairs:
        count = int(p[1])
        root = p[0]
        rootCounts[root]+= count
        flatFragment ='('+root+' '+terminal+')'
        frags.add((root, flatFragment, count))
    return frags, rootCounts

def rule2Frag(line, frags, rootCounts):
    line = line.strip()
    bitParLine = line.split("\t")
    count = int(bitParLine[0])
    root = bitParLine[1]
    rootCounts[root] += count
    children = ''
#    for child in bitParLine[2:]:
#        children+=' ('+child+')'
#    flatFragment = '('+root+children+')'

    children = ['(%s )'%s for s in bitParLine[2:]]
    flatFragment = '('+root+' '+' '.join(children)+')'
    frags.add((root,flatFragment,count))
    return frags,rootCounts



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
        if fragment.depth<1:
           print 'not a valid fragment:',frag.flat
           continue
        if fragment.weights[N] > 0:
           f.write(fragment.flat+'\t'+str(fragment.weights[N])+'\n')
    f.close()
    print "Grammar written to file:", fileName


def readFolds(postfix):
    #read in all folds, write to position start...start+folds-1:
    for n in range(1,nFolds+1):
        f = prefix+str(n)+postfix
        readFragments(f,n-1)


def processDOPS():
    #Process DOP* results:
    # read in the folds, interpolate them,
    # read in the PCFG grammar, smoothen

    pUnkn = computePunkn()

    #initialize the dictionary
    global fragments
    fragments = dict()
    # we need 10+3 positions for processing:
    # for each fold, the interpolation,
    #  the PCFG grammar, and the result
    global globalRuns
    globalRuns = nFolds+3

    readFolds('.sd.txt')

    INTERPOLATED = nFolds
    interpolateRuns(range(nFolds), INTERPOLATED)

    PCFG = INTERPOLATED+1
    readPCFG('bigRun/wsj-02-21.mrg.39833.bin.rules', 'bigRun/wsj-02-21.mrg.39833.bin.lex',PCFG)

    DOPS = PCFG+1
    smoothUnkn(INTERPOLATED,PCFG,DOPS,pUnkn)

    grammarToFile(DOPS, 'resultingGrammars/dops.txt')
    print 'processed DOP*'

def processDDOPS():
    #Process DDOP SPLIT results:
    # read in the folds, interpolate them

    #initialize the dictionary
    global fragments
    fragments = dict()
    # we need 10+1 positions for processing:
    # for each fold, and the interpolation
    global globalRuns
    globalRuns = nFolds+3

    readFolds('.mo.txt')

    DDOPS = nFolds
    interpolateRuns(range(nFolds), DDOPS)

    grammarToFile(DDOPS, 'resultingGrammars/ddopSplit.txt')
    print 'processed DDOP (split)'

def computePunkn():
    postfixNP = '.noparse.txt'
    postfixHC = '.aa'

    unparsed = set()

    for m in range(1,nFolds+1):
        hcSize = 19916
        NPf = open(prefix+str(m)+postfixNP, 'r')
        NPm = set(NPf)
        NPf.close()

        for n in [x for x in range (1,nFolds+1) if x!=m]:
#            print m,n, len(NPm)

            NPf = open(prefix+str(n)+postfixNP,'r')
            NPn = set(NPf)
            NPf.close()

            HCf = open(prefix+str(n)+postfixHC,'r')
            HCn = set(HCf)
            HCf.close()

            toKeep = NPm.difference(HCn)
            toCompare = unparsed.intersection(HCn)
            toAdd = toCompare.intersection(NPn)
            NPm = toKeep.union(toAdd)


        unparsed = unparsed.union(NPm)
#        print m, len(unparsed)
    return float(len(unparsed))/float(hcSize)





def processFrags():
    global nFolds
    nFolds = 10

    global prefix
    prefix = 'bigRun/wsj-02-21.mrg.split19916.'
#    print computePunkn(19916)
    processDOPS()
#    processDDOPS()





if __name__ == '__main__':
    processFrags()
