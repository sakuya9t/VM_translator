import consts


class CodeWriter:
    code_list = []
    label_id = 0
    return_id = 0

    def __init__(self, code_list, class_name):
        self.code_list = code_list
        self.constValues = consts.consts()
        self.className = str.split(class_name, '.')[0]

    def parse(self):
        asm_list = []
        # SP=256
        asm_list.append("@256")
        asm_list.append("D=A")
        asm_list.append("@SP")
        asm_list.append("M=D")
        for code in self.code_list:
            command_type = code[1]
            if command_type == self.constValues.C_ARITHMETIC:
                asm_list += self.write_arithmetic(code)
            elif command_type == self.constValues.C_PUSH:
                asm_list += self.write_push(code)
            elif command_type == self.constValues.C_POP:
                asm_list += self.write_pop(code)
            elif command_type == self.constValues.C_GOTO:
                asm_list += self.write_goto(code)
            elif command_type == self.constValues.C_IF:
                asm_list += self.write_if(code)
            elif command_type == self.constValues.C_LABEL:
                asm_list += self.write_label(code)
            elif command_type == self.constValues.C_FUNCTION:
                asm_list += self.write_function(code)
            elif command_type == self.constValues.C_RETURN:
                asm_list += self.write_return(code)
            elif command_type == self.constValues.C_CALL:
                asm_list += self.write_call(code)
        return asm_list

    def write_arithmetic(self, command):
        asm = []
        cmd = command[0]
        calc_type = self.constValues.getCalcType(str.lower(cmd))
        if calc_type == self.constValues.A_ADD or calc_type == self.constValues.A_SUB or \
                calc_type == self.constValues.A_AND or calc_type == self.constValues.A_OR:
            # SP --;
            asm.append("@SP")
            asm.append("M=M-1")
            # D=RAM[*SP];
            asm.append("A=M")
            asm.append("D=M")
            # SP --;
            asm.append("@SP")
            asm.append("M=M-1")
            # RAM[*SP] +=/-=/&=/|= RAM[*SP + 1];
            asm.append("A=M")
            if calc_type == self.constValues.A_ADD:
                asm.append("M=D+M")
            elif calc_type == self.constValues.A_SUB:
                asm.append("M=M-D")
            elif calc_type == self.constValues.A_AND:
                asm.append("M=D&M")
            elif calc_type == self.constValues.A_OR:
                asm.append("M=D|M")
            else:
                return []
        elif calc_type == self.constValues.A_NEG or calc_type == self.constValues.A_NOT:
            # SP --;
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            if calc_type == self.constValues.A_NEG:
                asm.append("M=-M")
            elif calc_type == self.constValues.A_NOT:
                asm.append("M=!M")
            else:
                return []
        elif calc_type == self.constValues.A_EQ or calc_type == self.constValues.A_LT or \
                calc_type == self.constValues.A_GT:
            # SP --; PRETEND *SP == 257
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            asm.append("D=M")       # D=RAM[256]
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")       # M=RAM[255]
            asm.append("D=M-D")     # D=RAM[255]-RAM[256]
            # JMP IF D =/>/< 0
            asm.append("@label" + self.className + "." + str(self.label_id))
            if calc_type == self.constValues.A_EQ:
                asm.append("D;JEQ")
            elif calc_type == self.constValues.A_LT:
                asm.append("D;JLT")
            elif calc_type == self.constValues.A_GT:
                asm.append("D;JGT")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=0")       # false
            asm.append("@end" + self.className + "." + str(self.label_id))
            asm.append("0;JMP")
            asm.append("(label" + self.className + "." + str(self.label_id) + ")")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=-1")      # true
            asm.append("@end" + self.className + "." + str(self.label_id))
            asm.append("0;JMP")
            asm.append("(end" + self.className + "." + str(self.label_id) + ")")
        else:
            return[]
        # SP++;
        asm.append("@SP")
        asm.append("M=M+1")
        self.label_id += 1
        return asm

    def write_push(self, command):
        asm = []
        mem_type_str = command[2]
        offset = command[3]
        mem_type = self.constValues.getMemType(str.lower(mem_type_str))
        # D = RAM[TARGET_ADDRESS];
        if mem_type == self.constValues.M_LOCAL or mem_type == self.constValues.M_ARGUMENT or \
                mem_type == self.constValues.M_THIS or mem_type == self.constValues.M_THAT:
            if mem_type == self.constValues.M_LOCAL:
                asm.append("@LCL")
            elif mem_type == self.constValues.M_ARGUMENT:
                asm.append("@ARG")
            elif mem_type == self.constValues.M_THIS:
                asm.append("@THIS")
            elif mem_type == self.constValues.M_THAT:
                asm.append("@THAT")
            asm.append("D=M")
            asm.append("@" + offset)
            asm.append("A=D+A")
            asm.append("D=M")
        elif mem_type == self.constValues.M_CONSTANT:
            asm.append("@" + offset)
            asm.append("D=A")
        elif mem_type == self.constValues.M_STATIC:
            asm.append("@" + self.className + "." + offset)
            asm.append("D=M")
        elif mem_type == self.constValues.M_POINTER:
            asm.append("@R" + str(3 + int(offset)))
            asm.append("D=M")
        elif mem_type == self.constValues.M_TEMP:
            asm.append("@R" + str(5 + int(offset)))
            asm.append("D=M")
        # RAM[*SP] = D
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=D")
        # SP++;
        asm.append("@SP")
        asm.append("M=M+1")
        return asm

    def write_pop(self, command):
        asm = []
        mem_type_str = command[2]
        offset = command[3]
        mem_type = self.constValues.getMemType(str.lower(mem_type_str))
        # RAM[13] = TARGET_ADDRESS;
        if mem_type == self.constValues.M_LOCAL or mem_type == self.constValues.M_ARGUMENT or \
                mem_type == self.constValues.M_THIS or mem_type == self.constValues.M_THAT:
            if mem_type == self.constValues.M_LOCAL:
                asm.append("@LCL")
            elif mem_type == self.constValues.M_ARGUMENT:
                asm.append("@ARG")
            elif mem_type == self.constValues.M_THIS:
                asm.append("@THIS")
            elif mem_type == self.constValues.M_THAT:
                asm.append("@THAT")
            asm.append("D=M")
            asm.append("@" + offset)
            asm.append("D=D+A")
            asm.append("@R13")
            asm.append("M=D")
            # SP--;
            asm.append("@SP")
            asm.append("M=M-1")
            # RAM[TARGET_ADDRESS] = RAM[*SP];
            asm.append("A=M")
            asm.append("D=M")
            asm.append("@R13")
            asm.append("A=M")
            asm.append("M=D")
        elif mem_type == self.constValues.M_STATIC or mem_type == self.constValues.M_POINTER or \
                mem_type == self.constValues.M_TEMP:
            # SP--;
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            asm.append("D=M")
            # RAM[TARGET_ADDRESS] = RAM[*SP];
            if mem_type == self.constValues.M_STATIC:
                asm.append("@" + self.className + "." + offset)
            elif mem_type == self.constValues.M_POINTER:
                asm.append("@R" + str(3 + int(offset)))
            elif mem_type == self.constValues.M_TEMP:
                asm.append("@R" + str(5 + int(offset)))
            asm.append("M=D")
        return asm

    def write_label(self, command):
        asm = []
        label_name = command[2]
        asm.append("(" + label_name + ")")
        return asm

    def write_goto(self, command):
        asm = []
        target_label = command[2]
        asm.append("@" + target_label)
        asm.append("0;JMP")
        return asm

    def write_if(self, command):
        asm = []
        target_label = command[2]
        # SP--;
        asm.append("@SP")
        asm.append("M=M-1")
        # D=RAM[*SP];
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@" + target_label)
        asm.append("D;JNE")
        return asm

    def write_function(self, command):
        asm = []
        function_name = command[2]
        num_local = int(command[3])
        asm.append("(" + function_name + ")")
        for i in range(num_local):
            # RAM[*SP] = 0;
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=0")
            # SP++;
            asm.append("@SP")
            asm.append("M=M+1")
        return asm

    def write_return(self, command):
        asm = []
        # FRAME = LCL, pretend FRAME=261
        asm.append("@LCL")
        asm.append("D=M")  # D=261
        asm.append("@R14")
        asm.append("M=D")  # R14=261
        # RET = *(FRAME - 5)
        asm.append("@5")
        asm.append("A=D-A")  # A=256
        asm.append("D=M")  # D=RAM[256]
        asm.append("@R15")
        asm.append("M=D")  # R15=RAM[256]
        # *ARG = POP()
        asm.append("@SP")
        asm.append("M=M-1")  # SP--
        asm.append("A=M")
        asm.append("D=M")  # D=*SP
        asm.append("@ARG")
        asm.append("A=M")
        asm.append("M=D")  # *ARG=D
        # SP = ARG + 1
        asm.append("@ARG")
        asm.append("D=M+1")
        asm.append("@SP")
        asm.append("M=D")
        # THAT = *(FRAME - 1)
        asm.append("@R14")
        asm.append("M=M-1")  # R14=260
        asm.append("A=M")
        asm.append("D=M")  # D=RAM[260]
        asm.append("@THAT")
        asm.append("M=D")
        # THIS = *(FRAME - 2)
        asm.append("@R14")
        asm.append("M=M-1")  # R14=259
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@THIS")
        asm.append("M=D")
        # ARG = *(FRAME - 3)
        asm.append("@R14")
        asm.append("M=M-1")  # R14=258
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@ARG")
        asm.append("M=D")
        # LCL = *(FRAME - 4)
        asm.append("@R14")
        asm.append("M=M-1")  # R14=257
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@LCL")
        asm.append("M=D")
        # goto RET
        asm.append("@R15")
        asm.append("A=M")
        asm.append("0;JMP")
        return asm

    def write_call(self, command):
        asm = []
        function_name = command[2]
        arg_cnt = int(command[3])
        return_label = "return" + "." + self.className + "." + str(self.return_id)
        # PUSH return_address
        asm.append("@" + return_label)
        asm.append("D=A")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=D")
        asm.append("@SP")
        asm.append("M=M+1")
        # PUSH LCL
        asm.append("@LCL")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=D")
        asm.append("@SP")
        asm.append("M=M+1")
        # PUSH ARG
        asm.append("@ARG")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=D")
        asm.append("@SP")
        asm.append("M=M+1")
        # PUSH THIS
        asm.append("@THIS")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=D")
        asm.append("@SP")
        asm.append("M=M+1")
        # PUSH THAT
        asm.append("@THAT")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=D")
        asm.append("@SP")
        asm.append("M=M+1")
        # ARG = SP - n - 5
        asm.append("@SP")
        asm.append("D=M")
        asm.append("@" + str(arg_cnt + 5))
        asm.append("D=D-A")
        asm.append("@ARG")
        asm.append("M=D")
        # LCL = SP
        asm.append("@SP")
        asm.append("D=M")
        asm.append("@LCL")
        asm.append("M=D")
        # goto function
        asm.append("@" + function_name)
        asm.append("0;JMP")
        # (return_address)
        asm.append("(" + return_label + ")")
        self.return_id += 1
        return asm
