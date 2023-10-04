import screen as sc
import keypad as kp
import speaker as sp
import numpy

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
        for i in range(self.speed):
            if not self.paused:
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
                self.execute_instruction(opcode)
        
        if not self.paused:
            self.update_timers()
        
        self.play_sound()
        self.screen.render()
    
    def execute_instruction(self, opcode):
        self.pc += 2

    def play_sound(self):
        if self.sound_timer > 0:
            pass
        else:
            pass

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        
        if self.sound_timer > 0:
            self.sound_timer -= 1

if __name__ == "__main__":
    numpy.set_printoptions(threshold=numpy.inf)

    screen = sc.Screen()
    speaker = sp.Speaker()
    keypad = kp.KeyPad()

    cpu = CPU(screen, keypad, speaker)
    cpu.load_sprites_into_memory()
    cpu.load_rom("roms/BLINKY")
    print(cpu.memory)