import tkinter as tk
import keypad
import random

class Screen(tk.Canvas):
    WIDTH = 64
    HEIGHT = 32
    X_OFFSET = 0
    Y_OFFSET = 0

    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.display = [0] * 2048
        self.scale_factor = self.winfo_reqwidth() // Screen.WIDTH
        self.bind("<Configure>", self.on_resize)

    def set_pixel(self, x, y):
        if x >= Screen.WIDTH:
            x -= Screen.WIDTH
        elif x < 0:
            x += Screen.WIDTH
        
        if y >= Screen.HEIGHT:
            y -= Screen.HEIGHT
        elif y < 0:
            y += Screen.HEIGHT
        
        pixel_loc = x + (y * self.WIDTH)
        self.display[pixel_loc] ^= 1

        return not self.display[pixel_loc]
    
    def on_resize(self, event):
        self.scale_factor = event.width // Screen.WIDTH
        self.render()
    
    def clear(self):
        self.display = [0] * self.WIDTH * self.HEIGHT
    
    def render(self):
        self.delete('on')

        for i in range(0, self.WIDTH * self.HEIGHT):
            x = i % self.WIDTH
            y = i // self.WIDTH

            if self.display[i]:
                self.create_rectangle(x * self.scale_factor, y * self.scale_factor,
                                             (x + 1) * self.scale_factor, (y + 1) * self.scale_factor,
                                             fill = "black", outline="black", tags="on")
                
    def test_render(self):
        for i in range(0, 2048, 2):
            self.set_pixel(i % Screen.WIDTH, i // Screen.WIDTH)
        
        self.render()

if __name__ == "__main__":
    root = tk.Tk()
    root_frame = tk.Frame(root)
    root_frame.pack(fill=tk.BOTH, expand=tk.YES)
    screen = Screen(root_frame, width=64*18, height=32*18, bg="white", highlightthickness=0)
    screen.pack(fill=tk.BOTH, expand=tk.YES)
    screen.test_render()
    root.mainloop()