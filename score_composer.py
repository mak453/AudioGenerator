"""_summary_

"""


def check(*arg, exp):
    """_summary_

    Args:
        exp (_type_): _description_

    Raises:
        TypeError: _description_
    """

    error = False
    for num, (i, j) in enumerate(zip(arg, exp)):
        try:
            if type(i) != j:
                error = True
                raise TypeError()
        except TypeError:
            print("\targ" + str(num) + " expected type: " +
                  str(j) + " recieved type: " + str(type(i)))
            continue
    if error:
        exit()


class Note:
    """_summary_
    """

    def __init__(self, pitch, octave, duration):
        check(pitch, octave, duration, exp=[str, str, str])
        self.pitch = pitch
        self.octave = octave
        self.duration = duration

    def __str__(self):
        return self.pitch + " " + str(self.octave) + " " + str(self.duration)


class Chord:

    def __init__(self):
        self.event = []
        self.current = 0
        self.size = 0

    def make_note_in_chord(self, pitch, octave, duration):
        """_summary_

        Args:
            pitch (_type_): _description_
            octave (_type_): _description_
            duration (_type_): _description_
        """
        new_note = Note(pitch, octave, duration)
        self.event.append(new_note)
        self.size += 1

    def __str__(self):
        notes = []

        for i in self.event:
            notes.append(str(i))

        notes = ", ".join(notes)

        return str("CHORD " + notes)

    def __iter__(self):
        return self

    def __next__(self):  # Python 2: def next(self)
        self.current += 1
        if self.current <= self.size:
            return self.event[self.current-1]

        raise StopIteration


class Staff:

    def __init__(self):
        self.notes = []
        self.current = 0
        self.size = 0

    def add_event(self, new_event):
        """_summary_

        Args:
            new_event (_type_): _description_
        """
        self.notes.append(new_event)
        self.size += 1

    def add_note(self, new_note):
        """_summary_

        Args:
            new_note (_type_): _description_
        """
        self.notes.append(new_note)
        self.size += 1

    def add_chord(self, new_chord):
        """_summary_

        Args:
            new_chord (_type_): _description_
        """
        check(new_chord, exp=[Chord])
        self.notes.append(new_chord)
        self.size += 1

    def __str__(self):
        events = []

        for i in self.notes:
            events.append(str(i))

        events = "|".join(events)

        return events

    def __iter__(self):
        return self

    def __next__(self):  # Python 2: def next(self)
        self.current += 1
        if self.current < self.size:
            return self.notes[self.current-1]
        raise StopIteration


class Score:
    """_summary_
    """
    key_signatures = {
        "0 major": ("C", 0, 0, "major"),
        "1s major": ("G", 1, 0, "major"),
        "2s major": ("D", 2, 0, "major"),
        "3s major": ("A", 3, 0, "major"),
        "4s major": ("E", 4, 0, "major"),
        "5s major": ("B", 5, 0, "major"),
        "6s major": ("F#", 6, 0, "major"),
        "5f major": ("Db", 0, 5, "major"),
        "4f major": ("Ab", 0, 4, "major"),
        "3f major": ("Eb", 0, 3, "major"),
        "2f major": ("Bb", 0, 2, "major"),
        "1f major": ("F", 0, 1, "major"),
        "0 minor": ("A", 0, 0, "minor"),
        "1s minor": ("E", 1, 0, "minor"),
        "2s minor": ("B", 2, 0, "minor"),
        "3s minor": ("F#", 3, 0, "minor"),
        "4s minor": ("C#", 4, 0, "minor"),
        "5s minor": ("G#", 5, 0, "minor"),
        "6s minor": ("D#", 6, 0, "minor"),
        "5f minor": ("Bb", 0, 5, "minor"),
        "4f minor": ("F", 0, 4, "minor"),
        "3f minor": ("C", 0, 3, "minor"),
        "2f minor": ("G", 0, 2, "minor"),
        "1f minor": ("D", 0, 1, "minor")
    }

    def __init__(self):
        self.title = "Title"
        self.composer = "Composer"

        self.key = ("C", 0, 0, "major")
        self.tempo = (112, "Moderato")
        self.time_sig = (4, 4)

        self.staffs: Staff = []
        self.current = 0
        self.size = 0
        self.initialized = False

    def add_staff(self, new_staff: Staff):
        """Add a staff object to the score."""
        check(new_staff, exp=[Staff])
        self.staffs.append(new_staff)
        self.size += 1

    def disp(self):
        """_summary_
        """
        print(self.title + " by " + self.composer + "\n" + str(self.key[0]) + " " + str(self.key[3]) +
              " | Time Signature: " + str(self.time_sig[0]) + "/" + str(self.time_sig[1]) + "\nTempo " + str(self.tempo[0]) + " BPM\n")

    def __str__(self):

        string = self.title + " by " + self.composer + "\n\n"

        for i, staff in enumerate(self.staffs):
            string += "Staff " + str(i+1) + ": " + str(staff) + "\n\n"

        return string

    def __iter__(self):
        return self

    def __next__(self):  # Python 2: def next(self)
        self.current += 1
        if self.current < self.size:

            return self.staffs[self.current-1]
        raise StopIteration
