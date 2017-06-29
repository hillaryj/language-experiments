#!/usr/bin/env python
"""
Provides translatePage and other functions for generating word lists from
input strings.

The function 'translatePage' comes configured for Wikipedia and has been tested
with Wikipedia pages. The translatePage method has been set for wikipedia pages
in particular, but uses parameters so it can be applied to a page with a
header (h1) and body div id; however this has not been extensively tested.

Also turns relative html paths to absolute paths for links, css, and images
so generated page looks like the source page (for Wikipedia at least).

Currently does not translate/gibberize the following cases:
- Words with accented letters
    (Future: convert to unaccented equivalents)
- Words with mixed letters/numbers (i.e. acronyms)
    (Future: gibberize individual letters of the mixing)
- Numerics e.g. dates
    (Future: Leave un-gibberized)

Other future plans:
- Allow percentages of words to be left un-gibberized
    (Future: Leave shortest words first e.g. a, the, and, etc.)
- Expand to detect suffixes/prefixes so root words are gibberized consistently
"""

# Python library imports
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
import random
import string
import re
import os

# Local imports
import wordgen


__author__ = "Hillary Jeffrey"
__copyright__ = "Copyright 2015"
__credits__ = ["Hillary Jeffrey"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Hillary Jeffrey"
__email__ = "hillaryaj@gmail.com"
__status__ = "Development"


DEFAULT_TEST_PAGE = 'https://en.wikipedia.org/wiki/Gladiola'
DEFAULT_OUTPUT_PATH = os.getcwd()
DEFAULT_OUTFILE_NAME = "test.html"
WIKI_TITLE_ID = "firstHeading"
WIKI_BODY_ID = "mw-content-text"

LOWER = "lower"
TITLE = "title"
UPPER = "upper"

NUMERIC = "num"
LETTER = "letter"
ALPHA = "alpha"

CAP_TYPES = {LOWER: string.lower,  # A standard, lower-case word
             TITLE: string.capitalize,  # Initial capital - a title-case word
             UPPER: string.upper,  # All-caps - an uppercase word
             NUMERIC: string.upper,  # A number or word that contains numbers
             }

# Set up regular expression for removing punctuation for parsing words
punctregex = re.compile('[%s]' % re.escape(string.punctuation))
# Set up regular expressions for determining word types/composition
numregex = re.compile('[0-9]')
capregex = re.compile('[A-Z]')
vowelregex = re.compile('[aoeui]')


def translatePage(pageurl=DEFAULT_TEST_PAGE,
                 outputpath=DEFAULT_OUTPUT_PATH,
                 outfile=DEFAULT_OUTFILE_NAME,
                 titleid=WIKI_TITLE_ID,
                 bodyid=WIKI_BODY_ID,
                 percent=100
                 ):
    """
    Loads a given URL and scrambles the page's header and bodytext contents.
    Defaults are set for Wikipedia pages.

    Keywords:
    pageurl - URL for html page to load
    outputpath - Output file directory path (default: current directory)
    outfile - Output file name (should end in ".html" for easy browser display)
    titleid - html tag id for header text
    bodyid - html tag id for body text
    percent - [UNIMPLEMENTED] Percentage of words (0-100) to gibberize

    Returns the output file path
    """
    # Initialize variables for scope
    pagetitle = ""
    bodytext = ""
    wordlist = {}

    # Load the page
    htmlobj = urllib2.urlopen(pageurl).read()
    titleStrainer = SoupStrainer(id=titleid)
    bodyStrainer = SoupStrainer(id=bodyid)

    # This is a hack to find baseurl for filling for absolute paths
    # DANGER: Requires properly-formatted url
    # DANGER: Performs no error checking for proper url
    baseurl = '/'.join(pageurl.split('/')[:3])

    # Make all links absolute to passed url so pages load css/etc properly
    # NOTE: Order is important so the // are done before the /
    htmlobj = re.sub('href="//', 'href="http://', htmlobj)
    htmlobj = re.sub('href="/', 'href="%s/' % baseurl, htmlobj)
    # Make image paths absolute so images load properly
    htmlobj = re.sub('src="//', 'src="http://', htmlobj)
    htmlobj = re.sub('srcset="//', 'srcset="http://', htmlobj)

    soup = BeautifulSoup(htmlobj, 'html.parser')

    # Find the "firstHeading" h1 so we can get the title as a random seed
    # h1 = BeautifulSoup(htmlobj, 'html.parser', parse_only=titleStrainer)
    h1 = soup.find_all(titleStrainer)[0]
    # Perform error checking
    if len(h1.contents) > 0:
        pagetitle = str(h1.get_text())
    else:
        raise ValueError("Header contents length error: len %i"
                         % (len(h1.contents)))

    # COOL PART: Set the random seed to the page title so the
    # article 'translation' will be reproducible
    random.seed(pagetitle)

    # Now get the body content
    div = BeautifulSoup(htmlobj, 'html.parser', parse_only=bodyStrainer)

    # Get the body text
    try:
        bodytext = div.get_text().encode('utf-8')
        # bodytext = soup.div.get_text().encode('utf-8')
    except Exception, e:
        print str(e)
        print len(div.contents)
        # print len(soup.div.contents)
        raise e

    # Now process the text into words - must include page title
    words = findUniqueWords(pagetitle + " " + bodytext)
    # Associate each word with the word type and number of syllables
    # Use a dictionary for future expansion of keywords (otherwise tuple)
    for word in words:
        wordkey = word.lower()
        wordtype = findWordType(word)
        syll = countSyllables(word)
        # FUTURE: Check for word roots (i.e. prefixes/suffixes)
        # FUTURE: If not using other keys outside 'rep' generation
        # then take out the rest of the dict
        wordlist[wordkey] = {'type': wordtype,
                             'syll': syll,
                             }

        # Generate new words/letters based on word types
        if wordtype is NUMERIC:
            # Don't currently replace numerics
            wordlist[wordkey]['rep'] = word
        else:
            if wordtype is LETTER:
                if syll == 0:
                    # Not a vowel? Replace with random consonant
                    wordlist[wordkey]['rep'] = wordgen.cons(syll)
                else:
                    # Replace single vowel with a single random vowel
                    wordlist[wordkey]['rep'] = wordgen.vowel(syll)
            else:
                # Normal word; generate a new one
                wordlist[wordkey]['rep'] = wordgen.word(syll)

    # Replace all the instances of the words in the title and body
    # Handles multi-word titles and punctuation like parentheses
    h1.string.replace_with(re.sub('(\w+)',
                           lambda x: regexWordMatch(x, wordlist),
                           unicode(h1.string)))

    # Parse through the body tag text and replace display text
    # Handles all children as well as punctuation
    # Words are replaced but maintain original capitalization
    text = [tagtxt for tagtxt in div.strings]
    text.reverse()
    for tagtxt in text:
        tagtxt.replace_with(re.sub('(\w+)',
                            lambda x: regexWordMatch(x, wordlist),
                            unicode(tagtxt)))

    # Update the html with the gibberized body text
    soup.find(bodyStrainer).replace_with(div)

    # Make sure the output path exists - rudimentary path compliance
    abspath = os.path.abspath(outputpath)
    outputfile = os.path.join(abspath, outfile)
    # If the path does not exist, create it
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    # Overwrite the file if it exists without asking
    with open(outputfile, 'w') as f:
        f.write(soup.encode())
    f.close()

    # Return the output file path
    return outputfile


def regexWordMatch(match, wordlist):
    """Returns the replacement text for a given match from a wordlist
    dict. Restores capitalization based on the matched text.

    Keywords:
    match - Match object from regex
    wordlist - Dict containing old/new word pairs

    Returns the gibberized word if it appears in the wordlist
    """
    matchtxt = str(match.group(0))
    matchkey = matchtxt.lower()
    matchcase = findCapsType(matchtxt)

    if matchkey in wordlist:
        # print "Matched word: ", matchkey
        return CAP_TYPES[matchcase](wordlist[matchkey]['rep'])
    else:
        # print "No match: ", matchkey
        return matchtxt


def stripPunctAndSplit(inputstring):
    """Strips punctuation from an input string and splits it into
    individual words. Returns an array of words.
    """
    return punctregex.sub(' ', inputstring).split()


def findUniqueWords(bodycontents, sortlist=True):
    """Takes an string input and compiles a list of unique words

    Keywords:
    bodycontents - string input
    sortlist - T/F whether to sort word list by length (ascending)

    Returns an array of unique words.
    """

    # Remove punctuation and all whitespace by turning contents
    # into an array of words
    words = stripPunctAndSplit(bodycontents)

    # Remove duplicate words
    wordlist = list(set(words))

    # If desired, sort the returning wordlist by length
    # This is for future expansion to only gibberize partial articles
    # because gibberizing should leave the most common short words
    # (e.g. a, and, the, etc.) and gibberize the longer ones
    if sortlist:
        wordlist.sort(key=len)

    # TODO: Search for suffixes such as -ing -s -ed -ly so root words
    # remain related after gibberizing
    return wordlist


def findWordType(word):
    """Finds whether the given word is a normal word (alpha), numeric,
    or single letters"""
    # Find the number of numeric characters in the word
    nums = len(re.findall(numregex, word))

    if nums > 0:
        return NUMERIC
    elif len(word) == 1:
        return LETTER
    else:
        return ALPHA


def findCapsType(word):
    """Determine given word's capitalization type"""
    # Find the number of capital letters in the word
    caps = len(re.findall(capregex, word))
    nums = len(re.findall(numregex, word))

    if caps == len(word):
        return UPPER
    elif caps == 1:
        # TODO: Verify it's the first letter that's capitalized
        # return WORD_TYPES.index(TITLE)
        return TITLE
    elif caps + nums == len(word):
        # This is a mixed numeric with all-caps letters in it
        return UPPER
    else:
        return LOWER


def countSyllables(word):
    """Returns the number of syllables in a word.
    As a simplification, uses the number of vowels to approximate
    syllable count."""
    # As a simplification, let's count the number of vowels
    # TODO: Figure out some rough syllable count
    return countVowels(word)


def countVowels(word):
    """Returns the number of vowels in the word"""
    numvowels = len(re.findall(vowelregex, word))

    if numvowels > 2:
        numvowels = numvowels / 2

    return numvowels


def alterString(inputstring, wordlist):
    """Replaces words in the input string with their replacements
    in the given wordlist dict. Any word not in the wordlist keys
    will be skipped.

    This functionality has been superseded in main program flow
    by regex but is kept as a utility.

    Keywords:
    inputstring - input string to substitute words inputstring
    wordlist - Dict containing old/new word information
    """
    newstr = inputstring.split(" ")

    for kk in range(len(newstr)):
        words = punctregex.sub(' ', newstr[kk].strip()).split()
        # print repr(words)
        for word in words:
            if word in wordlist:
                rep = wordlist[word]['rep']
                newstr[kk] = string.replace(newstr[kk], word, rep)

    return " ".join(newstr)

if __name__ is "__main__":
    # FUTURE: Handle or prompt for keyword arguments
    outfile = translatePage()
    print "Page scrambled! Output is at:\n", outfile
