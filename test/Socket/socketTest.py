import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/Socket'))
from socket_utils import checkFile
import pathlib


class socketTest2(unittest.TestCase):
    """This is the socketTest Class

    This is used to test the socket modules.
    """

    def test_checkFile(self):
        """This function is to test socket connection

        """
        path = str(pathlib.Path(__file__).resolve().parents[2])
        path = path + "/src/Facial recognition/dataset"
        print(path)
        isVaild = checkFile(path)
        self.assertTrue(isVaild)

if __name__ == '__main__':
    unittest.main()
