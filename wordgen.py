#!/usr/bin/env python
"""
Provides functions for randomly generating words, letters, and syllables.

Syllables are constructed CVC-style, i.e. consonants (C) and
vowels (V), and further differentiates from onset and end
consonants.

Words are n-syllables long.

Also provides access to generators for random letters and options
for using frequency weights or equally weighted sets from syllables.py.
"""

import random

import syllables as syll

__author__ = "Hillary Jeffrey"
__copyright__ = "Copyright 2015"
__credits__ = ["Hillary Jeffrey"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Hillary Jeffrey"
__email__ = "hillaryaj@gmail.com"
__status__ = "Development"

# Global variables
DEFAULT_WEIGHT = True
# Future expansion: Allow selection of a 'dialect'


def selectRandom(inputarray):
    """Selects and returns a random entry from the input array"""
    return inputarray[random.randint(0, len(inputarray)-1)]


def cons(weighted=DEFAULT_WEIGHT):
    """Returns a random consonant from the overall consonant list

    Keywords:
    weighted - True/False to use the weighted/unweighted set
    """
    if not weighted:
        return selectRandom(syll.consonants.keys())
    else:
        return selectRandom(syll.consonants_weighted)


def vowel(weighted=DEFAULT_WEIGHT):
    """Returns a random vowel

    Keywords:
    weighted - True/False to use the weighted/unweighted set
    """
    if not weighted:
        return selectRandom(syll.vowels.keys())
    else:
        return selectRandom(syll.vowels_weighted)


def onsetC(weighted=DEFAULT_WEIGHT):
    """Returns a random onset consonant

    Keywords:
    weighted - True/False to use the weighted/unweighted set
    """
    if not weighted:
        return selectRandom(syll.onset_consonants.keys())
    else:
        return selectRandom(syll.onset_weighted)


def endC(weighted=DEFAULT_WEIGHT):
    """Returns a random ending consonant

    Keywords:
    weighted - True/False to use the weighted/unweighted set
    """
    if not weighted:
        return selectRandom(syll.end_consonants.keys())
    else:
        return selectRandom(syll.end_weighted)


def syllCVC(weighted=DEFAULT_WEIGHT):
    """Constructs a CVC-style syllable and returns as a tuple

    Keywords:
    weighted - True/False to use weighted/unweighted letter sets
    """
    return onsetC(weighted), vowel(weighted), endC(weighted)


def word(n=1, weighted=DEFAULT_WEIGHT):
    """Constructs a word out of 'n' syllables.

    Keywords:
    n - Integer number of syllables to generate for the word
    weighted - Specifies whether to use weighted or unweighted letter sets

    Returns a string
    """
    # Enforce a minimum syllable count
    if n <= 0:
        n = 1

    w = []
    for kk in range(n):
        w.append(syllCVC(weighted))

    return wordformat(w)


# Utility functions for word manipulation
def wordformat(syllables, delim=""):
    """Formats a word from an input syllable array into
    a string. Performs translations for ease of reading.

    Keywords:
    syllables - Array of syllables to join
    delim - Delimiter to use between syllables (default:"")

    Returns a string
    """

    # Translate phonemes to their printable type
    ws = []
    for kk in range(len(syllables)):
        ws.append(delim.join(syllables[kk]))

    if syllables[-1] in syll.translation:
        syllables[-1] = syll.translation[syllables[-1]]

    return delim.join(ws)


def transliterate(ph):
    """Performs transliteration of a syllable string for readability
    and pronounceability for English speakers/readers"""
    if ph in translation:
        return translation[ph]


# Utility functions for multi-words e.g. command line interfacing etc.
def wordlist(n=10, minsyllables=1, maxsyllables=3):
    """Constructs a list of 'n' words with variable syllable length

    Keywords:
    n - Number of words to generate
    minsyllables - minimum number of syllables per word
    maxsyllables - maximum number of syllables per word

    Returns a list of strings
    """
    p = []
    for kk in range(n):
        p.append(word(random.randint(minsyllables, maxsyllables)))

    return p


def sentenceformat(words=None, delim=" "):
    """Formats a list of words into proper sentence display,
    including capitalization and punctuation

    Keywords:
    words - An existing list of words to format into a sentence.
            If 'None', will generate a new list of words using default options.
    delim - Delimiter to use between words (default:" ")
    """
    if pp is None:
        pp = wordlist()

    # Join the words together into a sentence
    txt = delim.join(pp)

    # Future upgrade: add commas inside sentences of sufficient length

    return txt.capitalize() + "."
