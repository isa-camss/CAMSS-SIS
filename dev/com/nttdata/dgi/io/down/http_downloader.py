from urllib import request
from com.nttdata.dgi.io.down.downloader import Downloader


class HTTPDownloader(Downloader):
    http_url: str
    http_content_path: str

    def __init__(self, downloader_url: str = None, content_path: str = None):
        super().__init__()
        self.http_url = downloader_url
        self.http_content_path = content_path

    def __call__(self, url, content_path):
        self.__init__(url, content_path)
        return self

    def download(self):
        request.urlretrieve(url=self.http_url, filename=self.http_content_path)
        return self
