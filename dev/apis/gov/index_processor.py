import cfg.ctt as ctt
import com.ntt.dgi.util.io as io
from flask_restx import Namespace, Resource

api = Namespace('gov_index_processor',
                description='Index Corpus with Thesauri')

# ping_args = api.parser()


@api.route('/process_index')
class ProcessIndex(Resource):
    @api.doc("Index Corpus with Thesauri")
    # @api.expect(ping_args, validate=True)
    def post(self):
        # Instance IndexManager
        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
