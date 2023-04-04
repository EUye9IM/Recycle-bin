# ------------------------------------------------
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: Anakin
# Function: 实现词法分析器
# ------------------------------------------------

# 类C语言词法
# 保留字
reserve_words = {"int", "void", "if", "else", "while", "return"}

# A型单字符运算符，扫描到此类字符即返回 token，进行下一轮扫描
single_char_operations_typeA = {";", ",", "(", ")", "{", "}", "+", "-", "*"}

# B型单字符运算符，扫描到此类字符查看下一字符是否为"="
single_char_operations_typeB = {">", "<", "=", "!"}

# C型单字符运算符，扫描到此类字符考虑注释
single_char_operations_typeC = {"/"}

# 双字符运算符
double_char_operations = {">=", "<=", "==", "!="}


# Pos Class 定义
class Position:
    def __init__(self, _ln, _col, _num):
        self.ln = _ln
        self.col = _col
        self.num = _num


# Token Class 定义
class Token:
    def __init__(self, _type, _pos: Position, _val=None):
        self.pos = _pos
        self.symbol_table_entry = -1  # 符号表入口地址

        if _val is None:
            self.type = "T_" + _type.upper()
            self.val = _type
        else:
            self.type, self.val = _type.upper(), _val

    def set_sym_tab_entry(self, entry_num):
        self.symbol_table_entry = entry_num

    def get_sym_tab_entry(self):
        return self.symbol_table_entry

    def __str__(self):
        return "|%-15s|%-15s|%-10d|%-10d|%-10d|" % (
            self.type,
            self.val,
            self.pos.ln,
            self.pos.col,
            self.pos.num,
        )


# 字符判断函数
def is_whitespace(ch):
    return ch in " \t\r\a\n"


def is_digit(ch):
    return ch in "0123456789"


def is_letter(ch):
    return ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


# 是否为构成变量非首字的符号
def is_variable_symbol(ch):
    return is_digit(ch) or is_letter(ch) or ch == "_"


# Scanner Class 定义
class Scanner:
    def __init__(self, _file_name=None):
        self.file_name = _file_name
        self.text = None

    def _read_file(self):
        with open(self.file_name, "r", encoding="utf-8") as f:
            self.text = f.read()

    # 根据字符位置 i 计算行号和列号
    def _get_pos(self, i):
        pos = Position(1, 1, i)
        cnt = 0
        for ch in self.text:
            cnt += 1
            if i < cnt:
                break
            pos.col += 1
            if ch == "\n":
                pos.ln += 1
                pos.col = 1

        return pos

    # 词法扫描工具
    def scan(self):
        self._read_file()
        n, i = len(self.text), 0
        s = self.text  # s 代表文本，简化代码
        while i < n:
            ch, i = s[i], i + 1

            if is_whitespace(ch):
                continue

            if ch == "#":  # 遇见'#'表示结束
                return

            if ch in single_char_operations_typeA:
                yield Token(ch, self._get_pos(i - 1))
            elif ch in single_char_operations_typeB:
                if i < n and s[i] == "=":
                    i += 1
                    yield Token(ch + "=", self._get_pos(i - 2))
                else:
                    yield Token(ch, self._get_pos(i - 1))
            elif ch in single_char_operations_typeC:
                # '/'处理
                if s[i] == "/":  # 单行注释
                    begin = i - 1
                    while i < n and s[i] != "\n":
                        i += 1
                    comment = s[begin:i]
                    yield Token("T_comment", self._get_pos(begin), comment)
                elif s[i] == "*":  # 多行注释
                    begin = i - 1
                    while i < n and not (s[i - 1] == "*" and s[i] == "/"):
                        i += 1
                    i += 1  # 包含注释末尾的'/'
                    comment = s[begin:i]
                    yield Token("T_comment", self._get_pos(begin), comment)
                else:
                    yield Token(ch, self._get_pos(i - 1))

            elif is_letter(ch) or ch == "_":
                # 识别标识符与关键字
                begin = i - 1
                while i < n and is_variable_symbol(s[i]):
                    i += 1
                word = s[begin:i]
                if word in reserve_words:
                    yield Token(word, self._get_pos(begin))
                else:
                    yield Token("T_identifier", self._get_pos(begin), word)
            elif is_digit(ch):
                # 此处只考虑整型数，并未进行其他处理
                begin = i - 1
                while i < n and is_digit(s[i]):
                    i += 1
                yield Token("T_integer", self._get_pos(begin), s[begin:i])
            else:
                pos = self._get_pos(i - 1)
                raise Exception(
                    "Unknown symbol '%s' at ln %d, col %d" % (ch, pos.ln, pos.col)
                )

    # 获取 token 列表
    def get_token_list(self):
        tokens = []
        try:
            for token in self.scan():
                # 过滤注释
                if token.type != "T_COMMENT":
                    tokens.append(token)
        except Exception as err:
            print(err)

        return tokens

    # 输出 token 至文件
    def print_token_to_file(self):
        header = "|%-15s|%-15s|%-10s|%-10s|%-10s|\n" % (
            "TOKEN TYPE",
            "TOKEN VALUE",
            "TOKEN LN",
            "TOKEN COL",
            "TOKEN NUM",
        )
        line = "+{}+{}+{}+{}+{}+\n".format(
            "-" * 15, "-" * 15, "-" * 10, "-" * 10, "-" * 10
        )
        buf = "The tokens in '%s' are as following: \n" % self.file_name
        buf += line + header + line  # buf 缓冲输出
        try:
            for token in self.scan():
                if token.type != "T_COMMENT":
                    buf += str(token) + "\n" + line
        except Exception as err:
            buf += str(err)

        token_file = self.file_name + ".tn"
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(buf)

        print("The token information has been written into '%s' file." % token_file)
        # 选择是否输出至终端
        choose = input("The token will be print on screen, y/n ? Your choose: ")
        while True:
            if choose in ["y", "Y", "Yes", "yes"]:
                print(buf)
                break
            elif choose in ["n", "N", "No", "no"]:
                break
            else:
                choose = input("Input illegal, again: ")


if __name__ == "__main__":
    code_scan = Scanner("input2.cpp")
    tokens = code_scan.get_token_list()

    code_scan.print_token_to_file()
