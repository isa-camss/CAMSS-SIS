import cfg.ctt as ctt
import com.ntt.dgi.util.io as io
from flask_restx import Namespace, Resource

api = Namespace('gov_thes_processor',
                description='Download and process thesaurus')

# ping_args = api.parser()


@api.route('/process_thesaurus')
class ProcessThesaurus(Resource):
    @api.doc("Download and process thesaurus")
    # @api.expect(ping_args, validate=True)
    def post(self):
        # Instance ThesauriManager
        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
