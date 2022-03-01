#######################################################
# 
# IO.py
# Python implementation of the Class IO
# Created on:      19-feb-2022 12:46:38
# Original author: SEMBU-Team NTTData
#
#######################################################
import json
import ntpath
import os
import pathlib
import shutil
import unidecode
from datetime import datetime


class IO:
    """
    Class for common file and string input and output operations.
    """
    # CTT
    EOF = ''
    DEFAULT_ENCODING = 'utf-8'
    DEFAULT_FILE_OP_MODE = 'r'
    # Class global vars
    file_name: str
    file_opened: bool
    file_op_mode: str
    encoding: str

    def __init__(self, *args, **kwargs):
        self.file = None
        self.file_name = kwargs.get("file")
        self.file_opened = False
        self.encoding = kwargs.get('encoding')
        self.encoding = self.DEFAULT_ENCODING if self.encoding is None else self.encoding
        self.file_op_mode = kwargs.get('mode')
        self.file_op_mode = self.file_op_mode if self.file_op_mode is not None else self.DEFAULT_FILE_OP_MODE
        return

    @staticmethod
    def alpha2(lang: str) -> str:
        """
        WARNING: MOVED INTO util.string.py for generalization
        Returns the alpha-2 version of an expanded idb lang, like from 'en-US' into 'en'
        :param lang: idb version of the lang
        :return: alpha-2 version of the lang
        """
        return None if not lang else lang[:2]

    def __close_file(self):
        if self.file_opened:
            self.file.close()

    @staticmethod
    def drop_dir(path: str):
        if os.path.isdir(path):
            shutil.rmtree(path)

    @staticmethod
    def drop_file(path: str):
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def get_file_content(path: str, encoding: str = 'utf-8', bytes_number: int = 0):
        """
        Returns the content of a file as a string.
        :param path: the path filename;
        :param encoding: the encoding of the content if known, otherwise defaults to 'utf-8';
        :param bytes_number: the number of bytes to read; if '0' the entire file is read;
        :return: the file content as as string.
        """
        if not IO.path_exists(path):
            return None
        file_size = pathlib.Path(path).stat().st_size
        offset = bytes_number if bytes_number != 0 and bytes_number < file_size else file_size
        try:
            with open(path, 'rb') as fin:
                return fin.read(offset).decode(encoding)
        except Exception:
            raise Exception

    @staticmethod
    def json_str_to_dict(json_line: str) -> dict:
        """
        Used to read JSON objects expressed as texts and transform them into Python's dictionaries.
        One usage of this method is to read JSONL files and process the contents, e.g. to store these
        contents into NO-SQL databased, such as in an Elasticsearch index as Elastic documents.
        """
        try:
            return json.loads(json_line)
        except Exception as ex:
            raise Exception("FAILED: An exception was cast while trying to cast a JSON str line into a Python dict. "
                            f"The original exception thrown by the json library follows: {ex}")

    @staticmethod
    def make_dirs(path: str):
        """
        :param path: a relative or absolute path or path file name
        :return: None
        """
        dir_, file_ = ntpath.split(path)
        os.makedirs(dir_, exist_ok=True)
        return

    def next(self, *args, **kwargs):
        """
        Dynamic. Needs instantiation of the class IO.
            1. Opens a file if not opened yet;
            2. Reads line and remembers its position, so next call to next returns the following line
            3. Closes file upon EOF

        Arguments:
        :param: *args: the file path and name
        :param: *kwargs: file=<filepathname>, mode=<file_mode> (defaults to 'r')
        :return: next line or none if EOF
        """
        '''
        1. Open the file. Forces mode to READ 
        '''
        kwargs['mode'] = 'r'
        self.__open_file(*args, **kwargs)
        '''
        2. Read line
        '''
        line = self.file.readline()
        '''
        3. Return line if not <EOF> otherwise closes file and returns None 
        '''
        if line == self.EOF:
            self.file_opened = False
            self.__close_file()
            return None
        return line

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def nnl(text: str) -> str:
        """
        Replaces all new lined '\n' with ' '
        :param text: text with new lines
        :return: text without new lines
        """
        return text.replace("\n", " ")

    def __open_file(self, *args, **kwargs):
        """ Opens the default file passed either at construction time or via method call"""

        '''
        Early return if the file is already open
        '''
        if self.file_opened:
            return
        '''
        1. Get the file name
        '''
        file_name = args[0] if args else None
        file_name = kwargs.get('file') if file_name is None else file_name
        file_name = file_name if file_name else self.file_name
        if file_name is None:
            raise ValueError("FAILED: The IO.next() method could not read lines from a file because the file path "
                             "and name were not provided. Please check the documentation.")
        '''
        2. Get the encoding. Defaults to 'utf-8'
        '''
        encoding = kwargs.get('encoding')
        encoding = self.encoding if encoding is None else encoding

        '''
        3. Get the operation mode (e.g., 'r', 'w+', etc.)
        '''
        mode = kwargs.get('mode')
        mode = self.file_op_mode if mode is None else mode
        '''
        1. Open the file if closed. 
        '''
        try:
            self.file = open(file=self.file_name, mode=mode, encoding=encoding)
            self.file_opened = True
        except IOError as ex:
            raise Exception(ex)

    @staticmethod
    def path_exists(path: str) -> bool:
        """
        Checks whether a file or directory exists or not.
        :param path:  the path to the dir or file
        :return: the result of the checking
        """
        return os.path.isdir(path) or os.path.isfile(path)

    @staticmethod
    def unaccent(text: str) -> str:
        return unidecode.unidecode(text)
