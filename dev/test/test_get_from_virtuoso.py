import sys
import unittest
from SPARQLWrapper import SPARQLWrapper, JSON
import cfg.ctt as ctt
import cfg.queries as query
import cfg.crud as crud
import json
import com.nttdata.dgi.util.io as io


class GetFromVirtuosoTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GetFromVirtuosoTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_search_lemmatized_concepts_in_virtuoso(self):
        legal_query = query.EIRA_LEGAL_ABBS_QUERY
        virtuoso_connection = SPARQLWrapper(crud.VIRTUOSO_EIRA_LOAD_RDF_FILE.get('query_endpoint'))
        virtuoso_connection.setQuery(legal_query)
        virtuoso_connection.setReturnFormat(JSON)
        virtuoso_response = virtuoso_connection.query().convert()
        results_format = virtuoso_response['results']['bindings']

        for
        for item_list in results_format:
            abb_value = item_list.get('Lemma').get('value')

            # Create jsonl with lemmatized terms
            date_time_now = io.now()
            date_time_now_str = io.datetime_to_string(date_time_now)
            terms_document_dict = {
                "timestamp": date_time_now_str,
                "lemma_id": io.hash(abb_value),
                "lemma": abb_value
            }
            with open(ctt.EIRA_CONCEPTS_DETAILS.get('lemmatized_jsonl'), 'a+') as outfile:
                json.dump(terms_document_dict, outfile)
                outfile.write('\n')
                outfile.close()

            terms_document_dict['timestamp'] = date_time_now
            str_date = io.now().strftime("%Y%m%d")
            elastic_terms_index = self.lemmatization_details.get(
                'elastic_lemmas_index') + f"-{str_date}"

        return self

    def test_001_dynamic_query(self):
        for view in ctt.EIRA_VIEWS_LIST:
            print(view)
        return self


    def tearDown(self) -> None:
        return self


if __name__ == '__main__':
    unittest.main()
