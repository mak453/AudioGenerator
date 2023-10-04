class Note:

    pitches = {
        "C0": 16.35,
        "C#0": 17.32,
        "Db0": 17.32,
        "D0": 18.35,
        "D#0": 19.44,
        "Eb0": 19.44,
        "E0": 20.6,
        "F0": 21.82,
        "F#0": 23.12,
        "Gb0": 23.12,
        "G0": 24.5,
        "G#0": 25.95,
        "Ab0": 25.95,
        "A0": 27.5,
        "A#0": 29.13,
        "Bb0": 29.13,
        "B0": 30.86,
        "C1": 32.7,
        "C#1": 34.64,
        "Db1": 34.64,
        "D1": 36.7,
        "D#1": 38.88,
        "Eb1": 38.88,
        "E1": 41.2,
        "F1": 43.64,
        "F#1": 46.24,
        "Gb1": 46.24,
        "G1": 49.0,
        "G#1": 51.9,
        "Ab1": 51.9,
        "A1": 55.0,
        "A#1": 58.26,
        "Bb1": 58.26,
        "B1": 61.72,
        "C2": 65.4,
        "C#2": 69.28,
        "Db2": 69.28,
        "D2": 73.4,
        "D#2": 77.76,
        "Eb2": 77.76,
        "E2": 82.4,
        "F2": 87.28,
        "F#2": 92.48,
        "Gb2": 92.48,
        "G2": 98.0,
        "G#2": 103.8,
        "Ab2": 103.8,
        "A2": 110.0,
        "A#2": 116.52,
        "Bb2": 116.52,
        "B2": 123.44,
        "C3": 130.8,
        "C#3": 138.56,
        "Db3": 138.56,
        "D3": 146.8,
        "D#3": 155.52,
        "Eb3": 155.52,
        "E3": 164.8,
        "F3": 174.56,
        "F#3": 184.96,
        "Gb3": 184.96,
        "G3": 196.0,
        "G#3": 207.6,
        "Ab3": 207.6,
        "A3": 220.0,
        "A#3": 233.04,
        "Bb3": 233.04,
        "B3": 246.88,
        "C4": 261.6,
        "C#4": 277.12,
        "Db4": 277.12,
        "D4": 293.6,
        "D#4": 311.04,
        "Eb4": 311.04,
        "E4": 329.6,
        "F4": 349.12,
        "F#4": 369.92,
        "Gb4": 369.92,
        "G4": 392.0,
        "G#4": 415.2,
        "Ab4": 415.2,
        "A4": 440.0,
        "A#4": 466.08,
        "Bb4": 466.08,
        "B4": 493.76,
        "C5": 523.2,
        "C#5": 554.24,
        "Db5": 554.24,
        "D5": 587.2,
        "D#5": 622.08,
        "Eb5": 622.08,
        "E5": 659.2,
        "F5": 698.24,
        "F#5": 739.84,
        "Gb5": 739.84,
        "G5": 784.0,
        "G#5": 830.4,
        "Ab5": 830.4,
        "A5": 880.0,
        "A#5": 932.16,
        "Bb5": 932.16,
        "B5": 987.52,
        "C6": 1046.4,
        "C#6": 1108.48,
        "Db6": 1108.48,
        "D6": 1174.4,
        "D#6": 1244.16,
        "Eb6": 1244.16,
        "E6": 1318.4,
        "F6": 1396.48,
        "F#6": 1479.68,
        "Gb6": 1479.68,
        "G6": 1568.0,
        "G#6": 1660.8,
        "Ab6": 1660.8,
        "A6": 1760.0,
        "A#6": 1864.32,
        "Bb6": 1864.32,
        "B6": 1975.04,
        "C7": 2092.8,
        "C#7": 2216.96,
        "Db7": 2216.96,
        "D7": 2348.8,
        "D#7": 2488.32,
        "Eb7": 2488.32,
        "E7": 2636.8,
        "F7": 2792.96,
        "F#7": 2959.36,
        "Gb7": 2959.36,
        "G7": 3136.0,
        "G#7": 3321.6,
        "Ab7": 3321.6,
        "A7": 3520.0,
        "A#7": 3728.64,
        "Bb7": 3728.64,
        "B7": 3950.08,
        "C8": 4185.6,
        "C#8": 4433.92,
        "Db8": 4433.92,
        "D8": 4697.6,
        "D#8": 4976.64,
        "Eb8": 4976.64,
        "E8": 5273.6,
        "F8": 5585.92,
        "F#8": 5918.72,
        "Gb8": 5918.72,
        "G8": 6272.0,
        "G#8": 6643.2,
        "Ab8": 6643.2,
        "A8": 7040.0,
        "A#8": 7457.28,
        "Bb8": 7457.28,
        "B8": 7900.16,
    }

    def __init__(self, pitch_name="A4", num_beats=1/8):
        self.set_note_freq(pitch_name)
        self.set_note_length(self, num_beats)
        self.set_data_samples(self, [])

    def set_note_freq(self, freq):
        self.fundamental_freq = freq

    def set_note_length(self, length):
        self.num_beats = length

    def set_data_samples(self, data):
        self.data_samples = data


class Chord:

    def __init__(self) -> None:
        self.chord_data_samples = []

    def add_note_to_chord(self, pitch_name="A4", num_beats=1/8):
        new_note = Note(self, pitch_name, num_beats)
        self.chord_data_samples.append(new_note)


class Score:

    score_count = 0

    def __init__(self) -> None:
        self.set_title("Score #" + str(Score.score_count))
        self.set_composer("Composer")
        Score.score_count += 1
        self.staves = []

    def add_note_to_staff(self, staff_num=0, pitch_name="A4", num_beats=1/8):
        new_note = Note(self, pitch_name, num_beats)
        self.staves[staff_num].append(new_note.data_samples)

    def add_chord_to_staff(self, staff_num=0, chord=Chord()):
        self.staves[staff_num].append(chord.chord_data_samples)

    def set_title(self, title):
        self.title = title

    def set_composer(self, name):
        self.composer = name
