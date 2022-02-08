from urllib import request
import requests
from com.nttdata.dgi.io.down.downloader import Downloader
import cfg.ctt as ctt


class RequestDownloader(Downloader):
    http_url: list
    http_content_path: str

    def __init__(self, downloader_url: str = None, content_path: str = None):
        super().__init__()
        self.http_url = downloader_url
        self.http_content_path = content_path

    def request_corpus(self):
        response = requests.post(ctt.EURLEX_CORPORA_URL, data=ctt.EURLEX_CORPORA_QUERY_BODY, headers=ctt.EURLEX_CORPORA_QUERY_HEADERS)
        print(response.content)
        # TODO make a for loop to get a list of url from the response

    def download(self):
        # TODO make a for loop to name the files downloaded
        request.urlretrieve(url=self.http_url, filename=self.http_content_path)
        return self
