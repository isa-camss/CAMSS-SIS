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
    persistor: IPersistor
    persistor_details: dict
    concept_details: dict
    lemmatization_details: dict

    def __init__(self, list_thesauri_details: list = None,
                 dict_skos_lemmatizer_details: dict = None, connection_details: dict = None,
                 concepts_details: dict = None, lemmatization_details: dict = None):
        self.thesauri_details = list_thesauri_details
        self.skos_lemmatizer_details = dict_skos_lemmatizer_details
        self.persistor_details = connection_details
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

        # Prepare folder for Lemmatized terms
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

    def persist_thesauri(self, connection_details: dict, thesaurus_details: dict):
        self.persistor_details = connection_details
        self.persistor = PersistenceFactory().new(persistor_type=PersistorType.VIRTUOSO,
                                                  persistor_details=self.persistor_details)
        self.persistor.persist(thesaurus_details.get('location'), thesaurus_details.get('graph_name'))
        return self

    def lemmatize_terms(self, concept_details: dict, connection_details: dict, lemmatization_details: dict):
        self.concept_details = concept_details
        self.persistor_details = connection_details
        self.lemmatization_details = lemmatization_details
        self.persistor = PersistenceFactory().new(persistor_type=PersistorType.ELASTIC,
                                                  persistor_details=self.persistor_details)

        date_time_now = io.now()
        for term in self.concept_details.get('terms'):
            json_terms = {'phrase': term, 'lang': self.concept_details.get('rsc_lang')}
            lemmatizer_response = requests.post(url=self.lemmatization_details.get('endpoint'), json=json_terms)
            lemmatized_document_dict = {
                "timestamp": date_time_now,
                "term_id": io.hash(term),
                "term": term,
                "lemma": json.loads(lemmatizer_response.content)['unaccented-minus-stopwords']
            }

            # Create jsonl with lemmatized terms
            with open(self.concept_details.get('lemmatized_jsonl'), 'a+') as outfile:
                json.dump(lemmatized_document_dict, outfile)
                outfile.write('\n')
                outfile.close()

            # Persist in Elasticsearch terms
            str_date = io.now().strftime("%Y%m%d")
            elastic_metadata_index = self.concept_details.get('elastic_terms_index') + f"-{str_date}"
            self.persistor.persist(index=elastic_metadata_index,
                                   content=lemmatized_document_dict)

        return self
