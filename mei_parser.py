import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element
from score_composer import Score, Chord, Note
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

        traverse(root, new_score)

        scores.append(new_score)
        input()

    return scores, version


def traverse(root, score):

    for element in root:
        traverse(element, score)
