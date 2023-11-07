import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf


class GuitarSynth:
    def __init__(self, fundamental_freq=440.0, note_time=1.0, sampling_rate=44100):
        """Inits the guitar string."""
        self.freq = fundamental_freq
        self.num_samples = note_time*sampling_rate
        self.fs = sampling_rate
        self.data = self.karplus_strong()

    def karplus_strong(self):
        
        N = self.fs // int(self.freq)

        noise = 2.0*np.random.random(self.num_samples)-1
        y = np.zeros(self.num_samples)

        for n in range(0, self.num_samples):
            y[n] = (y[n-N] + y[n-N+1])/2 if n >= N else noise[n]
            print("n: " + str(n) + "\t" + str(y[n]))

        return y
