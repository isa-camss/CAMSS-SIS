import sys
import unittest
from SPARQLWrapper import SPARQLWrapper, JSON
import cfg.ctt as ctt
import cfg.queries as queries
import cfg.crud as crud
import json
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory, PersistorType


class GetFromVirtuosoTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GetFromVirtuosoTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_search_lemmatized_concepts_in_virtuoso(self):
        persistor = PersistenceFactory().new(persistor_type=PersistorType.VIRTUOSO,
                                             persistor_details=crud.VIRTUOSO_EIRA_LOAD_RDF_FILE)
        for concept in ctt.EIRA_CONCEPTS_DETAILS.get('vocabulary_details'):
            view_type = concept.get('view')
            skos_collection = concept.get('skos_collection')
            query_view_concepts = ctt.EIRA_CONCEPTS_DETAILS.get('query_terms') % skos_collection

            virtuoso_response = persistor.search_vituoso(query=query_view_concepts)
            results_format = virtuoso_response['results']['bindings']

            for item_list in results_format:
                abb_value = item_list.get('Lemma').get('value')

                # Create jsonl with lemmatized terms
                date_time_now = io.now()
                date_time_now_str = io.datetime_to_string(date_time_now)
                terms_document_dict = {
                    "timestamp": date_time_now_str,
                    "eira_view": view_type + "" + "view",
                    "lemma_id": io.hash(abb_value),
                    "lemma": abb_value
                }
                with open(ctt.EIRA_CONCEPTS_DETAILS.get('lemmatized_jsonl'), 'a+') as outfile:
                    json.dump(terms_document_dict, outfile)
                    outfile.write('\n')
                    outfile.close()

                terms_document_dict['timestamp'] = date_time_now
                str_date = io.now().strftime("%Y%m%d")
                elastic_eira_terms_index = ctt.EIRA_CONCEPTS_DETAILS.get('elastic_terms_index') + f"-{view_type}-view-{str_date}"

        return self

    def test_001_dynamic_query(self):
        for view in ctt.EIRA_CONCEPTS_DETAILS.get('vocabulary_details'):
            view_type = view.get('view')
            skos_collection = view.get('skos_collection')
            query = ctt.EIRA_CONCEPTS_DETAILS.get('query_terms') % skos_collection
            elastic_terms_index = ctt.EIRA_CONCEPTS_DETAILS.get('elastic_terms_index') + "-" + view_type + "-view"
        return self

    def tearDown(self) -> None:
        return self


if __name__ == '__main__':
    unittest.main()
