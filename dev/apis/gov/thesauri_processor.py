import com.nttdata.dgi.util.io as io
from flask_restx import Namespace, Resource
from com.nttdata.dgi.thes.thesauri_manager import ThesauriManager
from apis.nlp.lemmatizer import Lematize
import cfg.ctt as ctt
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

    # Create ThesaurusManager with the configuration for EIRA
    thesauri_manager = ThesauriManager(thesauri_details)

    # Download Thesaurus
    thesauri_manager.download_thesauri()

    # Analyze downloaded Thesaurus
    url = 'http://localhost:5000/camss-sis/v1/SKOS_Mapper/skos_map'
    thesauri = {
        "endpoint": "http://localhost:5000/camss-sis/v1/nlp/lemmatize",
        "thesauri": [
            ctt.EIRA_THESAURUS_MD5_DETAILS
        ]
    }
    skos_mapper_response = requests.post(url, json=thesauri)

    return {}


@api.route('/process_thesaurus')
class ProcessThesaurus(Resource):
    @api.doc("Download and process thesaurus")
    # @api.expect(ping_args, validate=True)
    def post(self):
        report = process_thesauri()

        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
