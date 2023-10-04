import tkinter as tk
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
    
    def __init__(self):
        self.keys_down = defaultdict(bool)
        self.on_next_key_down = None
    
    def is_valid_scan_code(self, scan_code):
        return scan_code in self.KEYBOARD_BINDINGS

    def is_key_down(self, scan_code):
        return self.keys_down[scan_code]
    
    def on_key_down(self, event):
        scan_code = event.keycode

        if self.is_valid_scan_code(scan_code):
            self.keys_down[scan_code] = True

        if self.on_next_key_down and self.is_valid_scan_code(scan_code):
            self.on_next_key_down(scan_code)
            self.on_next_key_down = None
    
    def on_key_up(self, event):
        key_code = event.keycode

        if self.is_valid_scan_code(key_code):
            self.keys_down[key_code] = False
    
if __name__ == "__main__":
    root = tk.Tk()
    keyboard = KeyPad()
    root.geometry('300x200')
    root.bind('<KeyPress>', keyboard.on_key_down)
    root.bind('<KeyRelease>', keyboard.on_key_up)

    def on_next_key_down(scan_code):
        print("VIRTUAL KEY PRESSED: ", keyboard.KEYBOARD_BINDINGS[scan_code])
                        
    keyboard.on_next_key_down = on_next_key_down
    root.mainloop()