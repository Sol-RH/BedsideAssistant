# Captures the voice input 

import sounddevice as sd
import numpy as np 
import scipy.io.wavfile as wf
import queue 
import logging 
import time

logger = logging.getLogger(__name__)

class AudioRecorder:
    def __init__(self):
        self.rate= 16000
        self.channels= 1
        self.buffer= 1024 

        self.silence_thresh= 0.01 
        self.silence_dur= 2.0
        self.min_audio= 0.5 

        self.audio_queue= queue.Queue()

    def _callback(self, indata, time, status):
        if status:
            logger.warning(f"Status: {status}")
        self.audio_queue.put(indata.copy())
    
    #Logic to decide whether to "wake-up" or not
    def listen(self):
        logger.info("Listening ... ")

        audio_frames= []
        silence_start= None
        recording= False 

        with sd.InputStream(samplerate=self.rate, channels= self.channels, blocksize=self.buffer, callback= self._callback):
            while True: 
                data= self.audio_queue.get()
                volume= np.linalg.norm(data)/len(data)  #calculate the audio volume 

                #When the audio volume is higher than normal,  indicating a possible request, start recording
                if volume > self.silence_thresh:
                    if not recording: 
                        logger.info("Voice detected. I'll record it.")
                        recording= True 
                    silence_start= None 
                    audio_frames.append(data)

                #When silence > 2.0 is detected, stop recording:
                else:
                    if recording: 
                        if silence_start is None:
                            silence_start= time.time()
                    elif time.time() - silence_start > self.silence_dur:
                        logger.info("Silence detected. I'll stop recording now.")
                        break 
        audio= np.concatenate(audio_frames, axis= 0)
        duration= len(audio)/ self.rate 

        if duration < self.min_audio: 
            logger.info("Audio is too short. Ignoring...")
            return None 
        logger.info(f"Audio recorded")
        return audio 


if __name__== "__main":
    import logging 
    logging.basicConfig(level= logging.INFO, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    recorder= AudioRecorder()
    while True: 
        audio= recorder.listen
        if audio is not None:
            logger.info("Audio has been successfully captured :D")



        

        
