import tkinter as tk
from tkinter import PhotoImage
from menus.options.game_options import GameOptions
import pickle
import gzip
import menus.speed_menu as sm

class GameMenu(tk.Menu):
    def __init__(self, parent, cpu):
        tk.Menu.__init__(self, tearoff=False)
        self.parent = parent
        self.cpu = cpu

        self.fast_forward_icon = PhotoImage(file="icons/fast_forward.png")
        self.rewind_icon = PhotoImage(file="icons/rewind.png")
        self.pause_icon = PhotoImage(file="icons/pause.png")

        self.speed_menu = sm.SpeedMenu(self.cpu, 0.25, 3)

        self.add_command(
            label="Pause", command=self.on_pause, accelerator="Ctrl+P", state="disabled")
        
        self.add_command(
            label="Rewind", command=self.on_rewind, accelerator="Ctrl+J", state="disabled")
        
        self.add_command(
            label="Fast Forward", command=self.on_fast_forward, accelerator="Ctrl+K", state="disabled")
        
        self.add_cascade(label="Speed", menu = self.speed_menu)
        
        parent.bind("<Control-j>", self.on_rewind)
        parent.bind("<Control-k>", self.on_fast_forward)
        parent.bind("<Control-KeyRelease-j>", self.off_rewind)
        parent.bind("<Control-KeyRelease-k>", self.off_fast_forward)
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
        status = self.cpu.paused

        # Update the pause menu option with the correct label.
        self.entryconfig(GameOptions.PAUSE, label=GameOptions.PAUSE_LABELS[status])

        if status:
            self.cpu.screen.create_image(20,20,image=self.pause_icon, tag="pause")
        else:
            self.cpu.screen.delete("pause")

        # Cycle the CPU if it is not paused.
        self.cpu.step()

    def on_fast_forward(self, event = None):
        if self.cpu.speed != self.cpu.FAST_SPEED:
            self.cpu.screen.create_image(20,20,image=self.fast_forward_icon, tag="fast_forward")
        
        self.cpu.speed = self.cpu.FAST_SPEED
    
    def off_fast_forward(self, event = None):
        self.cpu.speed = self.cpu.NORMAL_SPEED
        self.cpu.screen.delete("fast_forward")

    def on_rewind(self, event = None):
        if not self.cpu.paused:
            self.cpu.screen.create_image(20,20,image=self.rewind_icon, tag="rewind")
        
        if len(self.cpu.rewind_buffer) > 0:
            self.cpu.paused = True
            pickle_bytes = gzip.decompress(self.cpu.rewind_buffer.pop())
            state = pickle.loads(pickle_bytes)
            self.cpu.load_state(state)
    
    def off_rewind(self, event = None):
        self.cpu.screen.delete("rewind")
        self.cpu.paused = False
        self.cpu.step()