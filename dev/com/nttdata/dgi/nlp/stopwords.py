from __future__ import annotations
import langdetect
import com.nttdata.dgi.util.io as io
import spacy.lang.en.stop_words as en_stoppers
import spacy.lang.es.stop_words as es_stoppers
import spacy.lang.fr.stop_words as fr_stoppers
import spacy.lang.pt.stop_words as pt_stoppers

es_stoppers.STOP_WORDS.add('y')


class StopWords:
    """
    Removes stopwords from 'en', 'es', 'fr', and 'pt' language phrases.
    BEWARE THAT importing the stoppers takes a while. Hence, it is recommended to:
    1. Create an instance of the class once, and then
    2. Invoke the __cal__() method iteratively.
    Example:
          stoppers = StopWords()
          for i in range(1000):
            result_once_removed = stoppers('this is an English sentence', 'en').remove().result_
    """

    tokens: list
    tokens_: str
    lang: str
    result: list              # The result of removing the stopwords as a list
    result_: str              # The result of removing the stopwords as a string
    known_langs: tuple

    def __init__(self, tokens=None, lang: str = None, known_languages: tuple = ('en', 'es', 'fr', 'pt')):
        self.init(tokens, lang, known_languages)

    def init(self, tokens, lang: str, langs: tuple):
        self.tokens = tokens if type(tokens) == list else None
        self.tokens_ = tokens if type(tokens) == str else None
        self.known_langs = langs

        self.lang = lang
        self.result_ = ''
        self.result = []

    def __eval__(self):
        if self.lang not in self.known_langs:
            # io.log(f'StopWords() class says: language {self.lang} unknown for this project. '
            #       f'Please review content of the text.', level='w')
            return []
        return eval(self.lang + '_stoppers.STOP_WORDS')

    def __as_list__(self, l_: list) -> tuple(list, str):
        # This should also join the Spacy token.text(s)
        sl = self.__eval__()
        return ' '.join(token for token in l_ if token not in sl), \
               [token for token in l_ if token not in sl]

    def is_stopper(self, term: str, lang: str = None) -> bool:
        """
        Usage: 1) sw = StopWords(), 2) sw().is_stopper('the', 'en'); or alternatively, sw('en').is_stopper('the')
        :returns: True if the word is a stop word
        """
        # We're only interested in one-word terms
        if len(term.split()) > 1:
            return False

        self.lang = lang if lang else self.lang
        sl = self.__eval__()
        return term in sl

    def _tokenize_(self, term: str, lang: str = None) -> tuple(list, str):
        """
        Common operations prior to the stripping of stop-words
        :param term: the term to process
        :param lang: the lang of the term. If no lang available in lan or in self.lang, it is auto-detected.
        :return: a list with the tokens of the term, ready for stripping, along with the language of the term
        """
        l_ = term.split()
        lang = lang if lang else self.lang
        lang = langdetect.detect(term + '.') if not lang else lang
        return l_, lang

    def _check_post_strip(self, tokens: list, i: int, left: bool) -> str:
        if len(tokens) == 0:
            self.result_ = ''
            return self.result_

        l_ = tokens[i:] if left else tokens[:i]
        if len(l_) > 1:
            self.result_ = '' if len(l_) == 0 else ' '.join(l_)
        elif len(l_) > 0 and self.is_stopper(l_[0]):
            self.result_ = ''
        elif len(l_) > 0:
            self.result_ = l_[0]
        return self.result_

    def lstrip(self):
        """
        Removes any stop word(s) found at the beginning of a term
        """
        self.result_ = self.tokens_ if self.result_ == '' else self.result_
        if self.result_ == '': return self
        tokens, lang = self._tokenize_(self.result_, self.lang)
        i = 0
        for i in range(len(tokens)):
            if not self.is_stopper(tokens[i], lang):
                break
        self.result_ = self._check_post_strip(tokens, i, left=True)
        return self

    def rstrip(self):
        self.result_ = self.tokens_ if self.result_ == '' else self.result_
        if self.result_ == '': return self
        tokens, lang = self._tokenize_(self.result_, self.lang)
        i = len(tokens)
        for i in range(len(tokens), 0, -1):
            if not self.is_stopper(tokens[i-1], lang):
                break
        self.result_ = self._check_post_strip(tokens, i, left=False)
        return self

    def strip(self):
        self.lstrip().rstrip()
        return self

    def get_result_(self) -> str:
        return self.result_

    def get_result(self) -> list:
        return self.result

    def remove_stopwords(self) -> tuple(str, list):
        if self.tokens:  # If the phrase comes as a list of tokens
            self.result_, self.result = self.__as_list__(self.tokens)
        elif self.tokens_:  # If the phrase comes as a string
            self.result_, self.result = self.__as_list__(self.tokens_.split(' '))
        return self.result_, self.result

    def remove(self):
        self.remove_stopwords()
        return self

    def __call__(self, lang: str = None, tokens=None, known_languages: tuple = ('en', 'es', 'fr', 'pt')):
        self.lang = lang if lang else self.lang
        self.tokens = tokens if tokens else self.tokens
        self.init(self.tokens, self.lang, langs=known_languages)
        return self

    def __str__(self):
        return self.result_

    def __add__(self, other):
        if isinstance(other, StopWords):
            other = other.result_
        self.result_ += other
        return self

