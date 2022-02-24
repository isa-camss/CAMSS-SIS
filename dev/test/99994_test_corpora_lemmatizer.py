import unittest
from com.nttdata.dgi.io.textify.textify import Textifier
import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
import os
import json
import ast


class LemmatizerTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(LemmatizerTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_file_to_string(self):
        file_path = 'C:/SEMBUdev/Github/CAMSS/corpora/txt/1dc1db4eeeab4cd2bc39299151f57e46.pdf.txt'
        string_file = io.file_to_str(file_path)
        print(string_file)
        return string_file


    def test_002_lemmatize_file(self):
        jsonl_path = 'C:/SEMBUdev/Github/CAMSS/CAMSS-SIS/dev/arti/json/corpora_metadata.jsonl'
        # resource_dict = io.read_jsonl(jsonl_path)

        with open(jsonl_path, 'rb') as file:
            lines = file.readlines()
            for line in lines:
                line_value = line.strip()
                dict_str = line_value.decode("UTF-8")
                resource_dict = ast.literal_eval(dict_str)
                for part in resource_dict['parts']:
                    part_id = part['id']
                    textified_resource_file = '../' + ctt.TEXTIFICATION_DIR + '/' + part_id + '.' + 'txt'
                    string_file = io.file_to_str(textified_resource_file)

                print(string_file)
        return resource_dict
