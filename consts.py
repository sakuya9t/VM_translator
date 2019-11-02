class consts:
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9
    M_ARGUMENT = 0
    M_LOCAL = 1
    M_STATIC = 2
    M_CONSTANT = 3
    M_THIS = 4
    M_THAT = 5
    M_POINTER = 6
    M_TEMP = 7
    A_ADD = 0
    A_SUB = 1
    A_NEG = 2
    A_EQ = 3
    A_GT = 4
    A_LT = 5
    A_AND = 6
    A_OR = 7
    A_NOT = 8
    TYPE_ERROR = 999

    def getCommandType(self, command):
        if command.__eq__("push"):
            return self.C_PUSH
        if command.__eq__("pop"):
            return self.C_POP
        if command.__eq__("label"):
            return self.C_LABEL
        if command.__eq__("goto"):
            return self.C_GOTO
        if command.__eq__("if-goto"):
            return self.C_IF
        if command.__eq__("function"):
            return self.C_FUNCTION
        if command.__eq__("return"):
            return self.C_RETURN
        if command.__eq__("call"):
            return self.C_CALL
        return self.C_ARITHMETIC

    def getMemType(self, mem_target):
        if mem_target.__eq__("argument"):
            return self.M_ARGUMENT
        if mem_target.__eq__("local"):
            return self.M_LOCAL
        if mem_target.__eq__("static"):
            return self.M_STATIC
        if mem_target.__eq__("constant"):
            return self.M_CONSTANT
        if mem_target.__eq__("this"):
            return self.M_THIS
        if mem_target.__eq__("that"):
            return self.M_THAT
        if mem_target.__eq__("pointer"):
            return self.M_POINTER
        if mem_target.__eq__("temp"):
            return self.M_TEMP
        return self.TYPE_ERROR

    def getCalcType(self, cmd):
        if cmd.__eq__("add"):
            return self.A_ADD
        if cmd.__eq__("sub"):
            return self.A_SUB
        if cmd.__eq__("neg"):
            return self.A_NEG
        if cmd.__eq__("eq"):
            return self.A_EQ
        if cmd.__eq__("gt"):
            return self.A_GT
        if cmd.__eq__("lt"):
            return self.A_LT
        if cmd.__eq__("and"):
            return self.A_AND
        if cmd.__eq__("or"):
            return self.A_OR
        if cmd.__eq__("not"):
            return self.A_NOT
        return self.TYPE_ERROR
