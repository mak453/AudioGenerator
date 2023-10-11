import numpy as np

pitches = [
    16.35,
    17.32,
    17.32,
    18.35,
    19.44,
    19.44,
    20.6,
    20.6,
    21.82,
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
    32.7,
    30.86
]


names = ["C", "C#", "Db", "D", "D#", "Eb", "E", "E#", "Fb", "F",
         "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B", "B#", "Cb"]

with open("pitches.txt", "w", encoding="utf-8") as f:

    f.write("pitches = {\n")
    for octave in range(9):
        for num, i in enumerate(pitches):
            f.write('"' + names[num] + str(octave) +
                    '": ' + str(np.round(i*2**(octave), 2)) + ",\n")
    f.write('}')

f.close()
