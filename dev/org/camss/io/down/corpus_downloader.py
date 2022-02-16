from com.nttdata.dgi.io.down.request_downloader import RequestDownloader


class CorpusDownloader(RequestDownloader):

    def __init__(self, request_url: str = None, request_body: dict = None, request_headers: dict = None):
        super().__init__(request_url, request_body, request_headers)

    def get_corpus(self):
        super().download()

    def __call__(self, request_url: str = None, request_body: dict = None, request_headers: dict = None):
        super().__init__(request_url, request_body, request_headers)
        return self
