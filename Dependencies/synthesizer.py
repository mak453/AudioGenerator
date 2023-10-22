import numpy as np
from pedalboard import Pedalboard, Compressor, Reverb
from Dependencies.score_composer import Note, Chord, Score
import soundfile as sf
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def make_audio_file(score: Score, output_filepath):

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

    if(output_filepath == "" or output_filepath is None):
        file_name = score.title.split(" ")
        output_filepath = "/Output_audio/" + file_name[0] +".wav"

    sf.write(output_filepath[0], audio_data, score.sample_rate)


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

        for i in range(-3, 6, 1):
            data += np.array(np.cos(2*np.pi *
                                    fundamental*(2**i)*time_array))

        data = 2*((data - min(data)) / (max(data) - min(data)))-1
        data *= (2**(Score.bit_depth-2))
        event.data_samples = np.array(data, dtype=data_type)

    elif isinstance(event, Chord):
        data = np.zeros(time_array.size)

        for note in event.chord_notes:
            data += np.array(
                np.sin(2*np.pi*note.fundamental_freq*time_array))

        event.data_samples = np.array(
            (2**Score.bit_depth)/len(event.chord_notes) * data, dtype=data_type)


# def set_data(chord: Chord):
#     """_summary_

#     Args:
#         score (Score): _description_
#         chord (Chord): _description_
#     """
#     data = 0
#     for note in chord.chord_notes:
#         data += note.data_samples
#     chord.data_samples = data


# def make_layer(score: Score, layer: list, samples_per_measure):
#     """_summary_

#     Args:
#         score (Score): _description_
#         staff (_type_): _description_
#         samples_per_measure (_type_): _description_
#         layer_num (_type_): _description_
#     """
#     # print(score.num_measures)
#     data = np.zeros(samples_per_measure*score.num_measures, dtype=np.int16)
#     curr_measure = 0
#     start = 0

#     for event in layer:
#         num_samples = len(event.data_samples)
#         if curr_measure != event.measure:
#             curr_measure = event.measure
#             start = (curr_measure-1)*samples_per_measure
#             print("New measure " + str(curr_measure) + " " + str(event) +
#                   " " + str(start))
#             data[start:start+num_samples] = event.data_samples
#         else:
#             print("\tsame measure " + str(curr_measure) + " " + str(event) +
#                   " " + str(start))
#             data[start:start+num_samples] = event.data_samples

#         start += num_samples-1
#         # print("\t" + str(event) + str(len(event.data_samples)))

#     return data


# def write_audio_file(score: Score, data, temp=""):
#     """_summary_

#     Args:
#         score (Score): _description_
#         data (_type_): _description_
#     """
#     sf.write("./Output_Audio/"+score.title+".wav", data,
#              score.sample_rate)
#     return


# def play_each_note(score: Score):
#     """_summary_

#     Args:
#         score (Score): _description_
#     """

#     for staff in score.staves:
#         for layer in staff.layers:
#             for num, event in enumerate(layer):
#                 write_audio_file(score, event.data_samples, str(num))


# def make_audio_file(score: Score):
#     """_summary_

#     Args:
#         score (Score): _description_
#     """

#     samples_per_measure = int(
#         (score.tempo/60.0)*score.sample_rate*int(score.time_sig[0]))
#     print(samples_per_measure, score.num_measures)
#     data = np.zeros(samples_per_measure*score.num_measures, dtype=np.int16)

#     for staff in score.staves:
#         for layer in staff.layers:
#             start = (layer[0].measure-1)*samples_per_measure
#             layer_data = make_layer(score, layer, samples_per_measure)
#             data[start:start+len(layer_data)] = layer_data

#     write_audio_file(score, data)
