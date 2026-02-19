# Captures the voice input 

import sounddevice as sd
import numpy as np 
import scipy.io.wavfile as wf
import queue 

# Mic Configuration 
rate= 16000
channels= 1
buffer= 1024

silence_thresh= 0.01     # considering the hopsital room is mostly silent


silence_dur= 2.0    #silence after user stops talking
min_audio= 0.5      #minium audio duration

class AudioRecorder:
    def __init__(self, silence_thresh= silence_thresh):
        self.silence_thresh= silence_thresh
        self.rate= rate
        self.channels= channels 