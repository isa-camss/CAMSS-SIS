import requests
from com.nttdata.dgi.io.down.downloader import Downloader
import cfg.ctt as ctt


class RequestDownloader(Downloader):
    url: str
    body: dict
    headers: dict
    response: requests.Response

    def __init__(self, request_url: str = None, request_body: dict = None, request_headers: dict = None):
        super().__init__()

        self.url = request_url
        self.body = request_body
        self.headers = request_headers
        self.response = None

    def download(self):
        # request to EURLEX API
        self.response = requests.post(url=self.url, data=self.body, headers=self.headers)

        return self
