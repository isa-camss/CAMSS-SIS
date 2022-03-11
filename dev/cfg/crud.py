ELASTICSEARCH_HOST = "http://localhost:9200"
ELASTICSEARCH_USER = None
ELASTICSEARCH_PASSWORD = None
ELASTICSEARCH_DOCS_METADATA_INDEX = "eurlex-docs-metadata"
ELASTICSEARCH_TERMS_LEMMATIZED_INDEX = "eira-terms"
ELASTICSEARCH_DOCS_LEMMATIZED_INDEX = "eurlex-docs-lemmatized"

ELASTICSEARCH_DETAILS = {"host": ELASTICSEARCH_HOST,
                         "user": ELASTICSEARCH_USER,
                         "password": ELASTICSEARCH_PASSWORD
                         }

VIRTUOSO_EIRA_LOAD_RDF_FILE = {
    # "source": ctt.EIRA_THESAURUS_DETAILS.get('path'),
    "user": "dba",
    "password": "dba",
    # "graph": "http://eira.org/",
    "endpoint": "http://localhost:8890/sparql-graph-crud-auth?graph-uri=",
    }
