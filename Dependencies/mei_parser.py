"""

"""
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element
from Dependencies.score_composer import Score, Chord, Staff, Note
import Dependencies.synthesizer as synthesizer
import numpy as np

ns = {'default': '{http://www.music-encoding.org/ns/mei}'}

SKIP = len(ns["default"])


def disect_mei(folder: list, sample_rate: int, bit_depth: int, output_filepath):
    """_summary_

    Args:
        folder (list): _description_

    Returns:
        _type_: _description_
    """
    scores = []

    Score.sample_rate = sample_rate
    Score.bit_depth = bit_depth

    for num, file in enumerate(folder):
        mei = et.parse(file)
        root = mei.getroot()
        version = root.attrib["meiversion"]
        new_score = Score()

        traverse(root, new_score)
        synthesizer.make_audio_file(new_score, output_filepath)

        scores.append(new_score)
        #input()

    return scores, version


def set_score_info(element: Element, score: Score, found):
    """_summary_

    Args:
        element (Element): _description_
        score (Score): _description_
        found (_type_): _description_

    Returns:
        _type_: _description_
    """
    info = ["title", "persName", "key", "meter"]
    tag_name = element.tag[SKIP:]
    attributes = element.attrib

    if info[found] == "title" and tag_name == "title":
        score.set_title(element.text)
        return True

    if info[found] == "persName" and "role" in element.attrib and element.attrib["role"] == "composer":
        score.set_composer(element.text)
        return True

    if info[found] == "key" and tag_name == "key":
        name = element.attrib["pname"].upper()
        if "accid" in element.attrib and element.attrib["accid"] == "f":
            name += "b"
        elif "accid" in element.attrib and element.attrib["accid"] == "s":
            name += "#"
        elif "mode" in element.attrib and element.attrib["mode"] == "minor":
            name += "m"

        score.set_key(name)
        return True

    if info[found] == "meter" and "count" in attributes and "unit" in attributes:
        score.set_time_sig(
            element.attrib["count"], element.attrib["unit"])
        return True

    return False


def note_event(note_elem: Element, score: Score):
    """_summary_

    Args:
        note_elem (Element): _description_
        score (Score): _description_

    Returns:
        _type_: _description_
    """

    attrib = note_elem.attrib

    pitch = attrib["pname"].upper()
    if "accid.ges" in attrib and attrib["accid.ges"] == "n":
        pitch = attrib["pname"].upper()
    elif ("accid.ges" in attrib and attrib["accid.ges"] == "f") or (pitch in score.key_accidentals and score.key_accidentals[0] == "B"):
        pitch += "b"
    elif ("accid.ges" in attrib and attrib["accid.ges"] == "s") or (pitch in score.key_accidentals and score.key_accidentals[0] == "F"):
        pitch += "#"

    pitch += attrib["oct"]

    return str(pitch)


def chord_event(chord_elem: Element, score: Score):
    """_summary_

    Args:
        chord_elem (Element): _description_
        score (Score): _description_

    Returns:
        _type_: _description_
    """
    new_chord = Chord()
    duration = 0

    for chord_note in chord_elem.iter(ns["default"] + "note"):
        if "dots" in chord_elem.attrib:
            duration = float(chord_elem.attrib["dur"]) + \
                float(chord_elem.attrib["dur"])/2.0
        else:
            duration = float(chord_elem.attrib["dur"])

        new_note = Note(note_event(chord_note, score),
                        duration)
        synthesizer.set_data(score, new_note)
        new_chord.add_note_to_chord(new_note)

    new_chord.length = duration
    return new_chord


def beam_event(beam_elem: Element, staff: Staff, score: Score, curr_measure=0, curr_layer=0):
    """_summary_

    Args:
        note (Element): _description_
        score (Score): _description_
        staff_num (int): _description_
    """

    for elem in beam_elem:
        tag_name = elem.tag[SKIP:]
        if tag_name == "note":
            if "dots" in elem.attrib:
                duration = float(elem.attrib["dur"]) + \
                    float(elem.attrib["dur"])/2
            else:
                duration = float(elem.attrib["dur"])
            new_event = Note(note_event(elem, score),
                             duration)
            synthesizer.set_data(score, new_event)
        elif tag_name == "chord":
            new_event = chord_event(elem, score)
            synthesizer.set_data(score, new_event)

        staff.add_event_to_layer(new_event, curr_layer, curr_measure)


def traverse(root: Element, score: Score):
    """_summary_

    Args:
        root (Element): _description_
        score (Score): _description_
    """
    found = 0
    curr_measure = 0
    curr_staff = Staff
    curr_layer = 0

    for element in root.iter():
        if found < 4 and set_score_info(element, score, found):
            found += 1
        elif found >= 4:
            break

    for measure in root.iter(ns["default"] + "measure"):
        if "n" in measure.attrib and int(measure.attrib["n"]) > curr_measure:
            curr_measure += 1
            score.num_measures += 1
            for staff in measure.iter(ns["default"] + "staff"):
                if "n" in staff.attrib and int(staff.attrib["n"]) > len(score.staves):
                    score.add_staff_to_score()
                if "n" in staff.attrib:
                    curr_staff = score.get_staff(int(staff.attrib["n"])-1)

                    for layer in staff.iter(ns["default"] + "layer"):
                        if "n" in layer.attrib and int(layer.attrib["n"]) > len(curr_staff.layers):
                            curr_staff.add_layer_to_staff()
                        if "n" in layer.attrib:
                            curr_layer = int(layer.attrib["n"])-1

                        for event_elem in layer:
                            event = event_elem.tag[SKIP:]
                            if event == "beam":
                                beam_event(
                                    event_elem, curr_staff, score, curr_measure, curr_layer)
                            else:
                                if event == "note":
                                    pitch = note_event(
                                        event_elem, score)
                                    if "dots" in event_elem.attrib:
                                        duration = float(
                                            event_elem.attrib["dur"]) + float(event_elem.attrib["dur"])/2
                                    else:
                                        duration = float(
                                            event_elem.attrib["dur"])
                                    new_event = Note(
                                        pitch, duration)
                                elif event == "chord":
                                    new_event = chord_event(
                                        event_elem, score)
                                elif event == "rest":
                                    if "dots" in event_elem.attrib:
                                        duration = float(
                                            event_elem.attrib["dur"]) + int(event_elem.attrib["dur"])/2
                                    else:
                                        duration = float(
                                            event_elem.attrib["dur"])
                                    new_event = Note(
                                        "rest", duration)

                                elif event == "mRest":
                                    new_event = Note(
                                        "mRest", float(score.time_sig[0]))

                                new_event.measure = curr_measure
                                synthesizer.set_data(score, new_event)
                                curr_staff.add_event_to_layer(
                                    new_event, curr_layer, curr_measure)

    return
