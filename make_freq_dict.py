import numpy as np
pitches = [
    16.35,
    17.32,
    17.32,
    18.35,
    19.44,
    19.44,
    20.6,
    21.82,
    23.12,
    23.12,
    24.5,
    25.95,
    25.95,
    27.5,
    29.13,
    29.13,
    30.86,
]
names = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F",
         "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

with open("pitches.txt", "w") as f:

    f.write("pitches = {\n")
    for octave in range(9):
        for i in range(len(pitches)):
            f.write('"' + names[i] + str(octave) +
                    '": ' + str(np.round(pitches[i]*2**(octave), 2)) + ",\n")
    f.write('}')

f.close()
