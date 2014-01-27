"""
Get fragments in shortest derivations of a set of trees.

Usage: %s <rules> <lexicon> <trees> [options]

  -s X         the distinguished start symbol of the grammar
  --numproc=n  use n parallel processes.
  --bt=backtransform
               By default a DOP reduction grammar is expected. If the grammar
               is a Double-DOP grammar or a TSG, use this option.
  --unparsed=file
               write sentences which couldn't be parsed to this file

Output is sent to stdout and consist of tab-separated fragments and
pseudofrequencies, one per line.
When there are multiple derivations for a tree, the frequencies of its
fragments are uniformly divided."""

from __future__ import print_function, division
import io
import re
import sys
import gzip
import codecs
import multiprocessing
from getopt import gnu_getopt, GetoptError
from collections import Counter
from operator import itemgetter
from itertools import count
from discodop.containers import Grammar
from discodop import disambiguation
from discodop.treebank import LEAVESRE, POSRE

NUMDERIVS = 1000  # the number of derivations to consider for each tree
GRAMMAR = BACKTRANSFORM = None


def readgrammar(rulesfile, lexiconfile, start, backtransformfile=None):
	"""Read grammar into global variables."""
	global GRAMMAR, BACKTRANSFORM
	rules = (gzip.open if rulesfile.endswith('.gz') else open)(rulesfile).read()
	lexicon = codecs.getreader('utf-8')((gzip.open if lexiconfile.endswith('.gz')
			else open)(lexiconfile)).read()
	bitpar = rules[0] in '0123456789'
	GRAMMAR = Grammar(rules, lexicon,
			start=start, bitpar=bitpar)
	BACKTRANSFORM = None
	if backtransformfile:
		BACKTRANSFORM = (gzip.open if backtransformfile.endswith('.gz')
				else open)(backtransformfile).read().splitlines()
		_ = GRAMMAR.getmapping(None, neverblockre=re.compile(b'.+}<'))


def collectderivations(args):
	"""Find the shortest derivations for a tree, then extract fragments.

	If there is more than one derivation, the counts are divided by the number
	of derivations."""
	n, tree, sent, tags, treestr = args
	msg = '%d. %s' % (n, ' '.join(sent))
	fragments = Counter()
	# find derivations for this tree
	derivations, msg1, chart = disambiguation.treeparsing(
			[tree], sent, GRAMMAR, NUMDERIVS, BACKTRANSFORM,
			tags=tags)
	if not chart:  # no parse
		msg += '\nnot derivable: %s\n' % msg1
		return treestr, fragments, msg
	entries = chart.rankededges[chart.root()]
	_, maxprob = min(derivations, key=itemgetter(1))
	# remove sentence numbers so that we only keep unique derivations
	derivations = [(disambiguation.REMOVEIDS.sub('@0', deriv), entry)
			for (deriv, prob), entry in zip(derivations, entries)
			if prob == maxprob]
	numderivations = len(derivations)
	derivations = dict(derivations)
	numuniquederivations = len(derivations)
	for deriv, entry in derivations.items():
		fragments.update((frag, tuple(fragsent))
			for frag, fragsent in disambiguation.extractfragments(
				deriv if BACKTRANSFORM is None else entry.getkey(),
				chart, BACKTRANSFORM))

	if numderivations > 1:
		for frag in fragments:
			fragments[frag] /= numderivations
	msg += '\n%d derivations, of which %d unique\n' % (
			numderivations, numuniquederivations)
	return treestr, fragments, msg


def main():
	"""CLI."""
	options = 'relfreq numproc= bt= unparsed='.split()
	try:
		opts, args = gnu_getopt(sys.argv[1:], 's:', options)
		assert 2 <= len(args) <= 6, 'incorrect number of arguments'
	except (GetoptError, AssertionError) as err:
		print(err, __doc__)
		return
	opts = dict(opts)
	if int(opts.get('--numproc', 1)) == 1:
		readgrammar(args[0], args[1], opts.get('-s', b'TOP'), opts.get('--bt'))
		mymap = map
	else:
		pool = multiprocessing.Pool(processes=int(opts.get('--numproc', 1)),
				initializer=readgrammar, initargs=(args[0], args[1],
					opts.get('-s', b'TOP'), opts.get('--bt')))
		mymap = pool.imap_unordered
	if opts.get('--unparsed'):
		unparsed = open(opts.get('--unparsed'), 'w')
	else:
		unparsed = None

	# read trees
	trees = []
	for n, treestr in enumerate(io.open(args[2], encoding='utf8'), 1):
		cnt = count()
		tree = LEAVESRE.sub(lambda _: ' %d)' % next(cnt), treestr)
		sent = LEAVESRE.findall(treestr)
		tags = POSRE.findall(treestr)
		trees.append((n, tree, sent, tags, treestr))

	# do work
	fragments = Counter()
	for treestr, newfragments, msg in mymap(collectderivations, trees):
		print(msg, file=sys.stderr)
		for frag, cnt in newfragments.items():
			fragments[frag] += cnt
		if not newfragments and unparsed:
			unparsed.write(treestr)

	# print output
	if unparsed:
		unparsed.close()
	if '--relfreq' in opts:
		sums = Counter()
		for (frag, _), freq in fragments.items():
			sums[frag[1:frag.index(' ')]] += freq
	for (frag, sent), freq in fragments.items():
		word = iter(sent)
		frag = LEAVESRE.sub(lambda _: ' %s)' % (next(word) or ''), frag)
		if '--relfreq' in opts:
			print('%s\t%g/%g' % (frag, freq, sums[frag[1:frag.index(' ')]]))
		else:
			print('%s\t%d' % (frag, freq))

if __name__ == '__main__':
	main()