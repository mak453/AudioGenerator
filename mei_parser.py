import xml.etree.ElementTree as et
import numpy as np

ns = {'default': 'http://www.music-encoding.org/ns/mei',
      'xml': 'http://www.w3.org/XML/1998/namespace'}

curr_depth = 0

staff_one = []
staff_two = []


def disect_mei(filename):
    global staff_one, staff_two
    mei = et.parse(filename)
    root = mei.getroot()
    version = root.attrib["meiversion"]

    depth(root[1], -1)

    return (staff_one, staff_two), version


staff_notes = []
measure_count = 0


def depth(elem, level):
    global curr_depth, measure_count, staff_notes, staff_one, staff_two

    staff = 1
    layer = 1

    for child in elem:

        tag = child.tag[38:]

        if tag == "chord":
            staff_notes.append([("temp", "temp", "temp")])
            continue

        if tag == "note":
            try:
                if child[0].attrib["accid"] == "f":
                    accid = "b"
                elif child[0].attrib["accid"] == "s":
                    accid = "#"
                elif child[0].attrib["accid"] == "n":
                    accid = "n"
            except:
                accid = ""
            finally:
                staff_notes.append(
                    (child.attrib["pname"].upper() + accid, child.attrib["oct"], "1/"+child.attrib["dur"]))

        if tag == "rest":
            staff_notes.append(
                ("rest", "rest", "1/"+child.attrib["dur"]))

        if tag == "mRest":
            staff_notes.append(
                ("mRest", "mRest", "mRest"))
        if tag == "staff":
            # print(str(" " * level) + tag + " #" + str(staff))

            staff += 1

            # print(measure_count, "#: ", staff_notes)

            if staff == 2:
                staff_two += staff_notes
                measure_count += 1
            else:
                staff_one += staff_notes

            staff_notes = []

        if tag == "layer":
            layer += 1

        depth(child, level + 1)


def convert_to_music_xml():
    return
