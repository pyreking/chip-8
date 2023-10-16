"""
speaker.py:

Implements a virtual CHIP-8 speaker for the emulator.

The test program loads an audio file and plays it.
"""

import wave as wav
import pyaudio as py

class Speaker():
    """A virtual speaker for the CHIP-8 interpreter.

    Attributes:
        wav:  A wave.Wave_read object that can read frames of an audio file.
        stream: A PyAudio.Stream object that play frames of an audio file.
    """

    def __init__(self, path):
        """Initializes a virtual CHIP-8 speaker.

        A virtual speaker that can play frames of an audio file.

        Args:
            path (str): The relative or absolute path to a WAV file.
        """
        # Set up a new audio player.
        self.player = py.PyAudio()
        # Open the WAV file.
        self.wav = wav.open(path, 'rb')

        # Create a new audio stream that can play the loaded WAV file.
        self.stream = self.player.open(format=self.player.get_format_from_width(
                                    self.wav.getsampwidth()),
                                  channels=self.wav.getnchannels(),
                                  rate=self.wav.getframerate(),
                                  output=True)

    def play(self, chunk_size):
        """Plays the next chunk of a WAV file.

        Plays the next chunk of a WAV file. Rewinds the WAV file when the
        stream ends.

        Args:
            chunk_size (int): The number of frames of the WAV file to play.

        Returns:
            void
        """
        # Read the next chunk of the WAV file.
        data = self.wav.readframes(chunk_size)

        if data == b'':
            # Rewind the WAV file when the stream ends.
            self.wav.rewind()
            data = self.wav.readframes(chunk_size)

        # Play the next chunk of the WAV file.
        self.stream.write(data)

    def close(self):
        """Closes the audio stream.

        Closes the audio stream and releases PortAudio resources. This
        will make the virtual CHIP-8 speaker unusable.

        Returns:
            void
        """
        # Close the audio stream.
        self.stream.close()
        # Release PortAudio resources.
        self.player.terminate()

if __name__ == "__main__":
    # A test program for the virtual CHIP-8 speaker.
    #
    # Creates a virtual CHIP-8 speaker. Plays a small
    # chunk of a WAV file and closes the audio stream.

    # Create a virtual speaker.
    speaker = Speaker("../../sound/beep.wav")

    # Play a small chunk of the WAV file.
    for i in range(30):
        speaker.play(224)

    # Close the audio stream.
    speaker.close()
