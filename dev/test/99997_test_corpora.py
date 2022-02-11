import unittest
import requests
from bs4 import BeautifulSoup as bs
import cfg.ctt as ctt
import hashlib
from urllib import request


class Corpora(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Corpora, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_corpora_downloader(self):
        query = ctt.EURLEX_CORPORA_QUERY_BODY % (ctt.EURLEX_WEB_SERVICE_USER_NAME,
                                                 ctt.EURLEX_WEB_SERVICE_PASSWORD,
                                                 ctt.PAGE_NUMBER,
                                                 ctt.RESULTS_NUMBER_BY_PAGE)
        # request to EURLEX API
        eurlex_request = requests.post(ctt.EURLEX_CORPORA_URL, data=query,
                                       headers=ctt.EURLEX_CORPORA_QUERY_HEADERS)

        # Parse the EURLEX query response
        soup = bs(eurlex_request.content, 'xml')

        # Extract reference and url of the resource
        request_result = soup.find_all('result')

        corpus = []
        for result in request_result:
            reference = result.find('reference').text
            reference_md5 = hashlib.md5(reference.encode())
            reference_hash = reference_md5.hexdigest()

            # resources_link = [reference_hash]
            resources_link = []

            for document_type in ctt.CORPORA_DOCUMENT_TYPE:
                resources_link = result.find("document_link", {"type": document_type})

            corpus.append(resources_link)

        print(resources_link)
        print(corpus)
