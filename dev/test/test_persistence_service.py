#######################################################
# test_persistence_service.py
# Tests CRUD operations via the Persistence Service
# Created on:      25-feb-2022 13:26:59
# Author: SEMBU Team - NTTData Barcelona
#######################################################
import unittest
import requests

PERSISTENCE_HOST = 'http://localhost:5300/persistence'
ELASTIC_HOST = 'http://localhost:9200'
PERSIST_ENDPOINT = '/persist'
TEST_FILE_PERSISTOR = './arti/via_service.txt'
TEST_ELASTIC_INDEX = 'books'


class PersistenceServiceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PersistenceServiceTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_0001_write_file(self):
        persistor_endpoint = PERSISTENCE_HOST + PERSIST_ENDPOINT
        json_in = {
            'connection': {'store': 'FILE', 'file': TEST_FILE_PERSISTOR, 'mode': 'file'},
            'payload': {'content': 'This is the text to save in a file. \n The file has several lines.\n'}}
        res = requests.post(url=persistor_endpoint, json=json_in)
        assert res.ok
        return

    def test_0002_load_elastic_document(self):
        persistor_endpoint = PERSISTENCE_HOST + PERSIST_ENDPOINT
        doc = {'id': 1025, 'book': 'Dom Qitxot', 'author': 'Miguel Cervantes de Saavedra'}
        json_in = {
            'connection': {'store': 'ELASTIC', 'host': ELASTIC_HOST, 'user': '', 'password': ''},
            'payload': {'content': doc, 'index': TEST_ELASTIC_INDEX}}
        res = requests.post(url=persistor_endpoint, json=json_in)
        assert res.ok
        return

if __name__ == '__main__':
    unittest.main()
