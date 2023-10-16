"""
cpu.py:

Implements a virtual CHIP-8 CPU for the emulator.
"""
import random
import numpy

class CPU:
    """A virtual CPU for the CHIP-8 interpreter.

    Attributes:
        screen: The virtual CHIP-8 display for the emulator.
        keypad: The virtual CHIP-8 keypad for the emulator.
        speaker: The virtual CHIP-8 speaker for the emulator.
        memory: A list of 4096 unsigned 8-bit integers representing the 4KB memory for the CPU.
        v: A list of 16 unsigned 8-bit integers representing the general purpose registers for the
        CPU.
        i: A 16-bit integer representing a register used to store memory addresses for the CPU.
        delay_timer: An unsigned 8-bit integer representing the virtual delay timer for the CPU.
        sound_timer: An unsigned 8-bit integer representing the virtual sound timer for the CPU.
        pc: An unsigned 8-bit integer representing the virtual program counter for the CPU.
        stack: A list of 16 unsigned 16-bit integers representing the virtual stack for the CPU.
        sp: An unsigned 4-bit integer representing the virtual stack pointer for the CPU.
        paused: A bool representing the pause state of the CPU. When True, the CPU stops
                processing instructions. When False, the CPU continues processing instructions.
        speed: The number of instructions to execute per CPU cycle (default = 10).
    """

    def __init__(self, screen, keypad, speaker):
        """Initializes a virtual CHIP-8 CPU.

        A virtual CPU for the CHIP-8 interpreter that reads ROMS and processes opcodes.

        Args:
            screen (Screen): The virtual CHIP-8 display for the emulator..
            keypad (Keypad): The virtual CHIP-8 keypad for the emulator.
            speaker (Speaker): The virtual CHIP-8 speaker for the emulator.
        """
        # The virtual screen for the emulator.
        self.screen = screen

        # The virtual keypad for the emulator.
        self.keypad = keypad

        # The virtual speaker for the emulator.
        self.speaker = speaker

        # A list of 4096 unsigned 8-bit integers representing the 4KB memory for the CPU.
        self.memory = numpy.array([0] * 4096, dtype=numpy.uint8)

        # An array of 16 unsigned 8-bit integers representing the general purpose
        # registers for the CPU.
        self.v = numpy.array([0] * 16, dtype=numpy.uint8)

        # An unsigned 16-bit integer representing a register used to
        # store memory addresses for the CPU.
        self.i = 0

        # An unsigned 8-bit integer representing the delay timer for the CPU.
        self.delay_timer = 0

        # An unsigned 8-bit integer representing the sound timer for the CPU.
        self.sound_timer = 0

        # An unsigned 8-bit integer representing the virtual program counter for the CPU.
        self.pc = 0x200

        # The virtual stack for the CPU.
        self.stack = numpy.array([0] * 16, dtype=numpy.uint16)

        # The virtual stack pointer for the CPU.
        self.sp = 0

        # Represents the pause state for the CPU.
        self.paused = False

        # The number of instructions to process per CPU cycle.
        self.speed = 10

    def load_sprites_into_memory(self):
        """Loads sprites into memory.

        Loads a list of 16 5-byte sprites representing the hexadecimal
        digits 0 through F into memory.

        Returns:
            voids
        """
        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        # Loads each sprite into memory.
        for idx, sprite in enumerate(sprites):
            self.memory[idx] = sprite

    def load_program_into_memory(self, program):
        """Loads a program into memory.

        Clears the program space and loads a new program into memory starting
        at memory address 0x200 and ending at memory address 0xFFF. Programs
        that exceed the 3KB file size limit will be shrunk down to the first
        3KB of the program.

        Args:
            program (list[uint8]): A list of unsigned 8-bit integers representing a CHIP-8 ROM.

        Returns:
            void
        """
        # Clear the program space
        self.clear_program_from_memory()

        # Enforce a 3KB file size limit
        file_size = min(len(program), 0xE00)

        # Copy the program into memory starting at memory address 0x200.
        for idx in range(file_size):
            self.memory[0x200 + idx] = program[idx]

    def clear_program_from_memory(self):
        """Clears a program from memory.

        Clears a program from memory by resetting the program space and all of the
        registers.

        Returns:
            void
        """

        # Reset the registers and program counter.
        self.i = 0
        self.v = numpy.array([0] * 16, dtype=numpy.uint8)
        self.delay_timer = 0
        self.sound_timer = 0
        self.pc = 0x200

        # Reset the stack and stack pointer.
        self.stack = numpy.array([0] * 16, dtype=numpy.uint16)
        self.sp = 0

        # Clear memory starting at memory address 0x200 and ending at
        # memory address 0xFFF.
        for idx in range(0xE00):
            self.memory[0x200 + idx] = 0

        # Clear the screen.
        self.screen.clear()

    def load_rom(self, path):
        """Loads a ROM into memory.

        Loads a ROM into memory with a max file size of 3 KB. If a ROM is bigger than
        3 KB, only the first 3 KB are loaded into memory.

        Args:
            path (str): The relative or absolute path to the ROM file.

        Returns:
            void
        """
        try:
            with open(path, "rb") as rom_file:
                # Read the bytes of the ROM file.
                program_bytes = rom_file.read()
                # Load the program as an array of unsigned 8-bit integers.
                program = numpy.frombuffer(program_bytes, dtype=numpy.uint8)
                # Load the program into memory.
                self.load_program_into_memory(program)
        except FileNotFoundError:
            # Throw an error if the file does not exist.
            print(f"No such file or directory: {path}")

    def cycle(self):
        """Cycles the virtual CHIP-8 CPU.

        Cycles the CPU by processing a number of instructions depending on the speed
        that it is running at. Renders the frame buffer after all of the instructions are
        processed.

        Returns:
            void
        """

        for _ in range(self.speed):
            if not self.paused:
                # Find the next 2-byte opcode.
                # Pads the first 8-bit instruction to 16 bits and ORs it with
                # the next 8-bit instruction.
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]

                # Executes the next instruction.
                self.execute_instruction(opcode)

        # Update the delay and sound timers when the CPU is running.
        if not self.paused:
            self.update_timers()

        # Play sound from the speaker.
        self.play_sound()

        # Render the frame buffer to the screen.
        self.screen.render()

    def execute_instruction(self, opcode):
        """Executes an instruction.

        Parses and executes a 16-bit instruction. There are 36 valid instructions that
        the CPU can parse and execute. Throws a ValueError if the instruction is invalid.

        Args:
            opcode (int): An unsigned 16-bit integer representing the instruction
            to execute.

        Returns:
            void
        """
        # Advance the program counter by 2.
        self.pc += 2

        # The lower 4 bits of the high byte of the instruction.
        x = (opcode & 0x0F00) >> 8

        # The upper 4 bits of the low byte of the instruction.
        y = (opcode & 0x00F0) >> 4

        # Parse the instruction.
        match (opcode & 0xF000):
            case 0x0000:
                match opcode:
                    case 0x00E0:
                        #
                        # 00E0 - CLS
                        #
                        # Clear the display.
                        self.screen.clear()
                    case 0x00EE:
                        #
                        # 00EE - RET
                        #
                        # Return from subroutine.
                        self.pc = self.stack[self.sp]
                        self.sp -= 1

            case 0x1000:
                #
                # 1nnn - JP addr
                #
                # Jump to location nnn.
                self.pc = opcode & 0x0FFF

            case 0x2000:
                #
                # 2nnn - CALL addr
                #
                # Call subroutine at nnn.
                self.sp += 1
                self.stack[self.sp] = self.pc
                self.pc = opcode & 0x0FFF

            case 0x3000:
                #
                # 3xkk - SE Vx, byte
                #
                # Skip next instruction if Vx = kk.
                lowest_byte = opcode & 0x00FF

                if self.v[x] == lowest_byte:
                    self.pc += 2

            case 0x4000:
                #
                # 4xkk - SNE Vx, byte
                #
                # Skip next instruction if Vx != kk.
                lowest_byte = opcode & 0x00FF

                if self.v[x] != lowest_byte:
                    self.pc += 2

            case 0x5000:
                #
                # 5xkk - SE Vx, Vy
                #
                # Skip next instruction if Vx = Vy.
                if self.v[x] == self.v[y]:
                    self.pc += 2

            case 0x6000:
                #
                # 6xkk - LD Vx, byte
                #
                # Set Vx = kk.
                lowest_byte = opcode & 0x00FF
                self.v[x] = lowest_byte

            case 0x7000:
                #
                # 7xkk - ADD Vx, byte
                #
                # Set Vx = Vx + kk.
                lowest_byte = opcode & 0x00FF
                self.v[x] += lowest_byte

            case 0x8000:
                match (opcode & 0x000F):
                    case 0x0:
                        #
                        # 8xy0 - LD Vx, Vy
                        #
                        # Set Vx = Vy.
                        self.v[x] = self.v[y]

                    case 0x1:
                        #
                        # 8xy1 - OR Vx, Vy
                        #
                        # Set Vx = Vx OR Vy.
                        self.v[x] |= self.v[y]

                    case 0x2:
                        #
                        # 8xy2 - AND Vx, Vy
                        #
                        # Set Vx = Vx AND Vy.
                        self.v[x] &= self.v[y]

                    case 0x3:
                        #
                        # 8xy3 - XOR Vx, Vy
                        #
                        # Set Vx = Vx XOR Vy.
                        self.v[x] ^= self.v[y]

                    case 0x4:
                        #
                        # 8xy4 - ADD Vx, Vy
                        #
                        # Set Vx = Vx + Vy, set VF = carry.
                        total = self.v[x] + self.v[y]
                        self.v[0xF] = 0

                        if total > 0xFF:
                            self.v[0xF] = 1

                        self.v[x] = total

                    case 0x5:
                        #
                        # 8xy5 - SUB Vx, Vy
                        #
                        # Set Vx = Vx - Vy, set VF = NOT borrow.
                        self.v[0xF] = 0

                        if self.v[x] > self.v[y]:
                            self.v[0xF] = 1

                        self.v[x] -= self.v[y]

                    case 0x6:
                        #
                        # 8xy6 - SHR Vx {, Vy}
                        #
                        # Set Vx = Vx SHR 1.
                        self.v[0xF] = self.v[x] & 0x1
                        self.v[x] >>= 1

                    case 0x7:
                        #
                        # 8xy7 - SUBN Vx, Vy
                        #
                        # Set Vx = Vy - Vx, set VF = NOT borrow.
                        self.v[0xF] = 0

                        if self.v[y] > self.v[x]:
                            self.v[0xF] = 1

                        self.v[x] = self.v[y] - self.v[x]

                    case 0xE:
                        #
                        # 8xyE - SHL Vx {, Vy}
                        #
                        # Set Vx = Vx SHL 1.
                        self.v[0xF] = (self.v[x] & 0x80) >> 0x07
                        self.v[x] <<= 1

            case 0x9000:
                #
                # 9xy0 - SNE Vx, Vy
                #
                # Skip next instruction if Vx != Vy.
                if self.v[x] != self.v[y]:
                    self.pc += 2

            case 0xA000:
                #
                # Annn - LD I, addr
                #
                # Set I = nnn.
                self.i = opcode & 0x0FFF

            case 0xB000:
                #
                # Bnnn - JP V0, addr
                #
                # Jump to location nnn + V0.
                self.pc = (opcode & 0x0FFF) + self.v[0x0]

            case 0xC000:
                #
                # Cxkk - RND Vx, byte
                #
                # Set Vx = random byte AND kk.
                random_byte = random.randint(0x00, 0xFF)
                lowest_byte = opcode & 0x00FF

                self.v[x] = random_byte & lowest_byte

            case 0xD000:
                #
                # Dxyn - DRW Vx, Vy, nibble
                #
                # Display n-byte sprite starting at memory location I at (Vx, Vy),
                # set VF = collision.
                width = 8
                height = opcode & 0xF
                self.v[0xF] = 0

                for row in range(height):
                    sprite = self.memory[self.i + row]

                    for col in range(width):
                        if sprite & 0x80:
                            x_pos = self.v[x] + col
                            y_pos = self.v[y] + row
                            self.v[0xF] = self.screen.set_pixel(x_pos, y_pos)

                        sprite <<= 1

            case 0xE000:
                match (opcode & 0xFF):
                    case 0x9E:
                        #
                        # Ex9E - SKP Vx
                        #
                        # Skip next instruction if key with the value of Vx is pressed.
                        if self.keypad.is_key_down(self.v[x]):
                            self.pc += 2

                    case 0xA1:
                        #
                        # ExA1 - SKP Vx
                        #
                        # Skip next instruction if key with the value of Vx is not pressed.
                        if not self.keypad.is_key_down(self.v[x]):
                            self.pc += 2

            case 0xF000:
                match (opcode & 0xFF):
                    case 0x07:
                        #
                        # Fx07 - LD Vx, DT
                        #
                        # Set Vx = delay timer value.
                        self.v[x] = self.delay_timer

                    case 0x0A:
                        #
                        # Fx0A - LD Vx, K
                        #
                        # Wait for a key press, store the value of the key in Vx.
                        self.paused = True

                        def on_next_key_down(virtual_key):
                            self.v[x] = virtual_key
                            self.paused = False

                        self.keypad.on_next_key_down = on_next_key_down

                    case 0x15:
                        #
                        # Fx15 - LD DT, Vx
                        #
                        # Set delay timer = Vx.
                        self.delay_timer = self.v[x]

                    case 0x18:
                        #
                        # Fx18 - LD ST, Vx
                        #
                        # Set sound timer = Vx.
                        self.sound_timer = self.v[x]

                    case 0x1E:
                        #
                        # Fx1E - ADD I, Vx
                        #
                        # Set I = I + Vx.
                        self.i += self.v[x]

                    case 0x29:
                        #
                        # Fx29 - LD F, Vx
                        #
                        # Set I = location of sprite for digit Vx.
                        self.i = self.v[x] * 0x5

                    case 0x33:
                        #
                        # Fx33 - LD B, Vx
                        #
                        # Store BCD representation of Vx in memory locations I, I+1, and I+2.
                        decimal = self.v[x]

                        for idx in range(3):
                            digit = decimal % 10
                            self.memory[self.i + idx] = digit
                            decimal /= 10

                    case 0x55:
                        #
                        # Fx55 - LD [I], Vx
                        #
                        # Store registers V0 through Vx in memory starting at location I.
                        for idx in range(0x0, x + 0x1):
                            self.memory[self.i + idx] = self.v[idx]

                    case 0x65:
                        #
                        # Fx65 - LD Vx, [I]
                        #
                        # Read registers V0 through Vx from memory starting at location I.
                        for idx in range(0x0, x + 0x1):
                            self.v[idx] = self.memory[self.i + idx]
            case _:
                raise ValueError(f"Invalid opcode: {opcode}")

    def play_sound(self):
        """Plays sound out of the virtual CHIP-8 speaker.

        Plays a beeping sound out of the virtual CHIP-8 speaker for 1/60th of a second.

        Returns:
            void
        """
        if self.sound_timer > 0:
            self.speaker.play(224)

    def update_timers(self):
        """Updates the delay and sound timers.

        Decrements the delay timer if it is greater than 0.
        Decrements the sound timer if it is greater than 0.

        Returns:
            void
        """
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1