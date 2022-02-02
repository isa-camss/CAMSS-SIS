from flask import Blueprint
from flask_restx import Api
import cfg.ctt as ctt

# API
from apis.gov.thesauri_processor import api as thesauri_processor
from apis.gov.resources_processor import api as resources_processor
from apis.gov.index_processor import api as index_processor
from apis.nlp.basics import api as basics
from apis.gse.searcher import api as searcher

blueprint = Blueprint(name=ctt.API_NAME, import_name=__name__, url_prefix=ctt.API_PREFIX)
api = Api(blueprint,
          title=ctt.API_TITLE,
          version=ctt.VERSION,
          description=ctt.API_DESCRIPTION
          )

# GOVS API
api.add_namespace(thesauri_processor)
api.add_namespace(resources_processor)
api.add_namespace(index_processor)

# NLP API
api.add_namespace(basics)
api.add_namespace(lem)

# SEARCH API
api.add_namespace(searcher)