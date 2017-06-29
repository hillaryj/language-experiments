# language-experiments

Provides `translatePage` and other functions for generating word lists from input strings.

The function `translatePage` comes configured for Wikipedia and has been tested with Wikipedia pages. The `translatePage` method has been set for Wikipedia pages in particular, but uses parameters so it can be applied to a page with a header (h1) and body div id; however this has not been extensively tested.

This also takes relative HTML paths and outputs absolute paths for links, css, and images. This is so the generated page output looks like the source page as much as possible.

# Setup and run

TBD.

# Limitations

This script does not translate/gibberize the following cases:

- Words with accented letters
- Words with mixed letters/numbers (i.e. acronyms)
- Numerics e.g. dates

# Future plans:

- Convert words with accented letters to unaccented equivalents or support accents
- Gibberize individual letters of words with mixed letters and numbers (i.e. acronyms and initialisms)
- Add arguments for whether to gibberize numbers and dates
- Allow certain percentages of words to be left un-gibberized, e.g Leave shortest words first like `a`, `the`, `and` to make the text somewhat recognizable
- Expand to detect suffixes/prefixes so root words are gibberized consistently
