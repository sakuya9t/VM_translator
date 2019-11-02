import os
import VmParser


class FileHandler:

    def __init__(self, path):
        self.asm_code = []
        self.path = path
        if not self.isdir():
            self.asm_code += self.parse(self.path)
        else:
            files = self.find_files()
            for file in files:
                self.asm_code += self.parse(file)

    def parse(self, filename):
        vm_code = self.read(filename)
        class_name = str.split(filename, "\\")[-1]
        vm_parser = VmParser.VmParser(vm_code, class_name)
        asm_code = vm_parser.get_hack_code()
        return asm_code

    def find_files(self):
        vm_files = []
        path_dir = os.listdir(self.path)
        for filename in path_dir:
            if filename[-3:] == ".vm":
                vm_files.append(filename)
        if vm_files.__contains__("Sys.vm"):
            vm_files.remove("Sys.vm")
            vm_files.insert(0, "Sys.vm")
        for i in range(vm_files.__len__()):
            vm_files[i] = os.path.join('%s/%s' % (self.path, vm_files[i]))
        return vm_files

    def read(self, filename):
        file_object = open(filename)
        try:
            file_content = file_object.readlines()
        finally:
            file_object.close()
        return file_content

    def write(self, filename):
        file_object = open(filename, 'w')
        file_object.writelines(self.asm_code)
        file_object.close()

    def append_enter(self):
        length = len(self.asm_code)
        for i in range(0, length - 1):
            if not self.asm_code[i].__contains__("\n"):
                self.asm_code[i] += "\n"

    def isdir(self):
        if os.path.isdir(self.path):
            return True
        else:
            return False
