import VmParser
import FileHandler
import sys


class VMTranslator:
    def __init__(self, filename):
        if str.find(filename, '.') != -1:
            class_name = str.split(filename, ".")[0]
            target_name = class_name + ".asm"
            if not "vm".__eq__(str.split(filename, ".")[1]):
                print("File type error, .vm file expected.")
                return
        else:
            class_name = str.split(filename, "\\")[-1]
            target_name = filename + "\\" + class_name + ".asm"
        file_handler = FileHandler.FileHandler(filename)
        file_handler.append_enter()
        file_handler.write(target_name)


def main(filename):
    VMTranslator(filename)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filename")
        exit(1)
    main(sys.argv[1])
