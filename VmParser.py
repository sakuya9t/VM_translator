import consts
import CodeWriter


class VmParser:
    code = []

    def __init__(self, vm_code, class_name):
        self.code = vm_code
        self.constValues = consts.consts()
        self.code_writer = CodeWriter.CodeWriter(self.parse(), str.split(class_name, "/")[-1])

    def parse(self):
        code_list = []
        b_init = False
        for code_line in self.code:
            code_line = str.replace(code_line, "\n", "")
            if str.startswith(code_line, "//"):
                continue
            if len(code_line) < 2:
                continue
            if str.__eq__(code_line, "function Sys.init 0"):
                b_init = True
            code_line = str.split(code_line, "//")[0]
            commands = str.split(code_line, ' ')
            commands_length = len(commands)
            command_type = self.constValues.getCommandType(str.lower(commands[0]))
            arg1 = ""
            arg2 = ""
            if commands_length > 1:
                arg1 = commands[1]
            if commands_length > 2:
                arg2 = commands[2]
            code_list.append([commands[0], command_type, arg1, arg2])
        if b_init:
            code_list.insert(0, ["call", self.constValues.C_CALL, "Sys.init", "0"])
        return code_list

    def get_hack_code(self):
        return self.code_writer.parse()
