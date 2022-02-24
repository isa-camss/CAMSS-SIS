import requests
from com.nttdata.dgi.io.down.thesaurus_downloader import ThesaurusDownloader
from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory, PersistorType
import com.nttdata.dgi.util.io as io


class ThesauriManager:
    thesauri_details: list  # List of dicts with thesaurus url and path to save it
    skos_lemmatizer_details: dict
    report: dict

    def __init__(self, list_thesauri_details: list = None,
                 dict_skos_lemmatizer_details: dict = None,
                 report: dict = None):
        self.thesauri_details = list_thesauri_details
        self.skos_lemmatizer_details = dict_skos_lemmatizer_details
        self.report = report

    def prepare_thesauri_folders(self, thesauri_details: list, skos_lemmatizer_details: dict):
        # Iterate through every thesaurus to drop the file if exists and creates the folder
        self.thesauri_details = thesauri_details
        self.skos_lemmatizer_details = skos_lemmatizer_details
        for thesaurus in self.thesauri_details:
            io.log(f"Preparing: {thesaurus.get('path')}")
            # Drop file
            io.drop_file(thesaurus.get('path'))

            # Create the needed folders
            io.make_file_dirs(thesaurus.get('path'))

        # Delete the existing lemmatized thesaurus
        for lemmatized_thesaurus in self.skos_lemmatizer_details.get('body').get('thesauri'):
            io.log(f"Preparing: {lemmatized_thesaurus.get('target')}")
            # Drop file
            io.drop_file(lemmatized_thesaurus.get('target'))

            # Create the needed folders
            io.make_file_dirs(lemmatized_thesaurus.get('target'))
        return self

    def download_thesauri(self, download_thesauri_details: list):
        self.thesauri_details = download_thesauri_details
        downloader = ThesaurusDownloader()
        for thesaurus in self.thesauri_details:
            io.log(f"Downloading Thesaurus: {thesaurus.get('name')}")
            downloader(thesaurus.get("url"), thesaurus.get("path")).download()
        return self

    def analyse(self, skos_lemmatizer_details: dict):
        self.skos_lemmatizer_details = skos_lemmatizer_details
        skos_map_url = self.skos_lemmatizer_details.get('url')
        skos_map_json_details = self.skos_lemmatizer_details.get('body')
        skos_mapper_response = requests.post(skos_map_url, json=skos_map_json_details)
        if not skos_mapper_response.ok:
            raise (Exception(f'The skos mapper endpoint returned status code {skos_mapper_response.status_code}. '
                             f'Response content: {skos_mapper_response.content}'))
        return self

    def persist_thesauri(self, connection_details: dict, thesaurus_details: dict):
        p: IPersistor = PersistenceFactory().new(PersistorType.VIRTUOSO, **connection_details)
        p.persist(thesaurus_details.get('location'), thesaurus_details.get('graph_name'))
        return self
