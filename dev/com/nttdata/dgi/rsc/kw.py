"""
1. Extracts n-grams and frequencies (tf) from a resource,
2. Lemmatizes the ngrams,
3. Links the n-grams, lemmas and frequencies to the resource
4. Stores the results in two graph stores, a "kwr_tree" graph (keyword-resource) and a "terms" graph.

The terms graph is candidate to become the general pool of the corpus-terms. The code relating terms and concepts from
thesauri to terms in the resources can use this pool. But it also can be used to generate word-clouds per resource,
calculate resource and corpus-related frequencies and inverse frequencies, etc.
"""
import json
import requests
import langdetect as ld
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.nlp.stopwords import StopWords
from com.nttdata.dgi.nlp.bags.bagworker import BagWorker
from com.nttdata.dgi.nlp.lemma import lemmatize
from com.nttdata.dgi.nlp.langmodels import LangModel
from com.nttdata.dgi.rsc.kwi import KeywordWorkerInterface
from com.nttdata.dgi.rsc.document_part_type import DocumentPartType


class KeywordWorker(KeywordWorkerInterface):
    rsc_details: dict  # Resource path, etc.
    operational_details: dict  # Lemmatizer endpoint, the n of n-grams, ...
    connection_details: dict  # Connection to the graph store
    stopper: StopWords  # Eagerly instance used to determine whether a term is a stop-word
    bot: list  # Bag of lemmas, terms and frequencies extracted from the resource
    nlp: LangModel  # nlp: A specialization of Spacy, implemented as a Singleton, just in case a

    # lemmatizer endpoint is not supplied

    def __init__(self, operational_details: dict,
                 rsc_details: dict = None,
                 connection_details: dict = None,
                 nlp: LangModel = None):

        super(KeywordWorker, self).__init__()
        self.rsc_details = rsc_details
        self.operational_details = operational_details
        self.connection_details = connection_details
        self.nlp = nlp
        self.bot = None

    def _strip_stoppers_(self, neat_list: list, lang: str) -> list:
        """
        Removes stoppers from the head and tail of the term. This may cast empty string if the term was
        formed entirely of stop-words. We remove them, too.
        """
        neat_list = [(self.stopper(lang=lang, tokens=term).strip().__str__(), freq) for term, freq in neat_list]
        neat_list = [x for x in neat_list if x[0] != '']
        return neat_list

    def _cleanse_(self, terms: list, lang: str) -> list:
        """
        # Remove low frequencies, stopwords, and numbers
        """
        # The following line also removes one-word stoppers.
        # terms is a list of tuples (term, frequency)
        neat_list = [x for x in terms if not self.__skip__(x)]
        # Let's also remove heading and tailing stop-words, e.g. 'and to learn from here to' into 'learn', or
        # "y esto es una palabra de otras" into 'palabra', etc.
        # The neat_list is made of tuples (term, freq)...
        # Beware that after removing stopwords, the result may come empty
        neat_list = self._strip_stoppers_(neat_list, lang)
        # After that, duplicated tuples may exist, so let's remove them
        neat_list = list(set([i for i in neat_list]))
        return neat_list

    def __skip__(self, tup: tuple) -> bool:
        term = tup[0]
        freq = tup[1]
        min_tf = self.operational_details.get('min_tf')
        freq_ok = freq >= min_tf if min_tf else 1
        min_term_len = self.operational_details.get('min_term_len')
        size_ok = len(term) > min_term_len if min_term_len else 1
        is_number = True
        try:
            num = term.replace(' ', '')  # Many terms can be of the form 10 000 11 00
            int(num)
        except ValueError:
            is_number = False

        # Since this is an operation that is execute a zrillion times, the StopWords class is instantiated
        # eagerly, and the the __call__() method is invoked repeatedly. No need to specify the lang since
        # it was already initialized when creating the instance of the Stopword class, for this resource.
        is_stop = self.stopper().is_stopper(term)
        return not freq_ok or not size_ok or is_number or is_stop

    @staticmethod
    def __combinations__(phrase: str, ret: {}, lang: str) -> {}:
        # ret['accented-plus-stopwords'] = phrase
        # ret['accented-minus-stopwords'] = StopWords(phrase, lang=lang).remove_stopwords()[0]
        accented_minus_stopwords = StopWords(phrase, lang=lang).remove_stopwords()[0]
        # ret['unaccented-plus-stopwords'] = io.unaccent(ret['accented-plus-stopwords'])
        # ret['unaccented-minus-stopwords'] = io.unaccent(ret['accented-minus-stopwords'])
        ret['unaccented-minus-stopwords'] = io.unaccent(accented_minus_stopwords)
        return ret

    @staticmethod
    def _link_lemma_to_terms_(lemma_terms: dict, lemma: str, term: str, freq: int) -> dict:
        lemma_terms[lemma] = ([term], freq) if lemma not in lemma_terms.keys() else \
            lemma_terms[lemma] + (([lemma], freq) if lemma not in lemma_terms[lemma] else [])
        return lemma_terms

    @staticmethod
    def __md5_lemma_dict__(lemma: str, term: str) -> dict:
        """
        Builds a dictionary with its md5 hash, the lemma and the original term before lemmatization
        :param term: the term(s) with the same lemma
        :return: a dictionary with the lemma, its md5 and the original term before lemmatization
        """
        md5 = io.hash(lemma)
        return {'id': md5, 'lemma': lemma, 'terms': term}

    def __lemmatize__(self, term: str, lang: str) -> str:
        """
        This is the most internal lemmatization-related method...It this one that actually invokes the
        lemmatization service.
        :param term: the term to lemmatize
        :param lang: the language of the term
        :return: the lemmatized term

        ret = {'term': term,
               'accented-minus-stopwords': '',
               'accented-plus-stopwords': '',
               'unaccented-minus-stopwords': '',
               'unaccented-plus-stopwords': ''}
        """
        ret = {'term': term,
               'unaccented-minus-stopwords': ''}

        lemma = ''
        lem_endpoint = self.operational_details.get('lemmatizer_endpoint')
        if not lem_endpoint:
            unaccented_phrase_plus_stops = lemmatize(phrase=term, nlp=self.nlp, lang=lang)
            # ret['accented-plus-stopwords'] = unaccented_phrase_plus_stops
            lemma = self.__combinations__(unaccented_phrase_plus_stops, ret, lang)['unaccented-minus-stopwords']
        elif lem_endpoint:
            jo = {'phrase': term, 'lang': lang}
            res = requests.post(url=lem_endpoint, json=jo)
            if res.ok:
                lemma = json.loads(res.content)['unaccented-minus-stopwords']
            else:
                print("Something happened with the lemmatizer service: response NOT OK")
        return lemma

    def _decide_lang_(self, term: str, rsc_lang: str) -> str:
        """
        Decides whether the term is equal of the same language than the resources' language. This function is quite
        absurd, but it removes non-linguistic relevant items, e.g. terms containing only numbers or symbols.
        """
        try:
            term_lang = ld.detect(term)
        except Exception:
            # Normally a "non linguistic feature", e.g. '---' and similar trash
            return None
        return rsc_lang

    def _lemmatize_(self, terms: list,
                    rsc_lang: str) -> list:
        # Lemmatize
        lemma_list: list = []
        # We're interested in keeping the original term from where one lemma was originated
        lemma_terms: dict = {}
        for term, freq in terms:
            # Resources may contain terms in different languages. We need to decide whether the
            # language of the term coincides with the language of the whole rsc. If not a decision
            # needs to be made.
            lang = self._decide_lang_(term, rsc_lang)
            if lang:
                lemma = self.__lemmatize__(term, lang)
                lemma_list.append({
                    'lemma_id': io.hash(lemma),
                    'lemma': lemma,
                    'term': term,
                    'freq': freq})
            # If no lang -> the term contains no linguistic features, e.g. '---', and similar trash
        return lemma_list

    @staticmethod
    def _keep_higher_freq_term_(cleansed_terms: list):
        ret = {}
        for term, freq in cleansed_terms:
            ret[term] = freq if term not in ret.keys() else max(freq, ret[term])
        return list(ret.items())

    def _fo_freq_(self, terms: list) -> list:
        freq = self.operational_details.get('min_tf_body')
        if freq:
            terms = [t for t in terms if t[1] >= freq]
        return terms

    def extract(self, phrase: str, rsc_part: str, rsc_lang: str = None):
        """
        Extracts n-grams from a text and lemmatizes them.
        :param phrase: the text to extract n-grams from
        :param rsc_lang: the language of the resource text. If not provided it is auto-detected.
        :param rsc_part: signals whether the phrase comes in a title, an abstract, the body, etc.
        :return: a list of tuples with (lemma, term, freq)
        """
        # Checker
        if not phrase or phrase == '':
            self.bot = None
            return self
        rsc_lang = rsc_lang if rsc_lang else ld.detect(phrase)
        # The StopWords() class is used inside _skip_(), but it is eagerly instantiated here to save resources.
        self.stopper = StopWords(lang=rsc_lang)
        bw: BagWorker = BagWorker()
        # terms -> list of terms and frequency, wc -> word count
        terms = list(bw.bongrams(phrase=phrase,
                                 n_range=self.operational_details.get('ngram_range'),
                                 lang=rsc_lang,
                                 sentencize=False))
        # We need to reduce the cost of lemmatizing to the minimum, so let's do some house-cleansing:
        # The following method will remove low-frequency terms, stop-words, and only-numbers

        cleansed_terms = self._cleanse_(terms, rsc_lang)

        if rsc_part == DocumentPartType.BODY.name.lower():
            '''
            There is the need of filtering out very low frequencies of the tf (term frequency in one document). 
            Otherwise the lemmatizations takes an eternity. 'fo_freq' stands for 'filter out frequencies lesser than...'
            what it is in the ctt configuration file (variable MIN_RSC_TERM_FREQUENCY)  
            '''
            terms_filtered = self._fo_freq_(cleansed_terms)
        else:
            terms_filtered = cleansed_terms

        io.log(f"--- Terms: {len(terms)} // Cleaned terms: {len(cleansed_terms)} "
               f"// Filtered terms: {len(terms_filtered)} ---")
        del terms
        # This self.bot is a list of dictionaries. Each dictionary contains a triple lemma, term, freq of the resource.
        # The list will be used to build a n-quad and/or a json line with all these triples associated to a
        # history entry.
        self.bot = self._lemmatize_(terms=terms_filtered,
                                    rsc_lang=rsc_lang)
        return self
