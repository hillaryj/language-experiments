#!/usr/bin/env python
"""
Provides dictionaries of letter types for using CVC syllable construction [1].

Letter frequency is drawn from 10X the English letter frequencies. The
scaling factor was chosen to differentiate on an integer level between
tenths of percentages. These weightings have been modified slightly based on
experiment results during development from the entries in wikipedia [2].

Overall consonants are drawn from both onset and end type consonants and is
generated from both dicts.

The consonant and vowel dicts are of the form key: weight and a function
is provided (and used) to generate weighted lists of letters to simplify
selecting from a weighted set.

References:
[1] https://en.wikipedia.org/wiki/Syllable#Grouping_of_components
[2] https://en.wikipedia.org/wiki/Letter_frequency
"""

__author__ = "Hillary Jeffrey"
__copyright__ = "Copyright 2015"
__credits__ = ["Hillary Jeffrey"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Hillary Jeffrey"
__email__ = "hillaryaj@gmail.com"
__status__ = "Development"


# Information for altering syllables for readability/pronouncability
# when occurring at the ends of words
translation = {
    'aw': 'augh',
    'ou': 'ow',
    'zh': 'j',
    'ng': 'nge',
    'v': 've',
    'ng': 'nge',
}

# Onset consonants begin CVC syllables
# Dict format is key: letterweight*10 (English)
onset_consonants = {
    'b': 47,
    'd': 27,
    'f': 38,
    'g': 20,
    'h': 72,
    'j': 6,
    'k': 6,
    'l': 27,
    'm': 43,
    'n': 24,
    'p': 25,
    'r': 17,
    's': 78,
    't': 167,
    'v': 6,
    'w': 68,
    'y': 16,
    'z': 3,
    'th': 80,
    'ch': 25,
    'wh': 10,
    'sh': 30,
    }

# End consonants end CVC syllables
# Dict format is key: letterweight*10 (English)
end_consonants = {
    'b': 15,
    'd': 43,
    'f': 22,
    'g': 20,
    'k': 8,
    'l': 4,
    'm': 24,
    'n': 67,
    'p': 19,
    'r': 60,
    's': 63,
    't': 91,
    'v': 10,
    'w': 24,
    'z': 1,
    'ch': 10,
    'gh': 10,
    'ng': 20,
    'sh': 10,
    'th': 10,
    }

# Build an overall list of consonants
consonants = {}
consonants.update(onset_consonants)
consonants.update(end_consonants)

# Vowels are used to build syllables; Y is omitted because of CVC construction
# Dict format is key: letterweight*10 (English)
vowels = {
    'a': 82,
    'e': 127,
    'i': 70,
    'o': 75,
    'u': 28,
}


# Build the sets of weighted distributions
def buildWeightedSets(inputdict):
    """Converts a dict of keys and weights into an array expanded with weights
    of the full data set"""

    # We'll use total weight to double check our built array
    totalweight = sum(inputdict.values())

    weightedSet = []

    for letter, weight in inputdict.iteritems():
        weightedSet += [letter]*weight

    # Check that we got the expected length, otherwise raise an error
    if not totalweight == len(weightedSet):
        raise ValueError("Constructed length (%i) differs from expected (%i)"
                         % (len(weightedSet), totalweight))

    return weightedSet


# Build access lists of weighted sets for each dictionary
end_weighted = buildWeightedSets(end_consonants)
onset_weighted = buildWeightedSets(onset_consonants)
vowels_weighted = buildWeightedSets(vowels)
consonants_weighted = buildWeightedSets(consonants)
