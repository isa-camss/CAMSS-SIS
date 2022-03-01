#######################################################
# 
# FilePersistor.py
# Python implementation of the Class FilePersistor
# Created on:      19-feb-2022 10:31:43
# Original author: SEMBU-Team, NTTData
# 
#######################################################
from com.nttdata.dgi.io.IO import IO as IO
from com.nttdata.dgi.crud.Persistor import Persistor


class FilePersistor(Persistor):
    """File System-based persistence. E.g., text writing or text appending."""
    # A dictionary containing the configuration details for the configuration. such as target file and path name, etc.
    p_details: dict
    target_file: str
    file_reader: IO

    def __init__(self, **persistor_details):
        """
        :param persistor_details:
            1. target_path_filename: str (Mandatory: a relative or absolute path to the file where the content is
                to be persisted;
            2. make_dirs: bool (Optional: If True, the directories in the target_file_pathname are created, if
                not exist. Defaults to True);
            3. encoding: str (Optional: The encoding of a textual content. Defaults to 'utf-8').
            4. mode: str (Optional:
                If "file" the persistor will behave as a file writer and reader,
                If "line" the persistor will behave as a line writer and reader).
        """
        super(FilePersistor, self).__init__()
        # Persistor configuration details as a dictionary
        self.p_details = persistor_details
        self.file_reader = None
        return

    def __make_dirs(self, path):
        """
        Create directories in the target_path_filename if not exist
        :return: self
        """
        create = self.p_details.get("make_dirs")
        create = True if create is None else create
        if create and path:
            IO.make_dirs(path)
        return self

    def __append(self, filename: str, content: str):
        """
        Appends content to the target path_file_name. Defaults to content type "str"
        :return: self
        """
        '''
        checkers
        '''
        encoding = self.p_details.get('encoding')
        encoding = 'utf-8' if not encoding else encoding
        if not filename:
            raise FileExistsError("File could not be created because a path filename has not been provided. Check "
                                  "the persistor details.")
        '''
        Append str
        '''
        if type(content) is str:
            with open(filename, 'a+', encoding=encoding) as file:
                file.write(content)
        return self

    def drop(self, *args, **kwargs):
        """
        Drops file if a previous version exists and so specified in the details (defaults to True)
        :return: self
        """
        IO.drop_file(self.p_details.get('target_path_filename'))
        return self

    def __get_mode(self, **kwargs):
        mode = kwargs.get("mode")
        return mode if mode is not None else self.p_details.get("mode")

    @staticmethod
    def __get_content_from_args(*args, **kwargs):
        if args is not None and len(args) == 1:
            # Early return if the content comes as a single argument
            return args[0]
        elif args and len(args) > 1:
            raise ValueError("FAILURE: Only one no-mame argument was expected in the invocation to persist. Check "
                             "the documentation.")
        # Alternative return if the content comes as a named argument
        content = kwargs.get('content')
        if content is None:
            raise ValueError("FAILURE: No persistence has been performed because no content has been provide to "
                             "the FilePersistor.persist() method. Check the documentation.")
        return content

    def __get_file(self, **kwargs) -> (str, str):
        # If the file is not mentioned in the details ...
        file = kwargs.get('file')
        # ...then it has to be passed as a named parameter, otherwise ...
        file = file if file is not None else self.p_details.get('file')
        # ... raise exception.
        if file is None:
            raise ValueError("FAILED: A file content could not be persisted since no file path name has been provided. "
                             "Check the documentation.")
        return file

    def persist(self, *args, **kwargs):
        """
        Persists content into a file in different ways, by appending content to a file, by inserting the whole
        content into a file in a single shot, other.
        :param args: arguments
        :param kwargs: arguments parameters, a structure like a dict, a list, etc.
        :return: self
        """
        '''
        Get the file path name to create or to append lines into
        '''
        filename = self.__get_file(**kwargs)
        '''
        If not exist, create recursively the directories nested in the path filename, if any. 
        '''
        self.__make_dirs(filename)

        '''
        Argument management: If after details and argument evaluation, the mode continues to be None, 
        then the default mode will be "line", and the content will be appended to the file.
        '''
        mode = self.__get_mode(**kwargs)
        content = self.__get_content_from_args(*args, **kwargs)

        if mode == 'file':
            # The creation of a new file is equivalent to first drop and then append.
            IO.drop_file(filename)
        # Else, it's just append to an existing file.
        self.__append(filename, content)
        return self

    def select(self, *args, **kwargs) -> str:
        """
        If mode is 'file' it returns the entire content. If mode is 'line' or 'next' returns the next line
        :param args: args[0] -> the mode, e.g. 'next', 'line' or 'file'
        :param kwargs: kwargs {'mode': <mode>, 'file': <path_to_the_file>}
        :return: either the entire file content or a line.
        """
        '''
        Mode management: 
            1. Priority is given to the mode passed as an argument in args[0]
            2. If no args then it peeks into the named arguments for a 'mode' :param
            3. If no mode found -> defaults to 'file'
        '''
        mode = args[0] if args else None
        mode = mode if mode else self.__get_mode(**kwargs)
        mode = mode if mode else 'file'

        filename = self.__get_file(**kwargs)
        content = None
        if mode == 'file':
            content = IO.get_file_content(filename)
        if mode == 'line' or mode == 'next':
            if self.file_reader is None:
                self.file_reader = IO(file=filename)
            return self.file_reader.next(file=filename)
        return content

