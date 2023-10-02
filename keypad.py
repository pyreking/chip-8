import tkinter as tk
from collections import defaultdict

class KeyPad:
    KEY_BINDINGS = {
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
    
    def __init__(self):
        self.pressed = defaultdict(bool)
        self.on_next_key_press = None
    
    def is_valid(self, key_code):
        return key_code in self.KEY_BINDINGS

    def is_key_pressed(self, key_code):
        return self.pressed[key_code]
    
    def on_key_press(self, event):
        key_code = event.keycode

        if self.is_valid(key_code):
            self.pressed[key_code] = True
            print(self.pressed)
        
        if self.is_valid(key_code) and not self.on_next_key_press:
            self.on_next_key_press = None
            # call function not defined yet
    
    def on_key_release(self, event):
        key_code = event.keycode

        if self.is_valid(key_code):
            self.pressed[key_code] = False
            print(self.pressed)
    
if __name__ == "__main__":
    root = tk.Tk()
    keyboard = KeyPad()
    root.geometry('300x200')
    root.bind('<KeyPress>', keyboard.on_key_press)
    root.bind('<KeyRelease>', keyboard.on_key_release)
    root.mainloop()