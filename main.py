import bmp_parser as bm
import argparse


def main():
    try:
        args = parse_args()
        if args.file is None:
            filename = specify_filename()
        else:
            filename = args.file
        run_console_mode(filename)
    except Exception as e:
        print("Error: " + str(e))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file to extract")
    return parser.parse_args()


def specify_filename():
    name = input("Specify file name: ")
    while name == '':
        name = input("Specify file name: ")
    return name


def run_console_mode(filename):
    parser = bm.BMPParser()
    with open(filename, 'rb') as file:
        parser.parse(file)
    for prop in parser:
        print(*prop)


if __name__ == '__main__':
    main()
