def check(*arg, exp):
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
    def __init__(self, pitch, octave, duration):
        check(pitch, octave, duration, exp=[str, str, str])
        self.pitch = pitch
        self.octave = octave
        self.duration = duration

    def accidental(self, accid: str):
        check(accid, exp=[str])
        self.pitch = self.pitch+accid

    def __str__(self):
        return self.pitch + " " + str(self.octave) + " " + str(self.duration)

    def split(self):
        return str(self).split(" ")


class Chord:

    def __init__(self):
        self.event = []
        self.current = 0
        self.size = 0

    def make_note_in_chord(self, pitch, octave, duration):
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

    def split(self):
        return str(self).split(" ")


class Staff:

    def __init__(self):
        self.notes = []
        self.current = 0
        self.size = 0

    def add_event(self, new_event):
        self.notes.append(new_event)
        self.size += 1

    def add_note(self, new_note):
        self.notes.append(new_note)
        self.size += 1

    def add_chord(self, new_chord):
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

    def split(self):
        return str(self).split("|")


class Score:

    def __init__(self):
        self.title = "Title"
        self.composer = "Composer"
        self.key = "Key"
        self.tempo = 90
        self.time_sig = "4/4"
        self.staffs: Staff = []
        self.current = 0
        self.size = 0

    def add_staff(self, new_staff: Staff):
        """Add a staff object to the score."""
        check(new_staff, exp=[Staff])
        self.staffs.append(new_staff)
        self.size += 1

    def disp(self):
        print(self.title + " by " + self.composer + "\n" + self.key +
              " | Time Signature: " + self.time_sig + "\nTempo: " + str(self.tempo) + "\n")

    def __str__(self):
        string = self.title + " by " + self.composer
        string += "\n" + self.key + " | Time Signature: " + self.time_sig
        string += "\nTempo: " + str(self.tempo) + "\n\n"

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
