"""
screen.py:

Implements a virtual CHIP-8 display for the emulator.

The test program creates a virtual CHIP-8 display and renders every other pixel to the screen.
"""

import tkinter as tk

class Screen(tk.Canvas):
    """A virtual display for the CHIP-8 interpreter.

    Attributes:
        display: An array that tracks the pixels that have been turned on.
        scale_factor: An integer representing the scale factor for the display.
    """
    # The unscaled width for the diplay.
    WIDTH = 64
    # The unscaled height for the display.
    HEIGHT = 32

    def __init__(self, parent, **kwargs):
        """Initializes a virtual CHIP-8 display.

        A virtual display for the CHIP-8 interpreter that can render pixels to the screen.
 
        Args:
            parent (tkinter.Tk): The parent window for the display.
            kwargs (dict[str, Any]): Packing arguments inherited from the superclass. 
        """
        # Initialize the tkinter canvas.
        tk.Canvas.__init__(self, parent, **kwargs)

        # Set the parent window.
        self.parent = parent

        # A virtual display of pixels as an integer array.
        # 0 = pixel off
        # 1 = pixel on
        self.display = set()

        # Set the default scale factor based on the current window width.
        self.scale_factor = self.winfo_reqwidth() // Screen.WIDTH

        # Call the resize function when the window is resized.
        self.bind("<Configure>", self.on_resize)

    def set_pixel(self, x_loc, y_loc):
        """Set a pixel on the virtual CHIP-8 display.

        Turns on a pixel on the virtual CHIP-8 display at (x, y) when the pixel is off.
        Otherwise, turn the pixel off. 
 
        Args:
            x_loc (int): The x-coordinate of the pixel to turn on or off.
            y_loc (int): The y-coordinate of the pixel to turn on or off.

        Returns:
            bool: Returns true if a pixel was turned off. Returns False otherwise.  
        """
        # Wrap the x coordinate to the opposite side of the screen
        # if it is out of bounds.
        if x_loc >= Screen.WIDTH:
            x_loc -= Screen.WIDTH
        elif x_loc < 0:
            x_loc += Screen.WIDTH

        # Wrap the y coordinate to the opposite side of the screen
        # if it is out of bounds.
        if y_loc >= Screen.HEIGHT:
            y_loc -= Screen.HEIGHT
        elif y_loc < 0:
            y_loc += Screen.HEIGHT

        # Find the position of the pixel in the virtual display.
        pixel_loc = x_loc + (y_loc * self.WIDTH)

        # Turns on the pixel if it is not turned on.
        # Otherwise, turn it off.
        if pixel_loc not in self.display:
            self.display.add(pixel_loc)
        else:
            self.display.remove(pixel_loc)

        # Returns True if a pixel was turned off.
        return pixel_loc not in self.display

    def on_resize(self, event):
        """Fires when the screen is resized.

        This function is fired when the screen
        is resized. Calculates the new scale
        factor and rerenders the dipaly.

        Args:
            event (tkinter.Event): A Configure event.
        
        Returns:
            void
        """
        self.scale_factor = event.width // Screen.WIDTH
        self.render()

    def clear(self):
        """Clears the virtual CHIP-8 display.
 
        Returns:
            void
        """
        self.display = set()

    def render(self):
        """Renders the virtual CHIP-8 display.
 
        Clears the drawn pixels from the display and draws the pixels that are
        turned on in the virtual CHIP-8 diplay.

        Returns:
            void
        """
        # Delete any pixels that have been drawn on the canvas.
        self.delete('on')


        # Draws a pixel on the virtual display if it is turned on.
        # The pixel is scaled based on the current scale factor.
        
        for i in self.display:
            # Find the x and y coordinates for the current pixel.
            x_loc = i % self.WIDTH
            y_loc = i // self.WIDTH

            # Draw the current pixel.
            self.create_rectangle(x_loc * self.scale_factor, y_loc * self.scale_factor,
                                    (x_loc + 1) * self.scale_factor,
                                    (y_loc + 1) * self.scale_factor,
                                    fill = "black", outline="black", tags="on")

    def test_render(self):
        """Tests the rendering of the virtual CHIP-8 display.

        Turns on every other pixel on the virtual CHIP-8 display and renders
        them.
 
        Returns:
            void
        """
        # Turns on every other pixel.
        for i in range(0, Screen.WIDTH * Screen.HEIGHT, 2):
            self.set_pixel(i % Screen.WIDTH, i // Screen.WIDTH)

        # Render the display.
        self.render()

if __name__ == "__main__":
    # A test program for the virtual CHIP-8 display.
    #
    # Creates a virtual CHIP-8 display and binds it to a new window. Renders
    # every other pixel to the screen.

    # Create a new window.
    root = tk.Tk()
    root_frame = tk.Frame(root)
    root_frame.pack(fill=tk.BOTH, expand=tk.YES)

    # Create a virtual CHIP-8 display.
    screen = Screen(root_frame, width=64*18, height=32*18, bg="white", highlightthickness=0)
    screen.pack(fill=tk.BOTH, expand=tk.YES)

    # Test the display.
    screen.test_render()

    # Start the main GUI loop.
    root.mainloop()
