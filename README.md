# What is `language-experiments`? [![Total alerts](https://img.shields.io/lgtm/alerts/g/hillaryj/language-experiments.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/hillaryj/language-experiments/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/hillaryj/language-experiments.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/hillaryj/language-experiments/context:python)

Python2-based string/language experimentation which, as a whole, will turn a Wikipedia page into reasonable-looking gibberish.

Gibberizing the `dog` Wikipedia page:
![Dog turns into Sogh](https://github.com/hillaryj/language-experiments/blob/master/gibberizer-example-dog.png)

## Specifics

Provides `translatePage` and other functions for generating word lists from input strings.

The random seed is drawn from the page URL, so between script changes the same page will always be gibberized the same.

The function `translatePage` comes configured for Wikipedia and has been tested with Wikipedia pages. The `translatePage` method has been set for Wikipedia pages in particular, but uses parameters so it can be applied to a page with a header (h1) and body div id; however this has not been extensively tested.

This also takes relative HTML paths and outputs absolute paths for links, css, and images. This is so the generated page output looks like the source page as much as possible.

# Setup and run

First, clone the repository

Run via the command line to see example page ("Gladiola" Wikipedia page which outputs to `current-working-directory/test.html`) or specify other options via arguments.

    python2 pagetranslate.py

    optional arguments:
      -h, --help            show this help message and exit
      -url PAGEURL, --page-url PAGEURL
                            URL of page to be gibberized (Default:
                            https://en.wikipedia.org/wiki/Gladiola)
      -path OUTPUTPATH, --output-path OUTPUTPATH
                            Output path (Default: current directory)
      -file OUTPUTFILE, --output-file OUTPUTFILE
                            Output filename (Default: "test.html")
      -titleid TITLEID      Title HTML element ID to gibberize (Default:
                            Wikipedia: "firstHeading")
      -bodyid BODYID        Body HTML element ID to gibberize (Default: Wikipedia:
                            "mw-content-text")
      -pct PERCENT, --percent-gibberize PERCENT
                            (FUTURE)Percentage of words to change. (Default: 100)
      --convert-numbers     (FUTURE)Set to gibberize numbers. (Default: False)
      --convert-dates       (FUTURE)Set to gibberize dates. (Default: False)

Or, run inside a shell to be able to specify pages and locations. The function will return the output path to the gibberized file.

    python2
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

# Ideas for expansion

- Convert words with accented letters to unaccented equivalents or support accents
- Gibberize individual letters of words with mixed letters and numbers (i.e. acronyms and initialisms)
- Implement options for whether to gibberize numbers and dates
- Implement option for certain percentages of words to be left un-gibberized, e.g Leave shortest words first like `a`, `the`, `and` to make the text somewhat recognizable
- Expand to detect suffixes/prefixes so root words are gibberized consistently
