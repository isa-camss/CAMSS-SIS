import unittest
import cfg.ctt as ctt
import cfg.credentials as cred
import com.nttdata.dgi.util.io as io
import os
from org.camss.corpora.corpora_manager import CorporaManager


class Corpora(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Corpora, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_corpora_downloader(self):
        corpora_manager = CorporaManager(ctt.DOWNLOAD_CORPORA_DETAILS).prepare_corpus_folders().download_corpus()
        return self, corpora_manager

    def test_002_credentials(self):
        user = cred.EURLEX_WEB_SERVICE_USER_NAME
        password = cred.EURLEX_WEB_SERVICE_PASSWORD
        return self

    def test_003_create_file(self):
        file_path = '.' + ctt.CORPORA_DETAILS.get('corpora_metadata_file')
        corpora_path = '../' + ctt.CORPORA_DETAILS.get('corpora_dir')
        io.drop_file(file_path)
        os.makedirs(corpora_path, exist_ok=True)
        open(file_path, 'w+')
        return self
