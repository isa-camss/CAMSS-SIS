from com.nttdata.dgi.io.down.request_downloader import RequestDownloader


class CorpusDownloader(RequestDownloader):

    def __init__(self, url: str = None, content_path: str = None):
        super().__init__(url, content_path)

    def get_corpus(self):
        super().download()

    def __call__(self, url, content_path):
        super().__init__(url, content_path)
        return self
