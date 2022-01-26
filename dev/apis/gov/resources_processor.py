import cfg.ctt as ctt
import com.ntt.dgi.util.io as io
from flask_restx import Namespace, Resource

api = Namespace('gov_rsc_processor',
                description='Download the corpus and resources analysis')

# ping_args = api.parser()


@api.route('/process_corpus')
class ProcessCorpus(Resource):
    @api.doc("Download the corpus and resources analysis")
    # @api.expect(ping_args, validate=True)
    def post(self):
        # Instance CorporaManager, ResourceAnalyser
        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
