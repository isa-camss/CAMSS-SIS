import cfg.credentials as cred
import cfg.queries as queries

# PROJECT CONFIG
PROJECT_NAME = 'camss-sis'
VERSION = 'v1.0'

# API
API_PORT = 5000
API_DEBUG = False
API_NAME = 'apiCAMSS-SIS'
API_PREFIX = f'/{PROJECT_NAME}/{VERSION[:2]}'
API_TITLE = 'CAMSS-SIS.API - Development'
API_DESCRIPTION = 'It is an API...'
END_POINT_SWAGGER = f'{API_PREFIX}/swagger'
END_POINT_SWAGGER_JSON = f'{API_PREFIX}/swagger.json'
NAME_BLUEPRINT = 'swaggerCAMSS-SIS'

# API ENDPOINTS
API_HOST = 'http://localhost:5000'
BASE_URL = API_HOST + API_PREFIX
URL_THESAURI_PROCESSOR = BASE_URL + '/gov_thes_processor/process_thesaurus'
URL_SKOS_LEM = BASE_URL + '/SKOS_Lemmatizer/skos_lemmatize'
URL_NLP_LEMMATIZE = BASE_URL + '/nlp/lemmatize'
URL_RESOURCES_PROCESSOR = BASE_URL + '/gov_rsc_processor/process_corpus'
URL_SEARCHER = BASE_URL + '/gse_searcher/search'

# ARTIFACTS PATH
ARTIFACTS_DIR = "./arti"
RDF_DIR = ARTIFACTS_DIR + "/rdf"
JSON_DIR = ARTIFACTS_DIR + "/json"
CORPORA_DIR = '../../corpora'
TEXTIFICATION_DIR = CORPORA_DIR + '/txt'


# ------------------------------------------- PROJECT LANGUAGES -------------------------------------------

# The default language needs to be set compulsorily. Basic functionality would not work without it (e.g.,
# Taxonomy lemmatization, amongst other).
DEFAULT_LANGUAGE = 'en'

# Default four language models
MAIN_DEFAULT_LANGUAGE_MODEL = {'en': 'en_core_web_lg'}

DEFAULT_LANGUAGE_MODELS = {'en': 'en_core_web_lg'}

# The languages allowed for a specific project
PROJECT_LANGUAGES = ['en']

# The lemmatizer returns four possible combinations of modes. The options are:
# accented-minus-stopwords,
# accented_minus_stopwords,
# unaccented-plus-stopwords,
# unaccented-minus-stopwords,
# unaccented-minus-stopwords, or
# all
# If 'all' is supplied, a dictionary with all the options is returned.
PREFERRED_LEMMATIZATION_MODE = 'unaccented-minus-stopwords'

# ------------------------------------------- THESAURUS ---------------------------------------------------------------
# EIRA THESAURUS DETAILS
EIRA_THESAURUS_NAME = "eira_thesaurus.rdf"
EIRA_THESAURUS_FILE = EIRA_THESAURUS_NAME + ".rdf"
EIRA_THESAURUS_URL = "https://joinup.ec.europa.eu/sites/default/files/distribution/access_url/2021-03/d72a664c-70ea" \
                     "-4dd7-91ee-3768d44cc079/EIRA_SKOS.rdf "
EIRA_THESAURUS_DETAILS = {"name": EIRA_THESAURUS_NAME,
                          "url": EIRA_THESAURUS_URL,
                          "path": RDF_DIR + "/" + EIRA_THESAURUS_FILE}

# ------------------------------------------- CORPORA -----------------------------------------------------------------
CORPORA_DOCUMENT_TYPE = "pdf"
CORPORA_EXCLUDE_TEXTIFICATION_DOCUMENT_TYPE = ['html', 'txt']
RESOURCE_METADATA_JSON = JSON_DIR + '/resource_metadata.jsonl'
RESOURCE_LEMMATIZED_JSON = JSON_DIR + '/resource_lemmatized.jsonl'

# EURLEX CORPORA DETAILS
# EURLEX_DOCUMENT_NAME = "corpora.txt"
EURLEX_CORPORA_URL = "https://eur-lex.europa.eu/EURLexWebService"
PAGE_NUMBER = 1
RESULTS_NUMBER_BY_PAGE = 10
MAX_DOWNLOAD_DOCUMENT = 20
EURLEX_CORPORA_QUERY_HEADERS = {'content-type': 'application/soap+xml'}
EURLEX_CORPORA_QUERY_BODY = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
    <soap:Header>
        <wsse:Security soap:mustUnderstand="true" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken wsu:Id="UsernameToken-3" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:Username>{cred.EURLEX_WEB_SERVICE_USER_NAME}</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{cred.EURLEX_WEB_SERVICE_PASSWORD}</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header> 
    <soap:Body>
    <sear:searchRequest>
      <sear:expertQuery><{queries.EURLEX_EXPERT_QUERY}></sear:expertQuery>
      <sear:page>%s</sear:page>
      <sear:pageSize>%s</sear:pageSize>
      <sear:searchLanguage>en</sear:searchLanguage>
    </sear:searchRequest>
    </soap:Body>
</soap:Envelope>"""

EURLEX_COPORA_DETAILS = {'url': EURLEX_CORPORA_URL,
                         'body': EURLEX_CORPORA_QUERY_BODY,
                         'headers': EURLEX_CORPORA_QUERY_HEADERS,
                         'initial_page_number': PAGE_NUMBER,
                         'initial_page_size': RESULTS_NUMBER_BY_PAGE
                         }

DOWNLOAD_CORPORA_DETAILS = {'eurlex_details': EURLEX_COPORA_DETAILS,
                            'default_lang': DEFAULT_LANGUAGE,
                            'max_documents': MAX_DOWNLOAD_DOCUMENT,
                            'download_types': CORPORA_DOCUMENT_TYPE,
                            'json_dir': JSON_DIR,
                            'corpora_dir': CORPORA_DIR,
                            'resource_metadata_file': RESOURCE_METADATA_JSON,
                            'textification_dir': TEXTIFICATION_DIR
                            }
# ______________________________________________ TEXTIFICATION _______________________________________________________
TEXTIFICATION_CORPORA_DETAILS = {'corpus_dir': CORPORA_DIR,
                                 'textification_dir': TEXTIFICATION_DIR,
                                 'exclude_extensions_type': CORPORA_EXCLUDE_TEXTIFICATION_DOCUMENT_TYPE,
                                 'lang?': True}
# _______________________________________________ LEMMATIZATION ______________________________________________________
# EIRA THESAURUS LEMMATIZATION DETAILS

LEMMATIZATION_FUNCTIONS = ["md5lemma", "lemma"]
EIRA_MD5_NAME = "eira_thesaurus.md5lemmas.rdf"
EIRA_THESAURUS_MD5_DETAILS = {"source": EIRA_THESAURUS_DETAILS.get('path'),
                              "target": RDF_DIR + "/" + EIRA_MD5_NAME,
                              "function": LEMMATIZATION_FUNCTIONS[0]}

EIRA_LEMMA_NAME = "eira_thesaurus.lemmas.rdf"
EIRA_THESAURUS_LEMMA_DETAILS = {"source": EIRA_THESAURUS_DETAILS.get('path'),
                                "target": RDF_DIR + "/" + EIRA_LEMMA_NAME,
                                "function": LEMMATIZATION_FUNCTIONS[1]}
LABELS = ['<title', '<preflabel', '<altlabel', '<hiddenlabel', '<literal', '<literalform',
          '<skos:preflabel', '<skos:altlabel', '<skos:hiddenlabel']
SKOS_LEMMATIZER_REQUEST_DETAILS = {
    "endpoint": URL_NLP_LEMMATIZE,
    "labels": LABELS,
    "thesauri": [
        EIRA_THESAURUS_LEMMA_DETAILS
    ]
}

SKOS_MAPPER_DETAILS = {'url': URL_SKOS_LEM,
                       'body': SKOS_LEMMATIZER_REQUEST_DETAILS
                       }

# SKOS MAPPER
"""
Lemmatization provided via a lemmatization service endpoint...
"""
LEMMATIZER_ENDPOINT = "http://localhost:5000/camss-sis/v1/lemmatize"
LEMMATIZER_PREFERRED_METHOD = "unaccented-minus-stopwords"
DEFAULT_LANG = "en"

LEMMATIZATION_DETAILS = {"endpoint": URL_NLP_LEMMATIZE,
                         "method": LEMMATIZER_PREFERRED_METHOD
                         }

# CORPORA LEMMATIZATION
"""
KEY TERM CONFIGURATION...remember a 'Key Term' has been convened as a Term that is included in at least one 
controlled vocabularies of the Thesauri. A 'Key Word' is a collocation from the corpus that IS NOT present in
the Thesauri but can become a candidate to be included in one of the Thesauri controlled vocabularies.
"""
# Number of times a Term must occur in a resource to be included in the KR Tree .
# Play with this, if 1 -> [dramatically] more Key Terms and time-costly but higher discoverability
NGRAM_RANGE = (1, 5)  # Bags of 1, 2, 3, 4, and 5 terms will be extracted, unless specified differently
MIN_RSC_TERM_FREQUENCY = 1
MIN_RSC_BODY_TERM_FREQUENCY = 2
# 1-gram terms found in the document are to be considered terms, otherwise relevant terms
# like 3G, 4G and 5G would be discarded.
MIN_TERM_SIZE = 1

CORPORA_LEMMATIZATION_DETAILS = {
    "metadata_file":RESOURCE_METADATA_JSON,
    "lemmatized_jsonl": RESOURCE_LEMMATIZED_JSON,
    "corpus_path": TEXTIFICATION_DIR,
    "ops_metadata": '',
    "rsc_metadata": '',
    "abstract_sentence#": '',
    "out_nq_file": '',
    "out_jsonl_file": '',
    "labels_dictionary_pkl": '',
    "lemmatizer_endpoint": URL_NLP_LEMMATIZE,
    "ngram_range": NGRAM_RANGE,
    "rsc_part_types": [],
    "def_lang": DEFAULT_LANGUAGE,
    "min_tf": MIN_RSC_TERM_FREQUENCY,  # Number of times a Term must occur in a resource to be included in the KR Tree
    "min_tf_body": MIN_RSC_BODY_TERM_FREQUENCY,  # Number of times a Term must occur in a resource to be included in the KR Tree
    "min_term_len": MIN_TERM_SIZE  # 1-gram terms found in the document are to be considered terms, otherwise
    # relevant terms like 3G, 4G and 5G would be discarded.
}

# ------------------------------------------- PERSISTANCE -------------------------------------------------------------
'''
Information required for the connection to a database, e.g. a Graph Store like Stardog 
'''
STORE_DETAILS = {
    "store": "stardog",
    "details": {
        "connection": {
            "endpoint": "http://localhost:5820",
            "username": "admin",
            "password": "admin"
        },
        "database": "accelerators"
    }
}
EIRA_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS = {
    "location": EIRA_THESAURUS_DETAILS.get('path'),
    "graph_name": "http://data.europa.eu/dr8/"
}

EIRA_LEMMAS_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS = {
    "location": RDF_DIR + "/" + EIRA_LEMMA_NAME,
    "graph_name": "http://data.europa.eu/dr8/eira_lemmas/"
}
