import argparse
import Dependencies.mei_parser as mei_parser
import Helper_Files.demo as demo
import Dependencies.synthesizer as synth
from Dependencies.score_composer import Score


def display_information():
    """_summary_
    """
    if args.music_xml:
        print("MEI v" + str(version))
        print("MusicXML v")
    else:
        print("MEI v" + str(version))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='MEI to Audio Converter', description='Generates WAV file from MEI file')
    parser.add_argument('mei_file', nargs='+', help='Input .mei file(s)')
    parser.add_argument('-out', '--output', nargs='*', type=str,
                        default=None, help='Output filename')
    parser.add_argument('-v', '--show_version', action='store_true',
                        help='Show MEI (and MusicXML) file format version')
    parser.add_argument('-s', '--sample_rate', type=int,
                        default=44100, help='Sample rate')
    parser.add_argument('-b', '--bit_depth', type=int,
                        default=16, help='Bit depth')
    parser.add_argument('-c', '--channels', type=int,
                        default=1, help='Number of channels')
    parser.add_argument('--music_xml', action='store_true',
                        help='Create MusicXML file from MEI file')
    parser.add_argument('--demo', action='store_true',
                        help='Demos current state of code')

    args = parser.parse_args()
    bits = args.bit_depth

    # print(args.mei_file)
    while bits not in [16, 32]:
        print("ERROR **Bit depth must be either 16 or 32")
        bits = int(input("Enter bit depth: "))

    Score.sample_rate = args.sample_rate
    Score.bit_depth = bits

    if args.demo:
        string = "\n\nDEMO (Reading in 3 .mei files and displaying score info)\n"
        string += "\tScore info: Title, Composer, Note Accidentals (Key), Time Signature\n"
        string += "\tNote info divided by each staff, layer, and notes/chords with their fundamental frequencies"
        string += "\n\tWhen a note is created the data samples for the fundamental freq are immediately created"

        #input(string)
        scores, version = demo.disect_mei(
            args.mei_file, args.sample_rate, args.bit_depth)

        string = "\n\nDEMO (Making major scale audio file from .mei file)\n"
        print("\n\n**********************************************************")
        #input(string)

        synth.make_audio_file(scores[-1], args.output)

    else:
        scores, version = mei_parser.disect_mei(
            args.mei_file, args.sample_rate, args.bit_depth, args.output)

    if args.music_xml:
        mei_parser.convert_to_music_xml()

    if args.show_version:
        display_information()
