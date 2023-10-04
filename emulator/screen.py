from tkinter import *
import keypad

class Screen:
    WIDTH = 64
    HEIGHT = 32
    X_OFFSET = 0
    Y_OFFSET = 0

    def __init__(self, scale = 1):
        self.display = [0] * self.WIDTH * self.HEIGHT
        
        self.scale = scale
        self.scaled_w = Screen.WIDTH * self.scale
        self.scaled_h = Screen.HEIGHT * self.scale
        
        self.window = Tk()
        self.window.title("Chip-8")

        self.window.geometry(f'{self.scaled_w}x{self.scaled_h}+{Screen.X_OFFSET}+{Screen.Y_OFFSET}')
        self.canvas = Canvas(self.window, bg="white", height = self.scaled_h, width = self.scaled_w)
        self.canvas.pack()

    def set_pixel(self, x, y):
        if x > Screen.WIDTH:
            x -= Screen.WIDTH
        elif x < 0:
            x += Screen.WIDTH
        
        if y > Screen.HEIGHT:
            y -= Screen.HEIGHT
        elif y < 0:
            y += Screen.HEIGHT
        
        pixel_loc = x + (y * self.WIDTH)
        self.display[pixel_loc] ^= 1

        return not self.display[pixel_loc]
    
    def clear(self):
        self.display = [0] * self.WIDTH * self.HEIGHT
    
    def render(self):
        self.canvas.delete('all')

        for i in range(0, self.WIDTH * self.HEIGHT):
            x = i % self.WIDTH
            y = i // self.WIDTH

            if self.display[i]:
                self.canvas.create_rectangle(x * self.scale, y * self.scale,
                                             (x + 1) * self.scale, (y + 1) * self.scale,
                                             fill = "black", outline="blue")

    def test_render(self):
        for i in range(0, self.WIDTH * self.HEIGHT):
            self.set_pixel(i % self.WIDTH, i // self.WIDTH)

        self.render()

if __name__ == "__main__":
    screen = Screen(15)

    keyboard = keypad.KeyPad()

    screen.window.bind('<KeyPress>', keyboard.on_key_press)
    screen.window.bind('<KeyRelease>', keyboard.on_key_release)

    screen.test_render()
    screen.window.mainloop()