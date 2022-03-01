import unittest
from com.nttdata.sembu.crud.PersistenceFactory import PersistenceFactory
from com.nttdata.sembu.crud.PersistorType import PersistorType
from com.nttdata.sembu.crud.IPersistor import IPersistor


class FilePersistenceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(FilePersistenceTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def __write_textual_content(self, p: IPersistor, start: int, end: int):
        for i in range(end, start):
            p.persist(f"This is sentence number #{i}\n")

    def test_001_file_writer(self):
        """
        Use of the PersistorType.FILE to create a file with textual content.
        If the file exist the content is appended.
        If you want to replace the content of a file with a totally new content, just
        drop the file and persist the content.

        'persistor_details' is a dictionary expecting the following elements:
            1. target_path_filename: str (Mandatory: a relative or absolute path to the file where the content is
                to be persisted;
            2. make_dirs: bool (Optional: If True, the directories in the target_file_pathname are created, if
                not exist. Defaults to True);
            3. encoding: str (Optional: The encoding of a textual content. Defaults to 'utf-8').
            4. mode: "file" (== 'w+) or "line" (== 'a+")
        """

        content = ''
        for i in range(10):
            content += f"This is sentence #{i}\n"
        # Option 1: the file path and the mode are specified at construction time
        p_details = {"file": '../arti/writing-file-1.txt', "mode": "file"}
        p = PersistenceFactory().new(persistor_details=p_details, persistor_type=PersistorType.FILE)
        p.persist(content)
        # Option 2: the file and the mode are specified at method invocation time, and the content is named
        p.persist(content=content, mode="file", file="../arti/writing-file-2.txt")
        # Option 3: the file and the mode are specified at method invocation time, and the content is not named
        p.persist(content, mode="file", file="../arti/writing-file-3.txt")

    def test_002_file_appender(self):
        """
        Appends textual content to an existing file.

        'persistor_details' is a dictionary expecting the following elements:
            1. target_path_filename: str (Mandatory: a relative or absolute path to the file where the content is
                to be persisted;
            2. make_dirs: bool (Optional: If True, the directories in the target_file_pathname are created, if
                not exist. Defaults to True);
            3. encoding: str (Optional: The encoding of a textual content. Defaults to 'utf-8').
            4. mode: "file" (== 'w+) or "line" (== 'a+")
        """
        content = ''

        # Option 1: the file path and the mode are specified at construction time
        p_details = {"file": '../arti/appending-lines-1.txt', "mode": "line"}
        p = PersistenceFactory().new(persistor_details=p_details, persistor_type=PersistorType.FILE)
        for i in range(10):
            # Append line
            p.persist(f"This is sentence #{i}\n")
        # Option 2: the file and the mode are specified at method invocation time, and the content is named
        for i in range(10):
            p.persist(content=f"This is sentence #{i}\n", mode="line", file="../arti/appending-lines-2.txt")
        for i in range(10):
            # Option 3: the file and the mode are specified at method invocation time, and the content is not named
            p.persist(f"This is sentence #{i}\n", mode="line", file="../arti/appending-lines-3.txt")
        return

    def test_003_get_file_content(self):
        """
        Returns the entire content of a file as a string.
        :return:
        """
        # Option 1: the file path and the mode are specified at construction time
        p_details = {"file": '../arti/file-1.txt', "mode": "file"}
        p = PersistenceFactory().new(persistor_details=p_details, persistor_type=PersistorType.FILE)
        assert type(p.select()) is str

    def test_004_read_file_lines(self):
        """
        Returns the content of a file line per line.
        :return:
        """
        # Option 1: the file path and the mode are specified at construction time
        p_details = {"file": '../arti/file-1.txt', "mode": "line"}
        p = PersistenceFactory().new(persistor_details=p_details, persistor_type=PersistorType.FILE)
        print("Option 1: the file path and the mode are specified at construction time")
        line = 'dummy'
        while line:
            line = p.select()
            if line:
                print(line)
        # Option 2: the mode "next" clarifies better what is going on
        print("Option 2: use of select('next') clarifies better what is going on")
        line = 'dummy'
        while line:
            line = p.select("next")
            if line:
                print(line)

    def tearDown(self) -> None:
        return


if __name__ == '__main__':
    unittest.main()
