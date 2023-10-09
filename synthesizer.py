import numpy as np
from score_composer import Note, Chord, Staff, Score
import wave as wv


def make_fundamental(score: Score, note: Note):
    """_summary_

    Args:
        score (Score): _description_
        note (Note): _description_
    """
    num_beats = (1/note.note_length)/score.time_sig[1]
    note_time = num_beats*60/score.tempo
    time = np.arange(0, note_time, 1/score.sample_rate)
    note.data_samples = np.array(
        np.sin(note.fundamental_freq*time), dtype=np.float16)


def make_chord(chord: Chord):
    """_summary_

    Args:
        score (Score): _description_
        chord (Chord): _description_
    """
    data = 0
    for note in chord.chord_notes:
        data += note.data_samples
    chord.data_samples = data


def make_layer(score: Score, staff, samples_per_measure, layer_num):
    data = np.zeros(samples_per_measure*score.num_measures)
    curr_measure = 0
    start = 0
    for event in staff.layers[layer_num]:
        if curr_measure != event.measure:
            curr_measure += 1
            print("New measure " + str(curr_measure) + " " + str(start))
        else:
            print("\tsame measure" + str(curr_measure) + " " + str(start))
        print("\t" + str(event) + str(len(event.data_samples)))

    return


def make_audio_file(score: Score):
    """_summary_

    Args:
        score (Score): _description_
    """
    # file = wv.open(score.title + ".wav", "wb")
    # file.setnchannels(1)
    # file.setsampwidth(score.bit_depth/8)
    # file.setframerate(score.sample_rate)
    # file.close()
    samples_per_measure = int(
        score.time_sig[0]/score.tempo*60*score.sample_rate)
    data = np.zeros(samples_per_measure*score.num_measures)
    curr_sample = 0

    for staff in score.staves:
        for num, layer in enumerate(staff.layers):
            layer_data = make_layer(score, staff, samples_per_measure, num)
