"""
game_options.py:

Create symbolic constants for the options in the game menu.
"""

class GameOptions:
    """A list of options for the game menu.

    An enum class that reperesents the options availiable for the game menu.
    """
    # The labels for the pause option.
    PAUSE_LABELS = ["Pause", "Unpause"]
    PAUSE = 0
    REWIND = 1
    FAST_FORWARD = 2
