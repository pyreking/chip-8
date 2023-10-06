import pyaudio
import threading
import wave
import os
import time

class Speaker():
    CHUNK = 224

    def __init__(self, path):
        self.player = pyaudio.PyAudio()
        self.wf = wave.open(path, 'rb')

        self.stream = self.player.open(format = self.player.get_format_from_width(self.wf.getsampwidth()), 
                             channels = self.wf.getnchannels(),
                             rate = self.wf.getframerate(),
                             output = True)

    def play(self, chunk_size):
        data = self.wf.readframes(chunk_size)

        if data == b'':
            self.wf.rewind()
            data = self.wf.readframes(chunk_size)

        self.stream.write(data)
    
if __name__ == "__main__":
    speaker = Speaker("../sound/beep.wav")
    for i in range(30):
        speaker.play(224)