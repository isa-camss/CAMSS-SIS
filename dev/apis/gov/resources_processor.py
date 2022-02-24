import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
from flask_restx import Namespace, Resource
from org.camss.corpora.corpora_manager import CorporaManager

api = Namespace('gov_rsc_processor',
                description='Download the corpus and resources analysis')


# ping_args = api.parser()

def process_corpus() -> dict:
    # Download EURLex Corpus
    CorporaManager(ctt.DOWNLOAD_CORPORA_DETAILS, ctt.TEXTIFICATION_CORPORA_DETAILS).prepare_corpus_folders().download_corpus().textify_corpus()
    # CorporaManager(ctt.DOWNLOAD_CORPORA_DETAILS, ctt.TEXTIFICATION_CORPORA_DETAILS).textify_corpus()
    # CorporaManager(ctt.DOWNLOAD_CORPORA_DETAILS, ctt.TEXTIFICATION_CORPORA_DETAILS).lemmatize_resource()
    return {}


@api.route('/process_corpus')
class ProcessCorpus(Resource):
    @api.doc("Download the corpus and resources analysis")
    # @api.expect(ping_args, validate=True)
    def post(self):
        try:
            t0 = io.now()
            report = process_corpus()
            return {'message': f'Report: {report}. Done in: {str(io.now() - t0)}'}, 200
        except Exception as ex:
            io.log(f"Exception: {ex}")
            return {'message': f'Exception: {ex}'}, 555
