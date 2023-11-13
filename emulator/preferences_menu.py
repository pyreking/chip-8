import tkinter as tk
import tkinter.ttk as ttk

class PreferencesMenu(tk.Toplevel):
    HEADINGS = ["Key", "Binding"]
    KEY_LABELS = ['1', '2', '3', 'C', '4', '5', '6',
                  'D', '7', '8', '9', 'E', 'A', '0',
                  'B', 'F']

    def __init__(self, parent, cpu, config, step):
        super().__init__(parent)
        self.cpu = cpu
        self.keypad = self.cpu.keypad
        self.step = step
        self.config = config

        self.geometry('500x350')
        self.resizable(False, False)
        self.tree = ttk.Treeview(self, columns=self.HEADINGS, show="headings")

        for heading in self.HEADINGS:
            self.tree.heading(heading, text=heading)

        self.tree.column(0, anchor=tk.CENTER)
        self.tree.column(1, anchor=tk.CENTER)

        for key_label in self.KEY_LABELS:
            self.tree.insert('', 'end', key_label, values=(key_label,))

        for scan_code, virtual_key in self.keypad.KEYBOARD_BINDINGS.items():
            key_label = hex(virtual_key).upper()[-1]
            self.tree.item(key_label, values=(key_label, chr(scan_code).upper()))
        
        if "labels" in self.config.parser:
            self.config.load_labels(self.tree)
        
        self.style = ttk.Style()
        self.style.map('Treeview', background=[('selected', 'lightgray')])

        self.on_next_key_down = None
        self.bind('<ButtonRelease-1>', self.on_click)
        self.bind('<KeyPress>', self.on_key_down)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.tree.pack(fill="both", expand=True)

    def on_click(self, event):
        self.style.map('Treeview', background=[('selected', 'lightblue')])
        item = self.tree.selection()[0]

        def on_next_key_down(event):
            scan_code, scan_code_label = event.keycode, event.keysym.upper()

            virtual_key_label = self.tree.item(item, "values")[0]
            virtual_key = int(virtual_key_label, 16)
            
            evicted_key = self.keypad.update_key_binding(virtual_key, scan_code)

            if evicted_key != None:
                evicted_key_label = hex(evicted_key).upper()[-1]
                self.tree.item(evicted_key_label, values=(evicted_key_label,))

            self.tree.item(item, values=(virtual_key_label, scan_code_label))
        
        self.on_next_key_down = on_next_key_down

    def on_key_down(self, event):
        if self.on_next_key_down:
            self.on_next_key_down(event)
            self.on_next_key_down = None
            self.style.map('Treeview', background=[('selected', 'lightgray')])
    
    def on_exit(self):
        self.config.save_settings(self.tree)
        self.cpu.paused = False
        self.step()
        self.destroy()

if __name__ == '__main__':
    # Create a new menu bar.
    pass