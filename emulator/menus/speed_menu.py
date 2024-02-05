"""
speed_menu.py:

Implements a menu for changing the default emulation speed.
"""
import tkinter as tk


class SpeedMenu(tk.Menu):
    """A menu for changing the default emulation speed.

    Attributes:
        none
    """

    def __init__(self, cpu, min_speed, max_speed):
        """Initializes a menu for changing the default emulation speed.

        A menu that can change the default emulation speed for the
        emulator. The options are automatically created based on
        the min_speed and max_speed values and are scalar values
        of the normal emulation speed.

        Args:
            cpu (CPU): A virtual CHIP-8 CPU.
            min_speed (int): The minimum scalar speed option for the menu in the range [0, inf).
            max_speed (int): The maximum scalar speed option for the menu in the range [0, inf).
        """
        tk.Menu.__init__(self, tearoff=False)
        self.cpu = cpu
        self.radio_var = tk.IntVar(value=1.0)
        self.create_speed_commands(min_speed, max_speed)

    def create_speed_commands(self, min_speed, max_speed):
        """Creates radio buttons for changing the default
        emulation speed.

        Creates radio buttons for changing the default emulation speed
        based on the min_speed and max_speed values set by the user.
        All radio buttons are scalar values of the normal emulation
        speed.

        The scalar value for each option doubles in size until it reaches the normal
        emulation speed. Afterwards, the scalar value increases linearly until the max
        speed has been reached.

        Args:
            cpu (CPU): A virtual CHIP-8 CPU.
            min_speed (int): The minimum speed option for the menu in the range [0, inf).
            max_speed (int): The maximum speed option for the menu in the range [0, inf).
        """
        i = float(min_speed)

        while i <= max_speed:
            # Create the radio label
            radio_label = str(int(i * 100)) + "%"
            # Assign a function to each radio button so that the emulation speed
            # changes when it is selected.
            func = lambda i0 = i: self.change_speed(speed = int(i0 * self.cpu.NORMAL_SPEED))
            self.add_radiobutton(label=radio_label, variable=self.radio_var, value=i, command=func)

            if i < 1:
                i *= 2
            else:
                i += 1

    def change_speed(self, speed):
        """Changes the default emulation speed.

        Args:
            speed (int): The new emulation speed in instructions per cycle.

        Returns:
            void
        """
        self.cpu.speed = speed
