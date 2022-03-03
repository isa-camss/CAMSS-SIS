import unittest
from com.nttdata.dgi.io.IO import IO


class ReadLinesTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ReadLinesTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_0001_read_lines(self):
        file = '../arti/file-1.txt'
        io = IO(file=file)
        line = 'dummy'
        while line:
            line = io.next()
            if line:
                print(line)
        return


if __name__ == '__main__':
    unittest.main()
