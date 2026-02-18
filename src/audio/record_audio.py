# Captures the voice input 

import sounddevice as sd
import numpy as np 
import scipy.io.wavfile as wf
import queue 
import logging 



class AudioRecorder:
    def __init__(self):
        self.rate= 16000
        self.channels= 1
        self.buffer= 1024 

        self.silence_thresh= 0.01 
        self.silence_dur= 2.0
        self.min_audio= 0.5 

        self.audio_queue= queue.Queue()

    def _callback():
        pass 
