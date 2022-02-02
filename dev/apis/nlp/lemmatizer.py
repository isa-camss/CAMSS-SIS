import json
import langdetect
import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
import com.nttdata.dgi.nlp.lemma as lemma
from flask_restx import Namespace, Resource
from com.nttdata.dgi.nlp.langmodels import LangModel
from com.nttdata.dgi.nlp.stopwords import StopWords
from spacy.tokens import Doc

api = Namespace('nlp',
                description='NLP-related operations, e.g. lemmatization, stemming, bag of terms extraction, etc.')

model: LangModel = LangModel(lang_models=ctt.MAIN_DEFAULT_LANGUAGE_MODEL)

lem_args = api.parser()
lem_args.add_argument('phrase', required=True)
lem_args.add_argument('lang', required=False, default='')
lem_args.add_argument('mode', required=False, default=ctt.PREFERRED_LEMMATIZATION_MODE, help='modes: accented-plus-stopwords, accentend-minus-stopwords, unnaccented-plus-stopwords, unaccented-minus-stopwords or all')


def _combinations_(phrase: str, ret: dict, lang: str, term: str) -> dict:
    ret['accented-plus-stopwords'] = phrase
    # We need to allow for terms of 1 single word that may be confounded with stopwords, e.g. CAN, or BE, as
    # abbreviations of regions, countries, etc.
    t = StopWords(phrase, lang=lang).remove_stopwords()[0]
    ret['accented-minus-stopwords'] = term.lower() if t == '' else t
    accented_minus_stopwords = term.lower() if t == '' else t
    ret['unaccented-plus-stopwords'] = io.unaccent(ret['accented-plus-stopwords'])
    ret['unaccented-minus-stopwords'] = io.unaccent(ret['accented-minus-stopwords'])
    ret['unaccented-minus-stopwords'] = io.unaccent(accented_minus_stopwords)
    ret['lang'] = lang
    return ret


def _lang_allow_(lang: str):
    if lang not in ctt.PROJECT_LANGUAGES:
        io.log(f'Language provided/detected is {lang}, which does not belong to the set of languages allowed '
               f'for this project. Resetting language to {ctt.DEFAULT_LANGUAGE}')
        lang = ctt.DEFAULT_LANGUAGE
    return lang


@api.route('/lemmatize')
@api.expect(lem_args)
class Lematize(Resource):
    @api.doc("Given a term of one or more words, returns the original term and the corresponding "
             "accented/unaccented and stopped/unstopped lemmas")
    def post(self):
        """
        Lemmatizes a term of one or more words in a given language. If the language is not supplied, the lemmatizer will try to auto-detect it.
        """
        
        ret = {'term': None,
               'accented-minus-stopwords': None,
               'accented-plus-stopwords': None,
               'unaccented-minus-stopwords': None,
               'unaccented-plus-stopwords': None,
               'lang': None}
        
        try:
            args = lem_args.parse_args()
            phrase = args['phrase']
            mode = args['mode']
            if not args['lang'] or args['lang'] == '':
                io.log("Detecting language...")
                lang = langdetect.detect(phrase + '.')
                lang = _lang_allow_(lang)
            else:
                lang = io.alpha2(args['lang'])  # avoids en-US and similar, Spacy language models use ISO-alpha2
                lang = _lang_allow_(lang)
                
            combinations = lemma.lemmatize(phrase=phrase, nlp=model, lang=lang)
            ret['term'] = args['phrase']
            ret['lang'] = lang
            if not mode or mode != 'all':
                ret = {mode: _combinations_(combinations, ret, lang, args['phrase']).get(mode), 'lang': lang}
            else:
                ret = _combinations_(combinations, ret, lang, args['phrase'])
            io.log(json.dumps(ret))
            return ret, 200
        except Exception as e:
            m = f'The lemmatizer had some problem...possible cause: a requested language model may not have been loaded. ({e})'
            io.log(m)
            return {'message': m}, 500


_sent_args = api.parser()
_sent_args.add_argument("phrase", required=True, type=str,
                        help="The phrase (text) to break down into sentences.")
_sent_args.add_argument("lang", required=False, default=ctt.DEFAULT_LANGUAGE, type=str,
                        help="The language of the content to be split into sentences. If no language is "
                             "specified, it will be auto-detected (which introduces a relevant additional "
                             "calculation time-lapse).")

sentencizer_loaded: bool = False


def _sentencier_(args: dict) -> tuple:
    lang = args['lang']
    phrase = args['phrase']
    msg = {'message': 'Sentences successfully extracted. ', 'sentences': []}
    code = 201
    # 1. Make sure the phrase carries a period at the end
    phrase.rstrip('.') + '.'
    if len(lang) == 0 or lang not in ctt.PROJECT_LANGUAGES:
        msg['message'] += 'Language was auto-detected. '
        lang = langdetect.detect(phrase)
    # 2. Make sure the sentencier for this lang is loaded in the Spacy's pipeline, at no perceptible cost
    nlp = model.get_model(lang)
    doc: Doc = nlp(phrase)
    for sent in doc.sents:
        msg['sentences'].append(sent.text)
    return msg, code


@api.route('/sentencize')
@api.expect(_sent_args)
class Sentencizer(Resource):
    @api.doc("Given a text, it returns the sentences of the text. If no language is specified, the language is "                    
             "auto-detected (this has an impact on the performance).")
    def post(self):
        t0 = io.log(f'Splitting text into its sentences...')
        args = _sent_args.parse_args()
        msg, code = _sentencier_(args)
        msg['lapse'] = str(io.now()-t0)
        io.log(f'Text sentencized. It took {str(io.now()-t0)}.')
        return msg, code

@api.route('/ping')
class Ping(Resource):
    @api.doc("Returns 'pong' if invoked. Used to check that the NLP services are up and running.")
    def get(self):
        t0 = io.now()
        m = f'pong ({str(io.now()-t0)})'
        io.log(m)
        return {'message': m}, 200
