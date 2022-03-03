import os
import json
import ast
from bs4 import BeautifulSoup as bs
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.io.down.http_downloader import HTTPDownloader
from org.camss.io.down.corpus_downloader import CorpusDownloader
from com.nttdata.dgi.io.textify.textify import Textifier
from com.nttdata.dgi.rsc.document_part_type import DocumentPartType
from com.nttdata.dgi.rsc.kw import KeywordWorker


class CorporaManager:
    download_details: dict
    textification_details: dict
    lemmatization_details: dict

    def __init__(self, download_details: dict = None, textification_details: dict = None, lemmatization_details: dict = None):
        self.download_details = download_details
        self.textification_details = textification_details
        self.lemmatization_details = lemmatization_details
        return

    def prepare_corpus_folders(self):
        os.makedirs(self.download_details.get('json_dir'), exist_ok=True)
        io.drop_file(self.download_details.get('resource_metadata_file'))
        io.drop_file(self.lemmatization_details.get('lemmatized_jsonl'))
        os.makedirs(self.download_details.get('corpora_dir'), exist_ok=True)
        os.makedirs(self.textification_details.get('textification_dir'), exist_ok=True)
        with open(self.download_details.get('resource_metadata_file'), 'w+') as outfile:
            outfile.close()
        with open(self.lemmatization_details.get('lemmatized_jsonl'), 'w+') as outfile:
            outfile.close()
        return self

    def download_corpus(self):
        t0 = io.log("Starting download corpus")
        num_documents_download = 0
        initial_page_number = self.download_details.get('eurlex_details').get('initial_page_number')
        initial_page_size = self.download_details.get('eurlex_details').get('initial_page_size')
        max_documents_download = self.download_details.get('max_documents')
        http_downloader = HTTPDownloader()
        request_downloader = CorpusDownloader()
        io.log(f"Starting with page number '{initial_page_number}', "
               f"page size: '{initial_page_size}' and maximum number of "
               f"documents to download: '{max_documents_download}'")
        while num_documents_download < max_documents_download:
            io.log(f"Number of documents downloaded: {num_documents_download}/{max_documents_download}")
            # Create a dynamic query

            query = self.download_details.get('eurlex_details').get('body') % (initial_page_number,
                                                                                       initial_page_size)

            # Request to the website
            eurlex_document_request = request_downloader(self.download_details.get('eurlex_details').get('url'),
                                                         query,
                                                         self.download_details.get('eurlex_details').get(
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
                                    'lang': self.download_details.get('default_lang'),
                                    'parts': []}

                # Access to the links for each result
                for document in result.find_all('document_link'):
                    document_type = document['type'].lower()

                    # Only consider the files with corresponding document type (download_types)
                    if document_type == self.download_details.get('download_types'):
                        save_document_path = os.path.join(self.download_details.get('corpora_dir'),
                                                          document_type,
                                                          reference_hash + '.' + document_type)
                        io.make_file_dirs(save_document_path)
                        document_link = document.string
                        document_part = DocumentPartType.BODY.name.lower()
                        try:
                            http_downloader(document_link, save_document_path).download()
                            content_hash = io.hash(io.base64_(save_document_path))
                            document_part_hash = io.hash(document_part)
                            # part_id: int16(md5(refrence) + md5(b64 contingut) + md5(part_type))
                            part_hash_int16 = io.gen_entry_id((reference_hash, content_hash, document_part_hash))
                            save_txt_path = os.path.join(self.download_details.get('textification_dir'),
                                                         document_part,
                                                         str(part_hash_int16) + '.txt')
                            io.make_file_dirs(save_txt_path)
                            document_dict = {'id': part_hash_int16,
                                             'part_type': document_part,
                                             'reference_link': {'document_type': document_type,
                                                                'document_path': save_document_path,
                                                                'txt_path': save_txt_path,
                                                                'document_link': document_link
                                                                }}

                            result_documents['parts'].append(document_dict)
                            io.log(f"---- Processed document part: {document_part} with id: {part_hash_int16} "
                                   f"from reference: {reference} ----")
                        except Exception as ex:
                            io.log(f"Error downloading document reference: {reference} with link: {document_link}. "
                                   f"Exception: {ex}", "w")

                with open(self.download_details.get('resource_metadata_file'), 'a+') as outfile:
                    json.dump(result_documents, outfile)
                    outfile.write('\n')
                    outfile.close()

                num_documents_download += 1
            initial_page_number += 1
        return self

    def textify_corpus(self):
        textifier = Textifier()

        with open(self.download_details.get('resource_metadata_file'), 'rb') as file:
            lines = file.readlines()
            # Read each jsonl's line to get the 'part'
            io.log(f"--- Starting with Corpora Textification----")
            for line in lines:
                line_value = line.strip()
                dict_str = line_value.decode("UTF-8")
                resource_dict = ast.literal_eval(dict_str)

                # iterate each part of the parts (document)
                for part in resource_dict['parts']:
                    part_type = part.get('part_type')
                    document_type = part.get('reference_link').get('document_type')
                    source_path = part.get('reference_link').get('document_path')
                    target_path = part.get('reference_link').get('txt_path')
                    if part_type == DocumentPartType.BODY.name.lower():
                        io.log(f"--Processing document with reference: {resource_dict.get('reference')} and part "
                               f"document id: {part.get('id')}----")

                        #  Textify Corpora
                        if not document_type in self.textification_details.get('exclude_extensions_type'):
                            textifier.textify_file(resource_file=source_path, target_file=target_path)
                            io.log(f"---- The document with id: {part.get('id')} was successfully textified ----")
        return self

    def lemmatize_corpora(self, corpora_lemmatization_details: dict):
        io.log(f"---- Starting with Corpora Lemmatization ----")
        self.lemmatization_details = corpora_lemmatization_details

        with open(self.lemmatization_details.get('metadata_file'), 'rb') as file:
            lines = file.readlines()
            num_lines = len(lines)
            current_line = 0
            for line in lines:
                t0 = io.log(f"--- Processing line {current_line}/{num_lines} ---")
                line_value = line.strip()
                dict_str = line_value.decode("UTF-8")
                resource_dict = ast.literal_eval(dict_str)
                rsc_id = resource_dict.get('reference_hash')
                rsc_lang = resource_dict.get('lang')
                for part in resource_dict['parts']:
                    t1 = io.log(f"-- Processing resource id: {rsc_id}, part: {resource_dict.get('part_type')} "
                                f"with id: {resource_dict.get('part_id')} --")
                    part_id = part.get('id')
                    part_type = part.get('part_type')
                    textified_resource_file = part.get('reference_link').get('txt_path')
                    content_file = io.file_to_str(textified_resource_file)

                    # exists, entry_id = self.exists(rsc_id, part_id, part_type)
                    exists, entry_id = False, part_id
                    if not exists:
                        '''
                        Analyse the content and keep the tuples (lemma, term, freq). 
                        *** LEMMATIZATION OCCURS HERE ***
                        '''

                        bot = KeywordWorker(self.lemmatization_details).extract(content_file,
                                                                                rsc_part=part_type,
                                                                                rsc_lang=rsc_lang).bot
                        # Change the structure of bot json : "terms": [
                        #                               {
                        #                                   "lem_id": "ee5b02730f46da5da2693105aa308529",
                        #                                   "lemma": "member",
                        #                                   "term": "the member",
                        #                                   "freq": 2
                        #                               }
                        # Add all metadata details see json example in test_elastic_persistence
                        corpora_lemmatized_dict = {'id': part_id,
                                                   'terms': bot
                                                   }
                        with open(self.lemmatization_details.get('lemmatized_jsonl'), 'a+') as outfile:
                            json.dump(corpora_lemmatized_dict, outfile)
                            outfile.write('\n')
                            outfile.close()

                        io.log(f"-- The part with id: {part.get('id')} was successfully lemmatized in "
                               f"{io.now() - t1} --")
                    else:
                        io.log(f"-- Part id: {part_id} already exists in database, lemmatization skipped in "
                               f"{io.now() - t1} --", level="i")

                io.log(f"--- The resource id: {rsc_id} was successfully lemmatized in {io.now() - t0} ---")
                current_line += 1
        return self
