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
        terms_list = ["public policy", "europe", "binding instrument", "legal act"]
        elastic_index = "eurlex-docs-20220308"


        for term in terms_list:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"terms.lemma": f"""{term}"""}}
                        ]
                    }
                }
            }
            term_match = {'term': term,
                          'resources_matches': []
                          }

            rel = scan(client=es,
                       query=query,
                       scroll='1m',
                       index=elastic_index,
                       raise_on_error=True,
                       preserve_order=False,
                       clear_scroll=True)
            result = list(rel)
            for hit in result:
                term_match['resources_matches'].append(hit['_source']['rsc_id'])

        with open(self.download_details.get('resource_metadata_file'), 'a+') as outfile:
            json.dump(result_documents, outfile)
            outfile.write('\n')
            outfile.close()

        # df = pd.DataFrame(term_match)
        return term_match

    def tearDown(self) -> None:
        return
