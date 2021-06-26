# Spelling Bee Solver

Spelling Bee is a game in the New York Times where you find all words composed only of 7 letters.  Every word must
contain one of the letters.  Letters can be repeated.  There is always at least one work composed of all 7 letter.  Words
must be at least 4 characters.  No proper names.

Points are scored based on the length of the words:  1 point for 4 letters, 1 point per letter above that.  Any words containing
all of the letter get a 7 point bonus.  So, longer words are much more valuable.

This solver uses a dictionary of English words.  Unfortunately, this dictionary does not contain many inflections.  Inflections are
words with (typically) a suffix that modifies the meaning.  For example, "bake", "baker", "bakes", "baked", "baking" are all inflected
forms of "bake".

The dictionary being used is about 28,000 words, so it is far from comprehensive.  This dictionary is not the one used
for the "real" Spelling Bee, so there are cases where this includes words that the "real" Spelling Bee does not include, and vice versa.

The dictionary used identifies names with starting capital letters.  These are displayed but are typically not valid, since names are
not acceptable solutions.

To deal with the lack of inflections, the program suggests suffixes that are typical based on "part of speech".
So, manually scan the word list and try these suffixes to discover additional words.
(The program cannot do this since it does not have a dictionary identifying valid inflected words.)

It is possible for the required letter to be in a suffix:  the solver will never find these words.  To helpl with this situation, the
Solver will show the possibly inflected version of words with suffixes with the required letter.  Again, its up to you to scan
this list and identify additional valid words.

For instructions on running and deploying the code, see [Quickstart: Create a Python app in Azure App Service on Linux](https://docs.microsoft.com/azure/app-service/quickstart-python).

## Implementation

Implemented in Python and hosted by Microsoft Azure.
