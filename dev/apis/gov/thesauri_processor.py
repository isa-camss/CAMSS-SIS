import com.nttdata.dgi.util.io as io
from flask_restx import Namespace, Resource
from com.nttdata.dgi.thes.thesauri_manager import ThesauriManager
from apis.nlp.lemmatizer import Lematize
import cfg.ctt as ctt
import requests

api = Namespace('gov_thes_processor',
                description='Download and process Thesaurus')


# ping_args = api.parser()

def process_thesauri() -> dict:
    # Define thesaurus EIRA Thesaurus details
    eira_thesaurus_details = ctt.EIRA_THESAURUS_DETAILS
    thesauri_details = [eira_thesaurus_details]
    # TODO: Create the folders where the Thesaurus will be saved

    # Create ThesaurusManager with the configuration for EIRA
    thesauri_manager = ThesauriManager(thesauri_details)
    # Download Thesaurus
    thesauri_manager.download_thesauri()
    # Analyze downloaded Thesaurus
    return {}


@api.route('/process_thesaurus')
class ProcessThesaurus(Resource):
    @api.doc("Download and process thesaurus")
    # @api.expect(ping_args, validate=True)
    def post(self):
        report = process_thesauri()
        # TODO: Add the following lines inside process_thesauri()
        url = 'http://localhost:5000/camss-sis/v1/SKOS_Mapper/skos_map'
        thesauri = {
            "endpoint": "http://localhost:5000/camss-sis/v1/nlp/lemmatize",
            "thesauri": [
                ctt.TEST_EIRA_THESAURUS_LEMMA_DETAILS
            ]
        }
        skos_mapper_response = requests.post(url, json=thesauri)

        t0 = io.now()
        return {'message': f'{str(io.now() - t0)}'}, 200
