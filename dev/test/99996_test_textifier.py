import unittest
from com.nttdata.dgi.io.textify.textify import Textifier
import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
import os
import json
import ast


class TestifierTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestifierTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_get_content(self):
        text = io.get_content_from_file('C:/SEMBUdev/Github/corpora/pdf/3a99b8f82a0728f6cc2d492c1f255ee9.pdf', True)
        print(text)

    def test_002_textify_folder(self):
        args: dict = ctt.TEXTIFICATION_CORPORA_DETAILS

        textifier = Textifier()

        for dir_name in os.listdir(ctt.TEXTIFICATION_CORPORA_DETAILS.get('corpus_dir')):
            if os.path.isdir(ctt.TEXTIFICATION_CORPORA_DETAILS.get('corpus_dir') + '/' + dir_name):
                if dir_name in ctt.TEXTIFICATION_CORPORA_DETAILS.get('exclude_extensions_type'):
                    pass
                else:
                    textifier.textify_folder()

        return

    def test_003_textify_file(self):
        # new_json = io.read_jsonl('C:/SEMBUdev/Github/CAMSS/CAMSS-SIS/dev/arti/json/corpora_metadata.jsonl')
        jsonl_path = 'C:/SEMBUdev/Github/CAMSS/CAMSS-SIS/dev/arti/json/corpora_metadata.jsonl'
        with open(jsonl_path, 'rb') as file:
            lines = file.readlines()
            for line in lines:
                line_value = line.strip()
                dict_str = line_value.decode("UTF-8")
                resource_dict = ast.literal_eval(dict_str)
                for part in resource_dict['parts']:
                    part_type = part['part_type']
                    document_type = part['reference_link']['document_type']
                    if part_type == 3:
                        io.log("Resource obtained")
                        if not document_type in ctt.CORPORA_EXCLUDE_TEXTIFICATION_DOCUMENT_TYPE:
                            resource_file = ctt.CORPORA_DIR + '/' + document_type + '/' + part['id'] + '.' + document_type

                    print(resource_file, document_type, part_type, part)
                # print(resource_dict['parts'])
        return resource_dict
