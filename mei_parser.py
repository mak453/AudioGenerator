import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element
from score_composer import Score, Staff, Chord, Note
import numpy as np

ns = {'default': '{http://www.music-encoding.org/ns/mei}'}

SKIP = len(ns["default"])


def disect_mei(folder):

    scores = []

    for file in folder:
        print(file)

        mei = et.parse(file)
        root = mei.getroot()
        version = root.attrib["meiversion"]
        new_score = Score()

        traverse(root, -1, new_score)

        scores.append(new_score)
        input()

    return scores, version


def get_contained_elements(root: Element):
    elements = []
    names = []

    for elem in root:
        elements.append(elem)
        names.append(elem.tag[SKIP:])

    return elements, names


def has_accid(accid):
    if accid == "f":
        return "b"
    if accid == "s":
        return "#"
    if accid == "n":
        return "n"


def set_work_info(root: Element, score):
    elements, names = get_contained_elements(root)
    info = ["title", "composer"]

    if set(info).issubset(names):
        score.title = elements[names.index(info[0])].text

        sub_info = ["persName"]
        composer_elem, composer_name = get_contained_elements(
            elements[names.index(info[1])])

        if set(sub_info).issubset(composer_name):
            score.composer = composer_elem[names.index(info[0])].text

    return


def set_score_info(root, score):
    info = ["meter.count", "meter.unit", "keysig", "key.mode"]
    a = root.attrib

    if set(info).issubset(a):
        score.time_sig = (a[info[0]], a[info[1]])
        score.key = score.key_signatures[a[info[2]] + " " + a[info[3]]]
        return True
    # if set(info[0:1]).issubset(a):
    #     # add_event("")
    # elif set(info[2:3]).issubset(a):
    #     #add_event
    # else:
    #     #add_event

    return False


large_container = ["titleStmt", "scoreDef", "chord", "beam", "note"]


def get_info(root: Element, num, score):
    if num == 0:
        set_work_info(root, score)
    elif num == 1:
        if set_score_info(root, score):
            score.initialized = True
        # else:

    return


def traverse(root: Element, level, score):

    head = root.tag[SKIP:]
    if head in large_container:
        index = int(large_container.index(head))
        get_info(root, int(large_container.index(head)), score)
        if index == large_container[2] or index == large_container[3]:
            get_info(root, int(large_container.index(head)), score)

    for elem in root:
        traverse(elem, level+1, score)

    return


def convert_to_music_xml():
    return
