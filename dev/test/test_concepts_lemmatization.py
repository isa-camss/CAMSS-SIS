import sys
import unittest
import cfg.ctt as ctt
import cfg.crud as crud
import com.nttdata.dgi.util.io as io
import requests
import json
from com.nttdata.dgi.persistence.persistence_factory import PersistenceFactory
from com.nttdata.dgi.persistence.persistor_type import PersistorType


class EmptyTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(EmptyTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_lemmatize_concept_list(self):

        self.persistor = PersistenceFactory().new(persistor_type=PersistorType.ELASTIC,
                                                  persistor_details=crud.ELASTICSEARCH_DETAILS)
        terms_list = ctt.EIRA_ABBS
        terms_lang = ctt.EIRA_CONCEPTS_DETAILS.get('rsc_lang')
        date_time_now = io.now()
        date_time_now_str = io.datetime_to_string(date_time_now)
        for term in terms_list:
            json_terms = {'phrase': term, 'lang': terms_lang}
            lemmatizer_response = requests.post(url=ctt.LEMMATIZATION_DETAILS.get('endpoint'), json=json_terms)
            lemmatized_document_dict = {
                "timestamp": date_time_now,
                "term_id": io.hash(term),
                "term": term,
                "lemma": json.loads(lemmatizer_response.content)['unaccented-minus-stopwords']
            }

            self.persistor.persist(index=crud.ELASTICSEARCH_TERMS_LEMMATIZED_INDEX,
                                   content=lemmatized_document_dict)

        return self

    def tearDown(self) -> None:
        return


if __name__ == '__main__':
    unittest.main()
