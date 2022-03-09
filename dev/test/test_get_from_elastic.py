#######################################################
# test_get_from_elastic.py
# Tests CRUD operations via the Persistence Service
# Created on:      25-feb-2022 13:26:59
# Author: SEMBU Team - NTTData Barcelona
#######################################################
import unittest
import com.nttdata.dgi.util.io as io
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd


class GetFromElasticTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GetFromElasticTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_get_from_term(self):
        es = Elasticsearch("http://localhost:9200")
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"terms.lemma": "europe"}}
                    ]
                }
            }
        }
        elastic_index = "eurlex-docs-20220308"
        rel = scan(client=es,
                   query=query,
                   scroll='1m',
                   index=elastic_index,
                   raise_on_error=True,
                   preserve_order=False,
                   clear_scroll=True)
        result = list(rel)
        temp = []
        for hit in result:
            temp.append(hit['_source']['rsc_id'])

        # df = pd.DataFrame(temp)
        return temp


    def tearDown(self) -> None:
        return
