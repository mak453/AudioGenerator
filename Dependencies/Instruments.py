import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from pedalboard import Pedalboard, Chorus, Reverb, Compressor, Distortion


def normalize(x, bit_depth=16):
    high = 2**(bit_depth-1)
    low = 2**(bit_depth-1)
    return np.array(low + ((x - min(x))*(high - low))/(max(x)-min(x)), dtype=np.int16)


class Synthesizer:
    sample_rate = 44100
    data_type = np.int16
    bit_depth = 16

    def __init__(self, fundamental_freq: float, num_samples: int) -> None:
        self.max_value = 2**(self.bit_depth-1)
        self.data = np.zeros(num_samples, dtype=self.data_type)
        self.freq = fundamental_freq
        self.num_samples = num_samples
        self.pitch = str(fundamental_freq) + "_" + str(num_samples)

    def plot_audio(self, file_name: str):
        plt.figure(file_name)
        plt.plot(self.data)
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")

        plt.figure(file_name + "_FFT")
        freq_bins = np.fft.fftfreq(
            self.num_samples, 1/self.sample_rate)[:int(self.sample_rate/2)]
        fft = abs(np.fft.fft(self.data))[:int(self.sample_rate/2)]
        plt.stem(freq_bins, fft, markerfmt="", basefmt="")

    def write_audio(self, file_name: str):
        sf.write(file_name + ".wav", self.data, self.sample_rate)

    def cents(self, f1, cents):
        return f1*(2**(cents/1200))

    def normalize(self, x, high=2**(bit_depth-1), low=-(2**(bit_depth-1))):
        return np.array(low + ((x - min(x))*(high - low))/(max(x)-min(x)), dtype=self.data_type)


class PhysicalModeling(Synthesizer):

    def karplus_strong_algorithm(self, freq):
        N = self.sample_rate // int(freq)

        noise = 2.0*np.random.random(N)-1

        y = np.zeros(self.num_samples)

        for n in range(0, self.num_samples):
            y[n] = (y[n-N] + y[n-N+1])/2 if n >= N else noise[n]

        return y

    def make_data(self, freq, note_bank):
        if self.pitch in note_bank:
            # print("Repeat of " + self.pitch)
            return np.array(note_bank[self.pitch], dtype=np.float64)

        pluck = self.karplus_strong_algorithm(freq)
        note_bank.update({self.pitch: pluck})

        return pluck


class Guitar(PhysicalModeling):
    board = Pedalboard(
        [Reverb(room_size=.2, damping=.05, wet_level=.30, dry_level=.5)])
    note_bank = {}
    name = "Guitar"

    def __init__(self, fundamental_freq: float, num_samples: int, disp=False):
        super().__init__(fundamental_freq, num_samples)

        self.data = self.board(super().make_data(
            self.freq, self.note_bank), self.sample_rate)

        # super().write_audio(self.name + " " + str(self.freq) + "Hz")
        if disp:
            super().plot_audio(self.name + " " + str(self.freq) + "Hz")


class Mandolin(PhysicalModeling):
    board = Pedalboard(
        [Reverb(room_size=.4, damping=.4, wet_level=.30, dry_level=.20)])
    note_bank = {}
    name = "Mandolin"

    def __init__(self, fundamental_freq: float, num_samples: int, disp=False):
        super().__init__(fundamental_freq, num_samples)

        string_1 = super().make_data(self.freq, self.note_bank)
        freq_2 = super().cents(self.freq, -5)
        string_2 = super().make_data(freq_2, self.note_bank)

        self.data = self.board(string_1 + string_2, self.sample_rate)

        if disp:
            super().plot_audio(self.name + " " + str(self.freq) + "Hz")


class AdditiveSynthesis(Synthesizer):

    def make_cosine_wave(self, freq, amplitude, time):
        return np.array(amplitude*np.cos(2*np.pi*freq*time))

    def make_sine_wave(self, freq, time, amplitude=1):
        return np.array(amplitude*np.sin(2*np.pi*freq*time))


class Violin(AdditiveSynthesis):
    board = Pedalboard(
        [Reverb(room_size=.5, damping=.3, wet_level=.50, dry_level=.4)])
    amplitudes = [1, 0.263, 0.14, .099, .0209, .02, .029, .077, .017, .01]
    note_bank = {}
    vibrato_variance = 13
    vibrato_freq = 24
    name = "Violin"

    def __init__(self, fundamental_freq, num_samples: int, disp=False) -> None:
        super().__init__(fundamental_freq, num_samples)

        if self.pitch in self.note_bank:
            self.data = self.note_bank[self.pitch]
        else:
            time_array = np.linspace(0, self.num_samples /
                                     self.sample_rate, self.num_samples)

            data = np.zeros(num_samples)

            for harmonic, amp in enumerate(self.amplitudes, start=1):
                freq = (fundamental_freq*harmonic) + self.vibrato_variance * \
                    super().make_sine_wave(self.vibrato_freq*harmonic, time_array)
                phase = 2*np.pi*np.cumsum(freq) / self.sample_rate
                harmonic_data = amp*np.sin(phase)
                data += harmonic_data

            self.data = data

        # super().write_audio(self.name + " " + str(self.freq) + "Hz")
        if disp:
            super().plot_audio(self.name + " " + str(self.freq) + "Hz")


def amplitude_envelope(instrument: Synthesizer, sr=44100):
    envelope = np.zeros(len(instrument.data))

    attack_level = .6
    attack_length = 1
    sustain_level = .2
    decay_length = 5
    sustain_length = 5

    if isinstance(instrument, Guitar) == "guitar":
        attack_level = .5
        attack_length = 1
        sustain_level = .3
        decay_length = 3
        sustain_length = 4
    elif isinstance(instrument, Violin):
        attack_level = .4
        attack_length = .5
        sustain_level = .2
        decay_length = 1.2
        sustain_length = 20

    attack_length = attack_length*1e-2
    decay_length = decay_length*1e-2
    sustain_length = sustain_length*1e-2

    attack_time = np.arange(0, attack_length, 1/sr)
    attack = np.log10(1+attack_time*len(attack_time))*sustain_level
    attack = attack_level*attack/max(attack)
    envelope[:len(attack_time)] = attack

    decay_time = np.arange(0, decay_length, 1/sr)
    decay = np.linspace(attack_level, sustain_level, len(decay_time))
    envelope[len(attack_time):len(attack_time)+len(decay)] = decay

    sustain_start = len(attack_time)+len(decay)
    sustain_time = np.arange(0, sustain_length, 1/sr)
    envelope[sustain_start:sustain_start+len(sustain_time)] = sustain_level

    release_start = sustain_start+len(sustain_time)
    release_time = np.arange(
        0, (len(instrument.data)/sr)-(attack_length+decay_length+sustain_length), 1/sr)
    release = sustain_level*((1/10e32)**release_time)
    envelope[release_start:len(instrument.data)] = release[:len(
        instrument.data)-release_start]

    return envelope
