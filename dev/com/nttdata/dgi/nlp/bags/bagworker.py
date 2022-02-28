import json
import requests
import textacy
import langdetect
import numpy as np
import sklearn.feature_extraction.text as text
import com.nttdata.dgi.util.io as io
from spacy.tokens import Doc
from com.nttdata.dgi.nlp.langmodels import LangModel
from collections import Counter


class BagWorker:

    phrase: str     # The text from where to extract the terms
    nlp: LangModel  # Our pool of Spacy Lang Models
    ngrams: tuple   # The different n of the n-grams, e.g. (1, 2, 3, 4, 5)
    lang: str       # The lang of the phrase
    doc: Doc        # The tokenize phrase
    word_count: int  # The number of words in the phrase
    sent_endpoint: str # An endpoint to a sentencizer endpoint

    def __init__(self, phrase: str = None, nlp: LangModel = None, sent_endpoint: str = None):
        self.phrase = phrase
        self.nlp = nlp
        self.ngrams = (1, 2, 3, 4, 5)
        self.lang = 'en'
        self.doc = None
        self.word_count = 0
        self.sent_endpoint = sent_endpoint

    def __ngram__(self, doc, n: int) -> list:
        return list(set(textacy.extract.ngrams(doc, n, filter_stops=True, filter_punct=True, filter_nums=False)))

    def get_lang(self, phrase: str) -> str:
        try:
            return langdetect.detect(phrase)
        except Exception as e:
            raise e

    def bot(self, phrase: str, nlp: LangModel,
            ngrams: tuple = (1, 2, 3, 4, 5),
            min_len_4_gram_1: int = 3) -> ():
        """
        Beware bot() removes '\n' occurrences!
        """
        # TODO: DEPRECATE! the method bongram is much more efficient and lang-independent.
        lang = self.get_lang(phrase)
        doc = textacy.make_spacy_doc(phrase, nlp.get_model(lang))
        for n in ngrams:
            if n == 1:
                st = ' '.join([d.text for d in doc if len(d.text) >= min_len_4_gram_1 and '\n' not in d.text])
                doc = textacy.make_spacy_doc(st, nlp.get_model(lang))
            grams = self.__ngram__(doc, n)
            yield grams, lang

    def get_word_count(self, phrase: str = None):
        self.phrase = phrase if phrase else self.phrase
        vectorizer = text.CountVectorizer()
        self.word_count = len(vectorizer.fit_transform([self.phrase]).data)
        return self.word_count

    def _get_sents_from_enpoint_(self) -> []:
        if self.sent_endpoint:
            args: dict = {'phrase': self.phrase, 'lang': self.lang}
            res = requests.post(self.sent_endpoint, args)
            if res.ok:
                jo = json.loads(res.content)
                return jo['sentences']
        return []

    def _get_sents_from_nlp(self) -> []:
        """
        Uses the LangModel() class instead of a service's endpoint.
        :param sent_list: list of sentences already separated in a previous operation. If
        not empty then we do not want to re-get-them again. Otherwise we do
        :param lang: the language specified for the LangModel to know which model to use
        """

        model = self.nlp.get_model(self.lang)
        doc: Doc = model(self.phrase)
        return [sent.text for sent in doc.sents]
    
    def _get_sents_(self) -> []:
        sents: list = []
        if self.sent_endpoint:
            sents = self._get_sents_from_enpoint_()
        elif self.nlp:
            sents = self._get_sents_from_nlp()
        return sents

    def _get_bongrams_(self, sent: str, n_range: tuple):
        # Nasty effect of the vectorizer: words like 'revenue-based' are split into 'revenue' and 'based'. We need it
        # to be treated as one single word.
        sent = sent.replace('-', '__')
        sent = sent.strip().strip('\n')
        if len(sent) == 0:
            return []
        try:
            vectorizer = text.CountVectorizer(min_df=1, max_df=1.0, ngram_range=n_range)
            x_vec = vectorizer.fit_transform([sent])
            freqs = np.array(x_vec.todense()).tolist()
            # Retrieve back the hyphened words. Terms not containing '__' will remain unchanged
            terms = [term.replace('__', '-') for term in vectorizer.get_feature_names()]
            l_ = list(tuple(zip(terms, freqs[0])))
            return l_
        except Exception as ex:
            io.log(f'WARNING: Text {sent} could not be n-grammed because does not contain anything interesting, '
                   f'BagWorker class dixit. Exception: {ex}', level='w')
            return []

    def bongrams(self, phrase: str, n_range: tuple = (1, 5), lang: str = None, sentencize: bool = False) -> ([], int):
        """
        Extracts n-grams from the phrase, where n is specified in the n_range. Thus,
        if the n_range is (1, 2) n-grams of 1 and 2 terms only will be bagged. The occasion
        is used to calculate also the number of words inside the phrase, which is assigned
        to the class variable 'word_count'.
        :param phrase: the text from which to get the bag of terms
        :param n_range: the interval with the 'n' in n-grams
        :param lang: the language of the phrase. If None, it is self-detected (which has a cost!)
        :param sentencize: if true, the phrase is broken down into sentences, otherwise the whole phrase is bagged
            at once. The main reason for NOT to break down the bag into sentences is that the frequencies will
            be different: term-frequency-per-sentence vs. term-frequency-per-whole-text.
        :return: a list of tuples with the n-grams and the frequency the n-gram occurs in the text
        """
        self.phrase = phrase if phrase and len(phrase) > 0 else self.phrase
        self.lang = lang if lang and 0 < len(lang) < 3 else self.lang
        senta = self._get_sents_()
        ret = ()
        # If a sentencizer is provided, we break down the text into sentences,
        # Otherwise we return the n-grams of the text as provided (useful when
        # the text is just a small single sentence.
        if sentencize and len(senta) > 0:
            # Isn't this beautiful? it merges the inner lists into one single list...so elegant and efficient,
            # so pythonesc!
            ret = sum([self._get_bongrams_(sent, n_range) for sent in senta], [])
            # The identical (n-gram, freq) tuples in multiple sents have to be zipped/summed up...
            # The following line removes adds the frequencies of identical terms and removes the duplicated tuples
            ret = list(Counter(k for k, num in ret for i in range(num)).items())
        elif not sentencize:
            ret = self._get_bongrams_(self.phrase, n_range)
        return ret
