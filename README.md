# Simple English Dictionary
A simple English dictionary in JSON format - a list of words, with meanings.

These are the output files from [tusharlock10's dictionary repo](https://github.com/tusharlock10/Dictionary), which he uploaded to [Dropbox](https://www.dropbox.com/s/qjdgnf6npiqymgs/data.7z?dl=1) (c/o [Stack Overflow](https://stackoverflow.com/a/54982015/)).

This repo includes multiple versions of the data: the original, a combined list, and a "kid-safe" version (for making kids apps/games). You can also tweak the filtering to your liking.

# Usage

You can consume the data in a variety of formats:

- `data` contains the individual, raw files from tusharlock - they are broken out by letter.
- `processed/merged.json` contains a single JSON file with all the words in it.
- `processed/filtered.json` contains a version with filtered-out words, meanings, synonyms, and antonyms; you can see the list of filtered words in `data/filter_words.txt`

# Creating your own Filtered List

You will need Python 3.x. Simply update `filter_Words.txt` and run `python3 filter.py`. Consider opening a PR, too!
