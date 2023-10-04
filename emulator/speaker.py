import pyaudio
import threading
import wave
import os

class Speaker(threading.Thread):
    CHUNK = 1024

    def __init__(self, path, loop = True):
        super(Speaker, self).__init__()
        self.loop = loop
        self.path = os.path.abspath(path)
    
    def run(self):
        wf = wave.open(self.path, 'rb')
        player = pyaudio.PyAudio()

        stream = player.open(format = player.get_format_from_width(wf.getsampwidth()), 
                             channels = wf.getnchannels(),
                             rate = wf.getframerate(),
                             output = True)

        data = wf.readframes(self.CHUNK)

        while self.loop:
            stream.write(data)
            data = wf.readframes(self.CHUNK)
            if data == b'':
                wf.rewind()
                data = wf.readframes(self.CHUNK)

    def play(self):
        self.start()

    def stop(self) :
        self.loop = False
    
if __name__ == "__main__":
    speaker = Speaker("../sound/beep.wav")
    speaker.play()