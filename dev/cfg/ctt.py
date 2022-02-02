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

# ARTIFACTS PATH
ARTIFACTS_DIR = "./arti"

RDF_DIR = ARTIFACTS_DIR + "/rdf"

# EIRA THESAURUS DETAILS
EIRA_THESAURUS_NAME = "eira.rdf"
EIRA_THESAURUS_URL = "https://joinup.ec.europa.eu/sites/default/files/distribution/access_url/2021-08/8adc381e-6997" \
                     "-4d66-8ea3-b3d9edc6c42c/EIRA_SKOS.rdf "
EIRA_THESAURUS_DETAILS = {"url": EIRA_THESAURUS_URL, "path": RDF_DIR + "/" + EIRA_THESAURUS_NAME}

# LANGUAGES

# The default language needs to be set compulsorily. Basic functionality would not work without it (e.g.,
# Taxonomy lemmatization, amongst other).
DEFAULT_LANGUAGE = 'en'

# Default four language models
MAIN_DEFAULT_LANGUAGE_MODEL = {'en': 'en_core_web_lg'}

DEFAULT_LANGUAGE_MODELS = {'es': 'es_core_news_lg',
                           'pt': 'pt_core_news_lg',
                           'fr': 'fr_core_news_lg'}

# The languages allowed for a specific project
PROJECT_LANGUAGES = ('en', 'es', 'fr', 'pt')

# The lemmatizer returns four possible combinations of modes. The options are:
# accented-minus-stopwords,
# accented_minus_stopwords,
# unaccented-plus-stopwords,
# unaccented-minus-stopwords,
# unaccented-minus-stopwords, or
# all
# If 'all' is supplied, a dictionary with all the options is returned.
PREFERRED_LEMMATIZATION_MODE = 'unaccented-minus-stopwords'

# PERSISTENCE CONFIGURATION
THESAURI_FILE_PERSISTENCE_DETAILS = {'type': PersistorTypes.FILE,
                                     'source_path': EIRA_THESAURUS_DETAILS.get('path'),
                                     'target_path': ''}

THESAURI_VIRTUOSO_PERSISTENCE_DETAILS = {'type': PersistorTypes.VIRTUOSO,
                                         'source_path': EIRA_THESAURUS_DETAILS.get('path'),
                                         'endpoint': 'http://',
                                         'user': '',
                                         'password': ''}
