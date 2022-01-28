import com.ntt.dgi.util.io as io
from flask_restx import Namespace, Resource

api = Namespace('nlp_basic',
                description='NLP-related operations, e.g. lemmatization, stemming, bag of terms extraction, etc.')

# ping_args = api.parser()


@api.route('/ping')
class Ping(Resource):
    @api.doc("Returns 'pong' if invoked. Used to check that the NLP services are up and running.")
    # @api.expect(ping_args, validate=True)
    def get(self):
        t0 = io.now()
        return {'message': f'pong ({str(io.now() - t0)})'}, 200
