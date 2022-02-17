import unittest
import sys
import logging
from com.nttdata.dgi.io.textify.textify import Textify
import com.nttdata.dgi.util.io as io
import cfg.ctt as ctt
import os

"""
Test Tika Massively
-------------------
Testing the performance of Tika with the IDB Lab corpus
"""

CORPUS = '/Volumes/ext-hd/bidlab-corpus-txt/test-doc-analyser'
TXT_CORPUS = '/Volumes/ext-hd/bidlab-corpus-txt'

LOG = './test-doc-analyser.log'
io.drop_file(LOG)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO, filename=LOG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
log = logging.getLogger("DocGov")


class TestifierTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestifierTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_get_content(self):
        text = Textify.get_content('C:/SEMBUdev/Github/corpora/pdf/3a99b8f82a0728f6cc2d492c1f255ee9.pdf', True)
        print(text)

    def test_001_textify(self):
        t0 = io.now()
        io.log(f'Transforming original content into TXT with Tika...', logger=log)
        # If
        flawed = []
        index = 0
        args: dict = ctt.TEXTIFICATION_DETAILS

        os.makedirs(ctt.TEXTIFICATION_DETAILS.get('textification_dir'), exist_ok=True)

        textifier = Textify()

        for dir_name in os.listdir(ctt.TEXTIFICATION_DETAILS.get('corpus_dir')):
            if os.path.isdir(ctt.TEXTIFICATION_DETAILS.get('corpus_dir') + '/' + dir_name):
                if dir_name in ctt.TEXTIFICATION_DETAILS.get('exclude_extensions_type'):
                    pass
                else:
                    textifier.textify({'source_dir': ctt.TEXTIFICATION_DETAILS.get('corpus_dir') + '/' + dir_name,
                                       'target_dir': ctt.TEXTIFICATION_DETAILS.get('textification_dir'),
                                       'lang?': ctt.TEXTIFICATION_DETAILS.get(True)
                                       })

        return
