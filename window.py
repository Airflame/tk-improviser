import _thread as thread
from tkinter import *
from tkinter import ttk
from synth import Synth


class Window(object):
    def __init__(self, master):
        self.root = master
        self.root.resizable(False, False)
        self.root.title("pyImprov")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.synth = Synth()
        self.content = ttk.Frame(self.root)
        self.length_label = Label(self.content, text="Set length")
        self.length_text = Text(self.content, height=1, width=14)
        self.meter_label = Label(self.content, text="Set meter")
        self.meter_variable = StringVar(self.root)
        self.meter_variable.set("4/4")
        self.meter_menu = OptionMenu(self.content, self.meter_variable,
                                     "4/4", "3/4")
        self.scale_label = Label(self.content, text="Set scale")
        self.scale_variable = StringVar(self.root)
        self.scale_variable.set("Pentatonic")
        self.scale_menu = OptionMenu(self.content, self.scale_variable,
                                     "Pentatonic", "Blues", "Major", "Minor")
        self.tonic_label = Label(self.content, text="Set tonic")
        self.tonic_variable = StringVar(self.root)
        self.tonic_variable.set("C")
        self.tonic_menu = OptionMenu(self.content, self.tonic_variable,
                                     "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
        self.tempo_label = Label(self.content, text="Set tempo")
        self.tempo_text = Text(self.content, height=1, width=14)
        self.instrument_label = Label(self.content, text="Set instrument")
        self.instrument_variable = StringVar(self.root)
        self.instrument_variable.set("Piano")
        self.instrument_menu = OptionMenu(self.content, self.instrument_variable,
                                          "Piano", "Plucked", "Sawtooth", "Square", "Rhodes")
        self.filename_label = Label(self.content, text="Set name")
        self.filename_text = Text(self.content, height=1, width=14)
        self.separator_label = Label(self.content)
        self.status_label = Label(self.content)
        self.button = Button(self.content, text="Create", width=16, height=2,
                             command=self.on_click)
        self.content.grid(column=0, row=0)
        self.length_label.grid(column=0, row=0)
        self.length_text.insert(END, "30")
        self.length_text.grid(column=1, row=0)
        self.meter_label.grid(column=0, row=1)
        self.meter_menu.grid(column=1, row=1)
        self.scale_label.grid(column=0, row=2)
        self.scale_menu.grid(column=1, row=2)
        self.tonic_label.grid(column=0, row=3)
        self.tonic_menu.grid(column=1, row=3)
        self.tempo_label.grid(column=0, row=4)
        self.tempo_text.insert(END, "150")
        self.tempo_text.grid(column=1, row=4)
        self.instrument_label.grid(column=0, row=5)
        self.instrument_menu.grid(column=1, row=5)
        self.filename_label.grid(column=0, row=6)
        self.filename_text.insert(END, "output")
        self.filename_text.grid(column=1, row=6)
        self.separator_label.grid(column=0, row=7, columnspan=2)
        self.status_label.grid(column=0, row=8, columnspan=2)
        self.button.grid(column=0, row=9, columnspan=2)
        self.content.pack(padx=10, pady=11)
        self.separator_label.config(text=" ")
        self.status_label.config(text="Ready")

    def on_closing(self):
        self.root.destroy()
        exit()

    def on_click(self):
        self.button.configure(state=DISABLED)
        thread.start_new_thread(self.create, ())

    def create(self):
        self.status_label.config(text="Processing")
        self.synth.set_length(self.length_text.get("1.0", "end-1c"))
        self.synth.set_meter(self.meter_variable.get())
        self.synth.set_scale(self.scale_variable.get(), self.tonic_variable.get())
        self.synth.set_tempo(self.tempo_text.get("1.0", "end-1c"))
        self.synth.set_instrument(self.instrument_variable.get())
        self.synth.set_filename(self.filename_text.get("1.0", "end-1c"))
        self.synth.create()
        self.status_label.config(text="Done")
        self.button.configure(state=NORMAL)

