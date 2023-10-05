import screen as sc
import keypad as kp
import speaker as sp
import random
import numpy
import tkinter as tk

class CPU:

    def __init__(self, screen, keypad, speaker):
        self.screen = screen
        self.keypad = keypad
        self.speaker = speaker
        self.memory = numpy.array([0] * 4096, dtype=numpy.uint8)

        self.v = numpy.array([0] * 16, dtype=numpy.uint8)
        self.i = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.pc = 0x200

        self.stack = []

        self.paused = False
        self.speed = 10
    
    def load_sprites_into_memory(self):
        sprites = [
        0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
        0x20, 0x60, 0x20, 0x20, 0x70, # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
        0x90, 0x90, 0xF0, 0x10, 0x10, # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
        0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        for idx in range(len(sprites)):
            self.memory[idx] = sprites[idx]
    
    def load_program_into_memory(self, program):
        for idx in range(len(program)):
            self.memory[0x200 + idx] = program[idx]

    def load_rom(self, path):
        try:
            with open(path, "rb") as rom_file:
                bytes = rom_file.read()
                program = numpy.frombuffer(bytes, dtype=numpy.uint8)
                self.load_program_into_memory(program)
        except FileNotFoundError as e:
            print(f"No such file or directory: {path}")

    def cycle(self):
        for _ in range(self.speed):
            if not self.paused:
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
                self.execute_instruction(opcode)
        
        if not self.paused:
            self.update_timers()
        
        self.play_sound()
        self.screen.render()
    
    def execute_instruction(self, opcode):
        self.pc += 2
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        match (opcode & 0xF000):
            case 0x0000:
                match opcode:
                    case 0x00E0:
                        """
                        00E0 - CLS

                        Clear the display.
                        """
                        self.screen.clear()
                    case 0x00EE:
                        """
                        00EE - RET

                        Return from subroutine.
                        """
                        self.pc = self.stack.pop()

            case 0x1000:
                """
                1nnn - JP addr

                Jump to location nnn.
                """
                self.pc = opcode & 0x0FFF

            case 0x2000:
                """
                2nnn - CALL addr

                Call subroutine at nnn.
                """
                self.stack.append(self.pc)
                self.pc = opcode & 0x0FFF

            case 0x3000:
                """
                3xkk - SE Vx, byte

                Skip next instruction if Vx = kk.
                """
                lowest_byte = opcode & 0x00FF

                if self.v[x] == lowest_byte:
                    self.pc += 2

            case 0x4000:
                """
                4xkk - SNE Vx, byte
                
                Skip next instruction if Vx != kk.
                """
                lowest_byte = opcode & 0x00FF

                if self.v[x] != lowest_byte:
                    self.pc += 2

            case 0x5000:
                """
                5xkk - SE Vx, Vy
                
                Skip next instruction if Vx = Vy.
                """
                if self.v[x] == self.v[y]:
                    self.pc += 2

            case 0x6000:
                """
                6xkk - LD Vx, byte

                Set Vx = kk.
                """
                lowest_byte = opcode & 0x00FF
                self.v[x] = lowest_byte 

            case 0x7000:
                """
                7xkk - ADD Vx, byte

                Set Vx = Vx + kk.
                """
                lowest_byte = opcode & 0x00FF
                self.v[x] += lowest_byte

            case 0x8000:
                match (opcode & 0x000F):
                    case 0x0:
                        """
                        8xy0 - LD Vx, Vy

                        Set Vx = Vy.
                        """
                        self.v[x] = self.v[y]

                    case 0x1:
                        """
                        8xy1 - OR Vx, Vy

                        Set Vx = Vx OR Vy.
                        """
                        self.v[x] |= self.v[y]

                    case 0x2:
                        """
                        8xy2 - AND Vx, Vy
                        
                        Set Vx = Vx AND Vy.
                        """
                        self.v[x] &= self.v[y]

                    case 0x3:
                        """
                        8xy3 - XOR Vx, Vy
                        
                        Set Vx = Vx XOR Vy.
                        """
                        self.v[x] ^= self.v[y]

                    case 0x4:
                        """
                        8xy4 - ADD Vx, Vy
                        
                        Set Vx = Vx + Vy, set VF = carry.
                        """
                        total = self.v[x] + self.v[y]
                        self.v[0xF] = 0

                        if total > 0xFF:
                            self.v[0xF] = 1
                        
                        self.v[x] = total
  
                    case 0x5:
                        """
                        8xy5 - SUB Vx, Vy
                        
                        Set Vx = Vx - Vy, set VF = NOT borrow.
                        """
                        self.v[0xF] = 0

                        if self.v[x] > self.v[y]:
                            self.v[0xF] = 1
                        
                        self.v[x] -= self.v[y]

                    case 0x6:
                        """
                        8xy6 - SHR Vx {, Vy}

                        Set Vx = Vx SHR 1.
                        """
                        self.v[0xF] = self.v[x] & 0x1
                        self.v[x] >>= 1

                    case 0x7:
                        """
                        8xy7 - SUBN Vx, Vy

                        Set Vx = Vy - Vx, set VF = NOT borrow.
                        """
                        self.v[0xF] = 0

                        if self.v[y] > self.v[x]:
                            self.v[0xF] = 1
                        
                        self.v[x] = self.v[y] - self.v[x]

                    case 0xE:
                        """
                        8xyE - SHL Vx {, Vy}

                        Set Vx = Vx SHL 1.
                        """
                        self.v[0xF] = (self.v[x] & 0x80) >> 0x07
                        self.v[x] <<= 1

            case 0x9000:
                """
                9xy0 - SNE Vx, Vy

                Skip next instruction if Vx != Vy.
                """
                if self.v[x] != self.v[y]:
                    self.pc += 2

            case 0xA000:
                """
                Annn - LD I, addr

                Set I = nnn.
                """
                self.i = opcode & 0x0FFF

            case 0xB000:
                """
                Bnnn - JP V0, addr

                Jump to location nnn + V0.
                """
                self.pc = (opcode & 0x0FFF) + self.v[0x0]

            case 0xC000:
                """
                Cxkk - RND Vx, byte

                Set Vx = random byte AND kk.
                """
                random_byte = random.randint(0x00, 0xFF)
                lowest_byte = opcode & 0x00FF

                self.v[x] = random_byte & lowest_byte

            case 0xD000:
                """
                Dxyn - DRW Vx, Vy, nibble

                Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
                """
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
                        """
                        Ex9E - SKP Vx

                        Skip next instruction if key with the value of Vx is pressed.
                        """
                        if self.keypad.is_key_down(self.v[x]):
                            self.pc += 2

                    case 0xA1:
                        """
                        ExA1 - SKP Vx

                        Skip next instruction if key with the value of Vx is not pressed.
                        """
                        if not self.keypad.is_key_down(self.v[x]):
                            self.pc += 2

            case 0xF000:
                match (opcode & 0xFF):

                    case 0x07:
                        """
                        Fx07 - LD Vx, DT

                        Set Vx = delay timer value.
                        """
                        self.v[x] = self.delay_timer

                    case 0x0A:
                        """
                        Fx0A - LD Vx, K

                        Wait for a key press, store the value of the key in Vx.
                        """
                        self.paused = True
                        
                        def on_next_key_down(virtual_key):
                            self.v[x] = virtual_key
                            self.paused = False
                        
                        self.keypad.on_next_key_down = on_next_key_down

                    case 0x15:
                        """
                        Fx15 - LD DT, Vx

                        Set delay timer = Vx.
                        """
                        self.delay_timer = self.v[x]

                    case 0x18:
                        """
                        Fx18 - LD ST, Vx

                        Set sound timer = Vx.
                        """
                        self.sound_timer = self.v[x]

                    case 0x1E:
                        """
                        Fx1E - ADD I, Vx

                        Set I = I + Vx.
                        """
                        self.i += self.v[x]

                    case 0x29:
                        """
                        Fx29 - LD F, Vx

                        Set I = location of sprite for digit Vx.
                        """
                        self.i = self.v[x] * 0x5

                    case 0x33:
                        """
                        Fx33 - LD B, Vx

                        Store BCD representation of Vx in memory locations I, I+1, and I+2.
                        """
                        decimal = self.v[x]

                        for idx in range(3):
                            digit = decimal % 10
                            self.memory[self.i + idx] = digit
                            decimal /= 10

                    case 0x55:
                        """
                        Fx55 - LD [I], Vx

                        Store registers V0 through Vx in memory starting at location I.
                        """
                        for idx in range(0x0, x + 0x1):
                            self.memory[self.i + idx] = self.v[idx]

                    case 0x65:
                        """
                        Fx65 - LD Vx, [I]

                        Read registers V0 through Vx from memory starting at location I.
                        """
                        for idx in range(0x0, x + 0x1):
                            self.v[idx] = self.memory[self.i + idx]
            case _:
                raise ValueError(f"Invalid opcode: {opcode}")

    def play_sound(self):
        if self.sound_timer > 0:
            pass

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        
        if self.sound_timer > 0:
            self.sound_timer -= 1

if __name__ == "__main__":
    numpy.set_printoptions(threshold=numpy.inf)

    t = tk.Tk()
    cpu = CPU(sc.Screen(t), kp.KeyPad(t), sp.Speaker("../sound/beep.wav"))

    cpu.load_sprites_into_memory()
    cpu.load_rom("../roms/BLINKY")
    print(cpu.memory)