#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:

    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):                         
        self.dictionary = {}
        for pair in pairs:
            self.put(pair[0], pair[1])

    # Associates the value v with the key k.
    def put(self, k, v):

        #TODO: prevent value list duplicates!

        if self.get(k) != []:
            if v not in self.get(k):
                self.dictionary[k].append(v)
        else:
            self.dictionary[k] = [v]

    # # Checks if value is already present
    # def checkDuplicate(self, values):
    

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.dictionary[k]
        except KeyError:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):

    try:
        position = 0
        subsequence = ""
        while len(subsequence) < k:
            subsequence += seq.next()
        subsHash = RollingHash(subsequence)
        yield (position, subsequence, subsHash.current_hash())

        while True:
            prev_item = subsequence[0]
            next_item = seq.next()
            position += 1
            subsHash.slide(prev_item, next_item)
            subsequence = subsequence[1:] + next_item
            # subsHash = RollingHash(subsequence)
            yield (position, subsequence, subsHash.current_hash())
            
    except StopIteration:
        return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    
    try:
        position = 0    
        subsequence = ""
        while len(subsequence) < k:
            subsequence += seq.next()
        subsHash = RollingHash(subsequence)
        yield (position, subsequence, subsHash.current_hash())

        while True:
            for i in xrange(0, m): 
                prev_item = subsequence[0]
                next_item = seq.next()
                position += 1
                subsHash.slide(prev_item, next_item)
                subsequence = subsequence[1:] + next_item
            # subsHash = RollingHash(subsequence)
            yield (position, subsequence, subsHash.current_hash())
            
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    # print "Not implemented: getExactSubmatches"
    # raise Exception("Not implemented!")
    matches = []
    aHashes = Multidict()
    aPositions = Multidict()
    # bHashes = Multidict()
    for posSsqssqHash in intervalSubsequenceHashes(a, k, m):
        aHashes.put(posSsqssqHash[2], posSsqssqHash[1])
        aPositions.put(posSsqssqHash[1], posSsqssqHash[0])
        # print posSsqssqHash

    for posSsqssqHash in subsequenceHashes(b, k):
        for ssq in  aHashes.get(posSsqssqHash[2]):
            for pos in aPositions.get(ssq):
                yield (pos, posSsqssqHash[0])

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
