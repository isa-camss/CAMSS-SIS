import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
from flask_restx import Namespace, Resource

api = Namespace(ctt.GOVERNORS_NAME,
                description='These microservices are responsible of generating the needed resources to enable the '
                            'search engine.')


# ping_args = api.parser()
@api.route(f'/{ctt.GOV_INDEXATION_ENDPOINT}')
class ProcessIndex(Resource):
    @api.doc("Index Corpus with Thesauri")
    # @api.expect(ping_args, validate=True)
    def post(self):
        try:
            t0 = io.now()
            # Instance IndexManager
            report = {}
            return {'message': f'Report: {report}. Done in: {str(io.now() - t0)}'}, 200
        except Exception as ex:
            io.log(f"Exception: {ex}")
            return {'message': f'Exception: {ex}'}, 555
