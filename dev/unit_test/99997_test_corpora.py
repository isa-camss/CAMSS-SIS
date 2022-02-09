import unittest
import requests
from bs4 import BeautifulSoup as bs
import cfg.ctt as ctt
from urllib import request


class Corpora(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Corpora, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_corpora_downloader(self):
        # request to EURLEX API
        eurlex_request = requests.post(ctt.EURLEX_CORPORA_URL, data=ctt.EURLEX_CORPORA_QUERY_BODY,
                                       headers=ctt.EURLEX_CORPORA_QUERY_HEADERS)

        # Parse the EURLEX query response
        soup = bs(eurlex_request.content, 'xml')

        # Extract attribute with the document link
        tag_link = soup.find_all("document_link", {"type": "pdf"})

        # save in a list the document link
        corpora_list_links = []
        for link in tag_link:
            link_pdf = link.get_text()
            corpora_list_links.append(link_pdf)
        print(corpora_list_links)

        # download the list of the EURLEX documents
        for i, url in enumerate(corpora_list_links):
            save_path = f'C:/SEMBUdev/Github/CAMSS/CAMSS-SIS/dev/arti/corpus/corpus_{i}.pdf'
            request.urlretrieve(url, save_path)
