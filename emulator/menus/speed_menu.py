import tkinter as tk

class SpeedMenu(tk.Menu):
    def __init__(self, cpu, min_speed, max_speed):
        tk.Menu.__init__(self, tearoff=False)
        self.cpu = cpu
        self.radio_var = tk.IntVar(value = 1.0)
        self.create_speed_commands(min_speed, max_speed)

    def create_speed_commands(self, min_speed, max_speed):
        i = float(min_speed)

        while i <= max_speed:
            radio_label = str(int(i * 100)) + "%"
            func = lambda i0 = i: self.change_speed(speed = int(i0 * self.cpu.NORMAL_SPEED))
            self.add_radiobutton(label=radio_label, variable=self.radio_var, value=i, command=func)

            if i < 1:
                i *= 2
            else:
                i += 1
    
    def change_speed(self, speed):
        self.cpu.speed = speed