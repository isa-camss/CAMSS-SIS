from urllib import request
import cfg.ctt as ctt


class Downloader:
    downloader_details: dict

    def __init__(self, downloader_details, thesauri_uri: str):
        self.downloader_details = downloader_details
        self.uri = thesauri_uri

    def download_http(self) -> dict:
        # Download from URL
        return {}

    def download_api(self) -> dict:
        # Download from URL
        return {}

    def download_virtuoso(self) -> dict:
        # Download from URL
        return {}

    def get_thesauri(self, uri: str):
        # Set download url
        thesauri_uri = ctt.EIRA_THESAURI

        # Set file location, name and extension
        local_file = 'C:/SEMBUdev/Github/CAMSS/CAMSS-SIS/dev/arti/rdf/eira_410.rdf'

        # Download thesauri
        request.urlretrieve(thesauri_uri, local_file)
