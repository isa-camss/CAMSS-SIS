import cfg.ctt as ctt
import cfg.crud as crud
import com.nttdata.dgi.util.io as io
from flask_restx import Resource, Namespace
from com.nttdata.dgi.thes.thesauri_manager import ThesauriManager

api = Namespace(ctt.GOVERNORS_NAME,
                description='These microservices are responsible of generating the needed resources to enable the '
                            'search engine.')


# ping_args = api.parser()
def process_thesauri() -> (dict, int):
    report = {"message": [],
              "warning": [],
              "error": []}
    try:
        t0 = io.log("Process Thesauri started")
        # 0. Initialize the needed variables for this process
        # Download variables
        download_eira_thesaurus_details = ctt.EIRA_THESAURUS_DETAILS
        download_thesauri_details = [download_eira_thesaurus_details]

        # SKOS Lemmatizer variables
        skos_lemmatizer_details = ctt.SKOS_MAPPER_DETAILS

        # Lematization variables
        eira_terms_details = ctt.EIRA_CONCEPTS_DETAILS
        lemmatization_details = ctt.LEMMATIZATION_DETAILS

        # Persistor variables
        virtuoso_connection_details = crud.VIRTUOSO_EIRA_LOAD_RDF_FILE
        eira_thesaurus_persistor_details = ctt.EIRA_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS
        eira_thesaurus_lemma_persistor_details = ctt.EIRA_LEMMAS_THESAURUS_VIRTUOSO_PERSISTENCE_DETAILS
        elastic_connection_details = crud.ELASTICSEARCH_DETAILS

        # 1. Create ThesaurusManager
        thesauri_manager = ThesauriManager()

        # 2. Prepare all process folders/files
        thesauri_manager.prepare_thesauri_folders(download_thesauri_details,
                                                  skos_lemmatizer_details,
                                                  eira_terms_details)
        report['message'].append(f"Thesauri folders preparation finished in {str(io.now() - t0)}")
        t1 = io.log(f"Thesauri configuration done in {str(io.now() - t0)}")

        # 3. Download Thesauri
        thesauri_manager.download_thesauri(download_thesauri_details)
        report['message'].append(f"Thesauri download finished in {str(io.now() - t1)}")
        t2 = io.log(f"Thesauri download done in {str(io.now() - t1)}")

        # 4. SKOS Lemmatizer of downloaded Thesaurus
        thesauri_manager.analyse_thesauri(skos_lemmatizer_details)
        report['message'].append(f"Thesauri lemmatization finished in {str(io.now() - t2)}")
        t3 = io.log(f"Thesauri lemmatization done in {str(io.now() - t2)}")

        # 5. Persist original Thesaurus in Virtuoso
        thesauri_manager.persist_thesauri(virtuoso_connection_details,
                                          eira_thesaurus_persistor_details)

        report = io.merge_dicts([report, thesauri_manager.persistor.report])

        # 6. Persist the lemmatized skos in Virtuoso
        thesauri_manager.persist_thesauri(virtuoso_connection_details,
                                          eira_thesaurus_lemma_persistor_details)

        report = io.merge_dicts([report, thesauri_manager.persistor.report])
        report['message'].append(f"Persistence finished in {str(io.now() - t3)}")
        t4 = io.log(f"Thesauri persistence done in {str(io.now() - t3)}")

        # 7. Lemmatize EIRA terms
        thesauri_manager.lemmatize_terms(eira_terms_details, elastic_connection_details, lemmatization_details)
        report['message'].append(f"Terms lemmatization finished in {str(io.now() - t4)}")
        io.log(f"Terms lemmatization done in {str(io.now() - t4)}")

        status_code = 200

    except Exception as ex:
        status_code = 555
        exception_message = f"Exception: {ex}"
        report['error'].append(f"It was an error during the Thesaurus process. {exception_message}")
        io.log(exception_message)

    return report, status_code


@api.route(f'/{ctt.GOV_THESAURI_PROCESSOR_ENDPOINT}')
class ProcessThesaurus(Resource):
    @api.doc("Download and process thesaurus")
    # @api.expect(ping_args, validate=True)
    def post(self):
        t0 = io.now()
        report, status_code = process_thesauri()
        return {'message': f'Report: {report}. Done in: {str(io.now() - t0)}'}, 200
