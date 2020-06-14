import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/Socket'))
from socket_utils import checkFile
import pathlib
from reception import reception


class socketTest2(unittest.TestCase):
    """This is the socketTest Class

    This is used to test the socket modules.
    """

    __socket_obj = reception()
    __socket_obj.main()

    def test_checkFile(self):
        """This function is to test socket connection

        """
        path = str(pathlib.Path(__file__).resolve().parents[2])
        path = path + "/src/Facial recognition/dataset"
        print(path)
        isVaild = checkFile(path)
        self.assertTrue(isVaild)

    def test_assigned_engineer(self):
        """This function is to test socket connection

        """
        engineer_details = self.__socket_obj.load_engineer_details("1")
        self.assertTrue(engineer_details)
        
    def test_unassigned_engineer(self):
        """This function is to test socket connection

        """
        engineer_details = self.__socket_obj.load_engineer_details("E")
        self.assertTrue(engineer_details=={})

if __name__ == '__main__':
    unittest.main()
