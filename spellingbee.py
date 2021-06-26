#!python
#
# SpellingBee solver.  Words containing only letters from a string,
# and word must contain first letter.
#

from english_words import english_words_alpha_set
from typing import List, Tuple, Dict
import sys

class SpellingBee:
    def __init__(self, letters: str):
        self.letters = letters.lower()
        if len(self.letters) != 7:
            raise Exception("String of letters to form words from must be of length 7" )

        self._all_words = english_words_alpha_set

        # results available as fields
        self.names, self.words = self.find_words()
        self.all_letter_words = self.max_word()
        self.candidate_suffixes = SpellingBee.possible_suffixes(self.letters)
        self.inflections, self.inflection_max_words = self.inflected_words()

    @staticmethod
    def _vowel(c: str) -> bool:
        return c in 'aeiouy'
    
    @staticmethod
    def _append_suffix(w: str, sfx: str) -> str:
        ''' Append suffix to word, but don't just append if words ends with vowel and
            suffix starts with vowel. '''
        if SpellingBee._vowel(sfx[0]) and SpellingBee._vowel( w[-1] ):
            return w[0:-1] + sfx
        else:
            return w + sfx
    
    @staticmethod
    def _max_word(w: str) -> bool:
        ''' Is this a maximal word? '''
        return len(set(w)) == 7

    def score(self) -> int:
        ''' Calculate the score for the word list, which must exist. '''
        score = lambda x: 0 if len(x) <= 3 else 1 if len(x) == 4 else (len(x) + 7) if len(set(x)) == 7 else len(x)
        return sum([score(w) for w in self.words])
    
    def find_words(self) -> Tuple[List[str], List[str]]:
        ''' Get lists of words and names, in member variables. '''
        # words must be at least 4 letters and contain the first letter in the target
        self._all_words = english_words_alpha_set
        only = filter(lambda x: len(x) >= 4 and self.letters[0] in x.lower(), self._all_words)
    
        # check if only target letters by translating into Nones
        all_letters = self.letters + self.letters.upper()
        x = str.maketrans("", "", all_letters)
        self._result = sorted( [ w for w in only if not w.translate(x) ] )
    
        # Names are capitalized, and aren't valid
        names = [ w for w in self._result if str.isupper(w[0]) ]
        words = [ w for w in self._result if str.islower(w[0]) ]
        return (names, words)
    
    
    def consider(self, additional: str) -> List[str]:
        ''' Consider words with additional letter not in set at end, e.g.,
            an ending "e" that gets dropped for a suffix. '''
        add_only = filter(lambda x: len(x) >= 4 and self.letters[0] in x.lower() and x[-1] == additional, self._all_words)
        add_x = str.maketrans("", "", self.letters + additional)
        add_result = sorted( [ w for w in add_only if not w.translate(add_x) ] )
        return add_result
    
    def max_word(self) -> List[str]:
        # Was the word with all letters found?
        all_letters_words = [w for w in self._result if SpellingBee._max_word(w) ]
        return all_letters_words
    
    # this dictionary does not deal with inflection.  The problem is the inverse of
    # stemming and lematization:  adding additional words to lemmas based on available
    # suffixes.  Doing this properly requires categorizing words in parts of speech. 
    # Could use NLTK to do this.  It also has a larger dictionary.
    
    # suffixes by part of speech (POS)
    suffixes = {
            "noun": ["er", "ion", "ity", "ment", "nes", "or", "sion", "ship", "th", "s"], 
            "adj":  ["able", "ible", "al", "ant", "ary", "ful", "ic", "ious", "ous", "ive", "les", "y"], 
            "verb": ["ed", "en", "er", "ing", "ize", "ise", "d", "s"], 
            "adv":  ["ly", "ward", "wise"]
            }

    @staticmethod
    def possible_suffixes(letters: str) -> Dict[str, List[str]]:
        ''' Get possible suffixes based on target letters. '''
        good_set = set(letters)
        candidate_suffixes = {}
        for pos,suffix_list in SpellingBee.suffixes.items():
            candidates = [ s for s in suffix_list if len(good_set & set(s)) == len(s) ]
            if candidates:
                candidate_suffixes[pos] = candidates
        return candidate_suffixes

    def inflected_words(self) -> Tuple[Dict[str, List[str]], List[str]]:
        ''' if the required letter is in a suffix, then there might be valid inflections with
            the suffix for lemmas that DON'T have the required letter.  Find those suffixes. '''
        sfx_list: List[str] = []
        for sfx in self.candidate_suffixes.values():
            l = [ x for x in sfx if self.letters[0] in x ]
            sfx_list.extend(l)
    
        # if there are such suffixes ...
        inflections = {}
        max_words = []
        if len(sfx_list) > 0:
            # get words with only target letters (except the required letter) and min length:
            # I suspect this list is always non-zero.
            good_set = set(self.letters)
            others = [x for x in self._all_words if self.letters[0] not in x and len(good_set & set(x)) == len(set(x))]
            for s in sfx_list:
                # combine the (possible) lemma with the suffix, taking into account vowels
                l = sorted( [SpellingBee._append_suffix(w, s) for w in others if len(SpellingBee._append_suffix(w, s)) >= 4] )

                inflections[s] = l

                all_let_word = [ w for w in l if SpellingBee._max_word(w) ]
                max_words.extend( all_let_word )

        return inflections, max_words

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error:  no target string")
        sys.exit(1)
    letters = sys.argv[1]
    bee = SpellingBee(letters)
    print("Letters: ", letters)
    print("Names:", len(bee.names))
    print("\t", bee.names)
    print("Words:", len(bee.words))
    print("\t", bee.words)
    print("Max Words:") 
    print("\t", bee.all_letter_words)
    print("Predicted score =", bee.score())
    print("Suffixes:")
    for k, v in bee.candidate_suffixes.items():
        print("\t", k, v)
    print("Possible inflections:")
    for k, v in bee.inflections.items():
        print("\t", k, v)
    print("Possible inflection max words:", bee.inflection_max_words)
