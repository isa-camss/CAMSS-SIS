import sys
import unittest
import com.nttdata.dgi.util.io as io


class EmptyTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(EmptyTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_log_elastic(self):
        io.log("test error log", 'e')
        io.log("test warning log", 'w')
        io.log("test info log", 'w')
        return

    def tearDown(self) -> None:
        return


if __name__ == '__main__':
    unittest.main()
