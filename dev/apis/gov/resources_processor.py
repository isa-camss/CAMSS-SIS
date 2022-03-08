import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
from flask_restx import Resource, Namespace
from org.camss.corpora.corpora_manager import CorporaManager

api = Namespace(ctt.GOVERNORS_NAME,
                description='These microservices are responsible of generating the needed resources to enable the '
                            'search engine.')


# ping_args = api.parser()
def process_corpus() -> dict:
    report = {"message": [],
              "warning": [],
              "error": []}
    try:
        t0 = io.log("Proccess Corpora started")

        # 0. Initialize the needed variables for this process
        # Download variables
        download_corpora_details = ctt.DOWNLOAD_CORPORA_DETAILS

        # Textification variables
        textify_corpora_details = ctt.TEXTIFICATION_CORPORA_DETAILS

        # Lematization variables
        lemmatization_corpora_details = ctt.CORPORA_LEMMATIZATION_DETAILS

        # Persistor variables
        persist_corpora_details = ctt.CORPORA_LEMMATIZATION_DETAILS

        # 1. Create CorporaManager
        corpora_manager = CorporaManager()

        # 2. Prepare all folders/files
        corpora_manager.prepare_corpus_folders(download_corpora_details,
                                               textify_corpora_details,
                                               lemmatization_corpora_details)
        report['message'].append(f"Corpora folders preparation finished in {str(io.now() - t0)}")
        t1 = io.log(f"Corpora configuration done in {str(io.now() - t0)}")

        # 3. Download EURLEX Corpus
        corpora_manager.download_corpus(download_corpora_details)
        report['message'].append(f"Corpora download finished in {str(io.now() - t1)}")
        t2 = io.log(f"Corpora download done in {str(io.now() - t1)}")

        # 4. Textify Corpus
        corpora_manager.textify_corpus(download_corpora_details, textify_corpora_details)
        report['message'].append(f"Corpora textification finished in {str(io.now() - t2)}")
        t3 = io.log(f"Corpora textification done in {str(io.now() - t2)}")

        # 5. Lemmatize Corpus
        corpora_manager.lemmatize_corpora(lemmatization_corpora_details)
        report['message'].append(f"Corpora lemmatization finished in {str(io.now() - t3)}")
        t4 = io.log(f"Corpora lemmatization done in {str(io.now() - t3)}")

        status_code = 200
    except Exception as ex:
        status_code = 555
        exception_message = f"Exception: {ex}"
        report['error'].append(f"It was an error during the Corpora process.  {exception_message}")
        io.log(exception_message)

    return report, status_code


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
