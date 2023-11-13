import configparser as parser

class ConfigWriter():
    def __init__(self, path, keypad):
        self.keypad = keypad
        self.parser = parser.ConfigParser()
        self.PATH = path
        self.parser.read(self.PATH)
        
        if "bindings" not in self.parser:
            self.parser.add_section("bindings")

        if "labels" not in self.parser:
            self.parser.add_section("labels")

    def save_settings(self, tree):
        self.parser['bindings'].clear()
        self.parser['labels'].clear()

        for scan_code, virtual_key in self.keypad.key_bindings.items():
            virtual_key_label = hex(virtual_key)[-1].upper()
            self.parser.set("bindings", str(scan_code), virtual_key_label)
            self.parser.set("labels", virtual_key_label, tree.item(virtual_key_label, option='values')[1])
        
        with open(self.PATH, 'w') as f:
            self.parser.write(f)
    
    def load_bindings(self):
        for scan_code, virtual_key in self.parser["bindings"].items():
            self.keypad.update_key_binding(int(virtual_key, 16), int(scan_code))
    
    def load_labels(self, tree):
        for virtual_key_label, scan_code_label in self.parser["labels"].items():
            tree.item(virtual_key_label.upper(), values=(virtual_key_label.upper(), scan_code_label))