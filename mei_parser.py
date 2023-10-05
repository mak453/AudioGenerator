import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element
from score_composer import Score, Chord, Note
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

        traverse(root, new_score, -1)

        scores.append(new_score)
        input()

    return scores, version


def traverse(root: Element, score: Score, level: int):
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
        for elem in root.iter():
            tag_name = elem.tag

    for child in root:
        traverse(child, score, level+1)
