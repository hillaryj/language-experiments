# language-experiments

Provides `translatePage` and other functions for generating word lists from input strings.

The random seed is drawn from the page URL, so between script changes the same page will always be gibberized the same.

The function `translatePage` comes configured for Wikipedia and has been tested with Wikipedia pages. The `translatePage` method has been set for Wikipedia pages in particular, but uses parameters so it can be applied to a page with a header (h1) and body div id; however this has not been extensively tested.

This also takes relative HTML paths and outputs absolute paths for links, css, and images. This is so the generated page output looks like the source page as much as possible.

# Setup and run

First, clone the repository

Run via the command line to see example page ("Gladiola" Wikipedia page which outputs to `current-working-directory/test.html`)

    python pagetranslate.py

Or, run inside a shell to be able to specify pages and locations. The function will return the output path to the gibberized file.

    python
    import pagetranslate
    translatePage(pageurl="<pageurl>",
                  outputpath="~/output-folder",
                  outfile="test.html",
                  titleid="firstHeading",
                  bodyid="mw-content-text",
                  percent=100)

# Examples

Original page is on the left and gibberized page is on the right.

Gibberizing the "dog" Wikipedia page:
![Dog turns into Sogh](https://github.com/hillaryj/language-experiments/blob/master/gibberizer-example-dog.png)

Gibberizing the "Jeep Wagoneer" Wikipedia page:
![Jeep Wagoneer turns into Bilner Wechwin](https://github.com/hillaryj/language-experiments/blob/master/gibberizer-example-wagoneer.png)

# Limitations

This script does not translate/gibberize the following cases:

- Words with accented letters
- Words with mixed letters/numbers (i.e. acronyms)
- Numerics e.g. dates

# Future plans:

- Add arguments to run via command line
- Convert words with accented letters to unaccented equivalents or support accents
- Gibberize individual letters of words with mixed letters and numbers (i.e. acronyms and initialisms)
- Add arguments for whether to gibberize numbers and dates
- Allow certain percentages of words to be left un-gibberized, e.g Leave shortest words first like `a`, `the`, `and` to make the text somewhat recognizable
- Expand to detect suffixes/prefixes so root words are gibberized consistently
