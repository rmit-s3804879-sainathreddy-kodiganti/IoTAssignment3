# Reference: https://pypi.org/project/SpeechRecognition/
# Reference: https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/

# pip3 install SpeechRecognition
# sudo apt-get install portaudio19-dev python-all-dev python3-all-dev
# pip3 install pyaudio
# pip3 install google-api-python-client
# sudo apt-get install flac

import speech_recognition as sr
import subprocess


class voice_rec:
    """This is the voice rec Class

    This is used to convert voice to text
    """
    __MIC_NAME = "USB PnP Sound Device: Audio (hw:1,0)"
    __SAMPLE_RATE = 48000
    __CHUNK_SIZE = 2048
    __TIMEOUT = 1.5
    __ENERGY_TRESHOLD = 4000
    __device_id = -1
    
    def __select_mircophone(self): 
        """This function is used to set the device ID 
        of the mic that we specifically want 
        to use to avoid ambiguity.
        """
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            print(microphone_name)
            if(microphone_name == self.__MIC_NAME):
                self.__device_id = i
                break
    
    def __text_to_speech(self): 
        """This function is used to record the audio
        and convert to text 

        :return: (String) converted text
        """
        self.__select_mircophone()
        # obtain audio from the microphone
        r = sr.Recognizer()
        r.energy_threshold = self.__ENERGY_TRESHOLD
        with sr.Microphone(device_index = self.__device_id, sample_rate = self.__SAMPLE_RATE, chunk_size = self.__CHUNK_SIZE) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            try:
                audio = r.listen(source, timeout =self.__TIMEOUT)
            except sr.WaitTimeoutError:
                return "Listening timed out whilst waiting for phrase to start"

        # recognize speech using Google Speech Recognition
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Error in understanding"
        except sr.RequestError as e:
            return "Error reaching google"
    
    def start(self):
        """This function is used to initaiate the voice_rec class.
        :return: (String)  converted text
        """
        text = self.__text_to_speech()
        return text
