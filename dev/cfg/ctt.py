import cfg.credentials as cred
import cfg.queries as queries
import cfg.crud as crud

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

# API HOST
API_HOST = f'http://localhost:{API_PORT}'
BASE_URL = API_HOST + API_PREFIX

# API SERVICES NAMES
GOVERNORS_NAME = 'GOVERNORS'
SEARCH_NAME = 'SEARCH'
NLP_NAME = 'NLP'
RDF_SKOS_NAME = 'RDF'

# API ENDPOINTS
NLP_LEMMATIZE_ENDPOINT = 'lemmatize'
NLP_SENTENCIZE_ENDPOINT = 'sentencize'
NLP_PING_ENDPOINT = 'ping'
SKOS_LEMMATIZER_ENDPOINT = 'skos_lemmatize'
GOV_THESAURI_PROCESSOR_ENDPOINT = 'process_thesaurus'
GOV_CORPUS_PROCESSOR_ENDPOINT = 'process_corpus'
GOV_INDEXATION_ENDPOINT = 'process_indexation'
SEARCHER_SEARCH_ENDPOINT = 'search'

# API URL ENDPOINTS
URL_NLP_LEMMATIZE = f'{BASE_URL}/{NLP_NAME}/{NLP_LEMMATIZE_ENDPOINT}'
URL_NLP_SENTENCIZE = f'{BASE_URL}/{NLP_NAME}/{NLP_SENTENCIZE_ENDPOINT}'
URL_NLP_PING = f'{BASE_URL}/{NLP_NAME}/{NLP_PING_ENDPOINT}'
URL_SKOS_LEM = f'{BASE_URL}/{RDF_SKOS_NAME}/{SKOS_LEMMATIZER_ENDPOINT}'
URL_THESAURI_PROCESSOR = f'{BASE_URL}/{GOVERNORS_NAME}/{GOV_THESAURI_PROCESSOR_ENDPOINT}'
URL_RESOURCES_PROCESSOR = f'{BASE_URL}/{GOVERNORS_NAME}/{GOV_CORPUS_PROCESSOR_ENDPOINT}'
URL_RESOURCES_INDEXATION = f'{BASE_URL}/{GOVERNORS_NAME}/{GOV_INDEXATION_ENDPOINT}'
URL_SEARCHER = f'{BASE_URL}/{SEARCH_NAME}/{SEARCHER_SEARCH_ENDPOINT}'

# ARTIFACTS PATH
ARTIFACTS_DIR = "./arti"
RDF_DIR = ARTIFACTS_DIR + "/rdf"
JSON_DIR = ARTIFACTS_DIR + "/json"
CORPORA_DIR = "../../corpora"
TEXTIFICATION_DIR = CORPORA_DIR + "/txt"

# ------------------------------------------- PROJECT LANGUAGES -------------------------------------------

# The default language needs to be set compulsorily. Basic functionality would not work without it (e.g.,
# Taxonomy lemmatization, amongst other).
DEFAULT_LANGUAGE = "en"

# ------------------------------------------- LANGUAGE MODELS ----------------------------------------------------
# Default four language models
MAIN_DEFAULT_LANGUAGE_MODEL = {"en": "en_core_web_lg"}

DEFAULT_LANGUAGE_MODELS = {"en": "en_core_web_lg"}

# The languages allowed for a specific project
PROJECT_LANGUAGES = ["en"]
DEFAULT_LANG = "en"

# The lemmatizer returns four possible combinations of modes. The options are:
# accented-minus-stopwords,
# accented_minus_stopwords,
# unaccented-plus-stopwords,
# unaccented-minus-stopwords,
# unaccented-minus-stopwords, or
# all
# If 'all' is supplied, a dictionary with all the options is returned.
PREFERRED_LEMMATIZATION_MODE = "unaccented-minus-stopwords"

# ------------------------------------------- THESAURUS ---------------------------------------------------------------
# EIRA ------------------------
# EIRA THESAURUS DETAILS
EIRA_THESAURUS_NAME = "eira_thesaurus"
EIRA_THESAURUS_FILE = EIRA_THESAURUS_NAME + ".rdf"
TERM_LEMMATIZED_JSON = JSON_DIR + "/camss_term_lemmatized.jsonl"
EIRA_THESAURUS_URL = "https://joinup.ec.europa.eu/sites/default/files/distribution/access_url/2021-03/d72a664c-70ea" \
                     "-4dd7-91ee-3768d44cc079/EIRA_SKOS.rdf"
EIRA_THESAURUS_DETAILS = {"name": EIRA_THESAURUS_NAME,
                          "url": EIRA_THESAURUS_URL,
                          "path": RDF_DIR + "/" + EIRA_THESAURUS_FILE
                          }
# ABBS PER EIRA VIEW
EIRA_LEGAL_SPECIFICATIONS = ["public policy", "interoperable digital public services implementation",
                             "public policy cycle", "binding instrument", "non-binding instrument", "legal act",
                             "legislation catalogue", "legal interoperability agreement",
                             "legislation on data information and knowledge exchange", "legal authority",
                             "shared legal framework", "legal agreements", "international treaties"
                             ]

EIRA_ORGANISATIONAL_SPECIFICATIONS = ["interoperability strategy", "interoperability framework",
                                      "interoperability governance", "interoperability organisation authority",
                                      "interoperability skill", "organisational interoperability agreement",
                                      "public service provider", "exchange of business information"]

EIRA_SEMANTIC_SPECIFICATIONS = ["data policy", "representation", "data set catalogue", "data set", "data",
                                "descriptive metada policy", "master data policy", "open data policy",
                                "base registry data policy", "data portability policy", "reference data policy",
                                "data entity", "core data model", "data syntax", "data model", "controlled vocabulary",
                                "shared knowledge base", "data mapping", "ontologies catalogue", "ontology",
                                "data owner", "semantic interoperability agreement", "data mapping",
                                "data mapping catalogue", "semantic agreement", "security policy", "privacy policy"
                                ]

EIRA_TECHNICAL_SPECIFICATIONS = ["machine to machine interface", "human interface",
                                 "interoperable european solution service", "interoperable european solution component",
                                 "access management service", "access management component", "audit service",
                                 "audit component", "interoperable european solution", "data transformation service",
                                 "data transformation component", "data validation service",
                                 "data validation component", "service discovery service",
                                 "service discovery component", "orchestration service", "orchestration component",
                                 "technical specification", "technical interoperability agreement", "shared platform",
                                 "conformance testing service", "conformance testing component",
                                 "conformance test report", "conformance test scenario", "technical agreement"
                                 ]
CAMSS_SIS_DISCOVERIES = ["interoperability certificate"]
EIRA_ABBS = EIRA_LEGAL_SPECIFICATIONS + EIRA_ORGANISATIONAL_SPECIFICATIONS + CAMSS_SIS_DISCOVERIES

EIRA_VIEWS_DETAILS = [{"view": "legal", "skos_collection": "LegalView"},
                      {"view": "organisational", "skos_collection": "OrganisationalView"}]

EIRA_CONCEPTS_DETAILS = {"vocabulary_details": EIRA_VIEWS_DETAILS,
                         "rsc_lang": DEFAULT_LANG,
                         "elastic_terms_index": crud.ELASTICSEARCH_TERMS_LEMMATIZED_INDEX,
                         "json_dir": JSON_DIR,
                         "lemmatized_jsonl": TERM_LEMMATIZED_JSON,
                         "query_terms": queries.EIRA_ABBS_QUERY
                         }
# ------------------------------------------- CORPORA -----------------------------------------------------------------
CORPORA_DOCUMENT_TYPE = "pdf"
CORPORA_EXCLUDE_TEXTIFICATION_DOCUMENT_TYPE = ["html", "txt"]
RESOURCE_METADATA_JSON = JSON_DIR + "/camss_rsc_metadata.jsonl"
RESOURCE_LEMMATIZED_JSON = JSON_DIR + "/camss_rsc_lemmatized.jsonl"
RESOURCE_PROCESSED_JSON = JSON_DIR + "/camss_rsc_processed.jsonl"


# EURLEX CORPORA DETAILS
# EURLEX_DOCUMENT_NAME = "corpora.txt"
EURLEX_CORPORA_URL = "https://eur-lex.europa.eu/EURLexWebService"
PAGE_NUMBER = 1
RESULTS_NUMBER_BY_PAGE = 10
MAX_DOWNLOAD_DOCUMENT = 100
EURLEX_CORPORA_QUERY_HEADERS = {"content-type": "application/soap+xml"}
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

EURLEX_COPORA_DETAILS = {"url": EURLEX_CORPORA_URL,
                         "body": EURLEX_CORPORA_QUERY_BODY,
                         "headers": EURLEX_CORPORA_QUERY_HEADERS,
                         "initial_page_number": PAGE_NUMBER,
                         "initial_page_size": RESULTS_NUMBER_BY_PAGE
                         }

DOWNLOAD_CORPORA_DETAILS = {"eurlex_details": EURLEX_COPORA_DETAILS,
                            "default_lang": DEFAULT_LANGUAGE,
                            "max_documents": MAX_DOWNLOAD_DOCUMENT,
                            "download_types": CORPORA_DOCUMENT_TYPE,
                            "json_dir": JSON_DIR,
                            "corpora_dir": CORPORA_DIR,
                            "elastic_metadata_index": crud.ELASTICSEARCH_DOCS_METADATA_INDEX,
                            "elastic_docs_processed_index": crud.ELASTICSEARCH_DOCS_PROCESSED_INDEX,
                            "resource_metadata_file": RESOURCE_METADATA_JSON,
                            "textification_dir": TEXTIFICATION_DIR
                            }
# ______________________________________________ TEXTIFICATION _______________________________________________________
TEXTIFICATION_CORPORA_DETAILS = {"corpus_dir": CORPORA_DIR,
                                 "textification_dir": TEXTIFICATION_DIR,
                                 "exclude_extensions_type": CORPORA_EXCLUDE_TEXTIFICATION_DOCUMENT_TYPE,
                                 "textification_lang": True}
# ------------------------------------------- LEMMATIZATION ----------------------------------------------------------
# THESAURUS LEMMATIZATION -------------------
# EIRA THESAURUS LEMMATIZATION DETAILS
LEMMATIZATION_FUNCTIONS = ["md5lemma", "lemma"]
EIRA_MD5_NAME = "eira_thesaurus.md5lemmas.rdf"
EIRA_THESAURUS_MD5_DETAILS = {"source": EIRA_THESAURUS_DETAILS.get("path"),
                              "target": RDF_DIR + "/" + EIRA_MD5_NAME,
                              "function": LEMMATIZATION_FUNCTIONS[0]}

EIRA_LEMMA_NAME = "eira_thesaurus.lemmas.rdf"
EIRA_THESAURUS_LEMMA_DETAILS = {"source": EIRA_THESAURUS_DETAILS.get("path"),
                                "target": RDF_DIR + "/" + EIRA_LEMMA_NAME,
                                "function": LEMMATIZATION_FUNCTIONS[1]}

# SKOS MAPPER
LABELS = ['<title', '<preflabel', '<altlabel', '<hiddenlabel', '<literal', '<literalform',
          '<skos:preflabel', '<skos:altlabel', '<skos:hiddenlabel']

SKOS_LEMMATIZER_REQUEST_DETAILS = {
    "endpoint": URL_NLP_LEMMATIZE,
    "labels": LABELS,
    "thesauri": [
        EIRA_THESAURUS_LEMMA_DETAILS
    ]
}

SKOS_MAPPER_DETAILS = {"url": URL_SKOS_LEM,
                       "body": SKOS_LEMMATIZER_REQUEST_DETAILS}

"""
Lemmatization provided via a lemmatization service endpoint...
"""
LEMMATIZER_ENDPOINT = "http://localhost:5000/camss-sis/v1/lemmatize"
LEMMATIZER_PREFERRED_METHOD = "unaccented-minus-stopwords"

LEMMATIZATION_DETAILS = {"endpoint": URL_NLP_LEMMATIZE,
                         "method": LEMMATIZER_PREFERRED_METHOD
                         }

# CORPORA LEMMATIZATION -------------------
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
    "elastic_lemmas_index": crud.ELASTICSEARCH_DOCS_LEMMATIZED_INDEX,
    "elastic_docs_processed_index": crud.ELASTICSEARCH_DOCS_PROCESSED_INDEX,
    "metadata_file": RESOURCE_METADATA_JSON,
    "lemmatized_file": RESOURCE_LEMMATIZED_JSON,
    "processed_file": RESOURCE_PROCESSED_JSON,
    "corpus_path": TEXTIFICATION_DIR,
    "ops_metadata": "",
    "rsc_metadata": "",
    "abstract_sentence#": "",
    "out_nq_file": "",
    "out_jsonl_file": "",
    "labels_dictionary_pkl": "",
    "lemmatizer_endpoint": URL_NLP_LEMMATIZE,
    "ngram_range": NGRAM_RANGE,
    "rsc_part_types": [],
    "def_lang": DEFAULT_LANGUAGE,
    "min_tf": MIN_RSC_TERM_FREQUENCY,  # Number of times a Term must occur in a resource to be included in the KR Tree
    "min_tf_body": MIN_RSC_BODY_TERM_FREQUENCY,
    # Number of times a Term must occur in a resource to be included in the KR Tree
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
    "location": EIRA_THESAURUS_DETAILS.get("path"),
    "graph_name": "http://data.europa.eu/dr8/"
}

EIRA_LEMMAS_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS = {
    "location": RDF_DIR + "/" + EIRA_LEMMA_NAME,
    "graph_name": "http://data.europa.eu/dr8/eira_lemmas/"
}

# ------------------------------------------- SEARCH -------------------------------------------------------------
MATCH_TERMS_JSON = JSON_DIR + "/match_terms.jsonl"
CONCEPTS_TEST = ["public policy", "europe", "binding instrument", "legal act"]
