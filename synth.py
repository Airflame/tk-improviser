import pysynth_b
import pysynth_c
import pysynth_d
import pysynth_e
import pysynth_s
import scales
from random import randint


class Synth(object):
    def __init__(self):
        self._length = 30
        self._scale = []
        self.set_scale("Pentatonic", "C")
        self._tempo = 150
        self._instrument = "Piano"
        self._filename = "output"

    def set_length(self, length):
        self._length = int(str(length))

    def set_scale(self, scale, tonic):
        self._scale = []
        scale = str(scale)
        tonic = scales.KEYS.index(str(tonic))
        self._scale.append(scales.CHROMATIC[tonic])
        index = tonic
        selected_scale = []
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
            self._scale.append(scales.CHROMATIC[index % len(scales.CHROMATIC)])

    def set_tempo(self, tempo):
        self._tempo = int(str(tempo))

    def set_instrument(self, instrument):
        self._instrument = str(instrument)

    def set_filename(self, filename):
        self._filename = "{}.wav".format(str(filename))

    def create(self):
        notes = self.improvise()
        if self._instrument == "Piano":
            pysynth_b.make_wav(notes, fn=self._filename, bpm=self._tempo)
        if self._instrument == "Plucked":
            pysynth_s.make_wav(notes, fn=self._filename, bpm=self._tempo)
        if self._instrument == "Sawtooth":
            pysynth_c.make_wav(notes, fn=self._filename, bpm=self._tempo)
        if self._instrument == "Square":
            pysynth_d.make_wav(notes, fn=self._filename, bpm=self._tempo)
        if self._instrument == "Rhodes":
            pysynth_e.make_wav(notes, fn=self._filename, bpm=self._tempo)

    def improvise(self):
        notes = []
        current = randint(len(self._scale)//4, len(self._scale)//2)
        rhythm = []
        rhythm_measure = []
        melody = []
        melody_measure = []

        for i in range(self._length):
            previous_rhythm_measure = rhythm_measure
            previous_melody_measure = melody_measure
            melody_measure = []
            repeat_rhythm = randint(1, 3)
            if len(previous_rhythm_measure) > 0 and repeat_rhythm == 1:
                rhythm_measure = previous_rhythm_measure
            else:
                measure_version = randint(1, 8)
                if measure_version == 1:
                    rhythm_measure = [1]
                elif measure_version == 2:
                    rhythm_measure = [2, 2]
                elif measure_version == 3:
                    rhythm_measure = [2, 4, 4]
                elif measure_version == 4:
                    rhythm_measure = [4, 4, 4, 4]
                elif measure_version == 5:
                    rhythm_measure = [4, 4, 8, 8, 8, 8]
                elif measure_version == 6:
                    rhythm_measure = [2, 8, 8, 8, 8]
                elif measure_version == 7:
                    rhythm_measure = [8, 8, 8, 8, 2]
                elif measure_version == 8:
                    rhythm_measure = [8, 8, 8, 8, 8, 8, 8, 8]
            rhythm.extend(rhythm_measure)
            repeat_melody = randint(1, 3)
            if len(previous_melody_measure) == len(rhythm_measure) and repeat_melody == 1:
                melody.extend(previous_melody_measure)
            else:
                for j in range(len(rhythm_measure)):
                    melody_measure.append(self._scale[current])
                    interval = randint(-2, 2)
                    if 0 <= current + interval < len(self._scale):
                        current = current + interval
                melody.extend(melody_measure)

        for i in range(len(melody)):
            notes.append((melody[i], rhythm[i]))
        return tuple(notes)
