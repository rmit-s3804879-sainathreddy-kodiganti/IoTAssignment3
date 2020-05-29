import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/Facial recognition'))
from encode import encode
from recognise import recognise
import pathlib

class faceRecognitionTest(unittest.TestCase):
    """This is the faceRecognitionTest Class

    This is used to test the face recogntion modules.
    """
    def test_isEncoderFileCreated(self):
        path = str(pathlib.Path(__file__).resolve().parents[2])
        path = path + "/src/Facial recognition/dataset"
        print(path)
        endcode_obj = encode()
        is_file_created = endcode_obj.run(path)
        self.assertTrue(is_file_created)

    def test_isPickingDefaultPath(self):
        path = ""
        endcode_obj = encode()
        is_file_created = endcode_obj.run(path)
        self.assertTrue(is_file_created)
    
    def test_isDetectingTrainedFace(self):
        face_rec = recognise()
        recognised_name = face_rec.start()
        self.assertEqual("sainath", recognised_name)

    def test_isNotDetectingUntrainedFace(self):
        face_rec_2 = recognise()
        recognised_name = face_rec_2.start()
        self.assertEqual("uknown user", recognised_name)
        
if __name__ == '__main__':
    unittest.main()
