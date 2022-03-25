import unittest
import cfg.crud as crud
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.search.search import Search
from elasticsearch import Elasticsearch
from com.nttdata.dgi.persistence.persistor_type import PersistorType
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory


class EmptyTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(EmptyTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_ask_elastic(self):
        ask = Search()
        es = Elasticsearch("http://localhost:9200")
        rsc_id_3 = "edc2e7b1598cfd853ec86b8399c51200"
        elastic_index = "camss-eira-terms*"
        query = {"query": {"term": {"lemma_id.keyword": rsc_id_3}}}
        # result = es.count(index=elastic_index, body=query)['count']
        # print(result)
        persistor = PersistenceFactory().new(persistor_type=PersistorType.ELASTIC,
                                             persistor_details=crud.ELASTICSEARCH_DETAILS)
        bool_exist = persistor.ask(index=elastic_index, query=query)
        print(bool_exist)

        return

    def tearDown(self) -> None:
        return


if __name__ == '__main__':
    unittest.main()
