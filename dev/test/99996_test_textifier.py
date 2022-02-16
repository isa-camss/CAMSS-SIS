import unittest
import sys
import logging
from com.nttdata.dgi.io.textify.textify import Textify
import com.nttdata.dgi.util.io as io


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
        args: dict = {'source-dir': 'C:/SEMBUdev/Github/corpora/pdf',
                      'target-dir': 'C:/SEMBUdev/Github/corpora/txt',
                      'exclude-ext': ['.html', '.ppt'],
                      'lang?': True}

        for index, path, error, _, _, _, _, _ in Textify.textify(args):

            if error:
                io.log(f'{index}. FILE {path} COULD NOT BE READ NOR TRANSFORMED.')
                flawed.append(path)
            else:
                io.log(f'{index}. {path}', logger=log)

        io.log(f'Done. It took {io.now() - t0} to transform {index} files', logger=log)
        io.log(f'{len(flawed)} files could not be transformed. Here they are: {flawed}')
        return
