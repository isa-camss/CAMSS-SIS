import os
import json
from bs4 import BeautifulSoup as bs
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.io.down.http_downloader import HTTPDownloader
from org.camss.io.down.corpus_downloader import CorpusDownloader
from com.nttdata.dgi.io.textify.textify import Textifier


class CorporaManager:
    download_corpora_details: dict
    textification_corpora_details: dict

    def __init__(self, download_details: dict = None, textification_details: dict = None):
        self.download_corpora_details = download_details
        self.textification_corpora_details = textification_details
        return

    def prepare_corpus_folders(self):
        io.drop_file(self.download_corpora_details.get('corpora_metadata_file'))
        os.makedirs(self.download_corpora_details.get('corpora_dir'), exist_ok=True)
        os.makedirs(self.textification_corpora_details.get('textification_dir'), exist_ok=True)
        with open(self.download_corpora_details.get('corpora_metadata_file'), 'w+') as outfile:
            outfile.close()
        return self

    def download_corpus(self):
        num_documents_download = 0
        initial_page_number = self.download_corpora_details.get('eurlex_details').get('initial_page_number')
        initial_page_size = self.download_corpora_details.get('eurlex_details').get('initial_page_size')
        http_downloader = HTTPDownloader()
        request_downloader = CorpusDownloader()

        while num_documents_download < self.download_corpora_details.get('max_documents'):
            # Create a dynamic query
            query = self.download_corpora_details.get('eurlex_details').get('body') % (
                initial_page_number, initial_page_size)

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
                result_documents = {'reference': reference,
                                    'reference_hash': reference_hash,
                                    'reference_links': []}

                # Access to the links for each result
                for document in result.find_all('document_link'):
                    document_type = document['type'].lower()

                    #
                    if document_type in self.download_corpora_details.get('download_types'):
                        textification_hash = io.hash(reference + document_type)
                        save_document_path = os.path.join(self.download_corpora_details.get('corpora_dir'),
                                                          document_type,
                                                          textification_hash + '.' + document_type)
                        io.make_file_dirs(save_document_path)
                        document_link = document.string
                        document_dict = {textification_hash: {'type': document_type, 'link': document_link}}
                        result_documents['reference_links'].append(document_dict)
                        http_downloader(document_link, save_document_path).download()

                with open(self.download_corpora_details.get('corpora_metadata_file'), 'a+') as outfile:
                    json.dump(result_documents, outfile)
                    outfile.write('\n')
                    outfile.close()

                num_documents_download += 1
            initial_page_number += 1

        return self

    def textify_corpus(self):
        textifier = Textifier()

        # loop for corpora folder and check if textified folder is ctt.TEXTIFICATION_FOLDER
        for dir_name in os.listdir(self.textification_corpora_details.get('corpus_dir')):

            # if os.path.isdir(self.textification_corpora_details.get('corpus_dir') + '/' + dir_name):
            if os.path.isdir(self.textification_corpora_details.get('corpus_dir') + '/' + dir_name):
                if dir_name in self.textification_corpora_details.get('exclude_extensions_type'):
                    pass
                else:
                    textifier(self.textification_corpora_details.get('corpus_dir'),
                              self.textification_corpora_details.get('textification_dir')).textify()

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
