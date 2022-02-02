import json
import requests
import com.nttdata.dgi.util.io as io
import com.nttdata.dgi.util.errors as e
import com.nttdata.dgi.rdf.graphstore as gs
import tqdm

LABELS = ['<title', '<preflabel', '<altlabel', '<hiddenlabel', '<literal', '<literalform']
CRLF = '\n'
EOF = ''


class SKOSMirror:
    lemmatization_details: dict     # A dictionary with every data required for the lemmatization
    store_details: dict             # A dictionary with data to establish the connection to a Data Base
    report: dict
    code: int
    ln: int     # line number
    pl: int     # prefLabel number
    al: int     # altLabel number
    hl: int     # hiddenLabel number
    tl: int     # title number
    l_: int     # literal number
    lf: int     # literalForm number
    sfn: str    # source file name (the SKOS file to mirror)
    tfn: str    # target file name (the SKOS file containing the mirrored labels)
    eof: bool   # signals the end of the source SKOS file
    stats: dict  # resulting stats
    graph: str  # the named graph to load onto a graph store
    function: str   # the name of the function to perform

    def __init__(self, lemmatization_details: dict):
        self.lemmatization_details = lemmatization_details
        self.report = {}
        self.code = -1
        self.ln, self.pl, self.al, self.hl, self.tl, self.l_, self.lf = 0, 0, 0, 0, 0, 0, 0
        self.sf = None      # Source file to mirror
        self.tf = None      # Target file with the mirrored labels
        self.sfn = ''
        self.tfn = ''
        self.eof = False
        self.stats = {}

    '''
    Default basic functions provided by the skos mirror component...This can be enriched with stemming and 
    other mapped return values.
    '''
    def md5lemma(self, content: str, lang: str) -> (str, int):
        """
        Returns the md5 hash of a lemmatized content.
        :param content: the content to lemmatize and hash
        :param lang: the language for the lemmatizer
        :return: the md5 string
        """
        return self.lemma(io.hash(content), lang)

    def lemma(self, content: str, lang: str) -> (str, int):
        """
        Returns a lemmatized content.
        :param content: the content to lemmatize
        :param lang: the language for the lemmatizer
        :return: the lemma(s)
        """
        endpoint = self.lemmatization_details.get('endpoint')
        call = self.lemmatization_details.get('raw-data')
        call['phrase'] = content
        call['lang'] = lang
        res = requests.post(endpoint, call)
        if res.ok:
            return json.loads(res.content)['unaccented-minus-stopwords'], 201
        else:
            io.log(f'Failed: {content} could not be lemmatized. Reason reported: + {res.reason}')
            return content, 501

    @staticmethod
    def _get_lang_(line: str) -> str:
        # remove blanks in the line
        ns_line = line.replace(' ', '')   # no spaced line
        # Get the position of where the language starts
        try:
            i = ns_line.index('lang=') + len('lang=') + 1
            # Discard the left side of the line, starting with 'lang=....'
            r = ns_line[i:]
            # Get the the position of the character used to end-delimit the language, normally a '""
            i2 = r.index(ns_line[i - 1:i])
            # Return from end 'lang=<delim>' to '<delim>' (normally '"'")
            lang = ns_line[i: i + i2]
        except ValueError:
            lang = None
        return lang

    @staticmethod
    def _get_content_(line: str) -> str:
        # Look for '</'
        end_tag = line.split('</')
        if len(end_tag) > 2:
            e.error(e.MULTIPLE_ELEMENTS_PER_LINE, (line,))
            raise Exception()
        return io.url_tail(end_tag[0], '>')

    def _get_label_(self, line: str) -> (str, str, str):
        """
        Given a line of text, detects whether it contains a label and extracts the label, the language and its content.
        :param line: the line coming from the SKOS file presumably containing a label
        :return: a tuple with the label, its language and content.
        """
        # label = [l_ for l_ in LABELS if l_.lower() in line]
        ls = line.split()
        label = [l_ for l_ in LABELS if ls and len(ls) > 0 and ls[0].lower() == l_.lower()]
        if len(label) > 0:
            lang = self._get_lang_(line)
            content = self._get_content_(line)
            content = None if content.strip().strip('\n').strip('\t') == '' else content
            return ls[0][1:], lang, content
        return None, None, None

    def _inc_label_type_(self, label: str):
        if label.lower() == 'title':
            self.tl += 1
        elif label.lower() == 'preflabel':
            self.pl += 1
        elif label.lower() == 'altlabel':
            self.al += 1
        elif label.lower() == 'hiddenlabel':
            self.hl += 1
        elif label.lower() == 'literal':
            self.l_ += 1
        elif label.lower() == 'literalform':
            self.lf += 1
        return self

    def __post__(self, content: str, lang) -> (str, int):
        endpoint = self.lemmatization_details.get('endpoint')
        call = self.lemmatization_details.get('raw-data')
        call['phrase'] = content
        call['lang'] = lang
        res = requests.post(endpoint, call)
        if res.ok:
            return json.loads(res.content)['unaccented-minus-stopwords'], 201
        else:
            io.log(f'Failed: {content} could not be lemmatized.')
            return content, 501

    def __replace__(self, line: str) -> str:
        label, lang, content = self._get_label_(line)
        ret = line
        if label and content:
            self.ln += 1
            self._inc_label_type_(label)
            # res, code = self.__post__(content, lang)
            res, code = eval('self.' + self.function + '(content, lang)')
            if code <= 400:
                content = '>' + content + '<'
                new_content = '>' + res + '<'
                ret = line.replace(content, new_content)
            else:
                m = f'{self.ln}. (FAILURE) -> Label: {label}, content: {content}, replaced with: {res}, lang: {lang}'
                self.report['warnings'] = self.report['warnings'] + [m] if 'warnings' in self.report.keys() else [m]
                ret = line
        return ret

    def _open_files_(self):
        self.sf = open(self.sfn, 'r')
        self.tf = open(self.tfn, 'a+')
        return self

    def _close_files_(self):
        self.sf.close()
        self.tf.close()
        return self

    def _read_(self) -> str:
        return self.sf.readline()

    def _write_(self, line: str):
        self.tf.write(line)
        return self

    def _process_(self, line: str):
        if line != EOF:
            res = self.__replace__(line)
            self._write_(res)
        else:
            self.eof = True

    def __stats__(self) -> dict:
        self.stats = {"title#": self.tl, "prefLabel#": self.pl, "altLabel#": self.al,
                      "hiddenLabel#": self.hl, "literal#": self.l_, "literalForm#": self.lf}
        return self.stats

    @staticmethod
    def __to_stardog__(connection_details: dict, thesaurus_file: str, graph_name: str, drop: bool):
        sd = gs.StarDog(**connection_details)
        sd.load(file=thesaurus_file, graph_name=graph_name, drop=drop)

    def store(self, thesauri: list, store_details: dict):
        for thesaurus in thesauri:
            t0 = io.log(f'Loading thesaurus {thesaurus["target"]}...')
            f = thesaurus.get('target')
            g = thesaurus.get('graph')
            s = store_details.get('store')
            if s.lower() == 'stardog':
                self.__to_stardog__(store_details.get('details'), f, g, drop=True)
            io.log(f'Thesaurus {thesaurus["target"]} loaded successfully (lapse: {io.now()-t0}, now: {io.now()})')

    def mirror(self, thesauri: list):
        """
        Takes an SKOS XML file and creates a copy in a named graph where the labels have been replaces with the
        value returned by a function or a service-endpoint.
        :param thesauri: a list with dictionaries containing details on the thesauri, such as:
            - the source SKOS thesaurus
            - the target SKOS mirror
            - the named graph for its loading onto a graph store
        """
        for thesaurus in thesauri:
            t0 = io.log(f"Processing thesaurus {thesaurus['source']} (now: {io.now()})")
            self.report['started'] = str(io.now())
            '''
            Get the number of labels in the thesaurus. This number is used to calculate 
            the tqdm total.
            '''
            self.sfn = thesaurus.get('source')
            self.tfn = thesaurus.get('target')
            self.graph = thesaurus.get('graph')
            self.function = thesaurus.get('function')
            self.eof = False    # Reset per thesaurus, otherwise only the first one will be processed

            # Checkers
            # If file does not exist...interrupt the process
            if not io.xst_file(self.sfn):
                e.error(e.FILE_NOT_FOUND, (self.sfn,))
                return
            # Drop previous mirrors with the same name
            io.drop_file(self.tfn)
            '''
            Get the data necessary for the progress bar
            '''
            fs = io.file_to_str(thesaurus.get('source'))
            total = io.wc(('\n', ), fs)
            io.log(f'Mapping {total} lines...')
            bar = tqdm.tqdm(total=total)

            try:
                '''
                Open the files to read and write
                '''
                self._open_files_()
                '''
                Read the source 
                '''
                while not self.eof:
                    line = self._read_()
                    '''
                    Processes the entry and writes the result in the mirror file
                    '''
                    self._process_(line)
                    bar.update(1)
                '''
                Return counters and statistics
                '''
                stats = self.__stats__()
                io.log(f'Totals follow: {stats}')
                io.log(f"Thesaurus {thesaurus['source']} processed successfully (lapse: {io.now() - t0}, now: {io.now()}")
                self.report['done'] = stats
            except IOError as ex:
                raise ex
            finally:
                self._close_files_()
                bar.close()

