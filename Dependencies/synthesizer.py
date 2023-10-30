import numpy as np
from Dependencies.score_composer import Note, Chord, Score
import soundfile as sf
from scipy.signal import butter, lfilter




def make_audio_file(score: Score, file_name: str):

    audio_data = np.zeros(score.num_measures *
                          score.samples_per_measure, dtype=np.int16)
    start = 0
    for staff in score.staves:
        for layer in staff.layers:
            for event in layer:
                end = start + len(event.data_samples)
                audio_data[start:end] += event.data_samples
                start = end

    for i in audio_data[::int(score.sample_rate/10)]:
        print(i, end=" ")

    file_name = "_".join(score.title.split(" "))
    sf.write("./Output_audio/" + file_name +
             ".wav", audio_data, score.sample_rate)


def set_data(score: Score, event):
    """_summary_

    Args:
        score (Score): _description_
        note (Note): _description_
    """
    event_time = event.length*float(score.time_sig[1])
    time_array = np.arange(0, (score.samples_per_beat *
                           event_time)/Score.sample_rate, 1/Score.sample_rate)
    data = np.zeros(len(time_array))
    data_type = np.int16

    if Score.bit_depth == 32:
        data_type = np.int32

    if isinstance(event, Note):
        fundamental = event.fundamental_freq

        for i in range(1):
            data += np.array(np.cos(2*np.pi *
                                    fundamental*(2**i)*time_array))

        data = 2*((data - min(data)) / (max(data) - min(data)))-1
        print(data)
        data *= (2**(Score.bit_depth-2))
        event.data_samples = np.array(data, dtype=data_type)

    elif isinstance(event, Chord):
        print("Chord", event_time)
        data = np.zeros(time_array.size)

        for note in event.chord_notes:
            data += np.array(
                np.sin(2*np.pi*note.fundamental_freq*time_array))

        event.data_samples = np.array(
            (2**Score.bit_depth)/len(event.chord_notes) * data, dtype=data_type)
