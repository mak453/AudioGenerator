import argparse
import mei_parser as mei_parser
import synthesizer as synth
import wave as wv


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
                        default="output.wav", help='Output filename')
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

    args = parser.parse_args()

    # print(args.mei_file)

    scores, version = mei_parser.disect_mei(args.mei_file)

    # one = song()
    # one.sample_rate = args.sample_rate
    # one.bit_depth = args.bit_depth
    # one.channels = args.channels
    # one.create_file(score)

    if args.music_xml:
        mei_parser.convert_to_music_xml()

    if args.show_version:
        display_information()
