import cpu
import screen as sc
import keypad as kp
import speaker as sp
import tkinter as tk


class Chip8:
    FPS = 60

    def __init__(self, scale = 18):
        self.root = tk.Tk()
        root_frame = tk.Frame(self.root)
        root_frame.pack(fill=tk.BOTH, expand=tk.YES)
        screen = sc.Screen(root_frame, width = 64 * scale, height = 32 * scale,
                           bg="white", highlightthickness=0)
        screen.pack(fill=tk.BOTH, expand=tk.YES)
        
        keypad = kp.KeyPad(self.root)
        speaker = sp.Speaker("../sound/beep.wav")

        self.comp = cpu.CPU(screen, keypad, speaker)
        self.comp.load_sprites_into_memory()
        self.comp.load_rom("../roms/PONG")
        self.step()
        self.root.mainloop()

    def step(self):
        self.comp.cycle()
        self.root.after(int(1000 / 60), self.step)

if __name__ == "__main__":
    emulator = Chip8()