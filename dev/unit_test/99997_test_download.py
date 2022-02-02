import unittest
import sys
import logging
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.io.down.thesaurus_downloader import ThesaurusDownloader
from com.nttdata.dgi.thes.thesauri_manager import ThesauriManager
from urllib import request
import cfg.ctt as ctt


class Downloader(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Downloader, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_thesauri_downloader(self):
        eira_uri = ctt.EIRA_THESAURI
        eira_local_path = '../arti/rdf/eira_410.rdf'
        thesauri = ThesaurusDownloader(url=eira_uri, content_path=eira_local_path)
        thesauri.get_thesauri()
        return

    def test_001_thesauri_manager(self):
        eira_uri = ctt.EIRA_THESAURI
        eira_local_path = '../arti/rdf/eira_410.rdf'
        eira_thesaurus_details = {"url": eira_uri, "path": eira_local_path}
        thesauri_details = [eira_thesaurus_details]
        thesauri_manager = ThesauriManager(thesauri_details)
        thesauri_manager.download_thesauri()
        return 
