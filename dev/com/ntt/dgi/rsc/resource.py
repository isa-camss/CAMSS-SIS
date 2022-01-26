from com.ntt.dgi.util.report import Report


class Resource:
    content: str
    uri: str
    target_resources_persistor_details: dict
    download_resource_details: dict  # MUST be what needs Downloader
    metadata: dict

    def __init__(self):
        return

    def analyse(self) -> dict:
        return {}

    def create_resource_details(self, resource_details: dict):
        self.download_resource_details = resource_details

    def download_content(self) -> str:
        # use self.download_resource_details to download the content
        # instance Downloader class
        # save the content to the atribute self.content = e.g.-> download_http
        return ""

    def drop(self) -> Report:
        report = Report()
        return report

    def get_content(self) -> str:
        return ""

    def get_id(self) -> str:
        # id will be generated from the content
        return ""

    def get_metadata(self):
        return self.metadata

    def parse_metadata(self, raw_metadata: dict):
        self.metadata = raw_metadata

    def lemmatize(self, content: str) -> str:
        return ""

    def persist_analysis_results(self, content: str, analysis_result: dict) -> Report:
        report = Report()
        return report

    def persist_metadata(self, metadata: dict) -> Report:
        report = Report()
        return report

    def textify(self, file_path: str) -> str:
        return ""

    def validate(self) -> Report:
        report = Report()
        return report
