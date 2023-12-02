import numpy as np
from Dependencies.score_composer import Note, Chord, Score
import soundfile as sf
import matplotlib.pyplot as plt
from Dependencies.Instruments import amplitude_envelope, normalize, Violin, Mandolin, Guitar


def make_audio_file(score: Score, filepath="default", instrument="mandolin"):
    # print(score.time_sig, score.tempo)

    samples_per_measure = int(
        (60.0/score.tempo)*float(score.time_sig[0])*Score.sample_rate)

    audio_data = np.zeros(score.num_measures *
                          samples_per_measure)

    curr_measure = 1

    for staff in score.staves:
        start = 0
        for layer in staff.layers:
            start = 0
            for event in layer:
                if event.measure != curr_measure:
                    start = int((event.measure-1)*samples_per_measure)
                    curr_measure = event.measure

                event_time = (60.0/score.tempo) * \
                    (float(score.time_sig[1])/event.length)

                num_samples = int(event_time * Score.sample_rate)
                smooth_gap = int(.25*num_samples)

                num_sound_samples = num_samples

                if instrument == "mandolin" and start + num_samples < len(audio_data):
                    num_sound_samples = num_samples+smooth_gap
                elif instrument == "violin":
                    num_sound_samples = num_samples-smooth_gap

                if isinstance(event, Chord):
                    chord_data = np.zeros(num_sound_samples)

                    for notes in event.chord_notes:
                        if notes.fundamental_freq == 0:
                            continue

                        if instrument == 'mandolin':
                            mandolin = Mandolin(
                                notes.fundamental_freq, num_sound_samples)
                            envelope = amplitude_envelope(mandolin)
                            chord_data += mandolin.data*envelope
                        elif instrument == 'guitar':
                            guitar = Guitar(
                                notes.fundamental_freq, num_sound_samples)
                            envelope = amplitude_envelope(guitar)
                            chord_data += guitar.data*envelope
                        elif instrument == 'violin':
                            violin = Violin(
                                notes.fundamental_freq, num_sound_samples)
                            envelope = amplitude_envelope(violin)
                            chord_data += violin.data*envelope

                    try:
                        audio_data[start:start+num_sound_samples] += chord_data
                    except ValueError:
                        print(event)
                        pass

                elif isinstance(event, Note):
                    note_data = np.zeros(num_sound_samples)
                    envelope = 0

                    if event.fundamental_freq == 0:
                        pass
                    elif instrument == 'mandolin':
                        mandolin = Mandolin(
                            event.fundamental_freq, num_sound_samples)
                        note_data += mandolin.data
                        envelope = amplitude_envelope(mandolin)
                    elif instrument == 'guitar':
                        guitar = Guitar(
                            event.fundamental_freq, num_sound_samples)
                        note_data += guitar.data
                        envelope = amplitude_envelope(guitar)
                    elif instrument == 'violin':
                        violin = Violin(
                            event.fundamental_freq, num_sound_samples)
                        note_data += violin.data
                        envelope = amplitude_envelope(violin)

                    note_data *= envelope

                    try:
                        audio_data[start:start+num_sound_samples] += note_data
                    except ValueError:
                        print(event)
                        pass

                start += num_samples

    if filepath == "default":
        filepath = "_".join(score.title.split(" "))
        filepath = "./Output_audio/" + filepath + ".wav"

    audio_data = (audio_data/max(audio_data))

    sf.write(filepath, audio_data, score.sample_rate)


# def set_data(score: Score, event):
#     """_summary_

#     Args:
#         score (Score): _description_
#         note (Note): _description_
#     """
#     event_time = event.length*float(score.time_sig[1])
#     num_event_samples = int(event_time*score.sample_rate)
#     bits = Score.bit_depth

#     data_type = np.int16
#     if bits == 32:
#         data_type = np.int32

#     data = np.zeros(num_event_samples, dtype=data_type)

#     if isinstance(event, Note) and event.fundamental_freq != 0:
#         data = np.array(2**(bits-1) * karplus_strong(
#             score.sample_rate, event.fundamental_freq, num_event_samples), dtype=data_type)
#     elif isinstance(event, Note):
#         event.data_samples = np.zeros(num_event_samples, dtype=data_type)
#     elif isinstance(event, Chord):
#         for note in event.chord_notes:
#             if note.fundamental_freq != 0:
#                 data += np.array(2**(bits-1) * karplus_strong(
#                     score.sample_rate, note.fundamental_freq, num_event_samples)/len(event.chord_notes), dtype=data_type)

#     event.data_samples = np.array(data, dtype=data_type)
