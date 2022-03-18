import unittest
import cfg.ctt as ctt
import cfg.crud as crud
import cfg.credentials as cred
import com.nttdata.dgi.util.io as io
import os
from org.camss.corpora.corpora_manager import CorporaManager
from com.nttdata.dgi.search.search import Search
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class Corpora(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Corpora, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_corpora_downloader(self):
        corpora_manager = CorporaManager(ctt.DOWNLOAD_CORPORA_DETAILS, ctt.TEXTIFICATION_CORPORA_DETAILS). \
            prepare_corpus_folders(). \
            download_corpus()
        return self

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

    def test_004_skip_downloaded_resources(self):
        ask = Search()
        es = Elasticsearch("http://localhost:9200")
        rsc_id_1 = "5e24407a9fe058e62f84046a7d79139a"
        rsc_id_2 = "3b0aabd7b44bbe11398d30f3518f989d"
        elastic_index = crud.ELASTICSEARCH_DOCS_PROCESSED_INDEX + "*"
        query = {"query": {
            "term": {"rsc_id.keyword": rsc_id_2}}
        }
        result = es.count(index=elastic_index, body=query)['count']

        print(result)
        return self
