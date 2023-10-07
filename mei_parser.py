import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element
from score_composer import Score, Chord, Staff
import numpy as np

ns = {'default': '{http://www.music-encoding.org/ns/mei}'}

SKIP = len(ns["default"])


def disect_mei(folder: list):
    """_summary_

    Args:
        folder (list): _description_

    Returns:
        _type_: _description_
    """
    scores = []

    for file in folder:
        print(file)

        mei = et.parse(file)
        root = mei.getroot()
        version = root.attrib["meiversion"]
        new_score = Score()

        traverse(root, new_score)

        print(new_score)

        scores.append(new_score)
        input()

    return scores, version


# def traverse(root: Element, score: Score, level: int):
    """_summary_

    Args:
        root (Element): _description_
        score (Score): _description_
        level (int): _description_
    """
    # print(" "*level + "| " + root.tag)

    if root.tag == ns["default"] + "workList":
        for elem in root.iter():
            tag_name = elem.tag

            if tag_name == ns["default"] + "title":
                score.set_title(elem.text)
            elif tag_name == ns["default"] + "persName":
                score.set_composer(elem.text)
            elif tag_name == ns["default"] + "key":
                name = elem.attrib["pname"].upper()
                if "accid" in elem.attrib:
                    if elem.attrib["accid"] == "f":
                        name += "b"
                    else:
                        name += "#"
                print(name)
                score.set_key(name)
            elif tag_name == ns["default"] + "meter":
                score.set_time_sig(elem.attrib["count"], elem.attrib["unit"])

    if root.tag == ns["default"] + "section":
        for num, elem in enumerate(root.iter()):
            tag_name = elem.tag[SKIP:]
            print(tag_name)

            if tag_name == "staff" and int(elem.attrib["n"]) > len(score.staves):
                print("New staff detected")
                score.add_staff_to_score()
            elif tag_name == "staff":
                curr_staff = int(elem.attrib["n"])-1

            if tag_name == "chord":
                print("\tNew chord detected")
                new_chord = Chord()
                score.add_chord_to_staff(new_chord, curr_staff)

    for child in root:
        traverse(child, score, level+1)


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

    name = attrib["pname"].upper()
    if "accid.ges" in attrib and attrib["accid.ges"] == "f":
        name += "b"
    elif "accid.ges" in attrib and attrib["accid.ges"] == "s":
        name += "#"
    elif name in score.key_accidentals:
        if score.key_accidentals[0] == "F":
            name += "#"
        elif score.key_accidentals[0] == "B":
            name += "b"

    name += attrib["oct"]

    return name


def chord_event(chord_elem: Element, score: Score):
    """_summary_

    Args:
        chord_elem (Element): _description_
        score (Score): _description_

    Returns:
        _type_: _description_
    """
    new_chord = Chord()

    for chord_note in chord_elem.iter(ns["default"] + "note"):
        new_chord.add_note_to_chord(
            note_event(chord_note, score), chord_elem.attrib["dur"])

    return new_chord


def beam_event(beam_elem: Element, score: Score, staff: Staff, layer_num=0):
    """_summary_

    Args:
        note (Element): _description_
        score (Score): _description_
        staff_num (int): _description_
    """
    for elem in beam_elem:
        tag_name = elem.tag[SKIP:]
        if tag_name == "note":
            staff.add_note_to_layer(note_event(
                elem, score), elem.attrib["dur"], layer_num)
        elif tag_name == "chord":
            new_chord = chord_event(elem, score)
            staff.add_chord_to_layer(new_chord, layer_num)


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
            # print("Measure " + measure.attrib["n"])
            for staff in measure.iter(ns["default"] + "staff"):
                if "n" in staff.attrib and int(staff.attrib["n"]) > len(score.staves):
                    score.add_staff_to_score()
                    curr_staff = score.staves[int(staff.attrib["n"])-1]
                elif "n" in staff.attrib:
                    curr_staff = score.staves[int(staff.attrib["n"])-1]

                # print("\tStaff " + str(curr_staff))

                for layer in staff.iter(ns["default"] + "layer"):
                    if "n" in layer.attrib and int(layer.attrib["n"]) > len(curr_staff.layers):
                        curr_staff.add_layer_to_staff()
                        curr_layer = int(layer.attrib["n"])-1
                    elif "n" in layer.attrib:
                        curr_layer = int(layer.attrib["n"])-1

                    # print("\t\tLayer " + str(curr_layer))

            for event_elem in layer:
                event = event_elem.tag[SKIP:]
                if event == "beam":
                    beam_event(event_elem, score,
                               curr_staff, curr_layer)
                elif event == "note":
                    curr_staff.add_note_to_layer(note_event(
                        event_elem, score), event_elem.attrib["dur"], curr_layer)
                elif event == "chord":
                    new_chord = chord_event(event_elem, score)
                    curr_staff.add_chord_to_layer(
                        new_chord, curr_layer)
                elif event == "rest":
                    curr_staff.add_note_to_layer(
                        "rest", event_elem.attrib["dur"], curr_layer)
                elif event == "mRest":
                    curr_staff.add_note_to_layer(
                        "mRest", score.time_sig[0], curr_layer)

    return
