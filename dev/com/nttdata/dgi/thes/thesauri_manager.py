from com.nttdata.dgi.util.report import Report
from com.nttdata.dgi.io.down.thesaurus_downloader import ThesaurusDownloader


class ThesauriManager:
    source_thesaurus_persistor_details: dict
    target_thesaurus_persistor_details: dict
    thesauri_details: list  # List of dicts with thesaurus url and path to save it
    thesauri_processed: str
    skos_mapper_details: dict
    http_downloader: ThesaurusDownloader

    def __init__(self, list_dicts_thesaurus_details):
        self.thesauri_details = list_dicts_thesaurus_details

    def download_thesauri(self):
        downloader = ThesaurusDownloader()
        for thesaurus in self.thesauri_details:
            downloader(thesaurus.get("url"), thesaurus.get("path")).download()

    def analyse(self) -> Report:
        report = Report()
        return report

    def load_thesauri(self, thesauri_details) -> dict:
        self.thesauri_details = thesauri_details
        return {}

    def persist_thesauri(self):
        return self

