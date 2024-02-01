![Chip-8 Emulator Window](https://i.imgur.com/FVkxUcl.png)

## Chip-8
This project implements the [Chip-8 virtual machine](https://en.wikipedia.org/wiki/CHIP-8) according to the technical reference written by Cowgod.

## User Manual

### Running the emulator
1. Open a console window.
2. run ``git clone https://github.com/pyreking/chip-8.git`` to clone this repository.
3. run ``cd chip-8/emulator`` to go to the project directory.
4. run ``python chip8.py`` to run the emulator.

### Opening a rom
1. Click ``File`` on the file menu and then click ``Open`` to load a rom.
2. Choose a rom from the ``chip-8/roms`` folder in the file browser and then click the ``Open`` button.

### Changing the default controls
1. Click ``Settings`` on the file menu and then click ``Preferences`` to change the default controls.
2. Click on the key that you want to remap and then press any button to set the new key binding.

## Default Controls
| Key | Chip-8 Key |
| -------- | ------- |
| 1 | 1|
| 2| 2|
| 3 | 3 |
| 4 | C |
| Q | 4 |
| W | 5 |
| E | 6 |
| R | D |
| A | 7 |
| S | 8 |
| D | 9 |
| F | E |
| Z | A |
| X | 0 |
| C | B |
| V | F |

## Keyboard shortcuts
| Option | Key Combination |
| -------- | ------- |
| Open | Ctrl+P|
| Load State|Ctrl+S|
| Save State|Ctrl+L|
| Exit|Ctrl+W|
| Pause/Unpause | Ctrl+P|
| Rewind|Ctrl+J|
| Fast Forward|Ctrl+K|
| Preferences|Ctrl+B|

## References

[CHIP-8 technical specification](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) by Cowgod.

[How to Create Your Very Own Chip-8 Emulator](https://www.freecodecamp.org/news/creating-your-very-own-chip-8-emulator/) by Eric Grandt.
