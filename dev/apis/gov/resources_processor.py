import cfg.ctt as ctt
import cfg.crud as crud
import com.nttdata.dgi.util.io as io
from flask_restx import Resource, Namespace
from org.camss.corpora.corpora_manager import CorporaManager


api = Namespace(ctt.GOVERNORS_NAME,
                description='These microservices are responsible of generating the needed resources to enable the '
                            'search engine.')


# ping_args = api.parser()
def process_corpus() -> dict:
    # Download EURLex Corpus
    CorporaManager(ctt.DOWNLOAD_CORPORA_DETAILS, ctt.TEXTIFICATION_CORPORA_DETAILS, ctt.CORPORA_LEMMATIZATION_DETAILS).\
        lemmatize_corpora(ctt.CORPORA_LEMMATIZATION_DETAILS, crud.ELASTICSEARCH_DETAILS)

    return {}


@api.route(f'/{ctt.GOV_CORPUS_PROCESSOR_ENDPOINT}')
class ProcessCorpus(Resource):
    @api.doc("Download corpora, textify and analysis resources.")
    # @api.expect(ping_args, validate=True)
    def post(self):
        try:
            t0 = io.now()
            report = process_corpus()
            return {'message': f'Done in: {str(io.now() - t0)}'}, 200
        except Exception as ex:
            io.log(f"Exception: {ex}")
            return {'message': f'Exception: {ex}'}, 555
