import requests
from com.nttdata.dgi.io.down.thesaurus_downloader import ThesaurusDownloader
from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory, PersistorType
import com.nttdata.dgi.util.io as io
import json
import os


class ThesauriManager:
    thesauri_details: list  # List of dicts with thesaurus url and path to save it
    skos_lemmatizer_details: dict
    virtuoso_persistor: IPersistor
    elastic_persistor: IPersistor
    virtuoso_persistor_details: dict
    elastic_persistor_details: dict
    concept_details: dict
    lemmatization_details: dict

    def __init__(self, list_thesauri_details: list = None,
                 dict_skos_lemmatizer_details: dict = None,
                 virtuoso_connection_details: dict = None,
                 elastic_connection_details: dict = None,
                 concepts_details: dict = None, lemmatization_details: dict = None):
        self.thesauri_details = list_thesauri_details
        self.skos_lemmatizer_details = dict_skos_lemmatizer_details
        self.virtuoso_persistor_details = virtuoso_connection_details
        self.elastic_persistor_details = elastic_connection_details
        self.concept_details = concepts_details
        self.lemmatization_details = lemmatization_details

    def prepare_thesauri_folders(self, thesauri_details: list, skos_lemmatizer_details: dict, concept_details: dict):
        self.thesauri_details = thesauri_details
        self.skos_lemmatizer_details = skos_lemmatizer_details
        self.concept_details = concept_details

        # Prepare folder for download Thesauri
        for thesaurus in self.thesauri_details:
            io.log(f"Preparing: {thesaurus.get('path')}")
            # Drop file
            io.drop_file(thesaurus.get('path'))
            # Create the needed folders
            io.make_file_dirs(thesaurus.get('path'))

        # Prepare folder for Lemmatized thesauri
        for lemmatized_thesaurus in self.skos_lemmatizer_details.get('body').get('thesauri'):
            io.log(f"Preparing: {lemmatized_thesaurus.get('target')}")
            # Drop file
            io.drop_file(lemmatized_thesaurus.get('target'))
            # Create the needed folders
            io.make_file_dirs(lemmatized_thesaurus.get('target'))

        # Prepare folder for thesauri lemmatized concepts
        # Create the needed folders
        os.makedirs(self.concept_details.get('json_dir'), exist_ok=True)
        # Drop existing files
        io.drop_file(self.concept_details.get('lemmatized_jsonl'))
        # Create files needed
        with open(self.concept_details.get('lemmatized_jsonl'), 'w+') as outfile:
            outfile.close()

        return self

    def download_thesauri(self, download_thesauri_details: list):
        self.thesauri_details = download_thesauri_details
        downloader = ThesaurusDownloader()
        for thesaurus in self.thesauri_details:
            io.log(f"Downloading Thesaurus: {thesaurus.get('name')}")
            downloader(thesaurus.get("url"), thesaurus.get("path")).download()
        return self

    def analyse_thesauri(self, skos_lemmatizer_details: dict):
        self.skos_lemmatizer_details = skos_lemmatizer_details
        skos_map_url = self.skos_lemmatizer_details.get('url')
        skos_map_json_details = self.skos_lemmatizer_details.get('body')
        skos_mapper_response = requests.post(skos_map_url, json=skos_map_json_details)
        if not skos_mapper_response.ok:
            raise (Exception(f'The skos mapper endpoint returned status code {skos_mapper_response.status_code}. '
                             f'Response content: {skos_mapper_response.content}'))
        return self

    def persist_thesauri(self, virtuoso_connection_details: dict, thesaurus_details: dict):
        self.virtuoso_persistor_details = virtuoso_connection_details
        self.virtuoso_persistor = PersistenceFactory().new(persistor_type=PersistorType.VIRTUOSO,
                                                           persistor_details=self.virtuoso_persistor_details)
        self.virtuoso_persistor.persist(thesaurus_details.get('location'), thesaurus_details.get('graph_name'))
        return self

    def persist_thesauri_lemmatized_concepts(self, concept_details: dict,
                                             virtuoso_connection_details: dict,
                                             elastic_connection_details: dict):
        self.concept_details = concept_details
        self.virtuoso_persistor_details = virtuoso_connection_details
        self.elastic_persistor_details = elastic_connection_details
        self.virtuoso_persistor = PersistenceFactory().new(persistor_type=PersistorType.VIRTUOSO,
                                                           persistor_details=self.virtuoso_persistor_details)
        self.elastic_persistor = PersistenceFactory().new(persistor_type=PersistorType.ELASTIC,
                                                          persistor_details=self.elastic_persistor_details)
        for concept in self.concept_details.get('vocabulary_details'):
            view_type = concept.get('view')
            skos_collection = concept.get('skos_collection')
            query_view_concepts = self.concept_details.get('query_terms') % skos_collection

            virtuoso_response = self.virtuoso_persistor.search(query=query_view_concepts)
            results_format = virtuoso_response['results']['bindings']

            for item_list in results_format:
                lemma_value = item_list.get('Lemma').get('value')
                lemma_id = io.hash(lemma_value)

                elastic_eira_terms_index = self.concept_details.get(
                    'elastic_terms_index') + "*"
                query = {"query": {"term": {"lemma_id.keyword": lemma_id}}}

                abb_exist = self.elastic_persistor.ask(index=elastic_eira_terms_index, query=query)

                if abb_exist:
                    io.log(f"Skipping persistence of the lemma '{lemma_id}' because it already exists in")
                else:

                    # Create jsonl with lemmatized terms
                    date_time_now = io.now()
                    date_time_now_str = io.datetime_to_string(date_time_now)
                    terms_document_dict = {
                        "timestamp": date_time_now_str,
                        "eira_view": view_type + " " + "view",
                        "lemma_id": lemma_id,
                        "lemma": lemma_value
                    }
                    with open(self.concept_details.get('lemmatized_jsonl'), 'a+') as outfile:
                        json.dump(terms_document_dict, outfile)
                        outfile.write('\n')
                        outfile.close()

                    str_date = io.now().strftime("%Y%m%d")
                    elastic_eira_terms_index_at_date = elastic_eira_terms_index + f"-{view_type}-view-{str_date}"
                    terms_document_dict['timestamp'] = date_time_now
                    self.elastic_persistor.persist(index=elastic_eira_terms_index_at_date,
                                                   content=terms_document_dict)
                    io.log(f"The lemma '{lemma_id}' from {view_type} view "
                           f"was succesfully persisted in the '{elastic_eira_terms_index}' index of elasticsearch")
            io.log("The lemmas of the processed controlled vocabularies, were correctly persisted in elasticsearch")
        return self

    def lemmatize_custom_terms(self, concept_details: dict, connection_details: dict, lemmatization_details: dict):
        self.concept_details = concept_details
        self.elastic_persistor_details = connection_details
        self.lemmatization_details = lemmatization_details
        self.elastic_persistor = PersistenceFactory().new(persistor_type=PersistorType.ELASTIC,
                                                          persistor_details=self.elastic_persistor_details)

        for term in self.concept_details.get('terms'):
            json_terms = {'phrase': term, 'lang': self.concept_details.get('rsc_lang')}
            lemmatizer_response = requests.post(url=self.lemmatization_details.get('endpoint'), json=json_terms)

            # Create jsonl with lemmatized terms
            date_time_now = io.now()
            date_time_now_str = io.datetime_to_string(date_time_now)
            lemmatized_document_dict = {
                "timestamp": date_time_now_str,
                "term_id": io.hash(term),
                "term": term,
                "lemma": json.loads(lemmatizer_response.content)['unaccented-minus-stopwords']
            }
            with open(self.concept_details.get('lemmatized_jsonl'), 'a+') as outfile:
                json.dump(lemmatized_document_dict, outfile)
                outfile.write('\n')
                outfile.close()

            # Persist in Elasticsearch terms
            lemmatized_document_dict = {
                "timestamp": date_time_now,
                "term_id": io.hash(term),
                "term": term,
                "lemma": json.loads(lemmatizer_response.content)['unaccented-minus-stopwords']
            }
            str_date = io.now().strftime("%Y%m%d")
            elastic_metadata_index = self.concept_details.get('elastic_terms_index') + f"-{str_date}"
            self.elastic_persistor.persist(index=elastic_metadata_index,
                                           content=lemmatized_document_dict)
        return self
