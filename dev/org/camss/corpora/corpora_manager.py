from bs4 import BeautifulSoup as bs
import os
from com.nttdata.dgi.io.down.http_downloader import HTTPDownloader
from org.camss.io.down.corpus_downloader import CorpusDownloader
import json
import com.nttdata.dgi.util.io as io


class CorporaManager:
    corpora_details: dict

    def __init__(self, corpora_details: dict = None):
        self.corpora_details = corpora_details
        return

    def prepare_corpus_folders(self):
        io.drop_file(self.corpora_details.get('corpora_metadata_file'))
        os.makedirs(self.corpora_details.get('corpora_dir'), exist_ok=True)
        with open(self.corpora_details.get('corpora_metadata_file'), 'w+') as outfile:
            outfile.close()
        return self

    def download_corpus(self):
        num_documents_download = 0
        initial_page_number = self.corpora_details.get('eurlex_details').get('initial_page_number')
        initial_page_size = self.corpora_details.get('eurlex_details').get('initial_page_size')
        http_downloader = HTTPDownloader()
        request_downloader = CorpusDownloader()

        while num_documents_download < self.corpora_details.get('max_documents'):
            query = self.corpora_details.get('eurlex_details').get('body') % (initial_page_number, initial_page_size)

            # request to EURLEX API
            eurlex_document_request = request_downloader(self.corpora_details.get('eurlex_details').get('url'),
                                                       query,
                                                       self.corpora_details.get('eurlex_details').get('headers')).download()
            if not eurlex_document_request.response.ok:
                raise Exception(f"Query to EURLex returned {eurlex_document_request.response.status_code}. "
                                f"Content: {eurlex_document_request.response.content}")

            # Parse the EURLEX query response
            soup = bs(eurlex_document_request.response.content, 'xml')

            # Extract reference and url of the resource
            request_result = soup.find_all('result')

            for result in request_result:
                reference = result.find('reference').text
                reference_hash = io.hash(reference)
                result_documents = {'reference': reference,
                                    'reference_hash': reference_hash,
                                    'reference_links': []}

                # Extraction all interesting document links by resources
                for document in result.find_all('document_link'):
                    document_type = document['type'].lower()
                    if document_type in self.corpora_details.get('download_types'):
                        textification_hash = io.hash(reference+document_type)
                        save_document_path = os.path.join(self.corpora_details.get('corpora_dir'), document_type,
                                                          textification_hash + '.' + document_type)
                        io.make_file_dirs(save_document_path)
                        document_link = document.string
                        document_dict = {textification_hash: {'type': document_type, 'link': document_link}}
                        result_documents['reference_links'].append(document_dict)
                        http_downloader(document_link, save_document_path).download()

                with open(self.corpora_details.get('corpora_metadata_file'), 'a+') as outfile:
                    json.dump(result_documents, outfile)
                    outfile.write('\n')
                    outfile.close()

                num_documents_download += 1
            initial_page_number += 1

        return self

    def textify_corpus(self):
        # loop for corpora folder and check if textified folder is ctt.TEXTIFICATION_FOLDER
            # loop for document
                # get name of file
                # textification with tika
                # save .txt file with teh same name in a new txt folder

        return self
