import unittest
from com.nttdata.dgi.io.textify.textify import Textify
import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
import os


class TestifierTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestifierTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_get_content(self):
        text = io.get_content_from_file('C:/SEMBUdev/Github/corpora/pdf/3a99b8f82a0728f6cc2d492c1f255ee9.pdf', True)
        print(text)

    def test_001_textify(self):
        args: dict = ctt.TEXTIFICATION_CORPORA_DETAILS

        textifier = Textify()

        for dir_name in os.listdir(ctt.TEXTIFICATION_CORPORA_DETAILS.get('corpus_dir')):
            if os.path.isdir(ctt.TEXTIFICATION_CORPORA_DETAILS.get('corpus_dir') + '/' + dir_name):
                if dir_name in ctt.TEXTIFICATION_CORPORA_DETAILS.get('exclude_extensions_type'):
                    pass
                else:
                    textifier.textify()

        return
