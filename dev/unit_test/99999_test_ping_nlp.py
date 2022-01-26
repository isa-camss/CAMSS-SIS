import unittest
import sys
import logging
import com.ntt.dgi.util.io as io


LOG = '../log/test_logger.log'
io.drop_file(LOG)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO, filename=LOG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger('test_logger')


class PingNLP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PingNLP, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_ping_nlp(self):
        io.log("TEST")


if __name__ == '__main__':
    unittest.main()
    # a = PingNLP()
    # a.check_new_rsc()
    # a.test_001_ping_mlp()
