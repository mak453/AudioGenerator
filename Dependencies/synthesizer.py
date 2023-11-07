import numpy as np
from Dependencies.score_composer import Note, Chord, Score
import soundfile as sf
import matplotlib.pyplot as plt


def make_audio_file(score: Score, file_name="default"):
    bits = Score.bit_depth

    data_type = np.int16
    if bits == 32:
        data_type = np.int32

    audio_data = np.zeros(score.num_measures *
                          score.samples_per_measure, dtype=data_type)
    start = 0
    for staff in score.staves:
        for layer in staff.layers:
            for event in layer:
                end = start + len(event.data_samples)
                audio_data[start:end] += event.data_samples
                start = end

    # for i in audio_data[::int(score.sample_rate/10)]:
    #     print(i, end=" ")

    if file_name == "default":
        file_name = "_".join(score.title.split(" "))

    sf.write("./Output_audio/" + file_name +
             ".wav", audio_data, score.sample_rate)


def karplus_strong(sr, freq, num_samples):

    N = int(sr // freq)

    noise = 2.0*np.random.random(num_samples)-1
    y = np.zeros(num_samples)

    for n in range(0, num_samples):
        y[n] = (y[n-N] + y[n-N+1])/2 if n >= N else noise[n]

    return y


def set_data(score: Score, event):
    """_summary_

    Args:
        score (Score): _description_
        note (Note): _description_
    """
    event_time = event.length*float(score.time_sig[1])
    num_event_samples = int(event_time*score.sample_rate)
    bits = Score.bit_depth

    data_type = np.int16
    if bits == 32:
        data_type = np.int32

    if isinstance(event, Note) and event.fundamental_freq != 0:
        event.data_samples = np.array(2**(bits-1) * karplus_strong(
            score.sample_rate, event.fundamental_freq, num_event_samples), dtype=data_type)
    elif isinstance(event, Chord):
        data = np.zeros(num_event_samples, dtype=np.int16)
        for note in event.chord_notes:
            if note.fundamental_freq != 0:
                data += np.array(2**(bits-1) * karplus_strong(
                    score.sample_rate, note.fundamental_freq, num_event_samples)/len(event.chord_notes), dtype=data_type)
        event.data_samples = data
