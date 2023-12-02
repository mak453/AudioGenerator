import argparse
import Dependencies.mei_parser as mei_parser
import Helper_Files.demo as demo
import Dependencies.Instruments as instruments
from Dependencies.score_composer import Score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='MEI to Audio Converter', description='Generates WAV file from MEI file')
    parser.add_argument('mei_file', nargs='+', help='Input .mei file(s)')
    parser.add_argument('-out', '--output', nargs='*', type=str,
                        default="default", help='Output filename')
    parser.add_argument('-tempo', '--tempo', type=float, default=60.0)
    parser.add_argument('-instrument', '--instrument', type=str,
                        default='mandolin', help='Select instrument to synthesize')
    # parser.add_argument('-v', '--show_version', action='store_true',
    #                     help='Show MEI (and MusicXML) file format version')
    # parser.add_argument('-s', '--sample_rate', type=int,
    #                     default=44100, help='Sample rate')
    # parser.add_argument('-b', '--bit_depth', type=int,
    #                     default=16, help='Bit depth')
    # parser.add_argument('-c', '--channels', type=int,
    #                     default=1, help='Number of channels')
    # parser.add_argument('--music_xml', action='store_true',
    #                     help='Create MusicXML file from MEI file')
    # parser.add_argument('--demo', action='store_true',
    #                     help='Demos current state of code')

    args = parser.parse_args()
    # bits = args.bit_depth

    # # print(args.mei_file)
    # while bits not in [16, 32]:
    #     print("ERROR **Bit depth must be either 16 or 32")
    #     bits = int(input("Enter bit depth: "))

    # Score.sample_rate = args.sample_rate
    # Score.bit_depth = bits

    scores, version = mei_parser.disect_mei(args.mei_file, args.output, args.tempo, args.instrument)

    # if args.music_xml:
    #     mei_parser.convert_to_music_xml()

    # if args.show_version:
    #     display_information()
