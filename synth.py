import pysynth_b
import pysynth_c
import pysynth_d
import pysynth_e
import pysynth_s
import scales
import measures
from random import *


class Synth(object):
    def __init__(self):
        self.length = 30
        self.meter = "4/4"
        self.scale = []
        self.set_scale("Pentatonic", "C")
        self.tempo = 150
        self.instrument = "Piano"
        self.filename = "output"

    def set_length(self, length):
        self.length = int(str(length))

    def set_meter(self, meter):
        self.meter = str(meter)

    def set_scale(self, scale, tonic):
        self.scale = []
        scale = str(scale)
        tonic = scales.KEYS.index(str(tonic))
        self.scale.append(scales.CHROMATIC[tonic])
        index = tonic
        selected_scale = ()
        if scale == "Pentatonic":
            selected_scale = scales.PENTATONIC
        elif scale == "Blues":
            selected_scale = scales.BLUES
        elif scale == "Major":
            selected_scale = scales.MAJOR
        elif scale == "Minor":
            selected_scale = scales.MINOR
        for i in range(3 * len(selected_scale)):
            index = index + selected_scale[i % len(selected_scale)]
            self.scale.append(scales.CHROMATIC[index % len(scales.CHROMATIC)])

    def set_tempo(self, tempo):
        self.tempo = int(str(tempo))

    def set_instrument(self, instrument):
        self.instrument = str(instrument)

    def set_filename(self, filename):
        self.filename = "{}.wav".format(str(filename))

    def create(self):
        notes = self.improvise()
        if self.instrument == "Piano":
            pysynth_b.make_wav(notes, fn=self.filename, bpm=self.tempo)
        elif self.instrument == "Plucked":
            pysynth_s.make_wav(notes, fn=self.filename, bpm=self.tempo)
        elif self.instrument == "Sawtooth":
            pysynth_c.make_wav(notes, fn=self.filename, bpm=self.tempo)
        elif self.instrument == "Square":
            pysynth_d.make_wav(notes, fn=self.filename, bpm=self.tempo)
        elif self.instrument == "Rhodes":
            pysynth_e.make_wav(notes, fn=self.filename, bpm=self.tempo)

    def improvise(self):
        notes = []
        current = randint(len(self.scale) // 4, len(self.scale) // 2)
        rhythm = []
        rhythm_measure = []
        melody = []
        melody_measure = []
        for i in range(self.length):
            previous_rhythm_measure = rhythm_measure
            previous_melody_measure = melody_measure
            melody_measure = []
            repeat_rhythm = randint(1, 3)
            if len(previous_rhythm_measure) > 0 and repeat_rhythm == 1:
                rhythm_measure = previous_rhythm_measure
            else:
                rhythm_measure = choice(measures.MEASURES[self.meter])
            rhythm.extend(rhythm_measure)
            repeat_melody = randint(1, 3)
            if len(previous_melody_measure) == len(rhythm_measure) and repeat_melody == 1:
                melody.extend(previous_melody_measure)
            else:
                for j in range(len(rhythm_measure)):
                    melody_measure.append(self.scale[current])
                    interval = randint(-2, 2)
                    if 0 <= current + interval < len(self.scale):
                        current = current + interval
                melody.extend(melody_measure)
        for i in range(len(melody)):
            notes.append((melody[i], rhythm[i]))
        return tuple(notes)
