import os
import json
import ast
from bs4 import BeautifulSoup as bs
from enum import IntEnum
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.io.down.http_downloader import HTTPDownloader
from org.camss.io.down.corpus_downloader import CorpusDownloader
from com.nttdata.dgi.io.textify.textify import Textifier


class DocumentPartType(IntEnum):
    TITLE = 1
    ABSTRACT = 2
    BODY = 3
    KEYWORDS = 4


class CorporaManager:
    download_corpora_details: dict
    textification_corpora_details: dict

    def __init__(self, download_details: dict = None, textification_details: dict = None):
        self.download_corpora_details = download_details
        self.textification_corpora_details = textification_details
        return

    def prepare_corpus_folders(self):
        os.makedirs(self.download_corpora_details.get('json_dir'), exist_ok=True)
        io.drop_file(self.download_corpora_details.get('corpora_metadata_file'))
        os.makedirs(self.download_corpora_details.get('corpora_dir'), exist_ok=True)
        os.makedirs(self.textification_corpora_details.get('textification_dir'), exist_ok=True)
        with open(self.download_corpora_details.get('corpora_metadata_file'), 'w+') as outfile:
            outfile.close()
        return self

    def download_corpus(self):
        t0 = io.log("Starting download corpus")
        num_documents_download = 0
        initial_page_number = self.download_corpora_details.get('eurlex_details').get('initial_page_number')
        initial_page_size = self.download_corpora_details.get('eurlex_details').get('initial_page_size')
        max_documents_download = self.download_corpora_details.get('max_documents')
        http_downloader = HTTPDownloader()
        request_downloader = CorpusDownloader()
        io.log(f"Starting with page number '{initial_page_number}', "
               f"page size: '{initial_page_size}' and maximum number of "
               f"documents to download: '{max_documents_download}'")
        while num_documents_download < max_documents_download:
            io.log(f"Number of documents downloaded: {num_documents_download}/{max_documents_download}")
            # Create a dynamic query

            query = self.download_corpora_details.get('eurlex_details').get('body') % (initial_page_number,
                                                                                       initial_page_size)


            # Request to the website
            eurlex_document_request = request_downloader(self.download_corpora_details.get('eurlex_details').get('url'),
                                                         query,
                                                         self.download_corpora_details.get('eurlex_details').get(
                                                             'headers')).download()
            if not eurlex_document_request.response.ok:
                raise Exception(f"Query to EURLex returned {eurlex_document_request.response.status_code}. "
                                f"Content: {eurlex_document_request.response.content}")

            # Parse the content response
            soup = bs(eurlex_document_request.response.content, 'xml')

            # Access to the result tag
            request_result = soup.find_all('result')

            # Extract and generate the identification for each object result
            for result in request_result:
                reference = result.find('reference').text
                reference_hash = io.hash(reference)
                io.log(f"-- {num_documents_download}/{max_documents_download} Processing document "
                       f"reference: {reference} --")
                result_documents = {'reference': reference,
                                    'reference_hash': reference_hash,
                                    'parts': []}

                # Access to the links for each result
                for document in result.find_all('document_link'):
                    document_type = document['type'].lower()


                    # Only consider the files with corresponding document type (download_types)
                    if document_type == self.download_corpora_details.get('download_types'):
                        document_part_str = str(DocumentPartType.BODY)
                        part_hash = io.hash(reference + document_part_str)
                        save_document_path = os.path.join(self.download_corpora_details.get('corpora_dir'),
                                                          document_type,
                                                          part_hash + '.' + document_type)
                        io.make_file_dirs(save_document_path)
                        document_link = document.string
                        document_dict = {'id': part_hash,
                                         'part_type': DocumentPartType.BODY,
                                         'reference_link': {'document_type': document_type,
                                                            'document_link': document_link}}

                        result_documents['parts'].append(document_dict)
                        http_downloader(document_link, save_document_path).download()
                        io.log(f"---- Processed document part: {document_part_str} with id: {part_hash} ----")

                with open(self.download_corpora_details.get('corpora_metadata_file'), 'a+') as outfile:
                    json.dump(result_documents, outfile)
                    outfile.write('\n')
                    outfile.close()

                num_documents_download += 1
            initial_page_number += 1
        io.log(f"Finished corpus download in: {io.now()-t0}")
        return self

    def textify_corpus(self):
        textifier = Textifier()

        with open(self.download_corpora_details.get('corpora_metadata_file'), 'rb') as file:
            lines = file.readlines()
            # Read each jsonl's line to get the 'part'
            io.log(f"--- Starting with Corpora Textification----")
            for line in lines:
                line_value = line.strip()
                dict_str = line_value.decode("UTF-8")
                resource_dict = ast.literal_eval(dict_str)

                # iterate each part of the parts (document)
                for part in resource_dict['parts']:
                    part_type = part['part_type']
                    document_type = part['reference_link']['document_type']

                    if part_type == DocumentPartType.BODY:
                        io.log(f"--Processing document reference: {resource_dict['reference']}----")

                        #  Textify Corpora
                        if not document_type in self.textification_corpora_details.get('exclude_extensions_type'):
                            resource_file = self.textification_corpora_details.get('corpus_dir') + '/' + document_type + '/' + part['id'] + '.' + document_type
                            textifier(resources_dir=None, resource_file=resource_file,
                                      target_dir=self.textification_corpora_details.get('textification_dir')).textify_file()
                            io.log(f"---- The document with id: {part['id']} was successfullt textified ----")

        io.log(f"Finished Copora Textification")
        return self

    def lemmatize_resource(self):
        # loop jsonl to read line by line
        # Read line metadata jsonl
        # Access to the id_part
        # Join to the txt path with the id_part (to obtain the path)
        # Read the txt of the part (with open...)
        # Call to Lemmatize microservice
        # ---------PERSIST---------
        # Prepare response to be persist
        # ¿Se puede agregar contenido nuevo a una linea de jsonl que ya existe?,
        # si se puede actualizar el diccionario y volver a escribirlo en la misma línea
        # Invoque the Persistor (further)
        return self
