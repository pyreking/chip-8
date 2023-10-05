import cpu
import screen as sc
import keypad as kp
import speaker as sp
import tkinter as tk


class Chip8:
    FPS = 60

    def __init__(self, scale = 1):
        self.window = tk.Tk()
        self.screen = sc.Screen(self.window, 15)
        self.keypad = kp.KeyPad(self.window)
        self.speaker = sp.Speaker("../sound/beep.wav")
        self.comp = cpu.CPU(self.screen, self.keypad, self.speaker)
        self.comp.load_sprites_into_memory()
        self.comp.load_rom("../roms/PONG")
        self.step()
        self.window.mainloop()

    def step(self):
        self.comp.cycle()
        self.window.after(int(1000 / 60), self.step)

if __name__ == "__main__":
    emulator = Chip8()