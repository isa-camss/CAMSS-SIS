import com.nttdata.dgi.util.io as io
from flask_restx import Namespace, Resource
from com.nttdata.dgi.thes.thesauri_manager import ThesauriManager
import cfg.ctt as ctt
import cfg.crud as crud
from com.nttdata.dgi.util.io import make_file_dirs
import requests

api = Namespace('gov_thes_processor',
                description='Download and process Thesaurus')


# ping_args = api.parser()

def process_thesauri() -> dict:
    # Define thesaurus EIRA Thesaurus details
    eira_thesaurus_details = ctt.EIRA_THESAURUS_DETAILS
    thesauri_details = [eira_thesaurus_details]

    # Create the folders where the Thesaurus will be saved
    make_file_dirs(ctt.EIRA_THESAURUS_DETAILS.get('path'))

    # 1. Create ThesaurusManager with the configuration for EIRA
    thesauri_manager = ThesauriManager(thesauri_details, ctt.SKOS_MAPPER_DETAILS)

    # 2. Download Thesaurus
    thesauri_manager.download_thesauri()

    # 3. Lemmatization and SKOS mapping of downloaded Thesaurus
    thesauri_manager.analyse()

    # 4. Persist original Thesaurus in Virtuoso
    thesauri_manager.persist_thesauri(crud.VIRTUOSO_EIRA_LOAD_RDF_FILE, ctt.EIRA_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS)

    # 5. Persist the lematized skos in Virtuoso
    thesauri_manager.persist_thesauri(crud.VIRTUOSO_EIRA_LOAD_RDF_FILE, ctt.EIRA_LEMMAS_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS)
    return {}


@api.route('/process_thesaurus')
class ProcessThesaurus(Resource):
    @api.doc("Download and process thesaurus")
    # @api.expect(ping_args, validate=True)
    def post(self):
        report = process_thesauri()

        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
