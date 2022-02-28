import json
import com.everis.dgi.util.io as io
from com.everis.dgi.his.historyinterface import HistoryInterface
from com.everis.dgi.nlp.summarization import summarize
from com.everis.dgi.rsc.kw import KeywordWorker
from com.everis.dgi.rdf.gdb_interface import GraphDBInterface
from com.everis.dgi.rsc.corpusparserinterface import CorpusParserInterface


class HistoryFactory(HistoryInterface, GraphDBInterface, CorpusParserInterface):

    def __init__(self,
                 connection_details: dict,
                 crud_details: dict,
                 operational_details: dict):
        super(HistoryFactory, self).__init__()
        self.connection_details = connection_details
        self.crud_details = crud_details
        self.operational_details = operational_details
        self.report = {}
        self.code = 200
        self.conn = None
        self.drop_graph = False
        self.drop_nq = False

    def _add_history_entry_(self, entry: tuple, json_l_s: str):
        """
        Inserts a record to the History Log. BEWARE THAT: the connection and transaction enclosing needs to be
        done outside this method. Use the get_connection() method to control the transaction.

        Also, take into account that the json_l_s is a JSON object transformed to string, it's "" have been
        transformed into "''". When retrieving back the JSON text you will have to unquote back to ""!!!!

        Example:
            
            rl = ResourceLog(connection_details, crud_details).connect().begin()
            for entry in entry_pool():
                rl.add(entry)
                rl.commit()
            rl.close()
        :param entry: ()
        """
        # DO NOT FORGET REVERSING THIS OPERATION WHEN DOING THE INVERSE OPERATION!
        json_l_s = json_l_s.replace('"', "'")
        # The entry variable is already a tuple, thus the tuple concatenation
        entry = entry + (json_l_s,)
        query = self.crud_details['queries']['insert_history_entry'] % entry
        self.conn.update(query)
        return self

    def _add_history_keywords_(self, bot: list, rsc_id: str, lang: str):
        """
        Inserts a term, its lemma and the resource(s) where it was found .
        """
        for t in bot:
            term_id = io.hash(t[1])
            lemma = t[0]
            label = t[1]
            entry = (term_id, lemma, label, lang, rsc_id)
            query = self.crud_details['queries']['insert_history_terms'] % entry
            self.conn.update(query)
        return self

    def clear(self):
        """
        Empties the History Log.
        """
        return self

    def remove(self, id_key: str, id_value: str):
        """
        Removes all entries in the History Log having a field id == _id_
        """
        return self

    def to_json(self, file: str):
        """
        Dumps the history onto a JSON file
        """

    def to_csv(self, file: str):
        """
        Dumps the history onto a JSON file
        """
        return self

    def exists(self, rsc_id: str, rsc_md5: str, part: str) -> tuple:
        """
        Determines whether a resource was logged in the history or not.
        The connection has to be opened and closed outside this method.
        The entry id is generated concatenating the rsc_id and the rsc_md5.
        :param rsc_id: the id of the resource
        :param rsc_md5: the md5 of the rsc content
        :param part: the resource part identifier, e.g. 'title', 'abstract', 'body', 'keywords'...
        :return: a tuple made of 1) True if the resource was previously logged, False otherwise, 2) The entry id for
        this resource, regardless of it exists or not (this way this very same entry id can be reused for subsequent
        insertion).
        """
        entry_id = str(self.gen_entry_id(rsc_id, rsc_md5, part))
        query = self.crud_details['queries']['ask'] % (entry_id, rsc_md5, part)
        ret = (self.conn.ask(query), entry_id)
        return ret

    def _create_body_(self, rmd: dict, path: str) -> str:
        """
        If a resource has no body, we create one based on the concatenation of the title, abstract and keywords
        (if any).
        """
        body = rmd['title'] if 'title' in rmd.keys() else ''
        body += rmd['abstract'] if 'abstract' in rmd.keys() else ''
        body += '\n'.join(rmd['subjects'])
        io.to_file(body, path)
        return path

    def _create_abstract_(self, rmd: dict, path: str, body: str, abstract_file: str) -> str:
        """
        If a resource has no abstract, we create one based on the body content. Since the abstract is created
        after the body, an abstract file will always exist.
        """
        ''' ABSTRACT EXTRACTION '''
        abstract = rmd['abstract']
        lang = rmd['lang'] if 'lang' in rmd.keys() else 'en'
        try:
            if not abstract or len(abstract) == '':
                body_file = io.find_first(path, body)
                body = io.file_to_str(body_file)
                abstract = summarize(body, lang, self.operational_details['abstract_sentence#'])
                io.to_file(abstract, abstract_file)
        except Exception as e:
            io.log(f'Resource {rmd["title"]} ({rmd["id"]}) could not be summarized...\n{e}')
        return abstract_file

    def _get_body_content_(self, path: str, rsc_id: str) -> str:
        """
        Returns the text extracted as a string from the resource file, the body of the resource, if it exists.
        """
        content = None
        file = ''
        try:
            # since all resources taken from file are bodies.
            file = io.find_first(path, rsc_id + '.txt')
            file = file if file else io.find_first(path, rsc_id + '.txt')
            if file:
                content = io.file_to_str(file)
            else:
                file = rsc_id + '.txt'
                io.log(f'File skipped: content could not be extracted. The file {file} does not exist.')
        except IOError as ex:
            error = f'Error while extracting the resource body: path {path} does not exist.' + ex.__str__()
            io.log(error, level='e')
            raise Exception(error)

        return content

    def _get_rsc_files_metadata_(self, record: dict, rsc_id: str) -> dict:
        path = io.slash(self.operational_details['corpus_path'])
        # Get the texts of title, abstract, keywords and body
        t = record['title'] if 'title' in record else ''
        a = record['abstract'] if 'abstract' in record else ''
        k = '\n'.join(record['subjects']) if 'subjects' in record else ''
        b = self._get_body_content_(path, rsc_id)
        b = b if b else ''
        # Preparing data to be inserted in the history log...
        title = {'rsc_id': rsc_id, 'content': t, 'md5': io.hash(t), 'contentType': record['contentType'],
                 'part_type': 'title'}
        abstract = {'rsc_id': rsc_id, 'content': a, 'md5': io.hash(a), 'contentType': record['contentType'],
                    'part_type': 'abstract'}
        body = {'rsc_id': rsc_id, 'content': b, 'md5': io.hash(b), 'contentType': record['contentType'],
                'part_type': 'body'}
        keywords = {'rsc_id': rsc_id, 'content': k, 'md5': io.hash(k), 'contentType': record['contentType'],
                    'part_type': 'keywords'}
        return {'title': title, 'abstract': abstract, 'body': body, 'keywords': keywords}

    @staticmethod
    def _clean_up_rsc_md_(rsc: dict) -> dict:
        ct = rsc.get('contentType')
        rsc['contentType'] = 'unknown' if not ct or ct == '' else ct
        lang = rsc.get('lang')
        rsc['lang'] = 'en' if not lang or lang == '' else rsc['lang']
        return rsc

    def _to_n_quad_(self, history_entry: tuple,
                    json_l_s: str,
                    out: str):
        """
        Writes n-quads to a .nq file.
        """
        CRLF = '\n'
        dgi = self.crud_details.get('namespace')
        rdf = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
        dt = 'http://www.w3.org/2001/XMLSchema#dateTime'
        graph_name = self.crud_details.get('graph_name')
        # DO NOT FORGET RE-REPLACING '' WITH " BEFORE TRANSFORMING THE STRING TO JSON
        json_l_s = json_l_s.replace('"', "'")
        lines = [f'<{dgi}{history_entry[0]}> <{rdf}type> <{dgi}Resource> <{graph_name}> .{CRLF}',
                 f'<{dgi}{history_entry[0]}> <{dgi}rscId> "{history_entry[1]}" <{graph_name}> .{CRLF}',
                 f'<{dgi}{history_entry[0]}> <{dgi}rscType> "{history_entry[2]}" <{graph_name}> .{CRLF}',
                 f'<{dgi}{history_entry[0]}> <{dgi}md5> "{history_entry[3]}" <{graph_name}> .{CRLF}',
                 f'<{dgi}{history_entry[0]}> <{dgi}modified> "{history_entry[4]}"^^<{dt}> <{graph_name}> .{CRLF}',
                 f'<{dgi}{history_entry[0]}> <{dgi}terms> "{json_l_s}" <{graph_name}> .{CRLF}']
        with open(out, 'a+') as nq:
            nq.writelines(lines)
        return

    @staticmethod
    def _to_json_l_(history_entry: tuple,
                    json_l_s: str,
                    out: str):
        """
        Writes json lines to a *.jsonl file.
        """
        CRLF = '\n'
        line = '{"history_entry": "%s", "rscId": "%s", "rscType": "%s", "md5": "%s", "modified": "%s", "terms": %s}'
        t = tuple([e for e in history_entry]) + (json_l_s,)
        line = (line % t) + CRLF
        with open(out, 'a+') as jl:
            jl.write(line)
        return

    def _drop_graph_(self):
        graph = self.crud_details.get('graph_name')
        if graph:
            # Checker, otherwise stardog throws an exception
            graph_exists = self.conn.ask(f'ASK WHERE ' + '{GRAPH ' + f'<{graph}> ' + ' {?s ?p ?o}}')
            if graph_exists:
                drop_query = f'DROP GRAPH <{graph}>'
                self.begin()
                self.conn.update(drop_query)
                self.conn.commit()

        # Drop n-quads file with previous graph
        nq_file = self.operational_details['out_nq_file']
        if nq_file and self.drop_nq:
            io.drop_file(nq_file)

    def parse_corpus(self, corpus_path: str, rsc_metadata_file: str, drop_graph: bool = False, drop_nq: bool = False):
        t0 = io.now()
        self.drop_nq = drop_nq
        self.drop_graph = drop_graph
        self.report['message'] = ''
        self.report['done'] = {'added_parts#': 0, 'added_bodies#': 0, 'skipped_parts#': 0}
        # Checkers
        if self._no_corpus_(self.operational_details['corpus_path']):
            self.report['message'] = f'Failed: corpus path {corpus_path} not found.'
            self.code = 404
            return self
        if not io.xst_file(rsc_metadata_file):
            self.report['message'] = f'Failed: resource metadata file {rsc_metadata_file} not found.'
            self.code = 404
            return self
        # Resource metadata iteration
        rmd = io.from_json(rsc_metadata_file)
        '''
        Connection to the stardog database. It's kept open until the whole parsing of resources is finished.
        '''
        rsc_added_index = 0  # Resources that are newly added to the history log.
        rsc_skipped_index = 0  # Resources that had been parsed in previous occasions and exist in the history.
        rsc_empty_index = 0  # Resources extracted from the metadata (e.g. abstract) that come empty in the json.
        rsc_not_found = 0  # Bodies mentioned in the metadata json but that were not textified.
        rsc_total_number = len(rmd)
        rsc_count = 0
        try:
            self.connect()
            # Drop previous version of the database graph
            if self.drop_graph:
                self._drop_graph_()

            for key in rmd:
                # Checkers
                rsc = rmd[key]
                rsc = self._clean_up_rsc_md_(rsc)
                mid = rsc.get('id')  # The md5 id of the resource
                io.log(f"Processing id '{mid}'")
                '''
                All resources are processed and historified, regardless of whether they're in the scope or not. 
                This is necessary for different reasons:
                    1. Resource relevance is calculated based on the terms found in the whole corpora
                    2. The user requires to see in the GUI all document related to the same operation, even if some 
                    are not linked to its terms (because these resources are not in the scope) 
                '''
                '''
                Every resource has (or may have) up to four PARTS: title, abstract, body and keywords. 
                The following method captures the necessary metadata on these parts to check whether they have been
                already historified or not.                                      
                '''
                # resource_parts = self._get_rsc_files_metadata_(rsc, key)
                resource_parts = self._get_rsc_files_metadata_(rsc, mid)
                '''
                Now, each resource-part is kept in the history, jointly with their (lemma, term, freq) tuples, and the 
                relation of the tuples to the "parent" resource. If any of these parts is later on modified, only the 
                modified part will be added to the history log. The method to identify each logged part is the 
                concatenation of the parent resource id and the md5 of the part content. This way, if the part being 
                logged already existed and has not been modified, it is not re-inserted, and if it existed but the 
                content is different a new entry is then created for that part. 
                This method is later on used by the resource analyser, which takes the parent-resource-id and the 
                md5 of the file's content specified in the metadata json to decide exactly which resource part to 
                chose for the linking of its terms to the terms of the thesauri.             
                '''
                # This timestamp will be applied to all resource-parts if the resource is totally new
                modified = str(io.now()).replace(' ', 'T') + 'Z'
                for part_type in resource_parts:
                    record = rmd[key]
                    # Only the modified resource-parts that do not exist in the history log are added
                    # If an entry does not exist in the history log, let's add it...
                    content_type = record['contentType']
                    # Make sure the rsc_type is lowered(), otherwise ANYTHING won't work!
                    rsc_type = f'{content_type}.{part_type}'.lower()
                    rsc_md5 = resource_parts[part_type]['md5']
                    # exists, entry_id = self.exists(mid, rsc_md5, part_type)
                    exists, entry_id = self.exists(mid, rsc_md5, rsc_type)
                    '''
                    # If an entry does not exist in the history log, let's add it...
                    content_type = record['contentType']
                    rsc_type = f'{content_type}.{part_type}'
                    '''
                    content = resource_parts[part_type]['content']
                    rsc_lang = record['lang']
                    if not exists:
                        t1 = io.now()
                        # Generate a new id...
                        # new_entry_id = self.gen_entry_id(mid, rsc_md5, rsc_type)
                        new_entry_id = entry_id
                        '''
                        Analyse the content and keep the tuples (lemma, term, freq). 
                        *** LEMMATIZATION OCCURS HERE ***
                        '''
                        bot = KeywordWorker(self.operational_details).extract(content,
                                                                              rsc_part=part_type,
                                                                              rsc_lang=rsc_lang).bot
                        # bot comes as a list of dictionaries {lemma: lx, term: tx, freq: fx}.
                        # But we want to register it as a json line
                        json_l_s = json.dumps({int(new_entry_id): bot})
                        ''' 
                        The transaction is at the resource level. This way, if something goes wrong the 
                        re-parsing of these resources is not necessary anymore.
                        Not bot implies that the resource came empty...
                        '''
                        if bot:
                            t2 = io.now()
                            # history_entry = (new_entry_id, rsc_id, rsc_type, rsc_md5, modified)
                            history_entry = (new_entry_id, mid, rsc_type, rsc_md5, modified)
                            self.begin()
                            self._to_n_quad_(history_entry=history_entry,
                                             json_l_s=json_l_s,
                                             out=self.operational_details['out_nq_file'])
                            self._to_json_l_(history_entry=history_entry,
                                             json_l_s=json_l_s,
                                             out=self.operational_details['out_jsonl_file'])
                            self._add_history_entry_(history_entry, json_l_s)
                            self.commit()
                            ''' 
                            logging results
                            '''
                            rsc_added_index += 1
                            '''
                            io.log(f'Resource-part added: {rsc_added_index}. {rsc_id}.{rsc_type} added '
                                   f'to the stardog history graphs (il: {io.now() - t2}, '
                                   f'tl: {io.now() - t1}, tp: {io.now() - t0}, now: {io.now()}).')
                            '''
                            io.log(f'Resource-part added: {rsc_added_index}. {mid}.{rsc_type} added '
                                   f'to the stardog history graphs (il: {io.now() - t2}, '
                                   f'tl: {io.now() - t1}, tp: {io.now() - t0}, now: {io.now()}).')
                            self.report['done']['added_parts#'] = rsc_added_index
                        else:
                            rsc_empty_index += 1
                            # io.log(f'Resource-part empty: {rsc_empty_index}. {rsc_id}.{rsc_type} ')
                            io.log(f'Resource-part empty: {rsc_empty_index}. {mid}.{rsc_type} ')
                            self.report['done']['empty_parts#'] = rsc_empty_index
                    else:
                        rsc_skipped_index += 1
                        '''
                        io.log(f'Resource-part skipped: {rsc_skipped_index}. {rsc_id}.{rsc_type} '
                               f'skipped because already existing.')
                        '''
                        io.log(f'Resource-part skipped: {rsc_skipped_index}. {mid}.{rsc_type} '
                               f'skipped because already existing.')
                        self.report['done']['skipped_parts#'] = rsc_skipped_index
                io.log(f"Processed id '{mid}' is {rsc_count}/{rsc_total_number}")
                rsc_count += 1
        except Exception as ex:
            io.log(f'Processed aborted ({io.now() - t0})')
            raise ex
        finally:
            '''
            The connection is closed at the end, no matter what happened.
            '''
            self.close()
        io.log(f'Exiting process ... ({io.now() - t0})')
        return self

    def count(self) -> int:
        """
        Counts the number of resources logged in the history.
        """
        self.connect()
        query = self.crud_details['queries']['count']
        result = self.conn.select(query)
        result = result['results']['bindings'][0]['total']['value']
        return int(result)
