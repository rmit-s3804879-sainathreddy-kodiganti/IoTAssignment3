import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/QRReader'))
sys.path.append(os.path.abspath('../../src/Socket'))
from create_qr import create_qr
from read_qr import read_qr
from socket_utils import checkFile
import pathlib


class qrTest(unittest.TestCase):
    """This is the qrTest Class

    This is used to test the QR code modules.
    """

    def test_createQrCode(self):
        """This function is to test qr generation
        """
        gen_qr_obj = create_qr()
        isCreated = gen_qr_obj.start("EngineerId: {}, carID: {}, MacID: {}".format('engineer2@password.com', '1', '5C:99:60:C4:49:2C'))
        self.assertTrue(isCreated)

    def test_checkFile(self):
        """This function is to test qr file creation
        """
        path = str(pathlib.Path(__file__).resolve().parents[2])
        path = path + "/src/QRReader/generatedimage/qr.jpg"
        isVaild = checkFile(path)
        self.assertTrue(isVaild)

    def test_readQR(self):
        """This function is to test qr code data
        """
        qrObj = read_qr()
        data  = qrObj.start()
        self.assertEqual(data, "EngineerId: engineer2@password.com, carID: 1, MacID: 5C:99:60:C4:49:2C")
        
    def test_wrongDataQR(self):
        """This function is to test qr code data
        """
        qrObj = read_qr()
        data  = qrObj.start()
        self.assertTrue(data != "EngineerId: engineer2@password.com, carID: 1, MacID: 5C:99:60:C4:49:2")

if __name__ == '__main__':
    unittest.main()
