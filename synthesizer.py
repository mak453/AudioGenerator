import numpy as np
from score_composer import Note, Chord

freqs = {"C": 16.35,
         "C#": 17.32222159277448,
         "Db": 17.32222159277448,
         "D": 18.35225448985825,
         "D#": 19.443536330294492,
         "Eb": 19.443536330294492,
         "E": 20.599709165781178,
         "F": 21.824631615680065,
         "F#": 23.122391744800108,
         "Gb": 23.122391744800108,
         "G": 24.497320706933746,
         "G#": 25.954007199680063,
         "Ab": 25.954007199680063,
         "A": 27.497312778796466,
         "A#": 29.132388083189095,
         "Bb": 29.132388083189095,
         "B": 30.86469002469138,
         "rest": 0}


def make_fundamental(note, spb):

    return


def synthesize_score(score, sr, bit_depth):
    beats_per_second = int(score.tempo / 60)
    samples_per_beat = int(sr / beats_per_second)
    data = []

    print(beats_per_second, samples_per_beat)
    # for staff in score:
    #     for note in staff:
    #         if type(note) == Chord:

    #         else:
    #             make_fundamental(note, )
