from com.ntt.dgi.util.report import Report


class ThesauriManager:
    source_thesaurus_persistor_details: dict
    target_thesaurus_persistor_details: dict
    thesauri: str
    thesauri_details: dict
    thesauri_processed: str
    skos_mapper_details: dict

    def __init__(self):
        self.thesauri_processed = ""

    def analyse(self) -> Report:
        report = Report()
        return report

    def load_thesauri(self, thesauri_details) -> dict:
        self.thesauri_details = thesauri_details
