import cpu
import screen as sc
import keypad as kp
import speaker as sp
import tkinter as tk


class Chip8(tk.Frame):
    FPS = 60

    def __init__(self, parent, scale, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        screen = sc.Screen(self, width = 64 * scale, height = 32 * scale,
                           bg="white", highlightthickness=0)
        
        screen.pack(fill=tk.BOTH, expand=tk.YES)
        
        keypad = kp.KeyPad(parent)
        speaker = sp.Speaker("../sound/beep.wav")

        self.comp = cpu.CPU(screen, keypad, speaker)

        self.comp.load_sprites_into_memory()
        self.comp.load_rom("../roms/PONG")
        self.step()

    def step(self):
        self.comp.cycle()
        self.after(int(1000 / Chip8.FPS), self.step)

if __name__ == "__main__":
    root = tk.Tk()
    emulator = Chip8(root, 18)
    emulator.pack(side="top", fill="both", expand=True)
    root.mainloop()