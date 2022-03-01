import unittest

import elasticsearch

import cfg.crud as crud
from datetime import datetime
from com.nttdata.dgi.crud.PersistenceFactory import PersistenceFactory
from com.nttdata.dgi.crud.Persistor import Persistor
from com.nttdata.dgi.crud.PersistorType import PersistorType


class ElasticSearchTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ElasticSearchTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_0001_no_persist_arguments(self):
        # Should fail, since no parameters are provided
        p: Persistor = PersistenceFactory().new(crud.ELASTICSEARCH_DETAILS, PersistorType.ELASTIC)
        p.persist()
        return

    def test_0002_persist_in_named_index_no_id(self):
        """
        Persists in ElasticPersistor a document in a given index.
        :return: self
        """
        p: Persistor = PersistenceFactory().new(crud.ELASTICSEARCH_DETAILS, PersistorType.ELASTIC)
        '''
        No document id is provided, therefore Elasticsearch has to provide its own.
        '''
        doc1 = {
            'author': 'Kimchy',
            'text': 'Kimchy cool.',
            'timestamp': datetime.now(),
        }
        '''
        If a doc is passed in the args, then the default index is taken from the persistor details. 
        If no default index  -> Exception. The id of the doc is auto-generated by Elasticsearch.  
        '''
        # p.persist(doc1)
        '''
        Index and document passed as argument to the method. The id is auto-generated by Elastic
        '''
        # p.persist(index="test3", document=doc1)
        '''
        Document id is provided inside the document. '''
        doc2 = {
            'id': '1',  # Used to identify the document in Elasticsearch
            'author': 'Ford',
            'text': 'Ford is cool.',
            'timestamp': datetime.now(),
        }
        # p.persist(index="test3", document=doc2)

        '''
        Document id is provided both inside the document and the method:
        In this case, the id for Elastic is the one in the method, and 
        the id inside the document is kept unaltered.'''
        doc2 = {
            'id': 'ABCDE',  # Used to identify the document in Elasticsearch
            'author': 'Pontiac',
            'text': 'Pontiac is cool.',
            'timestamp': datetime.now(),
        }
        p.persist(index="test3", content=doc2, id=1024)
        return

    def test_0002_drop(self):
        p: Persistor = PersistenceFactory().new(crud.ELASTICSEARCH_DETAILS, PersistorType.ELASTIC)
        '''
        Drop a document from default index, no need to specify that it's a document.
        '''
        try:
            p.drop(1)   # The id of the document can be an integer or a str
        except elasticsearch.NotFoundError:
            print("Document not found.")
        '''
        Or naming the argument
        '''
        try:
            p.drop(id=1)   # The id of the document can be an integer or a str
        except elasticsearch.NotFoundError:
            print("Document not found.")

        '''
        Drop a document of an index
        '''
        try:
            p.drop(id=2, index='sembu')
        except elasticsearch.NotFoundError:
            print("Document not found")
        '''
        Drop an index
        '''
        try:
            p.drop(index="sembu")
        except elasticsearch.NotFoundError:
            print("Index not found.")

        return

    def tearDown(self) -> None:
        return


if __name__ == '__main__':
    unittest.main()
