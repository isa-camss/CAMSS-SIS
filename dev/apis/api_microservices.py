from flask import Blueprint
from flask_restx import Api
import cfg.ctt as ctt

# API
from apis.gov.index_processor import api as index
from apis.gov.resources_processor import api as rsc
from apis.gov.thesauri_processor import api as thes
from apis.nlp.lemmatizer import api as nlp
from apis.rdf.skos_lemmatizer import api as rdf
from apis.gse.searcher import api as search

blueprint = Blueprint(name=ctt.API_NAME, import_name=__name__, url_prefix=ctt.API_PREFIX)
api = Api(blueprint,
          title=ctt.API_TITLE,
          version=ctt.VERSION,
          description=ctt.API_DESCRIPTION
          )

# GOVS API
api.add_namespace(thes)
api.add_namespace(rsc)
api.add_namespace(index)

# NLP API
api.add_namespace(nlp)

# RDF API
api.add_namespace(rdf)

# SEARCH API
api.add_namespace(search)
