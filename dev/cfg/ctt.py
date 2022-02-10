from com.nttdata.dgi.persistence.ipersistor import PersistorTypes

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

# USER CREDENTIALS
EURLEX_WEB_SERVICE_USER_NAME = 'n0037rne'
EURLEX_WEB_SERVICE_PASSWORD = 'ewRU4D6I3rW'

# API ENDPOINTS
API_HOST = 'http://localhost:5000'
BASE_URL = API_HOST + API_PREFIX
URL_SKOS_MAP = BASE_URL + '/SKOS_Mapper/skos_map'
URL_NLP_LEMMATIZE = BASE_URL + '/nlp/lemmatize'

# ARTIFACTS PATH
ARTIFACTS_DIR = "./arti"
RDF_DIR = ARTIFACTS_DIR + "/rdf"
CORPORA_DIR = ARTIFACTS_DIR + "/corpora"

# EIRA THESAURUS DETAILS
EIRA_THESAURUS_NAME = "eira_thesaurus.rdf"
EIRA_THESAURUS_URL = "https://joinup.ec.europa.eu/sites/default/files/distribution/access_url/2021-03/d72a664c-70ea" \
                     "-4dd7-91ee-3768d44cc079/EIRA_SKOS.rdf "
EIRA_THESAURUS_DETAILS = {"url": EIRA_THESAURUS_URL, "path": RDF_DIR + "/" + EIRA_THESAURUS_NAME}

# EURLEX CORPORA DETAILS
# EURLEX_DOCUMENT_NAME = "corpora.txt"
EURLEX_CORPORA_URL = "https://eur-lex.europa.eu/EURLexWebService"
PAGE_NUMBER = '1'
RESULTS_NUMBER_BY_PAGE = '10'
EURLEX_CORPORA_QUERY_HEADERS = {'content-type': 'application/soap+xml'}
EURLEX_CORPORA_QUERY_BODY = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
    <soap:Header>
        <wsse:Security soap:mustUnderstand="true" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken wsu:Id="UsernameToken-3" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:Username>%s</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">%s</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header> 
    <soap:Body>
    <sear:searchRequest>
      <sear:expertQuery><![CDATA[DTS_SUBDOM = "TREATIES" OR "INTER_AGREE" OR "LEGISLATION" OR "EFTA" OR "EU_LAW_ALL" AND PD >= 01/01/2012 <= 07/02/2022]]></sear:expertQuery>
      <sear:page>%s</sear:page>
      <sear:pageSize>%s</sear:pageSize>
      <sear:searchLanguage>en</sear:searchLanguage>
    </sear:searchRequest>
    </soap:Body>
</soap:Envelope>"""

EURLEX_COPORA_DETAILS = {"url": EURLEX_CORPORA_URL,
                         "body": EURLEX_CORPORA_QUERY_BODY,
                         "headers": EURLEX_CORPORA_QUERY_HEADERS}

CORPORA_DOCUMENT_TYPE = ['pdf', 'html']

# EIRA THESAURUS LEMMATIZATION DETAILS

LEMMATIZATION_FUNCTIONS = ["md5lemma", "lemma"]
EIRA_MD5_NAME = "eira_thesaurus.md5lemmas.rdf"
EIRA_THESAURUS_MD5_DETAILS = {"source": EIRA_THESAURUS_DETAILS.get('path'),
                              "target": RDF_DIR + "/" + EIRA_MD5_NAME,
                              "graph": '',
                              "function": LEMMATIZATION_FUNCTIONS[0]}

EIRA_LEMMA_NAME = "eira_thesaurus.lemmas.rdf"
EIRA_THESAURUS_LEMMA_DETAILS = {"source": EIRA_THESAURUS_DETAILS.get('path'),
                                "target": RDF_DIR + "/" + EIRA_LEMMA_NAME,
                                "graph": '',
                                "function": LEMMATIZATION_FUNCTIONS[1]}

SKOS_MAPPER_REQUEST_DETAILS = {
        "endpoint": URL_NLP_LEMMATIZE,
        "thesauri": [
            EIRA_THESAURUS_MD5_DETAILS
        ]
    }

SKOS_MAPPER_DETAILS = {'url': URL_SKOS_MAP,
                       'body': SKOS_MAPPER_REQUEST_DETAILS
                       }

# LANGUAGES

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

# SKOS MAPPER
"""
Lemmatization provided via a lemmatization service endpoint...
"""
LEMMATIZER_ENDPOINT = "http://localhost:5000/camss-sis/v1/lemmatize"
LEMMATIZER_PREFERRED_METHOD = "unaccented-minus-stopwords"
DEFAULT_LANG = "en"

LEMMATIZATION_DETAILS = {
    "endpoint": LEMMATIZER_ENDPOINT,
    "method": LEMMATIZER_PREFERRED_METHOD,
    "raw-data": {"phrase": "", "lang": DEFAULT_LANG}
}

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

# PERSISTENCE CONFIGURATION
THESAURI_FILE_PERSISTENCE_DETAILS = {'type': PersistorTypes.FILE,
                                     'source_path': EIRA_THESAURUS_DETAILS.get('path'),
                                     'target_path': ''}

THESAURI_VIRTUOSO_PERSISTENCE_DETAILS = {'type': PersistorTypes.VIRTUOSO,
                                         'source_path': EIRA_THESAURUS_DETAILS.get('path'),
                                         'endpoint': 'http://',
                                         'user': '',
                                         'password': ''}
