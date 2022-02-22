import unittest
from com.nttdata.dgi.io.textify.textify import Textifier
import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
import os
import json


class TestifierTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestifierTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_get_content(self):
        text = io.get_content_from_file('C:/SEMBUdev/Github/corpora/pdf/3a99b8f82a0728f6cc2d492c1f255ee9.pdf', True)
        print(text)

    def test_002_textify_folder(self):
        args: dict = ctt.TEXTIFICATION_CORPORA_DETAILS

        textifier = Textifier()

        for dir_name in os.listdir(ctt.TEXTIFICATION_CORPORA_DETAILS.get('corpus_dir')):
            if os.path.isdir(ctt.TEXTIFICATION_CORPORA_DETAILS.get('corpus_dir') + '/' + dir_name):
                if dir_name in ctt.TEXTIFICATION_CORPORA_DETAILS.get('exclude_extensions_type'):
                    pass
                else:
                    textifier.textify()

        return

    def test_003_textify_file(self):
        with open(ctt.DOWNLOAD_CORPORA_DETAILS.get('corpora_metadata_file'), 'r') as jsonl_file:
            data = json.load(jsonl_file)
            print(data)
