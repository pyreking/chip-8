import pyaudio
import threading
import wave
import os
import time

class Speaker():
    CHUNK = 1024

    def __init__(self, path, loop = True):
        super(Speaker, self).__init__()
        self.loop = loop
        self.path = os.path.abspath(path)
    
    def play(self):
        wf = wave.open(self.path, 'rb')
        player = pyaudio.PyAudio()

        stream = player.open(format = player.get_format_from_width(wf.getsampwidth()), 
                             channels = wf.getnchannels(),
                             rate = wf.getframerate(),
                             output = True)

        data = wf.readframes(wf.getnframes())
        stream.write(data)

        
    
if __name__ == "__main__":
    speaker = Speaker("../sound/beep.wav")
    speaker.play()