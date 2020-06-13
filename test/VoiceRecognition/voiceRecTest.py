import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/VoiceRecognition'))
from voice_rec import voice_rec
import pathlib


class voiceRecTest(unittest.TestCase):
    """This is the voiceRecTest Class

    This is used to test the voice rec modules.
    """

    def test_voice_connection(self):
        """This function is to test voice connection
        """
        voiceObj = voice_rec()
        text = voiceObj.start() 
        self.assertEqual("Listening timed out whilst waiting for phrase to start",text)

if __name__ == '__main__':
    unittest.main()
