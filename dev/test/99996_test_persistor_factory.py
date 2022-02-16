import unittest
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory, PersistorType
import cfg.crud as crud


class PersistorTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PersistorTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_persistor_virtuoso(self):
        p = PersistenceFactory().new(PersistorType.VIRTUOSO, **crud.VIRTUOSO_EIRA_LOAD_RDF_FILE)
        p.persist()
