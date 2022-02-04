import com.nttdata.dgi.util.io as io
from threading import Lock
from textacy import load_spacy_lang
from langdetect import detect
from spacy.tokens import Doc
import cfg.ctt as ctt


class SingletonMeta(type):
    _instances: dict
    _lock: Lock = Lock()
    _lang_models: dict

    def __call__(cls, lang_models: dict = {}, def_lang='en'):
        cls._lang_models = lang_models
        cls._instances = {}
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(lang_models)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DynamicLangModel:
    """
    Dynamic instantiation of the Language Models pool,
    used to load the language models once. Make sure that the instance is created in a safe thread context.
    See example below.
    """

    _nlp: dict
    _languages: dict
    doc: Doc

    def __init__(self, lang_models: dict = {}, def_lang: str = 'en') -> None:
        """
        Loads the following language models and exposes them through the property nlp(lang: str).
        :param lang_models: A dictionary like this:
            {   'es': 'es_core_news_lg',
                'pt': 'pt_core_news_lg',
                'fr': 'fr_core_news_lg'
            }
        """
        self._languages = lang_models
        # Since the nlp.lemma.lemmatize function sets 'en' as default when the required language is not found,
        # to make this function compatible with nlp package as it is, such a language has to be included as follows:
        self._languages.update(ctt.MAIN_DEFAULT_LANGUAGE_MODEL)
        self._def_lang: str = def_lang
        self._nlp = {}

        for lang in self._languages:
            self._nlp[lang] = load_spacy_lang(self._languages[lang], disable=("parser",))
            if 'sentencizer' not in self._nlp[lang].pipeline:
                # Add sentencizer, otherwise no access to doc.sents
                self._nlp[lang].add_pipe('sentencizer')
        io.log(f"All the linguistic models have been loaded.")

    def get_languages(self):
        return self._languages

    def get_model(self, lang: str):
        if lang not in self._languages:
            io.log(message="Language model '" + lang +
                   "' not found. Please review the configuration. Going on with the default language.")
            return self._nlp[self._def_lang]
        return self._nlp[lang]

    @staticmethod
    def detect_language(text: str) -> str:
        return detect(text)


class LangModel(metaclass=SingletonMeta):
    """
    Singleton used to load the language models once. Make sur that the instance is created in a safe thread context.
    See example below.
    """

    _nlp: dict
    _languages: dict
    doc: Doc

    def __init__(self, lang_models: dict = {}, def_lang: str = 'en') -> None:
        """
        Instantiates a singleton class, loads the following language models and exposes them through the property
        nlp(lang: str).
        :param lang_models: A dictionary like this:
            {   'es': 'es_core_news_sm',
                'pt': 'pt_core_news_sm',
                'fr': 'fr_core_news_sm'
            }
        """
        self._languages = lang_models
        # Since the nlp.lemma.lemmatize function sets 'en' as default when the required language is not found,
        # to make this function compatible with nlp package as it is, such a language has to be included as follows:
        self._languages.update(ctt.MAIN_DEFAULT_LANGUAGE_MODEL)
        self._def_lang: str = def_lang
        self._nlp = {}

        for lang in self._languages:
            self._nlp[lang] = load_spacy_lang(self._languages[lang], disable=("parser",))
            if 'sentencizer' not in self._nlp[lang].pipeline:
                # Add sentencizer, otherwise no access to doc.sents
                self._nlp[lang].add_pipe('sentencizer')
        io.log(f"All the linguistic models have been loaded.")

    def get_languages(self):
        return self._languages

    def get_model(self, lang: str):
        if lang not in self._languages:
            io.log(message="Language model '" + lang +
                   "' not found. Please review the configuration. Going on with the default language.")
            return self._nlp[self._def_lang]
        return self._nlp[lang]

    @staticmethod
    def detect_language(text: str) -> str:
        return detect(text)
