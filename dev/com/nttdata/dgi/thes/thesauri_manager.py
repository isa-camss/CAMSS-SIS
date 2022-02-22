import requests
from com.nttdata.dgi.io.down.thesaurus_downloader import ThesaurusDownloader
from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory, PersistorType


class ThesauriManager:
    thesauri_details: list  # List of dicts with thesaurus url and path to save it
    skos_lemmatizer_details: dict

    def __init__(self, list_dicts_thesaurus_details, dict_skos_lemmatizer_details):
        self.thesauri_details = list_dicts_thesaurus_details
        self.skos_lemmatizer_details = dict_skos_lemmatizer_details

    def download_thesauri(self):
        downloader = ThesaurusDownloader()
        for thesaurus in self.thesauri_details:
            downloader(thesaurus.get("url"), thesaurus.get("path")).download()

    def analyse(self):
        skos_map_url = self.skos_lemmatizer_details.get('url')
        skos_map_json_details = self.skos_lemmatizer_details.get('body')
        skos_mapper_response = requests.post(skos_map_url, json=skos_map_json_details)
        if not skos_mapper_response.ok:
            raise (Exception(f'The skos mapper endpoint returned status code {skos_mapper_response.status_code}. '
                             f'Response content: {skos_mapper_response.content}'))

    def persist_thesauri(self, connection_details: dict, thesaurus_details: dict):
        p: IPersistor = PersistenceFactory().new(PersistorType.VIRTUOSO, **connection_details)
        p.persist(thesaurus_details.get('location'), thesaurus_details.get('graph_name'))
        return self
