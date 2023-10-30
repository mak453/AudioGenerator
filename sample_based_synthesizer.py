import numpy as np
from numpy import cos, sin
from scipy import signal
import wave as wv
import matplotlib.pyplot as plt
import soundfile as sf

pitches = [16.35, 17.32, 17.32, 18.35, 19.44, 19.44, 20.6, 20.6, 21.82, 21.82, 23.12, 23.12, 24.5, 25.95, 25.95, 27.5, 29.13, 29.13, 30.86, 32.7, 30.86, 32.7, 34.64, 34.64, 36.7, 38.88, 38.88, 41.2, 41.2, 43.64, 43.64, 46.24, 46.24, 49.0, 51.9, 51.9, 55.0, 58.26, 58.26, 61.72, 65.4, 61.72, 65.4, 69.28, 69.28, 73.4, 77.76, 77.76, 82.4, 82.4, 87.28, 87.28, 92.48, 92.48, 98.0, 103.8, 103.8, 110.0, 116.52, 116.52, 123.44, 130.8, 123.44, 130.8, 138.56, 138.56, 146.8, 155.52, 155.52, 164.8, 164.8, 174.56, 174.56, 184.96, 184.96, 196.0, 207.6, 207.6, 220.0, 233.04, 233.04, 246.88, 261.6, 246.88, 261.6, 277.12, 277.12, 293.6, 311.04, 311.04, 329.6, 329.6, 349.12, 349.12, 369.92, 369.92, 392.0, 415.2, 415.2, 440.0, 466.08, 466.08,
           493.76, 523.2, 493.76, 523.2, 554.24, 554.24, 587.2, 622.08, 622.08, 659.2, 659.2, 698.24, 698.24, 739.84, 739.84, 784.0, 830.4, 830.4, 880.0, 932.16, 932.16, 987.52, 1046.4, 987.52, 1046.4, 1108.48, 1108.48, 1174.4, 1244.16, 1244.16, 1318.4, 1318.4, 1396.48, 1396.48, 1479.68, 1479.68, 1568.0, 1660.8, 1660.8, 1760.0, 1864.32, 1864.32, 1975.04, 2092.8, 1975.04, 2092.8, 2216.96, 2216.96, 2348.8, 2488.32, 2488.32, 2636.8, 2636.8, 2792.96, 2792.96, 2959.36, 2959.36, 3136.0, 3321.6, 3321.6, 3520.0, 3728.64, 3728.64, 3950.08, 4185.6, 3950.08, 4185.6, 4433.92, 4433.92, 4697.6, 4976.64, 4976.64, 5273.6, 5273.6, 5585.92, 5585.92, 5918.72, 5918.72, 6272.0, 6643.2, 6643.2, 7040.0, 7457.28, 7457.28, 7900.16, 8371.2, 7900.16]


def make_note(freq: float, t: np.ndarray, A: float, phase_shift=0):
    omega = 2*np.pi*freq
    wave = np.array(A*cos(omega*t+phase_shift) + 1j*A *
                    sin(omega*t+phase_shift), dtype=complex)
    shift = np.angle(wave[-1])
    return wave, shift


file_name = "C_Major_Scale_SaxMIDI.wav"
data, sr = sf.read("./Helper_Files/" + file_name)

# data = np.pad(data, int(sr/4), mode="constant", constant_values=0)

FFT_SIZE = 2**16
NUM_HARMONICS = 10

time_array = np.arange(0, len(data)/sr, 1/sr)
audio = np.zeros(len(time_array), dtype=complex)
rms_envelope = np.zeros(len(time_array), dtype=np.int16)


def normalize(array, low=0, high=1):
    return np.array(low+((array-min(array))*(high-low)/(max(array)-min(array))))


nyquist = int(sr/2)
frame_width = int(sr)
overlap = int(frame_width/4)
freqs = np.fft.fftfreq(FFT_SIZE, 1/sr)
start = 0
phase_shift = 0
# plt.plot(time_array, data)

while start <= len(data) - (frame_width + overlap):
    added_freq = []

    note = np.zeros(len(data[start:start+frame_width]), dtype=complex)

    fft = np.fft.fft(data[start:start+frame_width], n=FFT_SIZE)
    response = sorted(zip(np.abs(fft), abs(freqs)), reverse=True)

    # plt.figure()
    for mag, freq in response:
        if len(added_freq) < NUM_HARMONICS and freq not in added_freq:
            added_freq.append(freq)
            # plt.stem(freq, mag, markerfmt="")
            note_data, phase_shift = make_note(
                freq, time_array[start:start+frame_width], mag)
            note += note_data
        elif len(added_freq) >= NUM_HARMONICS:
            break
    audio[start:start+frame_width] = note
    start += (frame_width - overlap)

audio = normalize(audio, -2**15, 2**15)
audio = np.array(np.real(audio), dtype=np.int16)
rms_envelope = np.array(np.real(rms_envelope), dtype=np.int16)

plt.figure()
plt.plot(audio)
sf.write("./Output_Audio/Synthesized_" + file_name, audio, sr)
plt.show()
