import numpy as np
from score_composer import Note, Chord

def make_fundamental(note, spb):

    return data


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
