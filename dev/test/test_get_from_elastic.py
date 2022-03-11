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
import cfg.ctt as ctt
import pandas as pd
import json


class GetFromElasticTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GetFromElasticTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_get_from_term(self):
        # es = Elasticsearch("http://localhost:9200")
        # terms_list = ["public policy", "europe", "binding instrument", "legal act"]
        # elastic_index = "eurlex-docs-20220308"

        for term in ctt.SEARCH_DETAILS.get('eira_concepts'):
            # query = ctt.SEARCH_DETAILS['elastic_query']
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"terms.lemma": f"""{term}"""}}
                        ]
                    }
                }
            }
            terms_match = {'term': term,
                           'resources_matches': []
                           }

            rel = scan(client=ctt.SEARCH_DETAILS.get('client_host'),
                       query=query,
                       scroll='1m',
                       index=ctt.SEARCH_DETAILS.get('elastic_index'),
                       raise_on_error=True,
                       preserve_order=False,
                       clear_scroll=True)
            result = list(rel)
            for hit in result:
                terms_match['resources_matches'].append(hit['_source']['part_id'])

            with open('../arti/json/match_terms.jsonl', 'a+') as outfile:
                json.dump(terms_match, outfile)
                outfile.write('\n')
                outfile.close()

        # df = pd.DataFrame(term_match)
        return self

    def tearDown(self) -> None:
        return
