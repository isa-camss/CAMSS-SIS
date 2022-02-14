import cfg.ctt as ctt

VIRTUOSO_EIRA_LOAD_RDF_FILE = {
    "source": "." + ctt.EIRA_THESAURUS_DETAILS.get('path'),
    "user": "dba",
    "password": "dba",
    "graph": "http://eira.org/",
    "endpoint": "http://localhost:8890/sparql-graph-crud-auth?graph-uri=http://data.europa.eu/dr8/mirror3/",
    # "endpoint": "http://localhost:8890/DAV/home/eira/source.rdf",
    "method": "graph-uri"
    }
