import tkinter as tk
from menus.options.game_options import GameOptions
import pickle
import gzip

class GameMenu(tk.Menu):
    def __init__(self, cpu, step, parent):
        tk.Menu.__init__(self, tearoff=False)
        self.cpu = cpu
        self.step = step
        self.parent = parent

        self.add_command(
            label="Pause", command=self.on_pause, accelerator="Ctrl+P", state="disabled")
        
        self.add_command(
            label="Rewind", command=self.on_rewind, accelerator="J", state="disabled")
        
        self.add_command(
            label="Fast Forward", command=self.on_fast_forward, accelerator="K", state="disabled")
        
        parent.bind("<KeyPress-j>", self.on_rewind)
        parent.bind("<KeyPress-k>", self.on_fast_forward)
        parent.bind("<KeyRelease-j>", self.off_rewind)
        parent.bind("<KeyRelease-k>", self.off_fast_forward)
        parent.bind("<Control-p>", self.on_pause)

    def on_pause(self, event = None):
        """Fires when the pause option is selected from the menu.

        This function is fired when the pause option
        is selected from the menu. Pauses the CPU when it is running.
        Otherwise, it unpauses the CPU.

        Returns:
            void
        """
        # Pause or unpause the CPU.
        self.cpu.paused ^= 1

        # Get the pause status from the CPU.
        idx = self.cpu.paused

        # Update the pause menu option with the correct label.
        self.entryconfig(GameOptions.PAUSE, label=GameOptions.PAUSE_LABELS[idx])

        # Cycle the CPU if it is not paused.
        self.step()

    def on_fast_forward(self, event = None):
        self.cpu.speed = 30
    
    def off_fast_forward(self, event = None):
        self.cpu.speed = 10

    def on_rewind(self, event = None):
        if len(self.cpu.rewind_buffer) > 0:
            self.cpu.paused = True
            pickle_bytes = gzip.decompress(self.cpu.rewind_buffer.pop())
            state = pickle.loads(pickle_bytes)
            self.cpu.load_state(state)
    
    def off_rewind(self, event = None):
        self.cpu.paused = False
        self.step()   