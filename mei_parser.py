import xml.etree.ElementTree as et
from score_composer import Score, Staff, Chord, Note
import numpy as np

ns = {'default': 'http://www.music-encoding.org/ns/mei',
      'xml': 'http://www.w3.org/XML/1998/namespace'}

skip_ns = len("{" + ns["default"] + "}")


def disect_mei(folder):
    global num_staves
    scores = []

    for file in folder:
        print(file)

        num_staves = 1
        curr_measure = 0
        prev_measure = -1
        curr_staff = Staff

        mei = et.parse(file)
        root = mei.getroot()
        version = root.attrib["meiversion"]

        score = Score()

        traverse2(root, -1, score)

        print(score)
        scores.append(score)
        input()

    return scores, version


desired_tags = ["title", "persName", "staffDef", "chord", "note", "staff", "rest",
                "mRest", "layer", "meter"]

inChord = False
curr_chord = Chord()
curr_staff = Staff()
chord_dur = 0
set_title = 1


def traverse2(root, level, score: Score):
    global num_staves, inChord, curr_chord, chord_dur, curr_staff, set_title

    head = root.tag[skip_ns:]

    if head == 'measure':
        print("   " * level + "| " + head + "\t\tM" + root.attrib['n'])
    else:
        print("   " * level + "| " + head)

    if head in desired_tags:
        # print("   " * level + " \ " + str(root.text) + " " + str(root.attrib))
        if set_title >= 0 and head == desired_tags[0]:
            set_title -= 1
            score.title = root.text
        if head == desired_tags[1] and 'role' in root.attrib and root.attrib['role'] == 'composer':
            score.composer = root.text
        if head == desired_tags[2] and 'n' in root.attrib and int(root.attrib['n']) == num_staves:
            curr_staff = Staff()
            num_staves += 1
            score.staffs.append(curr_staff)
        if head == desired_tags[5] and 'n' in root.attrib:
            curr_staff = score.staffs[int(root.attrib['n'])-1]
        if head == desired_tags[3] or (head == desired_tags[8] and 'n' in root.attrib and int(root.attrib['n']) > 1):

            inChord = True
            curr_chord = Chord()

            if head == desired_tags[3]:
                chord_dur = root.attrib["dur"]

            for elem in root:
                if elem.tag[skip_ns:] != "note":
                    inChord = False
                    return
                print("   " * (level+1) + "| " + elem.tag[skip_ns:])

            curr_staff.add_chord(curr_chord)
        if head == desired_tags[6] or head == desired_tags[7]:
            inChord = False
            if 'dur' in root.attrib:
                curr_staff.add_note(Note('REST', '0', root.attrib['dur']))
            else:
                curr_staff.add_note(
                    Note('REST', '0', score.time_sig.split('/')[0]))
        if head == desired_tags[4]:
            a = root.attrib
            pitch = str(a['pname']).upper()

            if "accid" in a:
                if a['accid'] == 'f':
                    pitch += 'b'
                elif a['accid'] == 's':
                    pitch += '#'

            if inChord:
                curr_chord.make_note_in_chord(pitch, a['oct'], chord_dur)
            else:
                curr_staff.add_note(Note(pitch, a['oct'], a['dur']))

    for elem in root:
        traverse2(elem, level+1, score)

    return


# def traverse(elem, level, score: composer.Score):
    # global num_staves, curr_measure, prev_measure, curr_staff

    # head = elem.tag[skip_ns:]
    # print(" " * level + "| " + head)

    # if head == "work":
    #     for tag in elem:
    #         name = tag.tag[skip_ns:]
    #         if name == "title":
    #             score.title = tag.text
    #         elif name == "composer":
    #             for tag2 in tag:
    #                 name2 = tag2.tag[skip_ns:]
    #                 if name2 == "persName":
    #                     score.composer = tag2.text
    #         elif name == "key":
    #             pitch = tag.attrib["pname"].upper()

    #             try:
    #                 accid = tag.attrib["accid"]
    #                 if accid == "f":
    #                     pitch += "b"
    #                 else:
    #                     pitch += "#"
    #             except:
    #                 pass

    #             score.key = pitch + " " + tag.attrib["mode"]
    #         elif name == "meter":
    #             score.time_sig = str(
    #                 tag.attrib["count"]) + "/" + tag.attrib["unit"]
    #     return

    # if "staff" in head:
    #     if head == "staffGrp":
    #         for tag in elem:
    #             if "n" in tag.attrib and num_staves + 1 <= int(tag.attrib["n"]):
    #                 num_staves += 1
    #                 score.add_staff(composer.Staff(num_staves))
    #         return
    #     elif head == "staff":
    #         staff_num = int(elem.attrib["n"])
    #         # print(staff_num)
    #         curr_staff = score.staffs[staff_num-1]

    # if "measure" in head:
    #     # print(" " * level + " \ " + str(elem.attrib.values()))
    #     if "n" in elem.attrib and curr_measure == int(elem.attrib["n"]):
    #         return
    #     curr_measure += 1

    # if "chord" in head and prev_measure < curr_measure:
    #     curr_chord = composer.Chord()
    #     dur = elem.attrib["dur"]
    #     for note in elem:
    #         if "note" in note.tag[skip_ns:]:
    #             pitch = note.attrib["pname"].upper()
    #             oct = note.attrib["oct"]
    #             try:
    #                 accid = note.attrib["accid"]
    #                 if accid == "f":
    #                     pitch += "b"
    #                 else:
    #                     pitch += "#"
    #             except:
    #                 pass

    #             curr_chord.make_note_in_chord(pitch, oct, dur)

    #     # print(" " * level + " \ S" + curr_staff.name + " M" + str(curr_measure) + " " +
    #     #       str(curr_chord))
    #     curr_staff.add_chord(curr_chord)
    #     return

    # if head in ["rest", "mRest", "note"] and prev_measure < curr_measure:
    #     if head == "rest":
    #         pitch = "rest"
    #         oct = ""
    #         dur = elem.attrib["dur"]
    #     elif head == "mRest":
    #         pitch = "rest"
    #         oct = ""
    #         dur = score.time_sig.split('/')[0]
    #     else:
    #         pitch, oct, dur = accidental(elem)

    #     new_note = composer.Note(pitch, oct, dur)

    #     curr_staff.add_note(new_note)

    # for node in elem:
    #     traverse(node, level+1, score)

    # return


def convert_to_music_xml():
    return
