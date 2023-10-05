import tkinter as tk
import speaker as sp
from collections import defaultdict

class KeyPad:
    KEYBOARD_BINDINGS = {
        49: 0x1, # 1
        50: 0x2, # 2
        51: 0x3, # 3
        52: 0xC, # 4
        81: 0x4, # Q
        87: 0x5, # W
        69: 0x6, # E
        82: 0xD, # R
        65: 0x7, # A
        83: 0x8, # S
        68: 0x9, # D
        70: 0xE, # F
        90: 0xA, # Z
        88: 0x0, # X
        67: 0xB, # C
        86: 0xF, # V
        }
    
    def __init__(self, window):
        self.keys_down = defaultdict(bool)
        self.on_next_key_down = None

        window.bind('<KeyPress>', self.on_key_down)
        window.bind('<KeyRelease>', self.on_key_up)
    
    def is_valid_scan_code(self, scan_code):
        return scan_code in self.KEYBOARD_BINDINGS

    def is_key_down(self, virtual_key):
        return self.keys_down[virtual_key]
    
    def on_key_down(self, event):
        scan_code = event.keycode

        if self.is_valid_scan_code(scan_code):
            virtual_key = self.KEYBOARD_BINDINGS[scan_code]
            self.keys_down[virtual_key] = True

            if self.on_next_key_down:
                self.on_next_key_down(virtual_key)
                self.on_next_key_down = None

    def on_key_up(self, event):
        scan_code = event.keycode

        if self.is_valid_scan_code(scan_code):
            virtual_key = self.KEYBOARD_BINDINGS[scan_code]
            self.keys_down[virtual_key] = False
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('300x200')

    keyboard = KeyPad(root)
    speaker = sp.Speaker("../sound/beep.wav")

    def on_next_key_down(scan_code):
        speaker.play()
                        
    keyboard.on_next_key_down = on_next_key_down

    root.mainloop()