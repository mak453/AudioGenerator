import xml.etree.ElementTree as et
import Dependencies.mei_parser as mei_parser
from Dependencies.score_composer import Score

ns = {'default': '{http://www.music-encoding.org/ns/mei}'}

SKIP = len(ns["default"])


def disect_mei(folder: list, sample_rate: int, bit_depth: int):
    """_summary_

    Args:
        folder (list): _description_
        sample_rate (int): _description_
        bit_depth (int): _description_

    Returns:
        scores (list): a list of Score objects containing all of a music pieces information
        version (str): a string of the MEI format version the file is made with 
    """
    scores = []

    Score.sample_rate = sample_rate
    Score.bit_depth = bit_depth

    for file in folder:
        print("\n\n---------------------------------------------------------\n" + str(file))

        mei = et.parse(file)
        root = mei.getroot()
        version = root.attrib["meiversion"]
        new_score = Score()

        mei_parser.traverse(root, new_score)
        #input("Press 'ENTER' to print information\n")

        scores.append(new_score)
        #input()

    return scores, str(version)
