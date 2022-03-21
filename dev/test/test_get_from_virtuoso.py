import sys
import unittest
from SPARQLWrapper import SPARQLWrapper, JSON
import cfg.ctt as ctt
import cfg.queries as query
import json


class GetFromVirtuosoTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GetFromVirtuosoTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_search_lemmatized_concepts_in_virtuoso(self):
        # query
        legal_query = query.EIRA_LEGAL_ABBS_QUERY

        # Establish connection to virtuoso
        virtuoso_connection = SPARQLWrapper("http://localhost:8890/sparql")

        # Execute query
        virtuoso_connection.setQuery(legal_query)

        # Format results
        virtuoso_connection.setReturnFormat(JSON)
        qres = virtuoso_connection.query().convert()

        return qres

    def tearDown(self) -> None:
        return


if __name__ == '__main__':
    unittest.main()
