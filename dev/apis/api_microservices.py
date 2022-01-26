from flask import Blueprint, jsonify
from flask_restx import Api
import cfg.ctt as ctt

# SEARCH API
# from apis.gse.search import api as se

# GOVS API
# from apis.gov.pipeline_iii import api as pipe_iii

# NLP API
from apis.nlp.basics import api as basics


blueprint = Blueprint(name=ctt.API_NAME, import_name=__name__, url_prefix=ctt.API_PREFIX)
api = Api(blueprint,
          title=ctt.API_TITLE,
          version=ctt.VERSION,
          description=ctt.API_DESCRIPTION
          )


# SEARCH API
# api.add_namespace(se)

# GOVS API
# api.add_namespace(pipe_iii)

# NLP API
api.add_namespace(basics)

