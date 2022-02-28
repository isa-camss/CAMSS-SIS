import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
from flask_restx import Resource, Namespace

api = Namespace(ctt.SEARCH_NAME,
                description='Search concepts in the Corpora to find candidate Specifications.')


# ping_args = api.parser()
@api.route('/search')
class SearchSpecifications(Resource):
    @api.doc("Search concepts in the Corpus to find candidate Specifications")
    # @api.expect(ping_args, validate=True)
    def post(self):
        # Instance SpecificationManager, VocabularyManager
        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
