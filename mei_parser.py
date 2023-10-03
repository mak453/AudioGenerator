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

    if not score.initialized and set(info).issubset(a):
        score.time_sig = (a[info[0]], a[info[1]])
        score.key = score.key_signatures[a[info[2]] + " " + a[info[3]]]
        score.disp()
        return 1

    return 0


large_container = ["titleStmt", "scoreDef",
                   "staffDef", "chord", "beam", "note"]


def get_info(root: Element, num, score):

    if num == 0:
        set_work_info(root, score)
    elif num == 1:
        action = set_score_info(root, score)
        if action == 1:
            score.initialized = True
    elif score.initialized and num == 2:
        if int(root.attrib["n"]) > len(score.staffs):

            curr_staff.add_event(
                "Key change " + str(score.key[0]) + " " + str(score.key[3]))
            curr_staff.add_event(
                "Time change " + str(score.time_sig[0]) + "/" + str(score.time_sig[1]))
            curr_staff.add_event(
                "Tempo change " + str(score.tempo[0]) + " " + str(score.tempo[1]))

            score.staffs.append(curr_staff)
            print("new staff " + str(len(score.staffs)))
        else:
            curr_staff

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
